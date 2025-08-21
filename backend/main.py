from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re
import os

app = FastAPI(title="Medical Diagnosis API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
model = None
tokenizer = None

class SymptomRequest(BaseModel):
    symptoms: List[str]
    age: int
    gender: str
    medical_history: Optional[str] = ""

class Medicine(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str
    instructions: str

class DiagnosisResponse(BaseModel):
    disease: str
    confidence: float
    description: str
    severity: str
    medicines: List[Medicine]
    recommendations: List[str]

@app.on_event("startup")
async def load_model():
    """Load the MMed-Llama-3-8B-EnIns model on startup"""
    global model, tokenizer
    
    try:
        print("Loading MMed-Llama-3-8B-EnIns model...")
        model_name = "Henrychur/MMed-Llama-3-8B-EnIns"
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with appropriate device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True
        )
        
        if device == "cpu":
            model = model.to(device)
        
        print("Model loaded successfully!")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Falling back to mock responses...")

def create_medical_prompt(symptoms: List[str], age: int, gender: str, medical_history: str) -> str:
    """Create a structured prompt for the medical model"""
    symptoms_text = ", ".join(symptoms)
    
    prompt = f"""You are a medical AI assistant. Based on the following patient information, provide a medical diagnosis with treatment recommendations.

Patient Information:
- Age: {age}
- Gender: {gender}
- Symptoms: {symptoms_text}
- Medical History: {medical_history if medical_history else "None provided"}

Please provide your response in the following JSON format:
{{
    "disease": "Most likely condition name",
    "confidence": 85,
    "description": "Brief medical description of the condition",
    "severity": "Low|Medium|High|Critical",
    "medicines": [
        {{
            "name": "Medicine name",
            "dosage": "Dosage amount",
            "frequency": "How often to take",
            "duration": "How long to take",
            "instructions": "Special instructions"
        }}
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ]
}}

Important: Only suggest over-the-counter medications and general care recommendations. Always recommend consulting a healthcare professional for serious conditions."""

    return prompt

def parse_model_response(response_text: str) -> dict:
    """Parse the model's response and extract JSON"""
    try:
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
    except:
        pass
    
    # Fallback parsing if JSON extraction fails
    return {
        "disease": "General Symptom Assessment",
        "confidence": 75,
        "description": "Based on the symptoms provided, further medical evaluation is recommended.",
        "severity": "Medium",
        "medicines": [
            {
                "name": "Paracetamol",
                "dosage": "500mg",
                "frequency": "Every 6-8 hours as needed",
                "duration": "3-5 days",
                "instructions": "Take with food, do not exceed 4g per day"
            }
        ],
        "recommendations": [
            "Rest and get adequate sleep",
            "Stay hydrated with plenty of fluids",
            "Monitor symptoms and seek medical attention if they worsen",
            "Consult a healthcare professional for proper evaluation"
        ]
    }

def get_mock_diagnosis(symptoms: List[str], age: int, gender: str) -> dict:
    """Provide mock diagnosis when model is not available"""
    primary_symptom = symptoms[0].lower() if symptoms else "general"
    
    if any(s.lower() in ['fever', 'headache', 'cough', 'runny nose'] for s in symptoms):
        return {
            "disease": "Common Cold",
            "confidence": 82,
            "description": "A viral upper respiratory tract infection commonly caused by rhinovirus. Symptoms typically resolve within 7-10 days.",
            "severity": "Low",
            "medicines": [
                {
                    "name": "Paracetamol",
                    "dosage": "500mg",
                    "frequency": "Every 6 hours",
                    "duration": "3-5 days",
                    "instructions": "Take with food to reduce stomach irritation"
                },
                {
                    "name": "Cetirizine",
                    "dosage": "10mg",
                    "frequency": "Once daily",
                    "duration": "5-7 days",
                    "instructions": "May cause drowsiness, take before bedtime"
                }
            ],
            "recommendations": [
                "Get plenty of rest and sleep",
                "Drink warm fluids like herbal tea or warm water with honey",
                "Use a humidifier or inhale steam to relieve congestion",
                "Gargle with warm salt water for sore throat",
                "Avoid close contact with others to prevent spreading",
                "If symptoms persist beyond 10 days or worsen, consult a doctor"
            ]
        }
    
    return {
        "disease": "Symptom Complex Requiring Evaluation",
        "confidence": 70,
        "description": "The combination of symptoms requires professional medical evaluation for accurate diagnosis.",
        "severity": "Medium",
        "medicines": [
            {
                "name": "Paracetamol",
                "dosage": "500mg",
                "frequency": "As needed for pain/fever",
                "duration": "Short-term use only",
                "instructions": "Do not exceed 4g per day, take with food"
            }
        ],
        "recommendations": [
            "Schedule an appointment with a healthcare provider",
            "Keep a symptom diary noting when symptoms occur",
            "Stay hydrated and get adequate rest",
            "Avoid self-medication beyond basic pain relief",
            "Seek immediate medical attention if symptoms worsen rapidly"
        ]
    }

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(request: SymptomRequest):
    """Main endpoint for medical diagnosis"""
    try:
        if model is None or tokenizer is None:
            print("Model not available, using mock diagnosis")
            diagnosis_data = get_mock_diagnosis(request.symptoms, request.age, request.gender)
        else:
            # Create prompt for the model
            prompt = create_medical_prompt(
                request.symptoms, 
                request.age, 
                request.gender, 
                request.medical_history
            )
            
            # Tokenize and generate response
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode response
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response_text = response[len(prompt):].strip()
            
            # Parse the model's response
            diagnosis_data = parse_model_response(response_text)
        
        return DiagnosisResponse(**diagnosis_data)
        
    except Exception as e:
        print(f"Error in diagnosis: {e}")
        # Fallback to mock diagnosis
        diagnosis_data = get_mock_diagnosis(request.symptoms, request.age, request.gender)
        return DiagnosisResponse(**diagnosis_data)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Medical Diagnosis API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
