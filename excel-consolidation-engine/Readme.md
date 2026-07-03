# Excel Consolidation Engine (Config-Driven VBA)

A fully dynamic, configuration-driven Excel VBA engine designed to consolidate
multiple Excel workbooks into a single standardized output — without changing VBA code.

## 🔑 Key Features
- Config-driven schema, dataset, and column mapping
- Supports multi-sheet datasets from a single file
- Automatic header detection
- Safe null handling (row-level, not column-level)
- Missing sheet validation log
- Performance-optimized (screenless processing)
- Zero hardcoded business logic

## 🧠 Architecture
This solution separates **logic** from **configuration**:
- **Schema_Config** → output structure
- **Dataset_Config** → file + sheet definitions
- **Mapping_Config** → source-to-target mappings

Adding a new dataset requires **no VBA changes**.

## 🚀 How It Works
1. User selects required input files once
2. Macro processes all datasets silently
3. Output workbook is generated with:
   - Unified schema
   - Dataset lineage
   - Cleaned null handling
4. Missing sheets are logged separately

## 📁 Repository Structure
See `/config` for configuration templates  
See `/macro` for VBA core  
See `/sample_input` for dummy datasets

## ⚙️ Requirements
- Microsoft Excel (Windows)
- VBA enabled
- No external libraries required

## 📌 Use Cases
- Procurement / Finance reporting
- Operations dashboards
- Cross-system data harmonization
- Reusable enterprise Excel automation

## 📄 License
MIT (Free to use and modify)
---

Built for scalability, maintainability, and performance.

👤 Author & Credits

Developed by: Pranit Patil
Role: Tableau Developer | Automation & Data Analytics
Focus Areas: Excel VBA Automation, Data Consolidation, Reporting Efficiency, Data Analytics & Visualization

Designed and built to solve real-world enterprise-scale Excel consolidation challenges with a strong emphasis on configurability, performance, and maintainability.

![alt text](Excel_Macro.png)
![alt text](Output.png)