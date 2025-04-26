# CareCase 🏥 – AI-Powered Clinical Simulation Platform

**CareCase** is an AI-driven simulation tool that helps medical students practice patient interactions, diagnosis, and communication skills in a dynamic, realistic environment.  
It is designed to work both online and offline, using lightweight AI models for speech, vision, and intelligent feedback.

---

## 🛠️ Tech Stack

- **Frontend**: Python (Tkinter)
    
- **Backend**: Python (FastAPI), MongoDB Atlas
    
- **Audio Pipeline**: Whisper.cpp (STT) + OpenAI GPT + Edge-TTS (TTS) +  SentenceTransformer
    
- **Computer Vision**: Mediapipe + FER (Facial Expression Recognition)
    
- **Hardware**: Raspberry Pi 5 and  Raspberry Pi Zero 2w (WIP)
    

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/CareCase.git
cd CareCase
```

### Backend Setup

```bash
python3 -m venv backend-env
source backend-env/bin/activate
pip install -r requirements-backend.txt
```

Start the FastAPI server:

```bash
uvicorn server.main:app --reload
```

---

### Frontend (Desktop App) Setup

```bash
python3 -m venv frontend-env
source frontend-env/bin/activate
pip install -r requirements-frontend.txt
```

Launch the UI app:

```bash
python client/app.py
```

---

### Vision & Expression Tools Setup (FER, Gaze Tracking)

```bash
python3 -m venv fer-env
source fer-env/bin/activate
pip install -r requirements-fer.txt
```

Then enables you to run the gaze tracking or face/expression monitoring tools as needed.

---

## 📦 Notes

- **MongoDB credentials** are required in a `.env` file.
    
- **OpenAI API key** is needed if running online mode for dynamic content generation.
    
- Designed to **fallback** using local models if API keys are missing.
    

---
