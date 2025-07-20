# 🧠 Marketing Analytics ETL Pipeline with Apache Airflow

This project implements a modular ETL pipeline using **Apache Airflow** to extract, transform, and load marketing data from various sources. It uses custom Python scripts organized in `extract/`, `transform/`, and `load/` directories, and runs via Airflow using Docker Compose.


## ⚙️ Technologies

- **Apache Airflow 2.7.1**
- **Python 3.10+**
- **PostgreSQL (Airflow + Marketing DB)**
- **Docker + Docker Compose**


## 📸 Dashboard Preview

<div align="center">
  <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/streamlit.png" alt="Streamlit Dashboard 1" width="45%"/>
  <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/streamlit2.png" alt="Streamlit Dashboard 2" width="45%"/>
  <br/>
  <a href="https://github.com/bashoori/repo/blob/master/marketing-analytics-pipeline/airflow.png" target="_blank">
    <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/airflow.png" alt="Airflow DAG" width="45%"/>
  </a>
  <a href="https://github.com/bashoori/repo/blob/master/marketing-analytics-pipeline/airflow2.png" target="_blank">
    <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/airflow2.png" alt="Airflow DAG Status" width="45%"/>
  </a>
</div>


## 📂 Project Structure
```
marketing-analytics-pipeline/
├── dags/                     # Airflow DAGs
├── data/                     # Raw and staging data (JSON, CSV)
├── etl/                      # Modular ETL code
│   ├── extract/              # Data extraction scripts
│   ├── transform/            # Data cleaning & transformation
│   └── load/                 # Load to PostgreSQL
├── dashboard/                # Streamlit dashboard app
├── scripts/                  # Utility scripts (run_pipeline.py, test_json.py, etc.)
├── logs/                     # Airflow logs (gitignored)
├── plugins/                  # Airflow plugins (if any)
├── requirements.txt          # Python dependencies
├── docker-compose.yaml       # Container setup
├── .env                      # Environment variables (excluded from Git)
└── airflow.cfg               # Airflow config (excluded from Git)
```

---

## 🚀 Features

- Modular ETL: Cleanly separated Extract, Transform, Load steps

- Airflow 2.7.1: DAG-based orchestration with retries, scheduling, and logging

- PostgreSQL: Used for both Airflow metadata and final marketing DB

- Docker Compose: One-command containerized deployment

- Streamlit Dashboard: Real-time visualization of key marketing KPIs

---

🌐 Streamlit Dashboard Preview

The dashboard includes:

- 📊 Total Revenue, Average Order Value

- 📉 Conversion Rate & Click-Through Rate

- 📍 Sales Distribution by Region (Map)

- 🕒 Filters by Date & Product Category


###  Run locally:
```
cd dashboard
streamlit run dashboard.py
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/marketing-analytics-pipeline.git
cd marketing-analytics-pipeline
```

### 2. Add Environment Variables

Create a .env file:
```
AIRFLOW_DB_USER=airflow
AIRFLOW_DB_PASSWORD=airflow
AIRFLOW_DB_NAME=airflow

MARKETING_DB_USER=marketer
MARKETING_DB_PASSWORD=marketer
MARKETING_DB_NAME=marketing
```
### 3. Start Airflow + PostgreSQL Services
```
docker-compose down --volumes
docker-compose up --build 
```
### 4. Access Airflow UI

Visit: http://localhost:8080
Login: airflow / airflow

Enable the DAG named marketing_etl_pipeline.

## 🧪 DAG Logic
	•	extract_game_events: Pulls raw game events
	•	extract_campaign_data: Pulls ad campaign data
	•	transform_data: Joins & cleans the extracted data
	•	load_data: Loads final data into a PostgreSQL table

Dependency Flow:
```
[extract_game_events, extract_campaign_data] → transform_data → load_data
```

## 🧼 Troubleshooting

“ModuleNotFoundError: No module named ‘extract’”

Make sure the full project is mounted in Docker:

In docker-compose.yaml:
```
volumes:
  - .:/opt/airflow  # ✅ Mount the entire project root
```

Also, the DAG includes:
```
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
```

## 📈 Future Improvements
	•	Add unit tests
	•	Enable logging and monitoring
	•	Add email alerts for task failures
	•	Use Docker Secrets for credentials
	•	Deploy to cloud (e.g. AWS, GCP Composer)


## 👩‍💻 Author

Bita Ashoori
Data Engineer 