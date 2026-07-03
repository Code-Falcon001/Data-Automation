# 📋 Changelog

## [v5.2] — 2026-04-22 (Current)
### Added
- Auto-start on workbook open (no manual button)
- Sheet protection gate until user identifies
- "Change User" link to switch username
### Fixed
- `columnHidden` property syntax for Office.js
### Removed
- SSO attempt (not available with sideloading)
- Manual "Start Tracking" button

## [v5.1] — 2026-04-22
### Fixed
- `prompt()` replaced with inline HTML input (iframe-safe)
- `errorToString()` for proper Office.js error extraction
- Step-by-step logging for debugging

## [v5.0] — 2026-04-22
### Added
- Real-time detection via `worksheet.onChanged`
- In-memory shadow (instant comparison)
- Adaptive chunked I/O
- Structural change handling

## [v4.2] — 2026-04-21 (Office Scripts)
- Adaptive chunk sizing
- Auto-retry on payload errors

## [v4.1] — 2026-04-21
- Batch RowID creation
- Zero cell-by-cell API calls

## [v4.0] — 2026-04-21
- Chunked I/O (fixes payload limit)

## [v3.1] — 2026-04-21
- Excel Online safe API calls

## [v3.0] — 2026-04-20
- Initial version with shadow comparison
