CareerPilot AI



CareerPilot AI is an AI-powered career assistance platform that helps users analyze their CVs, discover suitable job opportunities, identify career skill gaps, generate personalized cover letters, detect potentially fraudulent job postings, and generate career insights and reports.



\# Features



\- CV Analysis

\- Job Recommendations

\- Career Insights

\- Career Report

\- AI Cover Letter Generation

\- Job Scam Detection

\- Backend API integration

\- Interactive analytics and charts

# How CareerPilot AI Works

CareerPilot AI takes information from a user's CV and uses it to provide different career support services.

The main process is:

1. The user uploads their CV.
2. The system analyzes the CV and extracts relevant information such as skills, education, and experience.
3. The extracted information is used to find suitable job and internship opportunities.
4. The system identifies skills that may be missing for recommended opportunities.
5. Users can also receive career insights, generate a personalized cover letter, and check job postings for possible scams.

This allows the user's CV information to be used across different features instead of requiring the user to enter the same information multiple times.


\# System Architecture



CareerPilot AI uses a frontend-backend architecture:



\- \*\*Frontend:\*\* Streamlit

\- \*\*Backend:\*\* FastAPI

\- \*\*Server:\*\* Uvicorn

\- \*\*Machine Learning:\*\* Scikit-learn and NLP models

\- \*\*Deployment:\*\* Streamlit Community Cloud and Render

\- \*\*Version Control:\*\* GitHub



The Streamlit frontend communicates with the FastAPI backend through HTTP requests.



\# Project Structure



```text

careerpilot-ai/

│

├── assets/

│   ├── logo.png

│   └── styles.css

│

├── data/

│   ├── Fake Postings.csv

│   ├── fake\_job\_postings.csv

│   └── ...

│

├── docs/

│   └── generated\_cover\_letter.txt

│

├── frontend/

│   ├── app.py

│   └── utils/

│       ├── api\_client.py

│       ├── charts.py

│       ├── constants.py

│       ├── helpers.py

│       └── mock\_data.py

│

├── models/

│   └── ...

│

├── main.py

├── requirements.txt

├── .python-version

└── README.md

