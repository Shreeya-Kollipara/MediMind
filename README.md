# 🩺 MediMind – Multi-Agent AI Clinical Assistant

<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python"/>
<img src="https://img.shields.io/badge/Flask-Web_App-black?logo=flask"/>
<img src="https://img.shields.io/badge/spaCy-NLP-09A3D5"/>
<img src="https://img.shields.io/badge/Gemini-LLM-orange"/>
<img src="https://img.shields.io/badge/Multi-Agent_AI-Enabled-success"/>
<img src="https://img.shields.io/badge/Healthcare-AI-red"/>

</p>

---

## 📖 Overview

**MediMind** is an explainable **Multi-Agent AI Clinical Assistant** that analyzes natural language symptom descriptions and generates structured healthcare insights using **Natural Language Processing (NLP)**, **rule-based clinical reasoning**, and the **Gemini Large Language Model (LLM)**.

The system follows an **agentic workflow** where specialized AI agents collaborate to extract symptoms, assess clinical risk, reason about possible medical conditions, and generate personalized healthcare guidance through an intuitive web interface.

---

# ✨ Features

- 🤖 Multi-Agent AI Architecture
- 🩺 Clinical Symptom Analysis
- 🧠 NLP-based Symptom Extraction
- ⚠️ Rule-based Risk Assessment
- 💡 Gemini LLM Reasoning
- 📊 Explainable AI Decision Pipeline
- 📋 Structured Healthcare Recommendations
- 🌐 Flask Web Application
- 🎯 Modular & Scalable Design

---

# 🤖 Agentic AI Workflow

Unlike traditional chatbots, MediMind follows an **Agentic AI** architecture where multiple specialized agents collaborate to solve a medical reasoning task.

Each agent has an independent responsibility while the **Manager Agent** orchestrates communication and ensures coherent decision-making.

```
                 User Input
                      │
                      ▼
          ┌────────────────────┐
          │     NLP Agent      │
          └────────────────────┘
                      │
          Extract Symptoms
          Normalize Text
          Clean Input
                      │
                      ▼
          ┌────────────────────┐
          │    Risk Agent      │
          └────────────────────┘
                      │
       Rule-based Medical Triage
       Emergency Detection
       Risk Score Calculation
                      │
                      ▼
          ┌────────────────────┐
          │   Gemini LLM Agent │
          └────────────────────┘
                      │
      Medical Reasoning
      Possible Conditions
      Personalized Advice
                      │
                      ▼
          ┌────────────────────┐
          │  Manager Agent     │
          └────────────────────┘
                      │
 Integrates outputs from all agents
 Generates structured response
                      │
                      ▼
          ┌────────────────────┐
          │   Frontend UI      │
          └────────────────────┘
```

---

# 🧠 Agent Responsibilities

## 🔹 NLP Agent

Responsible for understanding user input.

**Tasks**

- Text preprocessing
- Symptom extraction
- Medical term normalization
- Regex + spaCy processing

---

## 🔹 Risk Assessment Agent

Evaluates clinical severity.

**Tasks**

- Emergency symptom detection
- Rule-based medical reasoning
- Risk score calculation
- Risk classification

Possible Risk Levels

🟢 LOW

🟡 MODERATE

🟠 HIGH

🔴 EMERGENCY

---

## 🔹 Gemini LLM Agent

Provides intelligent clinical reasoning.

**Tasks**

- Predict possible conditions
- Generate healthcare advice
- Explain medical reasoning
- Produce natural language responses

---

## 🔹 Manager Agent

Acts as the orchestrator of the multi-agent system.

**Responsibilities**

- Coordinates all AI agents
- Aggregates outputs
- Maintains consistency
- Formats final response
- Sends structured results to the UI

---

# ⚙️ System Pipeline

```
User Symptom Input
        │
        ▼
Natural Language Processing
        │
        ▼
Symptom Extraction
        │
        ▼
Risk Assessment
        │
        ▼
Gemini Clinical Reasoning
        │
        ▼
Response Orchestration
        │
        ▼
Structured Healthcare Output
```

---

# 📊 Output

The application provides

✅ Extracted Symptoms

✅ Clinical Risk Level

✅ Risk Score

✅ Possible Medical Conditions

✅ Explainable AI Reasoning

✅ Personalized Healthcare Advice

---

# 💻 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Backend | Flask, Python |
| Frontend | HTML, CSS, JavaScript |
| NLP | spaCy, Regex |
| LLM | Gemini |
| AI Design | Multi-Agent Architecture |
| APIs | REST API |

---

# 📂 Project Structure

```
MediMind
│
├── app.py
├── requirements.txt
├── README.md
│
├── agents/
│   ├── nlp_agent.py
│   ├── risk_agent.py
│   ├── llm_agent.py
│   └── manager.py
│
├── utils/
│   ├── preprocess.py
│   ├── prompts.py
│   └── helper.py
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
└── models/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/MediMind.git
```

Move into the project

```bash
cd MediMind
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 🔮 Future Enhancements

- 🎤 Voice-based symptom analysis
- 🌍 Multilingual support
- 🏥 Electronic Health Record (EHR) integration
- 💊 Drug interaction analysis
- 📅 Appointment scheduling
- ☁️ Cloud deployment
- 📱 Mobile application

---

# 👨‍⚕️ Medical Disclaimer

**MediMind is an AI-assisted clinical decision support system intended for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns or emergencies.**

---

# 👩‍💻 Author

**Kollipara Naga Shreeya**

B.Tech CSE (AI & ML)

VIT Chennai

---

## ⭐ If you found this project interesting, consider giving it a Star!
