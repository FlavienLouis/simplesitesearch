from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model, login

from .indexing import lookup_access_user_id, parse_bearer_authorization


def _skip_for_path(path: str) -> bool:
    if "internal/indexing/token" in path or "internal/indexing/refresh" in path:
        return True
    return False


class IndexingAccessTokenMiddleware:
    """
    After AuthenticationMiddleware: if Authorization Bearer matches a valid indexing
    access token, log in as the configured indexer user for this request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_ENABLED", False):
            return self.get_response(request)
        if _skip_for_path(getattr(request, "path", "") or ""):
            return self.get_response(request)
        authz = request.META.get("HTTP_AUTHORIZATION", "")
        token = parse_bearer_authorization(authz)
        if not token:
            return self.get_response(request)
        user_id = lookup_access_user_id(token)
        if user_id is None:
            return self.get_response(request)
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return self.get_response(request)
        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return self.get_response(request)
