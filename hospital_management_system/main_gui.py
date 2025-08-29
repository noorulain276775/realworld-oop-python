#!/usr/bin/env python3
"""
Hospital Management System - Main GUI Application
A comprehensive hospital management system built with Python and Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from hospital import Hospital
from patient import Patient
from doctor import Doctor
from appointment import Appointment, AppointmentStatus
import json
from datetime import datetime

class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x800")
        
        # Initialize hospital
        self.hospital = Hospital()
        self.hospital.load_data()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_overview_tab()
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        
        # Refresh data
        self.refresh_all_data()
    
    def create_overview_tab(self):
        """Create the overview/dashboard tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Overview")
        
        # Title
        title_label = ttk.Label(overview_frame, text="Hospital Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(overview_frame, text="Hospital Statistics", padding=20)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Statistics labels
        self.patient_count_label = ttk.Label(stats_frame, text="Total Patients: 0")
        self.patient_count_label.pack(anchor='w', pady=5)
        
        self.doctor_count_label = ttk.Label(stats_frame, text="Total Doctors: 0")
        self.doctor_count_label.pack(anchor='w', pady=5)
        
        self.appointment_count_label = ttk.Label(stats_frame, text="Total Appointments: 0")
        self.appointment_count_label.pack(anchor='w', pady=5)
        
        self.active_appointment_label = ttk.Label(stats_frame, text="Active Appointments: 0")
        self.active_appointment_label.pack(anchor='w', pady=5)
        
        # Department overview
        dept_frame = ttk.LabelFrame(overview_frame, text="Department Overview", padding=20)
        dept_frame.pack(fill='x', padx=20, pady=10)
        
        self.dept_text = tk.Text(dept_frame, height=8, width=50)
        self.dept_text.pack(fill='both', expand=True)
        
        # Refresh button
        refresh_btn = ttk.Button(overview_frame, text="Refresh Data", command=self.refresh_overview)
        refresh_btn.pack(pady=20)
    
    def create_patients_tab(self):
        """Create the patients management tab"""
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="Patients")
        
        # Title
        title_label = ttk.Label(patients_frame, text="Patient Management", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(patients_frame, text="Add New Patient", padding=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Input fields
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.patient_name_entry = ttk.Entry(input_frame, width=30)
        self.patient_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Age:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.patient_age_entry = ttk.Entry(input_frame, width=10)
        self.patient_age_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Gender:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.patient_gender_var = tk.StringVar(value="Male")
        gender_combo = ttk.Combobox(input_frame, textvariable=self.patient_gender_var, 
                                   values=["Male", "Female"], state="readonly", width=15)
        gender_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Contact:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.patient_contact_entry = ttk.Entry(input_frame, width=20)
        self.patient_contact_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Add button
        add_btn = ttk.Button(input_frame, text="Add Patient", command=self.add_patient)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Patients list
        list_frame = ttk.LabelFrame(patients_frame, text="Patient List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for patients
        columns = ("ID", "Name", "Age", "Gender", "Contact")
        self.patient_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=100)
        
        # Scrollbar
        patient_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.patient_tree.yview)
        self.patient_tree.configure(yscrollcommand=patient_scrollbar.set)
        
        self.patient_tree.pack(side='left', fill='both', expand=True)
        patient_scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        btn_frame = ttk.Frame(patients_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_patients).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_patient).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_patient).pack(side='left', padx=5)
    
    def create_doctors_tab(self):
        """Create the doctors management tab"""
        doctors_frame = ttk.Frame(self.notebook)
        self.notebook.add(doctors_frame, text="Doctors")
        
        # Title
        title_label = ttk.Label(doctors_frame, text="Doctor Management", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(doctors_frame, text="Add New Doctor", padding=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Input fields
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.doctor_name_entry = ttk.Entry(input_frame, width=30)
        self.doctor_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Specialization:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.doctor_spec_entry = ttk.Entry(input_frame, width=20)
        self.doctor_spec_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Contact:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.doctor_contact_entry = ttk.Entry(input_frame, width=20)
        self.doctor_contact_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Department:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.doctor_dept_entry = ttk.Entry(input_frame, width=20)
        self.doctor_dept_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Add button
        add_btn = ttk.Button(input_frame, text="Add Doctor", command=self.add_doctor)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Doctors list
        list_frame = ttk.LabelFrame(doctors_frame, text="Doctor List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for doctors
        columns = ("ID", "Name", "Specialization", "Contact", "Department")
        self.doctor_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.doctor_tree.heading(col, text=col)
            self.doctor_tree.column(col, width=100)
        
        # Scrollbar
        doctor_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doctor_tree.yview)
        self.doctor_tree.configure(yscrollcommand=doctor_scrollbar.set)
        
        self.doctor_tree.pack(side='left', fill='both', expand=True)
        doctor_scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        btn_frame = ttk.Frame(doctors_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_doctors).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_doctor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_doctor).pack(side='left', padx=5)
    
    def create_appointments_tab(self):
        """Create the appointments management tab"""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="Appointments")
        
        # Title
        title_label = ttk.Label(appointments_frame, text="Appointment Management", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(appointments_frame, text="Book New Appointment", padding=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Input fields
        ttk.Label(input_frame, text="Patient ID:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.apt_patient_entry = ttk.Entry(input_frame, width=15)
        self.apt_patient_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Doctor ID:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.apt_doctor_entry = ttk.Entry(input_frame, width=15)
        self.apt_doctor_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Date:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.apt_date_entry = ttk.Entry(input_frame, width=15)
        self.apt_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.apt_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(input_frame, text="Time:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.apt_time_entry = ttk.Entry(input_frame, width=15)
        self.apt_time_entry.grid(row=1, column=3, padx=5, pady=5)
        self.apt_time_entry.insert(0, "10:00")
        
        # Book button
        book_btn = ttk.Button(input_frame, text="Book Appointment", command=self.book_appointment)
        book_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Appointments list
        list_frame = ttk.LabelFrame(appointments_frame, text="Appointment List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for appointments
        columns = ("ID", "Patient ID", "Doctor ID", "Date", "Time", "Status")
        self.appointment_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.appointment_tree.heading(col, text=col)
            self.appointment_tree.column(col, width=100)
        
        # Scrollbar
        apt_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.appointment_tree.yview)
        self.appointment_tree.configure(yscrollcommand=apt_scrollbar.set)
        
        self.appointment_tree.pack(side='left', fill='both', expand=True)
        apt_scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        btn_frame = ttk.Frame(appointments_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_appointments).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update Status", command=self.update_appointment_status).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_appointment).pack(side='left', padx=5)
    
    def add_patient(self):
        """Add a new patient"""
        try:
            name = self.patient_name_entry.get().strip()
            age = int(self.patient_age_entry.get())
            gender = self.patient_gender_var.get()
            contact = self.patient_contact_entry.get().strip()
            
            if not name or not contact:
                messagebox.showerror("Error", "Name and contact are required")
                return
            
            if age <= 0:
                messagebox.showerror("Error", "Age must be positive")
                return
            
            patient_id = self.hospital.add_patient(name, age, gender, contact)
            messagebox.showinfo("Success", f"Patient added with ID: {patient_id}")
            
            # Clear entries
            self.patient_name_entry.delete(0, tk.END)
            self.patient_age_entry.delete(0, tk.END)
            self.patient_contact_entry.delete(0, tk.END)
            
            # Refresh data
            self.refresh_all_data()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_doctor(self):
        """Add a new doctor"""
        try:
            name = self.doctor_name_entry.get().strip()
            specialization = self.doctor_spec_entry.get().strip()
            contact = self.doctor_contact_entry.get().strip()
            department = self.doctor_dept_entry.get().strip()
            
            if not all([name, specialization, contact, department]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            doctor_id = self.hospital.add_doctor(name, specialization, contact, department)
            messagebox.showinfo("Success", f"Doctor added with ID: {doctor_id}")
            
            # Clear entries
            self.doctor_name_entry.delete(0, tk.END)
            self.doctor_spec_entry.delete(0, tk.END)
            self.doctor_contact_entry.delete(0, tk.END)
            self.doctor_dept_entry.delete(0, tk.END)
            
            # Refresh data
            self.refresh_all_data()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def book_appointment(self):
        """Book a new appointment"""
        try:
            patient_id = self.apt_patient_entry.get().strip()
            doctor_id = self.apt_doctor_entry.get().strip()
            date = self.apt_date_entry.get().strip()
            time = self.apt_time_entry.get().strip()
            
            if not all([patient_id, doctor_id, date, time]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            appointment_id = self.hospital.book_appointment(patient_id, doctor_id, date, time)
            messagebox.showinfo("Success", f"Appointment booked with ID: {appointment_id}")
            
            # Clear entries
            self.apt_patient_entry.delete(0, tk.END)
            self.apt_doctor_entry.delete(0, tk.END)
            self.apt_time_entry.delete(0, tk.END)
            self.apt_time_entry.insert(0, "10:00")
            
            # Refresh data
            self.refresh_all_data()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_patient(self):
        """Update selected patient"""
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a patient to update")
            return
        
        # Get patient data and show update dialog
        patient_id = self.patient_tree.item(selection[0])['values'][0]
        patient = self.hospital.get_patient(patient_id)
        
        if patient:
            # Simple update dialog - in a real app, you'd have a more sophisticated form
            messagebox.showinfo("Info", f"Update functionality for patient {patient_id} would go here")
    
    def update_doctor(self):
        """Update selected doctor"""
        selection = self.doctor_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a doctor to update")
            return
        
        # Get doctor data and show update dialog
        doctor_id = self.doctor_tree.item(selection[0])['values'][0]
        doctor = self.hospital.get_doctor(doctor_id)
        
        if doctor:
            # Simple update dialog - in a real app, you'd have a more sophisticated form
            messagebox.showinfo("Info", f"Update functionality for doctor {doctor_id} would go here")
    
    def update_appointment_status(self):
        """Update appointment status"""
        selection = self.appointment_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return
        
        appointment_id = self.appointment_tree.item(selection[0])['values'][0]
        
        # Status selection dialog
        statuses = ["SCHEDULED", "CONFIRMED", "COMPLETED", "CANCELLED"]
        status = simpledialog.askstring("Update Status", 
                                      f"Enter new status for appointment {appointment_id}:\n" + 
                                      "\n".join(statuses))
        
        if status and status.upper() in statuses:
            try:
                result = self.hospital.update_appointment_status(appointment_id, 
                                                              AppointmentStatus[status.upper()])
                messagebox.showinfo("Success", result)
                self.refresh_all_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_patient(self):
        """Delete selected patient"""
        selection = self.patient_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        patient_id = self.patient_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient {patient_id}?"):
            try:
                result = self.hospital.remove_patient(patient_id)
                messagebox.showinfo("Success", result)
                self.refresh_all_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_doctor(self):
        """Delete selected doctor"""
        selection = self.doctor_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        doctor_id = self.doctor_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete doctor {doctor_id}?"):
            try:
                result = self.hospital.remove_doctor(doctor_id)
                messagebox.showinfo("Success", result)
                self.refresh_all_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_appointment(self):
        """Delete selected appointment"""
        selection = self.appointment_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return
        
        appointment_id = self.appointment_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete appointment {appointment_id}?"):
            try:
                result = self.hospital.remove_appointment(appointment_id)
                messagebox.showinfo("Success", result)
                self.refresh_all_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def refresh_patients(self):
        """Refresh the patients list"""
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Add patients
        for patient in self.hospital.get_all_patients():
            self.patient_tree.insert('', 'end', values=(
                patient.patient_id,
                patient.name,
                patient.age,
                patient.gender,
                patient.contact
            ))
    
    def refresh_doctors(self):
        """Refresh the doctors list"""
        # Clear existing items
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        
        # Add doctors
        for doctor in self.hospital.get_all_doctors():
            self.doctor_tree.insert('', 'end', values=(
                doctor.doctor_id,
                doctor.name,
                doctor.specialization,
                doctor.contact,
                doctor.department
            ))
    
    def refresh_appointments(self):
        """Refresh the appointments list"""
        # Clear existing items
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        # Add appointments
        for appointment in self.hospital.get_all_appointments():
            self.appointment_tree.insert('', 'end', values=(
                appointment.appointment_id,
                appointment.patient_id,
                appointment.doctor_id,
                appointment.date,
                appointment.time,
                appointment.status.value
            ))
    
    def refresh_overview(self):
        """Refresh the overview tab"""
        # Update statistics
        stats = self.hospital.get_hospital_statistics()
        self.patient_count_label.config(text=f"Total Patients: {stats['total_patients']}")
        self.doctor_count_label.config(text=f"Total Doctors: {stats['total_doctors']}")
        self.appointment_count_label.config(text=f"Total Appointments: {stats['total_appointments']}")
        self.active_appointment_label.config(text=f"Active Appointments: {stats['active_appointments']}")
        
        # Update department overview
        dept_stats = self.hospital.get_department_statistics()
        self.dept_text.delete(1.0, tk.END)
        for dept, count in dept_stats.items():
            self.dept_text.insert(tk.END, f"{dept}: {count} doctors\n")
    
    def refresh_all_data(self):
        """Refresh all data in the application"""
        self.refresh_patients()
        self.refresh_doctors()
        self.refresh_appointments()
        self.refresh_overview()
        
        # Save data
        try:
            self.hospital.save_data()
        except Exception as e:
            print(f"Error saving data: {e}")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = HospitalManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

