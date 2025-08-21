'use client';

import { useState } from 'react';
import SymptomInput from './SymptomInput';
import DiagnosisResults from './DiagnosisResults';
import Header from './Header';

export interface DiagnosisResult {
  disease: string;
  confidence: number;
  description: string;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  medicines: Medicine[];
  recommendations: string[];
}

export interface Medicine {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
  instructions: string;
}

export default function MedicalDiagnosis() {
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleDiagnosis = async (symptoms: string[], age: number, gender: string, medicalHistory: string) => {
    setLoading(true);
    
    try {
      // Call the real backend API
      const response = await fetch('http://localhost:8000/diagnose', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms,
          age,
          gender,
          medical_history: medicalHistory
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const diagnosisData = await response.json();
      setDiagnosis(diagnosisData);
      
    } catch (error) {
      console.error('Error calling diagnosis API:', error);
      
      // Fallback to mock data if API is not available
      const mockDiagnosis: DiagnosisResult = {
        disease: "API Connection Error - Mock Diagnosis",
        confidence: 75,
        description: "Unable to connect to the AI diagnosis server. This is a fallback diagnosis. Please ensure the backend server is running.",
        severity: "Medium",
        medicines: [
          {
            name: "Paracetamol",
            dosage: "500mg",
            frequency: "Every 6-8 hours",
            duration: "3-5 days",
            instructions: "Take with food to avoid stomach irritation"
          }
        ],
        recommendations: [
          "Please start the backend server by running the start_server.bat file",
          "Ensure Python and required dependencies are installed",
          "Check that port 8000 is not blocked by firewall",
          "Consult a healthcare professional for proper medical advice"
        ]
      };
      
      setDiagnosis(mockDiagnosis);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setDiagnosis(null);
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <Header />
      
      {!diagnosis ? (
        <SymptomInput onDiagnose={handleDiagnosis} loading={loading} />
      ) : (
        <DiagnosisResults diagnosis={diagnosis} onReset={handleReset} />
      )}
      
      {/* Disclaimer */}
      <div className="mt-12 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              Medical Disclaimer
            </h3>
            <div className="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
              <p>
                This AI diagnosis tool is for informational purposes only and should not replace professional medical advice, 
                diagnosis, or treatment. Always consult with qualified healthcare professionals for any medical concerns. 
                In case of emergency, contact your local emergency services immediately.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
