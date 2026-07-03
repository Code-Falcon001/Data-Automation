# 📊 Excel Change Tracker

**Real-time cell change tracking for Excel Online with per-user attribution**

![Version](https://img.shields.io/badge/version-5.2-blue)
![Platform](https://img.shields.io/badge/platform-Excel%20Online-green)
![License](https://img.shields.io/badge/license-MIT-gray)

---

## 🎯 What It Does

Monitors every cell edit in the **"Excel File"** sheet in real time. Records **who** changed **what**, **when**, the **old value**, and the **new value** — all logged into a **"changelog"** sheet. Like a **CCTV camera for your spreadsheet**.

---

## ⚡ Key Features

| Feature | Status |
|---|---|
| Real-time change detection (instant) | ✅ |
| Per-user attribution (browser-based) | ✅ |
| Handles 11,000+ rows (adaptive chunked I/O) | ✅ |
| Row insert/delete tracking (RowID-based) | ✅ |
| Ghost row prevention | ✅ |
| Smart value comparison (float-point safe) | ✅ |
| Auto-start on workbook open | ✅ |
| Sheet protection until user identifies | ✅ |

---

## 📋 Changelog Format

| Timestamp | Username | Sheet | Cell | Column Name | Old Value | New Value |
|---|---|---|---|---|---|---|
| 04/22/2026 5:30 PM | Pranit | Sheet1 | E7 | ITEM | EPH-480 | TEST1 |
| 04/22/2026 5:30 PM | Kevin | Sheet2 | B11 | COUNTRY | SINGAPORE | INDIA |

---

## 🚀 Quick Start

1. Open workbook in **Excel Online**
2. **Home** → **Add-ins** → **Upload My Add-in**
3. Select **`manifest_simple.xml`**
4. Enter your name when prompted (first time only)
5. Edit cells → changes logged **instantly**!

> 📖 See [Setup Guide](docs/setup-guide.md) for detailed instructions.

---

## 📂 Repository Structure

```
excel-change-tracker-v2/
├── taskpane.html          ← LIVE add-in (served by GitHub Pages)
├── manifest_simple.xml    ← Upload this to Excel Online
├── README.md              ← This file
├── CHANGELOG.md           ← Version history
├── LICENSE                ← MIT License
└── docs/
    ├── setup-guide.md     ← Step-by-step setup
    ├── architecture.md    ← Technical design
    └── limitations.md     ← Known limitations
```

---

## 🔧 How It Works

1. **On load:** Reads all data into memory (chunked, adaptive sizing)
2. **RowID:** Each row gets a hidden unique ID for stable tracking
3. **Event:** `worksheet.onChanged` fires instantly on every edit
4. **Compare:** New value vs in-memory shadow (smart float tolerance)
5. **Log:** Difference written to changelog (latest first)

---

## ⚠️ Limitations

| # | Limitation | Mitigation |
|---|---|---|
| 1 | Pane must be open | Shared runtime for production |
| 2 | Username self-reported | SSO with IT deployment |
| 3 | Value changes only | Formatting out of scope |
| 4 | Initial load 10-30s | Acceptable for 11K rows |
| 5 | Max ~50K rows | Current data within limits |

> 📖 See [Full Limitations](docs/limitations.md)

---

## 📄 Documentation

- [Setup Guide](docs/setup-guide.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [Changelog](CHANGELOG.md)

---

## 👥 Team

| Role | Name |
|---|---|
| **Developer** | Pranit Patil |
| **Role** | Tableau Developer & AI Enthusiast |

---

## 📜 License

[MIT License](LICENSE)
