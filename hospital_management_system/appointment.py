"""
Appointment Class for Hospital Management System
Represents an appointment between a patient and doctor with scheduling and status management.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum


class AppointmentStatus(Enum):
    """Enumeration for appointment statuses"""
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"


class Appointment:
    def __init__(self, patient_id: str, doctor_id: str, date: str, 
                 time_slot: str, appointment_type: str = "Regular", 
                 notes: str = "", status: AppointmentStatus = AppointmentStatus.SCHEDULED):
        """
        Initialize a new appointment
        
        Args:
            patient_id: ID of the patient
            doctor_id: ID of the doctor
            date: Appointment date (YYYY-MM-DD)
            time_slot: Time slot (HH:MM-HH:MM)
            appointment_type: Type of appointment (Regular, Emergency, Follow-up, etc.)
            notes: Additional notes about the appointment
            status: Current status of the appointment
        """
        self.appointment_id = str(uuid.uuid4())[:8]
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time_slot = time_slot
        self.appointment_type = appointment_type
        self.notes = notes
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.diagnosis: Optional[str] = None
        self.prescription: Optional[str] = None
        self.follow_up_date: Optional[str] = None
        self.cost: float = 0.0
        
    def update_status(self, new_status: AppointmentStatus, notes: str = "") -> str:
        """Update appointment status"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now()
        
        if notes:
            self.notes += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {notes}"
        
        return f"Appointment status updated from {old_status.value} to {new_status.value}"
    
    def add_diagnosis(self, diagnosis: str) -> str:
        """Add diagnosis to the appointment"""
        if self.status in [AppointmentStatus.IN_PROGRESS, AppointmentStatus.COMPLETED]:
            self.diagnosis = diagnosis
            self.updated_at = datetime.now()
            return "Diagnosis added successfully"
        return "Cannot add diagnosis to appointment with current status"
    
    def add_prescription(self, prescription: str) -> str:
        """Add prescription to the appointment"""
        if self.status in [AppointmentStatus.IN_PROGRESS, AppointmentStatus.COMPLETED]:
            self.prescription = prescription
            self.updated_at = datetime.now()
            return "Prescription added successfully"
        return "Cannot add prescription to appointment with current status"
    
    def set_follow_up_date(self, follow_up_date: str) -> str:
        """Set follow-up appointment date"""
        if self.status == AppointmentStatus.COMPLETED:
            self.follow_up_date = follow_up_date
            self.updated_at = datetime.now()
            return f"Follow-up date set to {follow_up_date}"
        return "Can only set follow-up date for completed appointments"
    
    def set_cost(self, cost: float) -> str:
        """Set appointment cost"""
        if cost >= 0:
            self.cost = cost
            self.updated_at = datetime.now()
            return f"Appointment cost set to ${cost:.2f}"
        return "Cost cannot be negative"
    
    def reschedule(self, new_date: str, new_time_slot: str) -> str:
        """Reschedule the appointment"""
        if self.status in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]:
            return "Cannot reschedule cancelled or completed appointments"
        
        old_date = self.date
        old_time = self.time_slot
        
        self.date = new_date
        self.time_slot = new_time_slot
        self.updated_at = datetime.now()
        
        return f"Appointment rescheduled from {old_date} {old_time} to {new_date} {new_time_slot}"
    
    def cancel_appointment(self, reason: str = "") -> str:
        """Cancel the appointment"""
        if self.status in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]:
            return "Appointment is already cancelled or completed"
        
        self.status = AppointmentStatus.CANCELLED
        self.updated_at = datetime.now()
        
        if reason:
            self.notes += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Cancelled - {reason}"
        
        return "Appointment cancelled successfully"
    
    def start_appointment(self) -> str:
        """Mark appointment as in progress"""
        if self.status == AppointmentStatus.CONFIRMED:
            self.status = AppointmentStatus.IN_PROGRESS
            self.updated_at = datetime.now()
            return "Appointment started"
        return "Appointment must be confirmed before starting"
    
    def complete_appointment(self) -> str:
        """Mark appointment as completed"""
        if self.status == AppointmentStatus.IN_PROGRESS:
            self.status = AppointmentStatus.COMPLETED
            self.updated_at = datetime.now()
            return "Appointment completed successfully"
        return "Appointment must be in progress before completing"
    
    def get_appointment_summary(self) -> str:
        """Get a summary of appointment information"""
        return (f"Appointment ID: {self.appointment_id}\n"
                f"Patient ID: {self.patient_id}\n"
                f"Doctor ID: {self.doctor_id}\n"
                f"Date: {self.date}\n"
                f"Time: {self.time_slot}\n"
                f"Type: {self.appointment_type}\n"
                f"Status: {self.status.value}\n"
                f"Cost: ${self.cost:.2f}\n"
                f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Last Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def get_detailed_summary(self) -> str:
        """Get detailed appointment information including medical details"""
        summary = self.get_appointment_summary()
        
        if self.diagnosis:
            summary += f"\nDiagnosis: {self.diagnosis}"
        
        if self.prescription:
            summary += f"\nPrescription: {self.prescription}"
        
        if self.follow_up_date:
            summary += f"\nFollow-up Date: {self.follow_up_date}"
        
        if self.notes:
            summary += f"\nNotes: {self.notes}"
        
        return summary
    
    def is_urgent(self) -> bool:
        """Check if appointment is urgent"""
        return self.appointment_type.lower() in ["emergency", "urgent", "critical"]
    
    def is_follow_up(self) -> bool:
        """Check if appointment is a follow-up"""
        return self.appointment_type.lower() in ["follow-up", "followup", "review"]
    
    def __str__(self) -> str:
        """String representation of appointment"""
        return f"Appointment({self.appointment_id}) - {self.date} {self.time_slot} - {self.status.value}"
    
    def __repr__(self) -> str:
        """Detailed representation of appointment"""
        return (f"Appointment(appointment_id='{self.appointment_id}', "
                f"patient_id='{self.patient_id}', doctor_id='{self.doctor_id}', "
                f"date='{self.date}', time_slot='{self.time_slot}')")
