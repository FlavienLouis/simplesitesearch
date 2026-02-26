"""
Quality-of-life utilities for simplesitesearch.
"""
from urllib.parse import quote_plus, urlencode

import requests

from django.conf import settings
from django.utils.translation import get_language


def parse_comma_separated_tags(value):
    """
    Parse a comma-separated string of tags into a list of stripped tags.

    Args:
        value: String (e.g. from request.GET) or None.

    Returns:
        List of non-empty tag strings. Empty list if value is falsy.

    Example:
        >>> parse_comma_separated_tags("news, blog, tutorial")
        ['news', 'blog', 'tutorial']
        >>> parse_comma_separated_tags(None)
        []
    """
    if not value or not value.strip():
        return []
    return [t.strip() for t in value.split(",") if t.strip()]


def tags_to_query_value(tags):
    """
    Convert a list of tags to a comma-separated string for query params or API.

    Args:
        tags: Iterable of tag strings.

    Returns:
        Comma-separated string, or None if tags is empty.
    """
    if not tags:
        return None
    return ",".join(str(t).strip() for t in tags if str(t).strip())


def build_search_query_string(term, page=1, tags=None):
    """
    Build the query string for search URLs (pagination, prev/next).

    Args:
        term: Search term.
        page: Page number (optional).
        tags: Optional list of tags or comma-separated string; as `tag` param.

    Returns:
        Query string with leading "?", e.g. "?q=foo&page=2&tag=a,b".
    """
    params = []
    if term:
        params.append(("q", term))
    if page and page != 1:
        params.append(("page", page))
    parsed = (
        parse_comma_separated_tags(tags) if isinstance(tags, str) else (tags or [])
    )
    tag_value = tags_to_query_value(parsed)
    if tag_value:
        params.append(("tag", tag_value))
    if not params:
        return ""
    return "?" + urlencode(params)


def normalize_search_term(term, max_words=10):
    """
    Limit search term to a maximum number of words (collapse whitespace).

    Args:
        term: Raw search string.
        max_words: Maximum number of words to keep.

    Returns:
        Normalized string with at most max_words.
    """
    if not term or not term.strip():
        return ""
    return " ".join(term.split()[:max_words])


def safe_int(value, default=None):
    """
    Safely convert a value to int.

    Args:
        value: Value to convert (e.g. from request.GET).
        default: Value to return on failure (default None).

    Returns:
        int, or default on failure.
    """
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_search_api_url(term, current_page, tags=None):
    """
    Build the full search API URL for the given term, page and optional tags.

    Args:
        term: Search term.
        current_page: Page number (1-based).
        tags: Optional list of tag strings; sent as comma-separated `tags` param.

    Returns:
        Full URL string for the search API.
    """
    base_url = settings.SITE_SEARCH_API_BASE_URL
    site_key = settings.SITE_SEARCH_SITE_KEY
    lang = get_language()
    url = "%s%s?term=%s&lang=%s&page=%s" % (
        base_url, site_key, quote_plus(term), lang, current_page
    )
    tag_value = tags_to_query_value(tags)
    if tag_value:
        url += "&tags=%s" % quote_plus(tag_value)
    return url


def get_search_results(term, current_page, tags=None):
    """
    Fetch search results from the API for the given term, page and optional tags.

    Args:
        term: Search term.
        current_page: Page number (1-based).
        tags: Optional list of tag strings (comma-separated in API).

    Returns:
        Dict with "total_hits" and "hits" (list). On request or JSON error,
        returns {"total_hits": 0, "hits": []}.
    """
    api_url = get_search_api_url(term, current_page, tags=tags)
    try:
        response = requests.get(api_url)
        return response.json()
    except Exception:
        return {"total_hits": 0, "hits": []}
