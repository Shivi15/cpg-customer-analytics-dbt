# 🏥 Consumer Healthcare (CPG) Analytics Engineering Pipeline

An enterprise-grade ELT pipeline designed for an Over-The-Counter (OTC) & Consumer Healthcare brand. Built with **Snowflake**, **dbt Core**, and **GitHub Actions** to model multi-market customer demographics, OTC product catalog unit economics, and gross margin analytics.

---

## 🎯 Project Motivation & Migration from Starter Scaffolding

When initializing dbt projects via `dbt init`, default scaffolding generates sandbox fixtures (such as the standard `jaffle_shop` restaurant template). While useful for basic syntax learning, generic tutorial models do not reflect real-world enterprise architectures, strict data contracts, or domain-specific analytics challenges.

**What We Achieved:**
* Completely stripped out default `jaffle_shop` starter templates and sample food-service models.
* Designed and deployed an enterprise-grade **CPG / OTC Healthcare Data Architecture** tailored to multi-regional retail and direct-to-consumer operations.
* Implemented strict Role-Based Access Control (RBAC) in Snowflake, structured modular staging views, dimension tables, automated schema tests, and continuous integration via GitHub Actions.

---

## 🏢 Business Problem & Industry Context

Consumer healthcare and OTC pharmaceutical brands operate in a high-compliance, multi-currency, and margin-sensitive environment. Business stakeholders (Commercial Finance, Regional Growth, and Supply Chain) require clean, governed data models to answer key operational questions:

1. **Unit Economics & Margin Health:** Raw transactional feeds often store pricing and cost data in raw formats without automated derivation of gross profit margins across regulated categories (e.g., *Skin Health*, *Self Care*, *Oral Care*).
2. **Multi-Market Demographic Fragmentation:** Customer registrations spanning the UK, US, and EU arrive with inconsistent casing, unvalidated dates, and unstructured identifiers.
3. **Data Quality SLAs & Contract Drift:** Upstream ingestion pipelines frequently suffer from missing emails, duplicate customer records, or mismatched product keys, leading to inaccurate commercial reporting.

---

## 🚧 Roadblocks & Technical Solutions

| Challenge / Roadblock | Impact | Engineering Solution |
| :--- | :--- | :--- |
| **Sandbox Scaffolding Conflicts** | Default starter models and legacy YAML syntax caused namespace collisions and macro compilation failures during builds. | Removed all default starter schemas; implemented isolated, dedicated `models/staging/` and `models/marts/` directories adhering to modular dbt design patterns. |
| **Credential & Secret Exposure** | Risk of leaking warehouse credentials, connection profiles, and local virtual environment binaries to public version control. | Configured strict `.gitignore` rules preventing tracking of `.env`, `logs/`, `target/`, and `dbt-env/`. Enforced out-of-repo credential management via `~/.dbt/profiles.yml`. |
| **Untyped Raw Ingestion** | Raw landing tables contained loose string typing and leading/trailing whitespace across customer keys and ISO country codes. | Built robust Staging Views (`stg_cpg__customers`, `stg_cpg__products`) utilizing SQL trimming, case normalization (`LOWER()`, `UPPER()`), and explicit date/decimal casting. |
| **Downstream Integrity Risks** | Risk of orphaned dimension records or duplicate customer profiles propagating to BI dashboards. | Established automated testing suites in `schema.yml` enforcing `unique` and `not_null` assertions on primary keys prior to gold-layer table materialization. |
| **Deployment & Code Fragility** | Manual SQL runs risking syntax bugs or breaking schema updates in production. | Engineered a GitHub Actions CI pipeline (`.github/workflows/dbt_ci.yml`) that validates syntax and parses DAG dependencies on every push and pull request. |

---

## 🏗️ End-to-End Architecture

[ Data Generation Layer ]
│
├── generate_data.py (Faker & Pandas: Multi-Region OTC Customers & SKUs)
│
▼
[ Snowflake Landing Zone ]
│
├── RAW_DB.CPG_RAW.RAW_CUSTOMERS (Raw Ingestion)
└── RAW_DB.CPG_RAW.RAW_PRODUCTS  (Raw Ingestion)
│
│  [ TRANSFORMING_WH Compute Engine ]
▼
[ dbt Transformation Pipeline ]
│
├── 1. Staging Layer (Models materialized as Views)
│      ├── stg_cpg__customers  ──> Cleans casing, trims strings, standardizes ISO country codes
│      └── stg_cpg__products   ──> Casts numeric types, derives unit gross margin (£)
│
├── 2. Data Quality & Assertions (schema.yml)
│      ├── unique & not_null tests on customer_id
│      └── unique & not_null tests on product_id
│
└── 3. Marts Layer (Models materialized as Tables)
├── dim_customers ──> Standardized multi-market customer profiles & registration metadata
└── dim_products  ──> Product catalog enriched with gross margin percentages
│
▼
[ CI/CD & Orchestration ]
├── GitHub Actions: Automated schema parsing and syntax validation on push/PR
└── dbt Docs: Interactive Directed Acyclic Graph (DAG) and data dictionary

---

## 📊 Dimensional Models & Business Metrics Solved

### `dim_products` (OTC Product Economics)
* **`product_id`**: Primary identifier for OTC products (e.g., *Daily Hydrating Cleanser*, *Rapid Pain Relief 500mg*).
* **`category_name`**: Product segmentation category (*Skin Health*, *Self Care*, *Oral Care*).
* **`unit_cost_gbp` & `msrp_gbp`**: Standardized baseline cost and recommended retail price.
* **`gross_margin_gbp`**: Calculated unit margin (`msrp_gbp - unit_cost_gbp`).
* **`gross_margin_percentage`**: Standardized gross profitability percentage metric for commercial analysis.

### `dim_customers` (Customer Demographics)
* **`customer_id`**: Unique customer key.
* **`email`**: Cleaned and validated lowercase contact handle.
* **`country_code`**: Standardized ISO market indicator (`UK`, `US`, `DE`).
* **`registered_date`**: Normalized registration date field for cohort retention modeling.

---

## 🛠️ Tech Stack

* **Cloud Data Warehouse:** Snowflake
* **Data Transformation Framework:** dbt Core (`dbt-snowflake`)
* **Languages:** SQL (Snowflake dialect), Python (Pandas, Faker)
* **DevOps / CI/CD:** GitHub Actions, Git
* **Testing & Governance:** dbt Schema Assertions (`unique`, `not_null`)