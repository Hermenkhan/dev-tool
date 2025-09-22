# **Name:Muhammad Hermen Khan**


# **Email:khanhermen@gmail.com**

# **Agentic AI Bootcamp Cohort 02**

# **Live App: [hermendevtool.streamlit.app](https://hermendevtool.streamlit.app/)**

# **Demo Video Link: https://drive.google.com/file/d/1WlrwVc7lPJVQfnHHYp607vh7084zFaXb/view?usp=sharing**

---

# 🛠️ Agentic AI Bootcamp – Capstone Project

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?logo=chainlink\&logoColor=white)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live App](https://img.shields.io/badge/Live%20App-Available-brightgreen)](https://hermendevtool.streamlit.app/)

> **An interactive Streamlit application showcasing LangChain agents with multiple tools — calculator, weather, news, movie details, recipes, and distance calculations — powered by structured function calling.**



---

## 📑 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture Diagram](#architecture-diagram)
* [Setup](#setup)
* [Agent Prompt Design](#agent-prompt-design)
* [LangSmith Tracing & Metrics](#langsmith-tracing--metrics)
* [Screenshots](#screenshots)
* [License](#license)

---

## 📝 Overview

This project demonstrates a **LangChain-based agent** integrated with multiple real-world APIs. It uses **Structured Chat Zero-Shot React Description** to invoke tools dynamically based on user prompts. Built with **Streamlit**, it’s a one-stop app to:

* Calculate mathematical expressions
* Fetch real-time weather
* Get latest news on a topic
* Fetch detailed movie information
* Search for recipes
* Compute distances between two locations

---

## ✨ Features

* **Six tools available**: Calculator, Weather, News, Movie Details, Recipe, Distance.
* **Streamlit UI** for selecting tools dynamically.
* **Google Generative AI (Gemini 1.5 Flash)** as the LLM backend.
* **Environment variables & secrets** for API keys.
* **LangSmith tracing** enabled to monitor token usage, latency, and failures.

---

## 🏗️ Architecture Diagram

```
┌────────────┐         ┌─────────────┐
│  Streamlit │  Input  │   LangChain  │
│    Frontend│ ──────▶ │ Agent + LLM  │
└────┬───────┘         └────┬────────┘
     │ Tools: calculator, weather, news, movies, recipes, distance
     │
     ▼
External APIs (OpenWeatherMap, NewsAPI, OMDb, Spoonacular, OpenCage)
```



---

## ⚙️ Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/function-calling-project.git
cd function-calling-project
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

> 💡 If you face any Streamlit errors:

```bash
pip install streamlit
```

### 3️⃣ Set Up Secrets

* Go to `.streamlit/secrets.toml` and add:

```toml
GOOGLE_API_KEY="your-google-api-key"
```

* Add your other API keys (OpenWeatherMap, NewsAPI, OMDb, Spoonacular, OpenCage) in the same file.

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📝 Agent Prompt Design

This project uses **AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION** which:

* Takes **user input** (tool selection + prompt).
* Parses it against available tools.
* Invokes the corresponding function automatically.

**Tools integrated:**

* `calculator` → evaluates math expressions
* `get_weather` → current weather for a city
* `get_latest_news` → topic-based news
* `get_movie_details` → fetch movie info from OMDb
* `get_recipe` → Spoonacular recipes
* `get_distance` → calculates distance between locations

---

## 📊 LangSmith Tracing & Metrics

**LangSmith tracing is enabled:**

```python
LANGSMITH_TRACING = True
```

| Prompt Example              | Latency (s) | Tokens | Cost (\$) |
| --------------------------- | ----------- | ------ | --------- |
| Spaghetti Recipe (Failed)   | 9.74s       | 7,003  | \$0.00063 |
| Spaghetti Recipe (Success)  | 5.06s       | 2,450  | \$0.00020 |
| Lahore → Islamabad Distance | 9.82s       | 1,890  | \$0.00017 |
| Lahore Weather              | 3.79s       | 1,788  | \$0.00015 |
| 6 + 6 Calculation           | 2.65s       | 1,764  | \$0.00015 |

> **Avg Tool Latency:** 2–10 seconds depending on API response.
> **Failure Counts:** Occasional API errors (recipe tool for certain dishes).
> **Revision ID:** `42d3f41-dirty`

---



## 📝 License

This project is licensed under the MIT License.

---

### ✅ Quick Links

* **Live App:** [hermendevtool.streamlit.app](https://hermendevtool.streamlit.app/)
* **Issues & Feedback:** Please open an issue on GitHub.

---


