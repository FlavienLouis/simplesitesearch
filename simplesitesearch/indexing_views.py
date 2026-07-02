from __future__ import annotations

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .indexing import (
    bootstrap_token_valid,
    consume_refresh_and_rotate,
    issue_token_pair,
    lookup_refresh_user_id,
    parse_bearer_authorization,
    resolve_indexing_user_id,
)


def _indexing_disabled_response():
    return JsonResponse({"detail": "indexing_disabled"}, status=403)


def _json_error(detail: str, status: int):
    return JsonResponse({"detail": detail}, status=status)


@csrf_exempt
@require_POST
def obtain_indexing_token(request):
    if not getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_ENABLED", False):
        return _indexing_disabled_response()
    user_id = resolve_indexing_user_id()
    if user_id is None:
        return _json_error("indexing_user_not_configured", 503)
    token = parse_bearer_authorization(request.META.get("HTTP_AUTHORIZATION", ""))
    if not token or not bootstrap_token_valid(token):
        return _json_error("invalid_bootstrap", 401)
    access, refresh, at, rt = issue_token_pair(user_id)
    return JsonResponse(
        {
            "access_token": access,
            "refresh_token": refresh,
            "expires_in": at,
            "refresh_expires_in": rt,
        }
    )


@csrf_exempt
@require_POST
def refresh_indexing_token(request):
    if not getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_ENABLED", False):
        return _indexing_disabled_response()
    token = parse_bearer_authorization(request.META.get("HTTP_AUTHORIZATION", ""))
    if not token:
        return _json_error("missing_refresh", 401)
    user_id = lookup_refresh_user_id(token)
    if user_id is None:
        return _json_error("invalid_refresh", 401)
    pair = consume_refresh_and_rotate(user_id, token)
    if pair is None:
        return _json_error("invalid_refresh", 401)
    access, refresh, at, rt = pair
    return JsonResponse(
        {
            "access_token": access,
            "refresh_token": refresh,
            "expires_in": at,
            "refresh_expires_in": rt,
        }
    )
