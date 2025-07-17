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


<div align="center">
  <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/streamlit.png" alt="Streamlit Dashboard 1" width="45%"/>
  <img src="https://raw.githubusercontent.com/bashoori/repo/master/marketing-analytics-pipeline/streamlit2.png" alt="Streamlit Dashboard 2" width="45%"/>
</div>
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
├── extract/                  # Extraction scripts
│   ├── extract_game_events.py
│   └── extract_campaigns.py
│
├── transform/                # Data transformation logic
│   └── transform_data.py
│
├── load/                     # PostgreSQL loader
│   └── load_to_postgres.py
│
├── dags/                     # Airflow DAGs
│   └── marketing_etl_dag.py
│
├── dashboard/                # Streamlit dashboard app
│   └── app.py
│
├── airflow/                  # Airflow docker-compose setup
│   └── docker-compose.yaml
│
├── data/                     # Sample CSV data
│   ├── game_events.csv
│   └── campaigns.csv
│
├── run_pipeline.py           # CLI runner for ETL
├── requirements.txt          # Python dependencies
└── README.md
```
---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/marketing-analytics-pipeline.git
cd marketing-analytics-pipeline
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

### 5. Run the ETL Pipeline Manually (Optional)
```
python run_pipeline.py
```

### 6. Run the Streamlit Dashboard
```
cd dashboard
streamlit run app.py
```

## 🔄 Run Apache Airflow Locally
# Navigate to Airflow folder:
```
cd airflow
```
# First-Time Initialization (run once):
```
docker-compose up --build
```
This automatically runs airflow db init and creates the admin user.

# Run Airflow services:
```
docker-compose up webserver scheduler
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

##  Initialize the Airflow database (first-time only)
docker-compose up airflow-init
docker-compose up webserver scheduler

## Start Airflow services
docker-compose up

```
cd airflow
docker-compose up airflow-init  # No need for this , becouse it include the docker Run once to initialize
docker-compose up webserver scheduler #bring up the main services:
docker-compose up               # Then start Airflow
```

🌐 Access Airflow UI
Visit:
http://localhost:8080

Login:
	•	Username: airflow
	•	Password: airflow

Make sure Docker is installed and running on your system. (for PostgreSQL you should install docker)

- [Install Docker](https://docs.docker.com/get-docker/)
- Then run:
```bash
docker-compose -f docker/docker-compose.yml up -d


