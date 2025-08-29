"""
Hospital Class for Hospital Management System
Main class that manages all hospital operations including patients, doctors, and appointments.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus
import json
import os


class Hospital:
    def __init__(self, name: str = "General Hospital", address: str = "", phone: str = "", email: str = ""):
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
    
    def add_patient(self, name: str, age: int, gender: str, contact: str) -> str:
        """
        Add a new patient to the hospital (simplified for GUI)
        
        Returns:
            patient_id
        """
        try:
            patient = Patient(name, age, gender, contact)
            self.patients[patient.patient_id] = patient
            return patient.patient_id
        except Exception as e:
            raise Exception(f"Error adding patient: {str(e)}")
    
    def add_doctor(self, name: str, specialization: str, contact: str, department: str) -> str:
        """
        Add a new doctor to the hospital (simplified for GUI)
        
        Returns:
            doctor_id
        """
        try:
            doctor = Doctor(name, specialization, contact, department)
            self.doctors[doctor.doctor_id] = doctor
            return doctor.doctor_id
        except Exception as e:
            raise Exception(f"Error adding doctor: {str(e)}")
    
    def book_appointment(self, patient_id: str, doctor_id: str, date: str, time: str) -> str:
        """
        Book a new appointment (simplified for GUI)
        
        Returns:
            appointment_id
        """
        # Validate patient and doctor exist
        if patient_id not in self.patients:
            raise Exception("Patient not found")
        if doctor_id not in self.doctors:
            raise Exception("Doctor not found")
        
        try:
            appointment = Appointment(patient_id, doctor_id, date, time)
            self.appointments[appointment.appointment_id] = appointment
            return appointment.appointment_id
        except Exception as e:
            raise Exception(f"Error booking appointment: {str(e)}")
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get patient by ID (alias for get_patient_by_id)"""
        return self.patients.get(patient_id)
    
    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Get doctor by ID (alias for get_doctor_by_id)"""
        return self.doctors.get(doctor_id)
    
    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return list(self.patients.values())
    
    def get_all_doctors(self) -> List[Doctor]:
        """Get all doctors"""
        return list(self.doctors.values())
    
    def get_all_appointments(self) -> List[Appointment]:
        """Get all appointments"""
        return list(self.appointments.values())
    
    def get_department_statistics(self) -> Dict[str, int]:
        """Get doctor count by department"""
        dept_stats = {}
        for doctor in self.doctors.values():
            dept = doctor.department
            dept_stats[dept] = dept_stats.get(dept, 0) + 1
        return dept_stats
    
    def load_data(self):
        """Load data from JSON files"""
        try:
            # Load patients
            if os.path.exists('patients.json'):
                with open('patients.json', 'r') as f:
                    patients_data = json.load(f)
                    for patient_id, data in patients_data.items():
                        patient = Patient(data['name'], data['age'], data['gender'], data['contact'])
                        patient.patient_id = patient_id
                        self.patients[patient_id] = patient
            
            # Load doctors
            if os.path.exists('doctors.json'):
                with open('doctors.json', 'r') as f:
                    doctors_data = json.load(f)
                    for doctor_id, data in doctors_data.items():
                        doctor = Doctor(data['name'], data['specialization'], data['contact'], data['department'])
                        doctor.doctor_id = doctor_id
                        self.doctors[doctor_id] = doctor
            
            # Load appointments
            if os.path.exists('appointments.json'):
                with open('appointments.json', 'r') as f:
                    appointments_data = json.load(f)
                    for appointment_id, data in appointments_data.items():
                        appointment = Appointment(data['patient_id'], data['doctor_id'], data['date'], data['time'])
                        appointment.appointment_id = appointment_id
                        appointment.status = AppointmentStatus[data['status']]
                        self.appointments[appointment_id] = appointment
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to JSON files"""
        try:
            # Save patients
            patients_data = {}
            for patient_id, patient in self.patients.items():
                patients_data[patient_id] = {
                    'name': patient.name,
                    'age': patient.age,
                    'gender': patient.gender,
                    'contact': patient.contact
                }
            with open('patients.json', 'w') as f:
                json.dump(patients_data, f, indent=2)
            
            # Save doctors
            doctors_data = {}
            for doctor_id, doctor in self.doctors.items():
                doctors_data[doctor_id] = {
                    'name': doctor.name,
                    'specialization': doctor.specialization,
                    'contact': doctor.contact,
                    'department': doctor.department
                }
            with open('doctors.json', 'w') as f:
                json.dump(doctors_data, f, indent=2)
            
            # Save appointments
            appointments_data = {}
            for appointment_id, appointment in self.appointments.items():
                appointments_data[appointment_id] = {
                    'patient_id': appointment.patient_id,
                    'doctor_id': appointment.doctor_id,
                    'date': appointment.date,
                    'time': appointment.time,
                    'status': appointment.status.name
                }
            with open('appointments.json', 'w') as f:
                json.dump(appointments_data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def remove_patient(self, patient_id: str) -> str:
        """Remove a patient from the hospital"""
        if patient_id not in self.patients:
            return "Patient not found"
        
        # Check if patient has active appointments
        for appointment in self.appointments.values():
            if appointment.patient_id == patient_id and appointment.status != AppointmentStatus.COMPLETED:
                return "Cannot remove patient with active appointments"
        
        patient_name = self.patients[patient_id].name
        del self.patients[patient_id]
        return f"Patient {patient_name} removed successfully"
    
    def remove_doctor(self, doctor_id: str) -> str:
        """Remove a doctor from the hospital"""
        if doctor_id not in self.doctors:
            return "Doctor not found"
        
        # Check if doctor has active appointments
        for appointment in self.appointments.values():
            if appointment.doctor_id == doctor_id and appointment.status != AppointmentStatus.COMPLETED:
                return "Cannot remove doctor with active appointments"
        
        doctor_name = self.doctors[doctor_id].name
        del self.doctors[doctor_id]
        return f"Doctor {doctor_name} removed successfully"
    
    def remove_appointment(self, appointment_id: str) -> str:
        """Remove an appointment"""
        if appointment_id not in self.appointments:
            return "Appointment not found"
        
        del self.appointments[appointment_id]
        return "Appointment removed successfully"
    
    def update_appointment_status(self, appointment_id: str, new_status: AppointmentStatus) -> str:
        """Update appointment status"""
        if appointment_id not in self.appointments:
            return "Appointment not found"
        
        self.appointments[appointment_id].status = new_status
        return f"Appointment status updated to {new_status.value}"
    
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
        active_appointments = 0
        completed_appointments = 0
        
        for apt in self.appointments.values():
            status = apt.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count active appointments (not completed or cancelled)
            if apt.status not in [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]:
                active_appointments += 1
            
            # Count completed appointments
            if apt.status == AppointmentStatus.COMPLETED:
                completed_appointments += 1
        
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
            'active_appointments': active_appointments,
            'completed_appointments': completed_appointments,
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
    
    def __str__(self) -> str:
        """String representation of hospital"""
        return f"Hospital: {self.name} - {len(self.patients)} patients, {len(self.doctors)} doctors"
    
    def __repr__(self) -> str:
        """Detailed representation of hospital"""
        return f"Hospital(name='{self.name}', address='{self.address}', phone='{self.phone}')"
