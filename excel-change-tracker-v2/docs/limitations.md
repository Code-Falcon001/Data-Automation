# ⚠️ Known Limitations

| # | Limitation | Impact | Mitigation |
|---|---|---|---|
| 1 | Pane must be open | Tracking pauses if closed | Shared runtime for production |
| 2 | Username self-reported | Could enter wrong name | SSO with IT deployment |
| 3 | Value changes only | Formatting invisible | By design |
| 4 | Formula results logged | Recalc = value change | Expected behavior |
| 5 | One sheet tracked | Only "STD format" | Extensible |
| 6 | HTTPS hosting needed | GitHub Pages / SharePoint | Currently GitHub Pages |
| 7 | Admin for org deploy | Sideload = per user | One-time IT task |
| 8 | SSO needs IT | Azure AD registration | Production enhancement |
| 9 | Initial load 10-30s | Reading 11K rows | Acceptable |
| 10 | Max ~50K rows | Browser timeout risk | Current data safe |
