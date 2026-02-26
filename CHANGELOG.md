# Changelog

## [0.0.4] - 2025-02-26

### Fixed

- **SSL verification**: API requests now use certificate verification by default (`verify=True`), removing the `InsecureRequestWarning` from urllib3 when the search API server has a valid certificate. Added optional setting `SITE_SEARCH_VERIFY_SSL` (default `True`); set to `False` only if the server uses a certificate that cannot be verified (e.g. self-signed).

## [0.0.3]

Previous release.
