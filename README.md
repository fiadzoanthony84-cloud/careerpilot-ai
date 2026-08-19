# CareerPilot AI

CareerPilot AI is an AI-powered career assistance platform that helps users analyze their CV, discover suitable job opportunities, identify career skill gaps, generate personalized cover letters, detect potentially fraudulent job postings, and generate career insights and reports.

## Features

- CV Analysis
- Job Recommendations
- Career Insights
- Career Report
- AI Cover Letter Generation
- Job Scam Detection
- Backend API integration
- Interactive analytics and charts

## System Architecture

CareerPilot AI uses a frontend-backend architecture:

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Server:** Uvicorn
- **Machine Learning:** Scikit-learn and NLP models
- **Deployment:** Streamlit Community Cloud and Render
- **Version Control:** GitHub

User
  │
  ▼
Streamlit Frontend
  │
  │ HTTP Requests
  ▼
FastAPI Backend
  |
  ├── backend/
   ├── career_insights.py
   ├── cover_letter.py
   ├── cv_analyzer.py
   ├──matcher.py
   ├──matcher_v2.py
   ├── matcher_v3.py
   ├── scam_detector.py
   └── ...

The Streamlit frontend communicates with the FastAPI backend through HTTP requests.

##Project Structure

CareerPilot-AI/
│
├── assets/
│   ├── logo.png
│   └── styles.css
│
├── backend/
│   ├── career_insights.py
│   ├── cover_letter.py
│   ├── cv_analyzer.py
|   ├──matcher.py
|   ├──matcher_v2.py
│   ├── matcher_v3.py
│   ├── scam_detector.py
│   └── ...
├── data/
│   ├── Fake Postings.csv
│   ├── fake_job_postings.csv
│   ├── linkedin-job-postings-dataset.ipynb
│   ├── realfakejobposting.ipynb
│   └── linkedin/
│       ├── companies/
│       ├── jobs/
│       ├── mappings/
│       └── postings.csv
│
├── docs/
│   └── generated_cover_letter.txt
│
├── frontend/
│   ├── app.py
│   └── utils/
│       ├── __init__.py
│       ├── api_client.py
│       ├── charts.py
│       ├── constants.py
│       ├── helpers.py
│       └── mock_data.py
│
├── models/
│   ├── __init__.py
│   ├── matcher.py
│   ├── matcher_v2.py
│   ├── skill_gap.py
│   └── debug_pdf.py
│
├── tests/
│   ├── test_csv
│   ├── legitimate_examples.txt
│   └── scam_examples.txt
│
├── main.py
├── requirements.txt
├── .python-version
├── .gitignore
└── README.md

Technologies Used
Python
FastAPI
Uvicorn
Streamlit
Pandas
NumPy
Scikit-learn
spaCy
Plotly
Requests
PDFMiner
PDFPlumber

Running the Project Locally
The hosted application is recommended for normal use. However, the project can also be reproduced locally using the source code in this repository.

1. Install the dependencies
After obtaining the project source code, install the required Python packages:

pip install -r requirements.txt
2. Start the FastAPI backend

From the project root directory, run:
uvicorn main:app --host 0.0.0.0 --port 8000

The backend will be available at:
http://localhost:8000
3. Start the Streamlit frontend

Open another terminal in the project directory and run:
streamlit run frontend/app.py
Streamlit will provide a local URL that can be opened in a web browser.

##For the easiest way to evaluate the completed system, use the hosted application:
Click the Streamlit link  → https://careerpilot-ai-h84hoxjddn8tlcnuh44d6j.streamlit.app/
Click the render link → https://careerpilot-backend-0moc.onrender.com/health for the server in render 
Deployment
The production version of CareerPilot AI is deployed using:
Streamlit Community Cloud – Frontend
Render – FastAPI Backend
GitHub – Source code and version control
The frontend is configured to communicate with the deployed backend API.

Data and Machine Learning Models
The project uses job-posting datasets for job recommendation and scam-detection functionality. Machine learning components use techniques such as TF-IDF vectorization and similarity-based matching.
The project also contains supporting datasets and notebooks used during development and analysis.

Scam Detection
The scam detection component analyzes job-posting descriptions and uses a trained machine learning model to estimate whether a job posting is legitimate or potentially fraudulent.
The project includes example legitimate and fraudulent job postings in the tests/ directory for testing and evaluation.

Reproducibility
The repository contains the source code, dependencies, model-related files, datasets used by the application, and supporting resources required to understand and reproduce the project.
The required Python dependencies are specified in:

Authors
Group 12


