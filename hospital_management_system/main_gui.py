#!/usr/bin/env python3
"""
Hospital Management System - Main GUI Application
A comprehensive desktop application built with Tkinter for managing hospital operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import filedialog
import json
from datetime import datetime, date
from typing import Dict, List

# Import our hospital management classes
from hospital import Hospital
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus


class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize hospital
        self.hospital = Hospital("City General Hospital", "123 Medical Center Dr", "555-0123", "info@cityhospital.com")
        
        # Add some sample data
        self.add_sample_data()
        
        # Create main interface
        self.create_widgets()
        
    def add_sample_data(self):
        """Add sample data for demonstration"""
        # Add sample patients
        self.hospital.add_patient("John Smith", 45, "Male", "555-0101", "123 Oak St", "555-0102", "O+", "Hypertension")
        self.hospital.add_patient("Sarah Johnson", 32, "Female", "555-0103", "456 Pine Ave", "555-0104", "A-", "Diabetes")
        self.hospital.add_patient("Mike Davis", 28, "Male", "555-0105", "789 Elm Rd", "555-0106", "B+", "")
        
        # Add sample doctors
        self.hospital.add_doctor("Dr. Emily Wilson", "Cardiology", "555-0201", "ewilson@hospital.com", 15, "MD, FACC", "Cardiology")
        self.hospital.add_doctor("Dr. Robert Chen", "Neurology", "555-0202", "rchen@hospital.com", 12, "MD, PhD", "Neurology")
        self.hospital.add_doctor("Dr. Lisa Rodriguez", "Pediatrics", "555-0203", "lrodriguez@hospital.com", 8, "MD", "Pediatrics")
        
        # Add sample appointments
        today = datetime.now().strftime("%Y-%m-%d")
        self.hospital.create_appointment("1", "1", today, "09:00-10:00", "Regular", "Annual checkup")
        self.hospital.create_appointment("2", "2", today, "14:00-15:00", "Follow-up", "Post-surgery review")
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        self.create_reports_tab()
        
    def create_dashboard_tab(self):
        """Create the dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Title
        title_label = tk.Label(dashboard_frame, text="Hospital Management Dashboard", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Hospital Statistics", padding=20)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Get statistics
        stats = self.hospital.get_hospital_statistics()
        
        # Create statistics display
        stats_text = f"""
Hospital: {stats['hospital_info']['name']}
Address: {stats['hospital_info']['address']}
Phone: {stats['hospital_info']['phone']}
Established: {stats['hospital_info']['established']}

📊 Current Statistics:
• Total Patients: {stats['total_patients']}
• Active Patients: {stats['active_patients']}
• Total Doctors: {stats['total_doctors']}
• Active Doctors: {stats['active_doctors']}
• Total Appointments: {stats['total_appointments']}
• Today's Appointments: {stats['today_appointments']}

🏥 Department Overview:
"""
        
        for dept, dept_stats in stats['departments'].items():
            stats_text += f"• {dept}: {dept_stats['doctors']} doctors ({dept_stats['active_doctors']} active)\n"
        
        # Display statistics
        stats_display = scrolledtext.ScrolledText(stats_frame, height=15, width=80, font=('Courier', 10))
        stats_display.pack(fill='both', expand=True)
        stats_display.insert('1.0', stats_text)
        stats_display.config(state='disabled')
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(dashboard_frame, text="Quick Actions", padding=20)
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        # Quick action buttons
        ttk.Button(actions_frame, text="Add New Patient", command=self.show_add_patient_dialog).pack(side='left', padx=10)
        ttk.Button(actions_frame, text="Add New Doctor", command=self.show_add_doctor_dialog).pack(side='left', padx=10)
        ttk.Button(actions_frame, text="Book Appointment", command=self.show_book_appointment_dialog).pack(side='left', padx=10)
        ttk.Button(actions_frame, text="View Today's Schedule", command=self.show_today_schedule).pack(side='left', padx=10)
        
    def create_patients_tab(self):
        """Create the patients management tab"""
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="👥 Patients")
        
        # Title and search
        title_frame = tk.Frame(patients_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="Patient Management", font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(side='left')
        
        # Search frame
        search_frame = ttk.Frame(title_frame)
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.patient_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.patient_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_patients).pack(side='left', padx=5)
        
        # Patients list
        list_frame = ttk.Frame(patients_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create Treeview for patients
        columns = ('ID', 'Name', 'Age', 'Gender', 'Phone', 'Status')
        self.patients_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.patients_tree.bind('<Double-1>', self.show_patient_details)
        
        # Buttons frame
        buttons_frame = ttk.Frame(patients_frame)
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(buttons_frame, text="Add Patient", command=self.show_add_patient_dialog).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Edit Patient", command=self.edit_selected_patient).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Remove Patient", command=self.remove_selected_patient).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_patients_list).pack(side='left', padx=5)
        
        # Load patients
        self.refresh_patients_list()
        
    def create_doctors_tab(self):
        """Create the doctors management tab"""
        doctors_frame = ttk.Frame(self.notebook)
        self.notebook.add(doctors_frame, text="👨‍⚕️ Doctors")
        
        # Title and search
        title_frame = tk.Frame(doctors_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="Doctor Management", font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(side='left')
        
        # Search frame
        search_frame = ttk.Frame(title_frame)
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.doctor_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.doctor_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_doctors).pack(side='left', padx=5)
        
        # Doctors list
        list_frame = ttk.Frame(doctors_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create Treeview for doctors
        columns = ('ID', 'Name', 'Specialization', 'Department', 'Experience', 'Status')
        self.doctors_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doctors_tree.yview)
        self.doctors_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doctors_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.doctors_tree.bind('<Double-1>', self.show_doctor_details)
        
        # Buttons frame
        buttons_frame = ttk.Frame(doctors_frame)
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(buttons_frame, text="Add Doctor", command=self.show_add_doctor_dialog).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Edit Doctor", command=self.edit_selected_doctor).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Remove Doctor", command=self.remove_selected_doctor).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Manage Schedule", command=self.manage_doctor_schedule).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_doctors_list).pack(side='left', padx=5)
        
        # Load doctors
        self.refresh_doctors_list()
        
    def create_appointments_tab(self):
        """Create the appointments management tab"""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="📅 Appointments")
        
        # Title
        title_frame = tk.Frame(appointments_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="Appointment Management", font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(side='left')
        
        # Date selection
        date_frame = ttk.Frame(title_frame)
        date_frame.pack(side='right')
        
        tk.Label(date_frame, text="Date:").pack(side='left')
        self.appointment_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(date_frame, textvariable=self.appointment_date_var, width=15)
        date_entry.pack(side='left', padx=5)
        ttk.Button(date_frame, text="View", command=self.view_appointments_by_date).pack(side='left', padx=5)
        
        # Appointments list
        list_frame = ttk.Frame(appointments_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create Treeview for appointments
        columns = ('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Type', 'Status')
        self.appointments_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.appointments_tree.bind('<Double-1>', self.show_appointment_details)
        
        # Buttons frame
        buttons_frame = ttk.Frame(appointments_frame)
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(buttons_frame, text="Book Appointment", command=self.show_book_appointment_dialog).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Update Status", command=self.update_appointment_status).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Cancel Appointment", command=self.cancel_selected_appointment).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_appointments_list).pack(side='left', padx=5)
        
        # Load appointments
        self.refresh_appointments_list()
        
    def create_reports_tab(self):
        """Create the reports and analytics tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Title
        title_label = tk.Label(reports_frame, text="Hospital Reports & Analytics", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Reports buttons frame
        reports_buttons_frame = ttk.Frame(reports_frame)
        reports_buttons_frame.pack(pady=20)
        
        ttk.Button(reports_buttons_frame, text="Patient Report", command=self.generate_patient_report).pack(side='left', padx=10)
        ttk.Button(reports_buttons_frame, text="Doctor Report", command=self.generate_doctor_report).pack(side='left', padx=10)
        ttk.Button(reports_buttons_frame, text="Appointment Report", command=self.generate_appointment_report).pack(side='left', padx=10)
        ttk.Button(reports_buttons_frame, text="Department Report", command=self.generate_department_report).pack(side='left', padx=10)
        
        # Export frame
        export_frame = ttk.LabelFrame(reports_frame, text="Export Data", padding=20)
        export_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(export_frame, text="Export All Data to JSON", command=self.export_data).pack(side='left', padx=10)
        ttk.Button(export_frame, text="Import Data from JSON", command=self.import_data).pack(side='left', padx=10)
        
        # Statistics display
        stats_frame = ttk.LabelFrame(reports_frame, text="Detailed Statistics", padding=20)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=80, font=('Courier', 10))
        self.stats_text.pack(fill='both', expand=True)
        
        # Load initial statistics
        self.update_statistics_display()
        
    # Placeholder methods for the GUI functionality
    def show_add_patient_dialog(self):
        messagebox.showinfo("Info", "Add Patient dialog would open here")
        
    def show_add_doctor_dialog(self):
        messagebox.showinfo("Info", "Add Doctor dialog would open here")
        
    def show_book_appointment_dialog(self):
        messagebox.showinfo("Info", "Book Appointment dialog would open here")
        
    def show_today_schedule(self):
        messagebox.showinfo("Info", "Today's schedule would display here")
        
    def search_patients(self):
        query = self.patient_search_var.get()
        if query:
            results = self.hospital.search_patients(query)
            self.display_search_results("Patient Search Results", results)
        
    def search_doctors(self):
        query = self.doctor_search_var.get()
        if query:
            results = self.hospital.search_doctors(query)
            self.display_search_results("Doctor Search Results", results)
        
    def show_patient_details(self, event):
        selection = self.patients_tree.selection()
        if selection:
            item = self.patients_tree.item(selection[0])
            patient_id = item['values'][0]
            patient = self.hospital.get_patient_by_id(patient_id)
            if patient:
                messagebox.showinfo("Patient Details", patient.get_patient_summary())
        
    def show_doctor_details(self, event):
        selection = self.doctors_tree.selection()
        if selection:
            item = self.doctors_tree.item(selection[0])
            doctor_id = item['values'][0]
            doctor = self.hospital.get_doctor_by_id(doctor_id)
            if doctor:
                messagebox.showinfo("Doctor Details", doctor.get_doctor_summary())
        
    def show_appointment_details(self, event):
        selection = self.appointments_tree.selection()
        if selection:
            item = self.appointments_tree.item(selection[0])
            appointment_id = item['values'][0]
            appointment = self.hospital.get_appointment_by_id(appointment_id)
            if appointment:
                messagebox.showinfo("Appointment Details", appointment.get_appointment_summary())
        
    def edit_selected_patient(self):
        messagebox.showinfo("Info", "Edit patient functionality would open here")
        
    def remove_selected_patient(self):
        selection = self.patients_tree.selection()
        if selection:
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this patient?"):
                item = self.patients_tree.item(selection[0])
                patient_id = item['values'][0]
                result = self.hospital.remove_patient(patient_id)
                messagebox.showinfo("Result", result)
                self.refresh_patients_list()
        
    def edit_selected_doctor(self):
        messagebox.showinfo("Info", "Edit doctor functionality would open here")
        
    def remove_selected_doctor(self):
        selection = self.doctors_tree.selection()
        if selection:
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this doctor?"):
                item = self.doctors_tree.item(selection[0])
                doctor_id = item['values'][0]
                result = self.hospital.remove_doctor(doctor_id)
                messagebox.showinfo("Result", result)
                self.refresh_doctors_list()
        
    def manage_doctor_schedule(self):
        messagebox.showinfo("Info", "Schedule management would open here")
        
    def update_appointment_status(self):
        messagebox.showinfo("Info", "Status update dialog would open here")
        
    def cancel_selected_appointment(self):
        selection = self.appointments_tree.selection()
        if selection:
            if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
                item = self.appointments_tree.item(selection[0])
                appointment_id = item['values'][0]
                result = self.hospital.cancel_appointment(appointment_id, "Cancelled by user")
                messagebox.showinfo("Result", result)
                self.refresh_appointments_list()
        
    def view_appointments_by_date(self):
        date = self.appointment_date_var.get()
        appointments = self.hospital.get_appointments_by_date(date)
        self.display_appointments_by_date(appointments, date)
        
    def refresh_patients_list(self):
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Add patients
        for patient in self.hospital.patients.values():
            status = "Active" if patient.is_active else "Inactive"
            self.patients_tree.insert('', 'end', values=(
                patient.patient_id, patient.name, patient.age, 
                patient.gender, patient.phone, status
            ))
        
    def refresh_doctors_list(self):
        # Clear existing items
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
        
        # Add doctors
        for doctor in self.hospital.doctors.values():
            status = "Active" if doctor.is_active else "Inactive"
            self.doctors_tree.insert('', 'end', values=(
                doctor.doctor_id, doctor.name, doctor.specialization,
                doctor.department, f"{doctor.experience_years} years", status
            ))
        
    def refresh_appointments_list(self):
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Add appointments
        for appointment in self.hospital.appointments.values():
            patient = self.hospital.get_patient_by_id(appointment.patient_id)
            doctor = self.hospital.get_doctor_by_id(appointment.doctor_id)
            
            patient_name = patient.name if patient else "Unknown"
            doctor_name = doctor.name if doctor else "Unknown"
            
            self.appointments_tree.insert('', 'end', values=(
                appointment.appointment_id, patient_name, doctor_name,
                appointment.date, appointment.time_slot, 
                appointment.appointment_type, appointment.status.value
            ))
        
    def display_search_results(self, title, results):
        if not results:
            messagebox.showinfo(title, "No results found")
            return
        
        result_text = f"Found {len(results)} results:\n\n"
        for item in results:
            result_text += f"• {str(item)}\n"
        
        messagebox.showinfo(title, result_text)
        
    def display_appointments_by_date(self, appointments, date):
        if not appointments:
            messagebox.showinfo(f"Appointments for {date}", "No appointments found for this date")
            return
        
        result_text = f"Appointments for {date}:\n\n"
        for appointment in appointments:
            patient = self.hospital.get_patient_by_id(appointment.patient_id)
            doctor = self.hospital.get_doctor_by_id(appointment.doctor_id)
            
            patient_name = patient.name if patient else "Unknown"
            doctor_name = doctor.name if doctor else "Unknown"
            
            result_text += f"• {appointment.time_slot} - {patient_name} with {doctor_name} ({appointment.status.value})\n"
        
        messagebox.showinfo(f"Appointments for {date}", result_text)
        
    def generate_patient_report(self):
        stats = self.hospital.get_hospital_statistics()
        report = f"PATIENT REPORT\n{'='*50}\n\n"
        report += f"Total Patients: {stats['total_patients']}\n"
        report += f"Active Patients: {stats['active_patients']}\n\n"
        
        for patient in self.hospital.patients.values():
            report += f"ID: {patient.patient_id}\n"
            report += f"Name: {patient.name}\n"
            report += f"Age: {patient.age}\n"
            report += f"Status: {'Active' if patient.is_active else 'Inactive'}\n"
            report += f"Appointments: {len(patient.appointments)}\n"
            report += f"Prescriptions: {len(patient.prescriptions)}\n"
            report += "-" * 30 + "\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', report)
        
    def generate_doctor_report(self):
        stats = self.hospital.get_hospital_statistics()
        report = f"DOCTOR REPORT\n{'='*50}\n\n"
        report += f"Total Doctors: {stats['total_doctors']}\n"
        report += f"Active Doctors: {stats['active_doctors']}\n\n"
        
        for doctor in self.hospital.doctors.values():
            report += f"ID: {doctor.doctor_id}\n"
            report += f"Name: {doctor.name}\n"
            report += f"Specialization: {doctor.specialization}\n"
            report += f"Department: {doctor.department}\n"
            report += f"Experience: {doctor.experience_years} years\n"
            report += f"Status: {'Active' if doctor.is_active else 'Inactive'}\n"
            report += f"Patients: {len(doctor.patients)}\n"
            report += "-" * 30 + "\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', report)
        
    def generate_appointment_report(self):
        stats = self.hospital.get_hospital_statistics()
        report = f"APPOINTMENT REPORT\n{'='*50}\n\n"
        report += f"Total Appointments: {stats['total_appointments']}\n"
        report += f"Today's Appointments: {stats['today_appointments']}\n\n"
        
        report += "Appointments by Status:\n"
        for status, count in stats['appointment_statuses'].items():
            report += f"• {status}: {count}\n"
        
        report += "\nRecent Appointments:\n"
        for appointment in list(self.hospital.appointments.values())[-10:]:
            patient = self.hospital.get_patient_by_id(appointment.patient_id)
            doctor = self.hospital.get_doctor_by_id(appointment.doctor_id)
            
            patient_name = patient.name if patient else "Unknown"
            doctor_name = doctor.name if doctor else "Unknown"
            
            report += f"• {appointment.date} {appointment.time_slot} - {patient_name} with {doctor_name} ({appointment.status.value})\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', report)
        
    def generate_department_report(self):
        stats = self.hospital.get_hospital_statistics()
        report = f"DEPARTMENT REPORT\n{'='*50}\n\n"
        
        for dept, dept_stats in stats['departments'].items():
            report += f"Department: {dept}\n"
            report += f"Total Doctors: {dept_stats['doctors']}\n"
            report += f"Active Doctors: {dept_stats['active_doctors']}\n"
            report += "-" * 30 + "\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', report)
        
    def update_statistics_display(self):
        stats = self.hospital.get_hospital_statistics()
        stats_text = f"HOSPITAL OVERVIEW\n{'='*50}\n\n"
        stats_text += f"Name: {stats['hospital_info']['name']}\n"
        stats_text += f"Address: {stats['hospital_info']['address']}\n"
        stats_text += f"Phone: {stats['hospital_info']['phone']}\n"
        stats_text += f"Established: {stats['hospital_info']['established']}\n\n"
        
        stats_text += f"Current Statistics:\n"
        stats_text += f"• Patients: {stats['total_patients']} (Active: {stats['active_patients']})\n"
        stats_text += f"• Doctors: {stats['total_doctors']} (Active: {stats['active_doctors']})\n"
        stats_text += f"• Appointments: {stats['total_appointments']}\n"
        stats_text += f"• Today's Appointments: {stats['today_appointments']}\n\n"
        
        stats_text += "Appointment Status Breakdown:\n"
        for status, count in stats['appointment_statuses'].items():
            stats_text += f"• {status}: {count}\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', stats_text)
        
    def export_data(self):
        """Export hospital data to JSON file"""
        data = {
            'hospital_info': {
                'name': self.hospital.name,
                'address': self.hospital.address,
                'phone': self.hospital.phone,
                'email': self.hospital.email
            },
            'patients': {},
            'doctors': {},
            'appointments': {}
        }
        
        # Export patients
        for patient_id, patient in self.hospital.patients.items():
            data['patients'][patient_id] = {
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone,
                'address': patient.address,
                'emergency_contact': patient.emergency_contact,
                'blood_group': patient.blood_group,
                'medical_history': patient.medical_history,
                'is_active': patient.is_active
            }
        
        # Export doctors
        for doctor_id, doctor in self.hospital.doctors.items():
            data['doctors'][doctor_id] = {
                'name': doctor.name,
                'specialization': doctor.specialization,
                'phone': doctor.phone,
                'email': doctor.email,
                'experience_years': doctor.experience_years,
                'qualification': doctor.qualification,
                'department': doctor.department,
                'is_active': doctor.is_active
            }
        
        # Export appointments
        for appointment_id, appointment in self.hospital.appointments.items():
            data['appointments'][appointment_id] = {
                'patient_id': appointment.patient_id,
                'doctor_id': appointment.doctor_id,
                'date': appointment.date,
                'time_slot': appointment.time_slot,
                'appointment_type': appointment.appointment_type,
                'status': appointment.status.value,
                'notes': appointment.notes,
                'cost': appointment.cost
            }
        
        # Save to file
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                messagebox.showinfo("Success", f"Data exported successfully to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
        
    def import_data(self):
        """Import hospital data from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Clear existing data
                self.hospital.patients.clear()
                self.hospital.doctors.clear()
                self.hospital.appointments.clear()
                
                # Import patients
                for patient_id, patient_data in data.get('patients', {}).items():
                    patient = Patient(
                        patient_data['name'],
                        patient_data['age'],
                        patient_data['gender'],
                        patient_data['phone'],
                        patient_data.get('address', ''),
                        patient_data.get('emergency_contact', ''),
                        patient_data.get('blood_group', ''),
                        patient_data.get('medical_history', '')
                    )
                    patient.patient_id = patient_id
                    patient.is_active = patient_data.get('is_active', True)
                    self.hospital.patients[patient_id] = patient
                
                # Import doctors
                for doctor_id, doctor_data in data.get('doctors', {}).items():
                    doctor = Doctor(
                        doctor_data['name'],
                        doctor_data['specialization'],
                        doctor_data['phone'],
                        doctor_data.get('email', ''),
                        doctor_data.get('experience_years', 0),
                        doctor_data.get('qualification', ''),
                        doctor_data.get('department', '')
                    )
                    doctor.doctor_id = doctor_id
                    doctor.is_active = doctor_data.get('is_active', True)
                    self.hospital.doctors[doctor_id] = doctor
                
                # Import appointments
                for appointment_id, appointment_data in data.get('appointments', {}).items():
                    appointment = Appointment(
                        appointment_data['patient_id'],
                        appointment_data['doctor_id'],
                        appointment_data['date'],
                        appointment_data['time_slot'],
                        appointment_data.get('appointment_type', 'Regular'),
                        appointment_data.get('notes', '')
                    )
                    appointment.appointment_id = appointment_id
                    appointment.cost = appointment_data.get('cost', 0.0)
                    
                    # Set status
                    status_value = appointment_data.get('status', 'Scheduled')
                    for status in AppointmentStatus:
                        if status.value == status_value:
                            appointment.status = status
                            break
                    
                    self.hospital.appointments[appointment_id] = appointment
                
                # Refresh all displays
                self.refresh_patients_list()
                self.refresh_doctors_list()
                self.refresh_appointments_list()
                self.update_statistics_display()
                
                messagebox.showinfo("Success", f"Data imported successfully from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {str(e)}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = HospitalManagementGUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()

