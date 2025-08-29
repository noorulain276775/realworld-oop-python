#!/usr/bin/env python3
"""
Hospital Management System Demo
Demonstrates the core functionality of the hospital management system
"""

from hospital import Hospital
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus
import json

def main():
    """Main demonstration function"""
    
    # Initialize hospital
    hospital = Hospital()
    
    print("Hospital Management System Demo")
    print("=" * 50)
    
    # PATIENT MANAGEMENT DEMO
    print("\nPATIENT MANAGEMENT DEMO")
    print("-" * 30)
    
    # Add patients
    patient1_id = hospital.add_patient("John Doe", 35, "Male", "555-0101")
    msg1 = f"Patient added with ID: {patient1_id}"
    print(f" {msg1}")
    
    patient2_id = hospital.add_patient("Jane Smith", 28, "Female", "555-0102")
    msg2 = f"Patient added with ID: {patient2_id}"
    print(f" {msg2}")
    
    patient3_id = hospital.add_patient("Bob Johnson", 45, "Male", "555-0103")
    msg3 = f"Patient added with ID: {patient3_id}"
    print(f" {msg3}")
    
    # View patient details
    print(f"\nPatient {patient1_id} details:")
    patient1 = hospital.get_patient(patient1_id)
    if patient1:
        print(f"  Name: {patient1.name}")
        print(f"  Age: {patient1.age}")
        print(f"  Gender: {patient1.gender}")
        print(f"  Contact: {patient1.contact}")
    
    # DOCTOR MANAGEMENT DEMO
    print("\nDOCTOR MANAGEMENT DEMO")
    print("-" * 30)
    
    # Add doctors
    doctor1_id = hospital.add_doctor("Dr. Sarah Wilson", "Cardiology", "555-0201", "Cardiology")
    msg1 = f"Doctor added with ID: {doctor1_id}"
    print(f" {msg1}")
    
    doctor2_id = hospital.add_doctor("Dr. Mike Brown", "Neurology", "555-0202", "Neurology")
    msg2 = f"Doctor added with ID: {doctor2_id}"
    print(f" {msg2}")
    
    doctor3_id = hospital.add_doctor("Dr. Lisa Davis", "Pediatrics", "555-0203", "Pediatrics")
    msg3 = f"Doctor added with ID: {doctor3_id}"
    print(f" {msg3}")
    
    # View doctor details
    print(f"\nDoctor {doctor1_id} details:")
    doctor1 = hospital.get_doctor(doctor1_id)
    if doctor1:
        print(f"  Name: {doctor1.name}")
        print(f"  Specialization: {doctor1.specialization}")
        print(f"  Contact: {doctor1.contact}")
        print(f"  Department: {doctor1.department}")
    
    # APPOINTMENT MANAGEMENT DEMO
    print("\nAPPOINTMENT MANAGEMENT DEMO")
    print("-" * 30)
    
    # Book appointments
    apt1_id = hospital.book_appointment(patient1_id, doctor1_id, "2024-01-15", "10:00")
    msg1 = f"Appointment booked with ID: {apt1_id}"
    print(f" {msg1}")
    
    apt2_id = hospital.book_appointment(patient2_id, doctor2_id, "2024-01-16", "14:00")
    msg2 = f"Appointment booked with ID: {apt2_id}"
    print(f" {msg2}")
    
    # View appointment details
    print(f"\nAppointment {apt1_id} details:")
    apt1 = hospital.get_appointment(apt1_id)
    if apt1:
        print(f"  Patient: {apt1.patient_id}")
        print(f"  Doctor: {apt1.doctor_id}")
        print(f"  Date: {apt1.date}")
        print(f"  Time: {apt1.time}")
        print(f"  Status: {apt1.status}")
    
    # Update appointment status
    print(f"\nUpdating appointment status...")
    result = hospital.update_appointment_status(apt1_id, AppointmentStatus.COMPLETED)
    print(f" {result}")
    
    # HOSPITAL OVERVIEW DEMO
    print("\nHOSPITAL OVERVIEW DEMO")
    print("-" * 30)
    
    # Get hospital statistics
    stats = hospital.get_hospital_statistics()
    print("Hospital Overview:")
    print(f"  Total Patients: {stats['total_patients']}")
    print(f"  Total Doctors: {stats['total_doctors']}")
    print(f"  Total Appointments: {stats['total_appointments']}")
    print(f"  Active Appointments: {stats['active_appointments']}")
    print(f"  Completed Appointments: {stats['completed_appointments']}")
    
    # Get department overview
    dept_stats = hospital.get_department_statistics()
    print(f"\nDepartment Overview:")
    for dept, count in dept_stats.items():
        print(f"  {dept}: {count} doctors")
    
    # ERROR HANDLING DEMO
    print("\nERROR HANDLING DEMO")
    print("-" * 30)
    
    # Try to get non-existent patient
    try:
        non_existent = hospital.get_patient("INVALID_ID")
        if non_existent is None:
            print("  Successfully handled non-existent patient (returned None)")
    except Exception as e:
        print(f"  Error handled: {e}")
    
    # Try to book appointment with invalid IDs
    try:
        invalid_apt = hospital.book_appointment("INVALID_PATIENT", "INVALID_DOCTOR", "2024-01-20", "15:00")
        print(f"  Invalid appointment booking handled gracefully")
    except Exception as e:
        print(f"  Error handled: {e}")
    
    # Try to update non-existent appointment
    try:
        result = hospital.update_appointment_status("INVALID_APT", AppointmentStatus.COMPLETED)
        print(f"  Invalid appointment update handled gracefully")
    except Exception as e:
        print(f"  Error handled: {e}")
    
    # DATA PERSISTENCE DEMO
    print("\nDATA PERSISTENCE DEMO")
    print("-" * 30)
    
    # Save data to file
    try:
        hospital.save_data()
        print("  Data saved successfully to JSON files")
    except Exception as e:
        print(f"  Error saving data: {e}")
    
    # Load data from file (simulate restart)
    try:
        new_hospital = Hospital()
        new_hospital.load_data()
        print("  Data loaded successfully from JSON files")
        
        # Verify data persistence
        new_stats = new_hospital.get_hospital_statistics()
        print(f"  Verified: {new_stats['total_patients']} patients loaded")
        print(f"  Verified: {new_stats['total_doctors']} doctors loaded")
        print(f"  Verified: {new_stats['total_appointments']} appointments loaded")
        
    except Exception as e:
        print(f"  Error loading data: {e}")
    
    print("\n" + "=" * 50)
    print("WELCOME TO THE HOSPITAL MANAGEMENT SYSTEM DEMO!")
    print("=" * 50)
    
    print("\nThis demo showcases:")
    print("  - Patient management (add, view, update)")
    print("  - Doctor management (add, view, update)")
    print("  - Appointment scheduling and status updates")
    print("  - Hospital statistics and department overview")
    print("  - Error handling and validation")
    print("  - Data persistence with JSON files")
    
    print("\nTo run the full GUI application, use: python main_gui.py")
    print("To run this demo again, use: python demo.py")

if __name__ == "__main__":
    main()

