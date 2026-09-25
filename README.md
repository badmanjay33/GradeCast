# 🎓 GradeCast

**Your AI-Powered Academic Strategist & Transcript Analyzer**

GradeCast is an intelligent academic tracking platform designed to transform raw student transcript data into actionable, human-readable advice. Built with Python and powered by Google's Gemini API, GradeCast acts as a personalized academic mentor—analyzing past performance, forecasting future scenarios, and helping students strategically navigate their degree paths.

Initially configured for the American University of Nigeria (AUN) grading system, the core engine is fully modular and adaptable to any university standard.

---

## ✨ Core Features

### 📊 1. Data Analytics & Visualization
* **Transcript Parsing:** Ingests CSV data of courses, units, and grades.
* **Chronological Sorting:** Intelligently maps American semester systems (Fall, Spring, Summer, Intersession) into a true chronological timeline.
* **Trend Visualization:** Generates Matplotlib line charts to visualize GPA momentum over time.

### 🔮 2. The Forecaster 
* **What-If Simulator:** Input hypothetical future grades to see the immediate mathematical impact on your overall CGPA.
* **Next Target Calculator:** Reverses the math to tell you the exact semester GPA required to hit a specific CGPA milestone.

### 🧠 3. The AI Advisor (Powered by Gemini)
The crown jewel of GradeCast. The AI Advisor acts as a "cool senior engineer/mentor," providing highly practical advice without robotic bureaucracy.
* **Goal Seeker:** Tells you exactly what you need to lock in to achieve honors (e.g., Magna Cum Laude). If mathematically impossible, it immediately calculates and pivots you to your maximum possible ceiling.
* **Subject Analysis:** Groups your transcript by course prefixes (e.g., MAT, CIE, WRI) to identify your strongest domains and areas for improvement.
* **Semester Retrospective:** Compares your most recent term to your historical average to contextualize your performance against credit load.
* **Smart Error Handling:** Features built-in exponential backoff, rate-limit management (HTTP 429), and server overload (HTTP 503) detection with custom `Retry-After` header extraction.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* A Google Gemini API Key (Free tier works perfectly)

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/badmanjay33/GradeCast.main](https://github.com/badmanjay33/GradeCast.main)
   cd GradeCast