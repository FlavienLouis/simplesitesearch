"""
Opaque indexing tokens stored in Django cache (shared backend required in multi-worker setups).
"""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Optional, Tuple

from django.conf import settings
from django.core.cache import cache


def indexing_cache_prefix() -> str:
    return getattr(
        settings,
        "SIMPLE_SITE_SEARCH_INDEXING_CACHE_PREFIX",
        "sss_idx",
    )


def access_ttl_seconds() -> int:
    return int(
        getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_ACCESS_TTL", 3600)
    )


def refresh_ttl_seconds() -> int:
    return int(
        getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_REFRESH_TTL", 86400)
    )


def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def access_cache_key(raw_access_token: str) -> str:
    return "%s:a:%s" % (indexing_cache_prefix(), _hash_token(raw_access_token))


def refresh_cache_key(raw_refresh_token: str) -> str:
    return "%s:r:%s" % (indexing_cache_prefix(), _hash_token(raw_refresh_token))


def parse_bearer_authorization(header_value: str) -> Optional[str]:
    if not header_value:
        return None
    parts = header_value.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1].strip()
    return token or None


def bootstrap_token_valid(given: str) -> bool:
    expected = getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_BOOTSTRAP_TOKEN", "") or ""
    if not expected or not given:
        return False
    try:
        eb = expected.encode("utf-8")
        gb = given.encode("utf-8")
    except UnicodeEncodeError:
        return False
    if len(eb) != len(gb):
        return False
    return hmac.compare_digest(eb, gb)


def issue_token_pair(user_id: int) -> Tuple[str, str, int, int]:
    access = secrets.token_urlsafe(32)
    refresh = secrets.token_urlsafe(32)
    at = access_ttl_seconds()
    rt = refresh_ttl_seconds()
    cache.set(
        access_cache_key(access),
        json.dumps({"user_id": user_id}),
        at,
    )
    cache.set(
        refresh_cache_key(refresh),
        json.dumps({"user_id": user_id}),
        rt,
    )
    return access, refresh, at, rt


def lookup_access_user_id(raw_access_token: str) -> Optional[int]:
    raw = cache.get(access_cache_key(raw_access_token))
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    try:
        data = json.loads(raw)
        uid = data.get("user_id")
        return int(uid) if uid is not None else None
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def consume_refresh_and_rotate(user_id: int, old_refresh: str) -> Optional[Tuple[str, str, int, int]]:
    """
    Validate refresh token, delete it, issue new access + refresh (rotation).
    Returns (access, refresh, access_ttl, refresh_ttl) or None if invalid.
    """
    rkey = refresh_cache_key(old_refresh)
    raw = cache.get(rkey)
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    try:
        data = json.loads(raw)
        if int(data.get("user_id")) != int(user_id):
            return None
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    cache.delete(rkey)
    return issue_token_pair(user_id)


def lookup_refresh_user_id(raw_refresh_token: str) -> Optional[int]:
    rkey = refresh_cache_key(raw_refresh_token)
    raw = cache.get(rkey)
    if raw is None:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    try:
        data = json.loads(raw)
        return int(data["user_id"])
    except (TypeError, ValueError, KeyError, json.JSONDecodeError):
        return None


def resolve_indexing_user_id() -> Optional[int]:
    spec = getattr(settings, "SIMPLE_SITE_SEARCH_INDEXING_USER", None)
    if spec is None:
        return None
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if isinstance(spec, int):
        pk = spec
    else:
        s = str(spec).strip()
        if s.isdigit():
            pk = int(s)
        else:
            lookup = {User.USERNAME_FIELD: s}
            u = User.objects.filter(**lookup).values_list("pk", flat=True).first()
            return int(u) if u is not None else None
    return pk if User.objects.filter(pk=pk).exists() else None
