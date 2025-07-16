# 📊 User Engagement & Marketing ETL Pipeline

A modular ETL pipeline project that simulates real-world data engineering tasks by combining **user behavior data** (gameplay logs) and **marketing campaign data** to generate actionable insights — all fully orchestrated and containerized using Docker.

---

## 🚀 Features

- 🛠 Extracts user event data and marketing campaigns from **JSON files** (simulating APIs or streaming data)
- 🔄 Transforms, aggregates, and joins datasets using **Pandas**
- 🔗 Merges campaign and gameplay data on `user_id` to create a unified engagement view
- 💾 Loads the final dataset into a **PostgreSQL** database (simulating cloud warehouse like Redshift)
- 📅 Scheduled and orchestrated with **Apache Airflow DAGs**
- 📦 Fully containerized using **Docker Compose** (Airflow + PostgreSQL)
- 🖥 Visualized with an interactive **Streamlit dashboard**
- ✅ Runs seamlessly inside **GitHub Codespaces**


## 📸 Dashboard Preview

![Streamlit Dashboard](https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/streamlit.png)
---

## 🧠 Project Architecture
```
data sources
↓
[ Extract ]
↓
[ Transform ]
↓
[ Load to PostgreSQL ]
↓
[ Ready for Analytics / BI Dashboards ]
```
---

## 🧱 Tech Stack
```
| Stage        | Tools/Technologies                  |
|--------------|-------------------------------------|
| Extract      | Python, Pandas                      |
| Transform    | Pandas, SQL                         |
| Load         | SQLAlchemy, PostgreSQL              |
| Orchestration| Apache Airflow                      |
| Containerize | Docker, docker-compose              |
| Dev Env      | GitHub Codespaces, Virtualenv       |
```
---

## 📂 Project Structure
```
marketing-analytics-pipeline/
│
├── extract/                 # Scripts to pull data
│   ├── extract_game_events.py
│   └── extract_campaigns.py
│
├── transform/              # Data cleaning and joining
│   └── transform_data.py
│
├── load/                   # Load transformed data to PostgreSQL
│   └── load_to_postgres.py
│
├── dags/                   # Airflow DAGs
│   └── marketing_etl_dag.py
│
├── docker/                 # Docker configuration
│   └── docker-compose.yml
│
├── data/                   # Sample input files
│   ├── game_events.csv
│   └── campaigns.csv
│
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
├── run_pipeline.py         # Main ETL runner
└── README.md
```
---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/user-engagement-marketing-etl.git
cd user-engagement-marketing-etl
```
### 2. 🐳 Start PostgreSQL with Docker
```
docker-compose -f docker/docker-compose.yml up -d
```
### 3. 🐍 Create & activate virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 4. 📦 Run ETL pipeline manually (or via Airflow later)
```
python run_pipeline.py
```
### ✅ Sample Use Case
```
This project answers questions like:
	•	Which campaigns lead to high user engagement?
	•	What’s the average playtime or purchase value per campaign?
	•	Are paid campaigns outperforming organic channels?
```

📊 Sample Output After Transformation

This will help answer questions like:
	•	Which campaigns led to higher revenue or playtime?
	•	Which users were engaged but did not click ads?

	
	1. pip install -r requirements.txt
	2. docker-compose -f docker/docker-compose.yml up -d
	

	these are in requirements:
	3. pip install streamlit
	4. streamlit run app.py

## how to run Streamlit:

	streamlit run dashboard/app.py

## 🔧 Requirements

Make sure Docker is installed and running on your system. (for PostgreSQL you should install docker)

- [Install Docker](https://docs.docker.com/get-docker/)
- Then run:
```bash
docker-compose -f docker/docker-compose.yml up -d


