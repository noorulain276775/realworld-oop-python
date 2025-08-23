#!/usr/bin/env python3
"""
Hospital Management System - Demo Script
This script demonstrates the core functionality of the HMS classes without the GUI.
Run this to test the backend logic and see how the classes work together.
"""

from hospital import Hospital
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus
from datetime import datetime


def print_separator():
    print("=" * 80)


def demo_patient_management():
    """Demonstrate patient management functionality"""
    print("\n👥 PATIENT MANAGEMENT DEMO")
    print_separator()
    
    hospital = Hospital("Demo Hospital")
    
    # Add patients
    print("Adding patients...")
    patient1_id, msg1 = hospital.add_patient("Alice Johnson", 35, "Female", "555-0101", 
                                            "123 Oak St", "555-0102", "O+", "Hypertension")
    print(f"✅ {msg1}")
    
    patient2_id, msg2 = hospital.add_patient("Bob Smith", 42, "Male", "555-0103", 
                                            "456 Pine Ave", "555-0104", "A-", "Diabetes")
    print(f"✅ {msg2}")
    
    patient3_id, msg3 = hospital.add_patient("Carol Davis", 28, "Female", "555-0105", 
                                            "789 Elm Rd", "555-0106", "B+", "")
    print(f"✅ {msg3}")
    
    # Search patients
    print("\n🔍 Searching patients...")
    results = hospital.search_patients("Alice")
    print(f"Found {len(results)} patients matching 'Alice':")
    for patient in results:
        print(f"   • {patient}")
    
    # Get patient details
    print(f"\n📋 Patient {patient1_id} details:")
    patient = hospital.get_patient_by_id(patient1_id)
    if patient:
        print(patient.get_patient_summary())
    
    return hospital, [patient1_id, patient2_id, patient3_id]


def demo_doctor_management():
    """Demonstrate doctor management functionality"""
    print("\n👨‍⚕️ DOCTOR MANAGEMENT DEMO")
    print_separator()
    
    hospital = Hospital("Demo Hospital")
    
    # Add doctors
    print("Adding doctors...")
    doctor1_id, msg1 = hospital.add_doctor("Dr. Emily Wilson", "Cardiology", "555-0201", 
                                          "ewilson@hospital.com", 15, "MD, FACC", "Cardiology")
    print(f"✅ {msg1}")
    
    doctor2_id, msg2 = hospital.add_doctor("Dr. Robert Chen", "Neurology", "555-0202", 
                                          "rchen@hospital.com", 12, "MD, PhD", "Neurology")
    print(f"✅ {msg2}")
    
    doctor3_id, msg3 = hospital.add_doctor("Dr. Lisa Rodriguez", "Pediatrics", "555-0203", 
                                          "lrodriguez@hospital.com", 8, "MD", "Pediatrics")
    print(f"✅ {msg3}")
    
    # Search doctors
    print("\n🔍 Searching doctors...")
    results = hospital.search_doctors("Cardiology")
    print(f"Found {len(results)} doctors in Cardiology:")
    for doctor in results:
        print(f"   • {doctor}")
    
    # Get doctor details
    print(f"\n📋 Doctor {doctor1_id} details:")
    doctor = hospital.get_doctor_by_id(doctor1_id)
    if doctor:
        print(doctor.get_doctor_summary())
    
    return hospital, [doctor1_id, doctor2_id, doctor3_id]


def demo_appointment_system():
    """Demonstrate appointment management functionality"""
    print("\n📅 APPOINTMENT SYSTEM DEMO")
    print_separator()
    
    hospital = Hospital("Demo Hospital")
    
    # Add sample data
    patient_id, _ = hospital.add_patient("Test Patient", 30, "Male", "555-0001")
    doctor_id, _ = hospital.add_doctor("Dr. Test", "General Medicine", "555-0002")
    
    # Create appointments
    print("Creating appointments...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    apt1_id, msg1 = hospital.create_appointment(patient_id, doctor_id, today, "09:00-10:00", 
                                               "Regular", "Annual checkup")
    print(f"✅ {msg1}")
    
    apt2_id, msg2 = hospital.create_appointment(patient_id, doctor_id, today, "14:00-15:00", 
                                               "Follow-up", "Post-surgery review")
    print(f"✅ {msg2}")
    
    # Get appointment details
    print(f"\n📋 Appointment {apt1_id} details:")
    appointment = hospital.get_appointment_by_id(apt1_id)
    if appointment:
        print(appointment.get_appointment_summary())
    
    # Update appointment status
    print(f"\n🔄 Updating appointment status...")
    result = hospital.update_appointment_status(apt1_id, AppointmentStatus.CONFIRMED, "Patient confirmed")
    print(f"✅ {result}")
    
    # Get appointments by date
    print(f"\n📅 Appointments for {today}:")
    appointments = hospital.get_appointments_by_date(today)
    for apt in appointments:
        print(f"   • {apt}")
    
    return hospital


