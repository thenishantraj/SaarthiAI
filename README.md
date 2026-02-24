<div align="center">
  
# 🎓 Saarthi AI - Your Personal Thinking Coach

### *"Empowering Students Through Guided Learning"*

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://saarthi-ai.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with%20%E2%9D%A4%20by-Nishant-00d4ff" alt="Made with love">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version">
</p>

---

https://github.com/user-attachments/assets/your-demo-video-link

</div>

## 🌟 **Live Demo**

Experience Saarthi AI in action: [Live Demo Link](https://saarthi-ai.streamlit.app)

---

## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📖 User Guide](#-user-guide)
- [💻 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Configuration](#️-configuration)
- [🔧 Development](#-development)
- [🌐 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [📞 Contact](#-contact)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ **Features**

<div align="center">

| Feature | Description | Status |
|---------|-------------|--------|
| 🔐 **Smart Authentication** | Neon-themed login/signup with SQLite | ✅ |
| 🌓 **Theme Switcher** | Toggle between Dark/Light modes | ✅ |
| 🧠 **Socratic AI Mentor** | Gemini-powered thinking coach | ✅ |
| 🌐 **Multilingual Support** | Hindi/English/Hinglish responses | ✅ |
| 📊 **Doubt Score Gauge** | Real-time confidence tracking | ✅ |
| 🔥 **Mastery Heatmap** | Visual progress tracking | ✅ |
| 📝 **Rubric Feedback** | Structured essay/code analysis | ✅ |
| 📱 **Responsive Design** | Perfect on mobile & desktop | ✅ |
| 💾 **Local Storage** | SQLite for user data | ✅ |
| 📈 **Progress Analytics** | Detailed learning insights | ✅ |

</div>

### 🎯 **Core Highlights**

- **🤖 Intelligent Socratic Method**: Never gives direct answers - guides you to discover solutions
- **📊 Smart Analytics**: Tracks your doubt patterns and learning progress
- **🌍 Language Flexible**: Ask questions in Hindi, English, or Hinglish
- **🎨 Beautiful UI**: Neon dark theme with smooth animations
- **📱 Mobile First**: Fully responsive design for all devices

---

## 🏗️ **Architecture**

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit UI] --> B[Custom CSS]
        A --> C[Session State]
    end
    
    subgraph "Application Layer"
        D[app.py - Main Controller]
        E[auth.py - Authentication]
        F[ai_engine.py - Gemini AI]
        G[ui_components.py - UI Components]
    end
    
    subgraph "Data Layer"
        H[(SQLite Database)]
        I[JSON Config]
        J[Session Cache]
    end
    
    subgraph "External Services"
        K[Google Gemini API]
    end
    
    A --> D
    D --> E
    D --> F
    D --> G
    E --> H
    F --> K
    F --> H
    G --> I
    C --> J
