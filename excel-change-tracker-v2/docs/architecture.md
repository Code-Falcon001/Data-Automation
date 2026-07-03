# 🏗️ Architecture

## Flow
```
User opens workbook → Add-in loads
    │
    ├── Username in localStorage? ──YES──→ Auto-start tracking
    │                                          │
    └── No ──→ PROTECT sheet ──→ Name input    │
                                    │          │
                              UNPROTECT ───────┘
                                    │
                              Read all data (chunked)
                                    │
                              Build in-memory shadow
                                    │
                              Register onChanged event
                                    │
                              ┌─────┴─────┐
                              │  TRACKING  │
                              │  ACTIVE    │
                              └───────────┘
                                    │
                         On cell edit (instant):
                         Read changed cells only
                         Compare vs shadow
                         Log to changelog
                         Update shadow
```

## Key Design Decisions

| Decision | Reason |
|---|---|
| In-memory shadow | Instant lookup (no sheet I/O per change) |
| Adaptive chunk size | `floor(80000/cols)` keeps under 5MB limit |
| RowID column | Stable row identity across inserts/deletes |
| Content hash | Prevents ghost rows from RowID regeneration |
| Number tolerance | `1e-10` avoids false floating-point changes |
