# 🏥 AI Medical Diagnosis System

A comprehensive medical diagnosis website powered by the MMed-Llama-3-8B-EnIns AI model from Hugging Face, designed specifically for medical instruction following.

## 🌟 Features

- **AI-Powered Diagnosis**: Uses MMed-Llama-3-8B-EnIns model for accurate medical assessment
- **Symptom Input Interface**: Easy-to-use symptom selection and input system
- **Personalized Treatment**: Customized medicine recommendations and dosages
- **Risk Assessment**: Color-coded severity levels (Low, Medium, High, Critical)
- **Professional UI**: Modern, responsive design with dark mode support
- **Safety Features**: Medical disclaimers and emergency alerts

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

### 1. Setup Frontend

```bash
# Navigate to the project directory
cd medico

# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 2. Setup Backend

```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

**Or use the batch file on Windows:**
```bash
# Double-click or run in command prompt
start_server.bat
```

The backend API will be available at `http://localhost:8000`

## 🧠 AI Model Information

This system uses the **MMed-Llama-3-8B-EnIns** model:
- **Model**: [Henrychur/MMed-Llama-3-8B-EnIns](https://huggingface.co/Henrychur/MMed-Llama-3-8B-EnIns)
- **Type**: Medical instruction-following language model
- **Base**: LLaMA-3-8B fine-tuned for medical applications
- **Capabilities**: Medical diagnosis, treatment recommendations, drug interactions

## 🚨 Important Disclaimers

- **Not a Medical Device**: This system is for educational and informational purposes only
- **No Medical Advice**: Results should not replace professional medical consultation
- **Emergency Situations**: Always contact emergency services for urgent medical needs
- **Accuracy**: AI predictions may not always be accurate - consult healthcare professionals
