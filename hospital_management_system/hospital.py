"""
Hospital Class for Hospital Management System
Main class that manages all hospital operations including patients, doctors, and appointments.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus


class Hospital:
    def __init__(self, name: str, address: str = "", phone: str = "", email: str = ""):
        """
        Initialize a new hospital
        
        Args:
            name: Hospital name
            address: Hospital address
            phone: Contact phone number
            email: Contact email
        """
        self.hospital_id = "HMS001"  # Simple ID for demo
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.established_date = datetime.now()
        
        # Data storage
        self.patients: Dict[str, Patient] = {}
        self.doctors: Dict[str, Doctor] = {}
        self.appointments: Dict[str, Appointment] = {}
        self.departments: List[str] = [
            "Cardiology", "Neurology", "Orthopedics", "Pediatrics", 
            "General Medicine", "Surgery", "Emergency", "Radiology"
        ]
        
    def add_patient(self, name: str, age: int, gender: str, phone: str, 
                    address: str = "", emergency_contact: str = "", 
                    blood_group: str = "", medical_history: str = "") -> Tuple[str, str]:
        """
        Add a new patient to the hospital
        
        Returns:
            Tuple of (patient_id, message)
        """
        try:
            patient = Patient(name, age, gender, phone, address, emergency_contact, blood_group, medical_history)
            self.patients[patient.patient_id] = patient
            return patient.patient_id, f"Patient {name} added successfully with ID: {patient.patient_id}"
        except Exception as e:
            return "", f"Error adding patient: {str(e)}"
    
    def add_doctor(self, name: str, specialization: str, phone: str, 
                   email: str = "", experience_years: int = 0, 
                   qualification: str = "", department: str = "") -> Tuple[str, str]:
        """
        Add a new doctor to the hospital
        
        Returns:
            Tuple of (doctor_id, message)
        """
        try:
            doctor = Doctor(name, specialization, phone, email, experience_years, qualification, department)
            self.doctors[doctor.doctor_id] = doctor
            return doctor.doctor_id, f"Doctor {name} added successfully with ID: {doctor.doctor_id}"
        except Exception as e:
            return "", f"Error adding doctor: {str(e)}"
    
    def create_appointment(self, patient_id: str, doctor_id: str, date: str, 
                          time_slot: str, appointment_type: str = "Regular", 
                          notes: str = "") -> Tuple[str, str]:
        """
        Create a new appointment
        
        Returns:
            Tuple of (appointment_id, message)
        """
        # Validate patient and doctor exist
        if patient_id not in self.patients:
            return "", "Patient not found"
        if doctor_id not in self.doctors:
            return "", "Doctor not found"
        
        # Check if patient is active
        if not self.patients[patient_id].is_active:
            return "", "Patient account is deactivated"
        
        # Check if doctor is active
        if not self.doctors[doctor_id].is_active:
            return "", "Doctor account is deactivated"
        
        try:
            appointment = Appointment(patient_id, doctor_id, date, time_slot, appointment_type, notes)
            self.appointments[appointment.appointment_id] = appointment
            
            # Add appointment to patient and doctor records
            self.patients[patient_id].add_appointment(appointment.appointment_id)
            
            return appointment.appointment_id, f"Appointment created successfully with ID: {appointment.appointment_id}"
        except Exception as e:
            return "", f"Error creating appointment: {str(e)}"
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        """Get patient by ID"""
        return self.patients.get(patient_id)
    
    def get_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        """Get doctor by ID"""
        return self.doctors.get(doctor_id)
    
    def get_appointment_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Get appointment by ID"""
        return self.appointments.get(appointment_id)
    
    def search_patients(self, query: str) -> List[Patient]:
        """Search patients by name or ID"""
        query = query.lower()
        results = []
        
        for patient in self.patients.values():
            if (query in patient.name.lower() or 
                query in patient.patient_id.lower() or
                query in patient.phone):
                results.append(patient)
        
        return results
    
    def search_doctors(self, query: str) -> List[Doctor]:
        """Search doctors by name, specialization, or ID"""
        query = query.lower()
        results = []
        
        for doctor in self.doctors.values():
            if (query in doctor.name.lower() or 
                query in doctor.specialization.lower() or
                query in doctor.doctor_id.lower() or
                query in doctor.department.lower()):
                results.append(doctor)
        
        return results
    
    def get_appointments_by_date(self, date: str) -> List[Appointment]:
        """Get all appointments for a specific date"""
        return [apt for apt in self.appointments.values() if apt.date == date]
    
    def get_appointments_by_doctor(self, doctor_id: str) -> List[Appointment]:
        """Get all appointments for a specific doctor"""
        return [apt for apt in self.appointments.values() if apt.doctor_id == doctor_id]
    
    def get_appointments_by_patient(self, patient_id: str) -> List[Appointment]:
        """Get all appointments for a specific patient"""
        return [apt for apt in self.appointments.values() if apt.patient_id == patient_id]
    
    def get_appointments_by_status(self, status: AppointmentStatus) -> List[Appointment]:
        """Get all appointments with a specific status"""
        return [apt for apt in self.appointments.values() if apt.status == status]
    
    def update_appointment_status(self, appointment_id: str, new_status: AppointmentStatus, notes: str = "") -> str:
        """Update appointment status"""
        if appointment_id not in self.appointments:
            return "Appointment not found"
        
        return self.appointments[appointment_id].update_status(new_status, notes)
    
    def cancel_appointment(self, appointment_id: str, reason: str = "") -> str:
        """Cancel an appointment"""
        if appointment_id not in self.appointments:
            return "Appointment not found"
        
        return self.appointments[appointment_id].cancel_appointment(reason)
    
    def get_hospital_statistics(self) -> Dict:
        """Get comprehensive hospital statistics"""
        total_patients = len(self.patients)
        active_patients = len([p for p in self.patients.values() if p.is_active])
        
        total_doctors = len(self.doctors)
        active_doctors = len([d for d in self.doctors.values() if d.is_active])
        
        total_appointments = len(self.appointments)
        today_appointments = len([apt for apt in self.appointments.values() 
                                if apt.date == datetime.now().strftime("%Y-%m-%d")])
        
        # Count appointments by status
        status_counts = {}
        for apt in self.appointments.values():
            status = apt.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Department statistics
        dept_stats = {}
        for dept in self.departments:
            dept_doctors = [d for d in self.doctors.values() if d.department == dept]
            dept_stats[dept] = {
                'doctors': len(dept_doctors),
                'active_doctors': len([d for d in dept_doctors if d.is_active])
            }
        
        return {
            'total_patients': total_patients,
            'active_patients': active_patients,
            'total_doctors': total_doctors,
            'active_doctors': active_doctors,
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'appointment_statuses': status_counts,
            'departments': dept_stats,
            'hospital_info': {
                'name': self.name,
                'address': self.address,
                'phone': self.phone,
                'email': self.email,
                'established': self.established_date.strftime("%Y-%m-%d")
            }
        }
    
    def get_urgent_appointments(self) -> List[Appointment]:
        """Get all urgent appointments"""
        return [apt for apt in self.appointments.values() if apt.is_urgent()]
    
    def get_follow_up_appointments(self) -> List[Appointment]:
        """Get all follow-up appointments"""
        return [apt for apt in self.appointments.values() if apt.is_follow_up()]
    
    def remove_patient(self, patient_id: str) -> str:
        """Remove a patient from the hospital"""
        if patient_id not in self.patients:
            return "Patient not found"
        
        # Check if patient has active appointments
        active_appointments = [apt for apt in self.appointments.values() 
                             if apt.patient_id == patient_id and 
                             apt.status not in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]]
        
        if active_appointments:
            return f"Cannot remove patient with {len(active_appointments)} active appointments"
        
        patient_name = self.patients[patient_id].name
        del self.patients[patient_id]
        return f"Patient {patient_name} removed successfully"
    
    def remove_doctor(self, doctor_id: str) -> str:
        """Remove a doctor from the hospital"""
        if doctor_id not in self.doctors:
            return "Doctor not found"
        
        # Check if doctor has active appointments
        active_appointments = [apt for apt in self.appointments.values() 
                             if apt.doctor_id == doctor_id and 
                             apt.status not in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]]
        
        if active_appointments:
            return f"Cannot remove doctor with {len(active_appointments)} active appointments"
        
        doctor_name = self.doctors[doctor_id].name
        del self.doctors[doctor_id]
        return f"Doctor {doctor_name} removed successfully"
    
    def __str__(self) -> str:
        """String representation of hospital"""
        return f"Hospital: {self.name} - {len(self.patients)} patients, {len(self.doctors)} doctors"
    
    def __repr__(self) -> str:
        """Detailed representation of hospital"""
        return f"Hospital(name='{self.name}', address='{self.address}', phone='{self.phone}')"
