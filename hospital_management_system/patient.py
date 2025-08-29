"""
Patient Class for Hospital Management System
Represents a patient with personal information, medical history, and appointments.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict


class Patient:
    def __init__(self, name: str, age: int, gender: str, phone: str, 
                 address: str = "", emergency_contact: str = "", 
                 blood_group: str = "", medical_history: str = ""):
        """
        Initialize a new patient
        
        Args:
            name: Patient's full name
            age: Patient's age
            gender: Patient's gender
            phone: Contact phone number
            address: Patient's address
            emergency_contact: Emergency contact information
            blood_group: Patient's blood group
            medical_history: Previous medical conditions
        """
        self.patient_id = str(uuid.uuid4())[:8]
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address
        self.emergency_contact = emergency_contact
        self.blood_group = blood_group
        self.medical_history = medical_history
        self.admission_date = datetime.now()
        self.is_active = True
        self.appointments: List[str] = []  # List of appointment IDs
        self.prescriptions: List[Dict] = []  # List of prescription dictionaries
        
        # Add contact property for GUI compatibility
        self.contact = phone
        
    def add_appointment(self, appointment_id: str) -> str:
        """Add an appointment to patient's record"""
        if appointment_id not in self.appointments:
            self.appointments.append(appointment_id)
            return f"Appointment {appointment_id} added successfully"
        return "Appointment already exists"
    
    def remove_appointment(self, appointment_id: str) -> str:
        """Remove an appointment from patient's record"""
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
            return f"Appointment {appointment_id} removed successfully"
        return "Appointment not found"
    
    def add_prescription(self, doctor_name: str, medicine: str, 
                        dosage: str, duration: str, notes: str = "") -> str:
        """Add a prescription to patient's medical record"""
        prescription = {
            'id': str(uuid.uuid4())[:8],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'doctor': doctor_name,
            'medicine': medicine,
            'dosage': dosage,
            'duration': duration,
            'notes': notes
        }
        self.prescriptions.append(prescription)
        return f"Prescription added successfully (ID: {prescription['id']})"
    
    def get_prescription_history(self) -> List[Dict]:
        """Get all prescriptions for the patient"""
        return self.prescriptions
    
    def update_medical_history(self, new_condition: str) -> str:
        """Update patient's medical history"""
        if self.medical_history:
            self.medical_history += f"\n{datetime.now().strftime('%Y-%m-%d')}: {new_condition}"
        else:
            self.medical_history = f"{datetime.now().strftime('%Y-%m-%d')}: {new_condition}"
        return "Medical history updated successfully"
    
    def deactivate_patient(self) -> str:
        """Deactivate patient account"""
        self.is_active = False
        return f"Patient {self.name} deactivated successfully"
    
    def activate_patient(self) -> str:
        """Reactivate patient account"""
        self.is_active = True
        return f"Patient {self.name} activated successfully"
    
    def get_patient_summary(self) -> str:
        """Get a summary of patient information"""
        status = "Active" if self.is_active else "Inactive"
        return (f"Patient ID: {self.patient_id}\n"
                f"Name: {self.name}\n"
                f"Age: {self.age}\n"
                f"Gender: {self.gender}\n"
                f"Phone: {self.phone}\n"
                f"Blood Group: {self.blood_group}\n"
                f"Status: {status}\n"
                f"Total Appointments: {len(self.appointments)}\n"
                f"Total Prescriptions: {len(self.prescriptions)}")
    
    def __str__(self) -> str:
        """String representation of patient"""
        status = "Active" if self.is_active else "Inactive"
        return f"Patient({self.patient_id}) - {self.name} ({self.age}, {self.gender}) - {status}"
    
    def __repr__(self) -> str:
        """Detailed representation of patient"""
        return f"Patient(patient_id='{self.patient_id}', name='{self.name}', age={self.age}, gender='{self.gender}')"
