# AI-Powered Finance Credit Follow-Up Agent

An AI-powered finance collections assistant that automates payment follow-up email generation for overdue invoices using Large Language Models (LLMs).

The application allows users to:
- Upload customer invoice datasets
- Automatically classify escalation stages
- Generate AI-based payment reminder emails
- Review escalation accounts requiring human intervention
- Download generated results in JSON format
- Simulate email sending through an interactive Streamlit UI

---

# Features

- AI-generated payment follow-up emails
- Dynamic escalation-stage handling
- Human intervention workflow for critical accounts
- CSV upload and validation
- Interactive Streamlit dashboard
- Downloadable JSON outputs
- Progress tracking and email preview
- Search and filtering functionality

---

# Tech Stack

- Python
- Streamlit
- Pandas
- OpenRouter API
- GPT-3.5 Turbo
- JSON
- dotenv

---

# STEPS TO RUN THE PROGRAM

STEP 1

git clone https://github.com/Shanwanth-16/Finance-Credit-follow-up-AI-Agent.git

---
STEP 2

cd Finance-Credit-follow-up-AI-Agent.git

---
STEP 3

Create a virtual enviroment 

python3 -m venv venv

Axtivate the virtual environment

source venv/bin/activate

---

STEP 4

Download dependencies mentioned in requirements.txt

pip install -r requirements.txt

---

STEP 5

Generating an openrouter api key to access the LLM

1. Visit:https://openrouter.ai/
2. Generate a key and copy the key to your clipboard
3. Create a .env file in the project folder and add the line api_key=YOUR_API_KEY
 
---

STEP 6

Generating Fake Data

Now just run the fakeDataGenerator.py file by running the coomand in VS Code terminal

python fake_data_generator.py

This will create an invoices.csv file in the project folder

---

STEP 7

To run the app

In vs code terminal write : streamlit run app.py

This will open the app in your browser.

THANK YOU


