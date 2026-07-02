# Changelog

## [0.0.6] - 2026-07-02

### Changed

- **Search results**: API hits are normalized to a lean template payload (`display_title`, `snippet`, `domain`, `type`, `language`, `tags`, `last_modified`) instead of passing the full API response (highlights blob, headings, score, etc.). Title uses highlighted text when available; snippet falls back from `highlight` → `description` → `content_preview`.
- **Templates**: Replaced deprecated `{% load staticfiles %}` with `{% load static %}` for Django 4+ compatibility.

## [0.0.5] - 2025-02-26

### Fixed

- **Tag parsing**: Single tag string (e.g. `Hometag`) was iterated by character, producing `tags=H,o,m,e,t,a,g`. `tags_to_query_value()` now treats a string as one tag so the API receives `tags=Hometag`. Comma encoding in API URL: commas are left unencoded (`safe=","`) so the API can split multiple tags correctly.

## [0.0.4] - 2025-02-26

### Fixed

- **SSL verification**: API requests now use certificate verification by default (`verify=True`), removing the `InsecureRequestWarning` from urllib3 when the search API server has a valid certificate. Added optional setting `SITE_SEARCH_VERIFY_SSL` (default `True`); set to `False` only if the server uses a certificate that cannot be verified (e.g. self-signed).

## [0.0.3]

Previous release.
