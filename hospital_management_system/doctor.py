"""
Doctor Class for Hospital Management System
Represents a doctor with specialization, schedule, and patient management.
"""

import uuid
from datetime import datetime, time
from typing import List, Dict, Optional, Set


class Doctor:
    def __init__(self, name: str, specialization: str, phone: str, 
                 email: str = "", experience_years: int = 0, 
                 qualification: str = "", department: str = ""):
        """
        Initialize a new doctor
        
        Args:
            name: Doctor's full name
            specialization: Medical specialization
            phone: Contact phone number
            email: Email address
            experience_years: Years of experience
            qualification: Medical qualifications
            department: Hospital department
        """
        self.doctor_id = str(uuid.uuid4())[:8]
        self.name = name
        self.specialization = specialization
        self.phone = phone
        self.email = email
        self.experience_years = experience_years
        self.qualification = qualification
        self.department = department
        self.join_date = datetime.now()
        self.is_active = True
        self.patients: Set[str] = set()  # Set of patient IDs
        self.schedule: Dict[str, List[Dict]] = {}  # Schedule by date
        self.consultation_fee = 0.0
        
    def add_patient(self, patient_id: str) -> str:
        """Add a patient to doctor's patient list"""
        if patient_id not in self.patients:
            self.patients.add(patient_id)
            return f"Patient {patient_id} added to doctor's list"
        return "Patient already in doctor's list"
    
    def remove_patient(self, patient_id: str) -> str:
        """Remove a patient from doctor's patient list"""
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            return f"Patient {patient_id} removed from doctor's list"
        return "Patient not found in doctor's list"
    
    def set_consultation_fee(self, fee: float) -> str:
        """Set consultation fee for the doctor"""
        if fee >= 0:
            self.consultation_fee = fee
            return f"Consultation fee set to ${fee:.2f}"
        return "Consultation fee cannot be negative"
    
    def add_schedule_slot(self, date: str, start_time: str, end_time: str, 
                          max_patients: int = 10) -> str:
        """
        Add a schedule slot for a specific date and time
        
        Args:
            date: Date in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            max_patients: Maximum number of patients for this slot
        """
        if date not in self.schedule:
            self.schedule[date] = []
        
        # Check for overlapping slots
        for slot in self.schedule[date]:
            if (start_time < slot['end_time'] and end_time > slot['start_time']):
                return f"Time slot conflicts with existing schedule: {slot['start_time']}-{slot['end_time']}"
        
        slot = {
            'id': str(uuid.uuid4())[:8],
            'start_time': start_time,
            'end_time': end_time,
            'max_patients': max_patients,
            'current_patients': 0,
            'booked_patients': []
        }
        
        self.schedule[date].append(slot)
        self.schedule[date].sort(key=lambda x: x['start_time'])
        return f"Schedule slot added: {date} {start_time}-{end_time}"
    
    def remove_schedule_slot(self, date: str, slot_id: str) -> str:
        """Remove a schedule slot"""
        if date in self.schedule:
            for i, slot in enumerate(self.schedule[date]):
                if slot['id'] == slot_id:
                    if slot['current_patients'] > 0:
                        return f"Cannot remove slot with {slot['current_patients']} booked patients"
                    del self.schedule[date][i]
                    if not self.schedule[date]:
                        del self.schedule[date]
                    return f"Schedule slot {slot_id} removed successfully"
        return "Schedule slot not found"
    
    def book_appointment(self, date: str, slot_id: str, patient_id: str) -> str:
        """Book an appointment in a schedule slot"""
        if date not in self.schedule:
            return f"No schedule available for {date}"
        
        for slot in self.schedule[date]:
            if slot['id'] == slot_id:
                if slot['current_patients'] >= slot['max_patients']:
                    return "This time slot is fully booked"
                
                if patient_id in slot['booked_patients']:
                    return "Patient already has an appointment in this slot"
                
                slot['current_patients'] += 1
                slot['booked_patients'].append(patient_id)
                self.add_patient(patient_id)
                return f"Appointment booked successfully for {date} {slot['start_time']}-{slot['end_time']}"
        
        return "Schedule slot not found"
    
    def cancel_appointment(self, date: str, slot_id: str, patient_id: str) -> str:
        """Cancel an appointment"""
        if date not in self.schedule:
            return f"No schedule available for {date}"
        
        for slot in self.schedule[date]:
            if slot['id'] == slot_id:
                if patient_id in slot['booked_patients']:
                    slot['booked_patients'].remove(patient_id)
                    slot['current_patients'] -= 1
                    return "Appointment cancelled successfully"
                return "Patient not found in this slot"
        
        return "Schedule slot not found"
    
    def get_available_slots(self, date: str) -> List[Dict]:
        """Get available schedule slots for a specific date"""
        if date not in self.schedule:
            return []
        
        available_slots = []
        for slot in self.schedule[date]:
            if slot['current_patients'] < slot['max_patients']:
                available_slots.append({
                    'slot_id': slot['id'],
                    'start_time': slot['start_time'],
                    'end_time': slot['end_time'],
                    'available_spots': slot['max_patients'] - slot['current_patients']
                })
        
        return available_slots
    
    def get_doctor_summary(self) -> str:
        """Get a summary of doctor information"""
        status = "Active" if self.is_active else "Inactive"
        total_patients = len(self.patients)
        total_slots = sum(len(slots) for slots in self.schedule.values())
        
        return (f"Doctor ID: {self.doctor_id}\n"
                f"Name: Dr. {self.name}\n"
                f"Specialization: {self.specialization}\n"
                f"Department: {self.department}\n"
                f"Experience: {self.experience_years} years\n"
                f"Qualification: {self.qualification}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}\n"
                f"Status: {status}\n"
                f"Consultation Fee: ${self.consultation_fee:.2f}\n"
                f"Total Patients: {total_patients}\n"
                f"Total Schedule Slots: {total_slots}")
    
    def __str__(self) -> str:
        """String representation of doctor"""
        status = "Active" if self.is_active else "Inactive"
        return f"Dr. {self.name} ({self.specialization}) - {status}"
    
    def __repr__(self) -> str:
        """Detailed representation of doctor"""
        return f"Doctor(doctor_id='{self.doctor_id}', name='{self.name}', specialization='{self.specialization}')"