def demo_hospital_statistics():
    """Demonstrate hospital statistics and reporting"""
    print("\n📊 HOSPITAL STATISTICS DEMO")
    print_separator()
    
    hospital = Hospital("Demo Hospital")
    
    # Add sample data
    hospital.add_patient("Patient 1", 25, "Female", "555-0001")
    hospital.add_patient("Patient 2", 35, "Male", "555-0002")
    hospital.add_patient("Patient 3", 45, "Female", "555-0003")
    
    hospital.add_doctor("Dr. A", "Cardiology", "555-0001", department="Cardiology")
    hospital.add_doctor("Dr. B", "Neurology", "555-0002", department="Neurology")
    
    # Create some appointments
    today = datetime.now().strftime("%Y-%m-%d")
    hospital.create_appointment("1", "1", today, "09:00-10:00")
    hospital.create_appointment("2", "2", today, "10:00-11:00")
    
    # Get statistics
    stats = hospital.get_hospital_statistics()
    
    print("🏥 Hospital Overview:")
    print(f"   Name: {stats['hospital_info']['name']}")
    print(f"   Address: {stats['hospital_info']['address']}")
    print(f"   Phone: {stats['hospital_info']['phone']}")
    
    print(f"\n📊 Current Statistics:")
    print(f"   Total Patients: {stats['total_patients']}")
    print(f"   Active Patients: {stats['active_patients']}")
    print(f"   Total Doctors: {stats['total_doctors']}")
    print(f"   Active Doctors: {stats['active_doctors']}")
    print(f"   Total Appointments: {stats['total_appointments']}")
    print(f"   Today's Appointments: {stats['today_appointments']}")
    
    print(f"\n🏥 Department Overview:")
    for dept, dept_stats in stats['departments'].items():
        print(f"   {dept}: {dept_stats['doctors']} doctors ({dept_stats['active_doctors']} active)")
    
    print(f"\n📅 Appointment Status Breakdown:")
    for status, count in stats['appointment_statuses'].items():
        print(f"   {status}: {count}")


def demo_error_handling():
    """Demonstrate error handling and validation"""
    print("\n⚠️ ERROR HANDLING DEMO")
    print_separator()
    
    hospital = Hospital("Demo Hospital")
    
    # Test invalid patient data
    print("Testing invalid patient data...")
    try:
        patient_id, msg = hospital.add_patient("", 0, "Invalid", "")
        print(f"Result: {msg}")
    except Exception as e:
        print(f"Error caught: {e}")
    
    # Test appointment with non-existent patient/doctor
    print("\nTesting appointment with non-existent patient/doctor...")
    apt_id, msg = hospital.create_appointment("invalid_patient", "invalid_doctor", "2024-01-01", "09:00-10:00")
    print(f"Result: {msg}")
    
    # Test removing patient with active appointments
    print("\nTesting patient removal with active appointments...")
    patient_id, _ = hospital.add_patient("Test Patient", 30, "Male", "555-0001")
    doctor_id, _ = hospital.add_doctor("Dr. Test", "General Medicine", "555-0001")
    hospital.create_appointment(patient_id, doctor_id, "2024-01-01", "09:00-10:00")
    
    result = hospital.remove_patient(patient_id)
    print(f"Result: {result}")


def main():
    """Main demo function"""
    print("🏥 WELCOME TO THE HOSPITAL MANAGEMENT SYSTEM DEMO!")
    print("This demo showcases the core functionality of our OOP-based hospital system.")
    print_separator()
    
    # Run all demo sections
    demo_patient_management()
    demo_doctor_management()
    demo_appointment_system()
    demo_hospital_statistics()
    demo_error_handling()
    
    print("\n🎉 Demo completed! Thanks for exploring the Hospital Management System.")
    print("This project demonstrates:")
    print("   • Advanced Object-Oriented Programming principles")
    print("   • Professional software architecture")
    print("   • Real-world business logic implementation")
    print("   • Comprehensive error handling and validation")
    print("   • Modern Python features and best practices")
    print("\n🚀 To run the full GUI application, use: python main_gui.py")


if __name__ == "__main__":
    main()

