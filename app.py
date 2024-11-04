import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    
    # Create Fest table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Fest (
                        Fid INTEGER PRIMARY KEY,
                        Fname TEXT NOT NULL,
                        Organisations TEXT,
                        Coordinator TEXT,
                        No_events INTEGER,
                        Total_expenditure REAL,
                        Date TEXT,
                        Venue TEXT)''')
    
    # Create Attendees table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Attendees (
                        Fid INTEGER,
                        Aid INTEGER PRIMARY KEY,
                        Eid INTEGER,
                        Name TEXT NOT NULL,
                        Phone_no TEXT,
                        Mail_id TEXT,
                        Semester INTEGER,
                        Branch TEXT,
                        College TEXT,
                        FOREIGN KEY (Fid) REFERENCES Fest(Fid),
                        FOREIGN KEY (Eid) REFERENCES Event(Eid))''')
    
    # Create Expenditure table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Expenditure (
                        Fid INTEGER,
                        Type TEXT,
                        Tid INTEGER PRIMARY KEY,
                        Amount_estimated REAL,
                        Actual_expenditure REAL,
                        FOREIGN KEY (Fid) REFERENCES Fest(Fid))''')
    
    # Create Event table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Event (
                        Fid INTEGER,
                        Eid INTEGER PRIMARY KEY,
                        Event_name TEXT NOT NULL,
                        Event_head TEXT,
                        Reg_fee REAL,
                        FOREIGN KEY (Fid) REFERENCES Fest(Fid))''')
    
    # Create Guest table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Guest (
                        Eid INTEGER,
                        Gid INTEGER PRIMARY KEY,
                        Guest_name TEXT NOT NULL,
                        Guest_remuneration REAL,
                        Guest_contact_number TEXT,
                        FOREIGN KEY (Eid) REFERENCES Event(Eid))''')
    
    # Create Winners table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Winners (
                        Eid INTEGER,
                        Aid INTEGER,
                        Prize_money REAL,
                        FOREIGN KEY (Eid) REFERENCES Event(Eid),
                        FOREIGN KEY (Aid) REFERENCES Attendees(Aid),
                        PRIMARY KEY (Eid, Aid))''')
    
    # Create Students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        Student_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    
    # Create Registrations table
    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                        student_id INTEGER,
                        event_id INTEGER,
                        FOREIGN KEY (student_id) REFERENCES students(Student_id),
                        FOREIGN KEY (event_id) REFERENCES Event(Eid))''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Run the setup function to create the tables
setup_database()
print("Database and tables created successfully.")

def generate_aid():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Aid) FROM Attendees")
    max_aid = cursor.fetchone()[0]
    conn.close()
    return max_aid + 1 if max_aid is not None else 1  # Start Aid at 1 if table is empty

# Add attendee to the database
def add_attendee(aid, name, phone, mail, semester, branch, college):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Attendees (Aid, Name, Phone_no, Mail_id, Semester, Branch, College) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (aid, name, phone, mail, semester, branch, college))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Attendee added successfully with Aid: {aid}!")

def search_attendee(name, aid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Attendees WHERE Name = ? AND Aid = ?", (name, aid))
    result = cursor.fetchone()
    conn.close()
    return result

# Open Student Registration Page
def open_registration_page():
    reg_window = tk.Toplevel(root)
    reg_window.title("Student Registration")
    reg_window.geometry("400x400")
    
    # Registration form labels and entries
    tk.Label(reg_window, text="Name").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(reg_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(reg_window, text="Phone Number").grid(row=1, column=0, padx=10, pady=5)
    entry_phone = tk.Entry(reg_window)
    entry_phone.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(reg_window, text="Mail ID").grid(row=2, column=0, padx=10, pady=5)
    entry_mail = tk.Entry(reg_window)
    entry_mail.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(reg_window, text="Semester").grid(row=3, column=0, padx=10, pady=5)
    entry_semester = tk.Entry(reg_window)
    entry_semester.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(reg_window, text="Branch").grid(row=4, column=0, padx=10, pady=5)
    entry_branch = tk.Entry(reg_window)
    entry_branch.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Label(reg_window, text="College").grid(row=5, column=0, padx=10, pady=5)
    entry_college = tk.Entry(reg_window)
    entry_college.grid(row=5, column=1, padx=10, pady=5)
    
    # Submit button
    def submit_registration():
        aid = generate_aid()  # Generate new unique Aid
        add_attendee(
            aid, 
            entry_name.get(), 
            entry_phone.get(), 
            entry_mail.get(), 
            entry_semester.get(), 
            entry_branch.get(), 
            entry_college.get()
        )
        reg_window.destroy()

    tk.Button(reg_window, text="Submit", command=submit_registration).grid(row=6, columnspan=2, pady=10)
# Open Student Login Page
def open_login_page():
    login_window = tk.Toplevel(root)
    login_window.title("Student Login")
    login_window.geometry("300x200")
    
    tk.Label(login_window, text="Name").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(login_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(login_window, text="Attendee ID").grid(row=1, column=0, padx=10, pady=5)
    entry_aid = tk.Entry(login_window)
    entry_aid.grid(row=1, column=1, padx=10, pady=5)
    
    # Login button
    def login():
        result = search_attendee(entry_name.get(), entry_aid.get())
        if result:
            info = f"ID: {result[1]}\nEvent ID: {result[2]}\nName: {result[3]}\nPhone: {result[4]}\nEmail: {result[5]}\nSemester: {result[6]}\nBranch: {result[7]}\nCollege: {result[8]}"
            messagebox.showinfo("Attendee Details", info)
        else:
            messagebox.showerror("Error", "Attendee not found.")
    
    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)

# Main Window
root = tk.Tk()
root.title("College Fest Management System")
root.geometry("400x200")
root.configure(bg="black")

# Title
title_label = tk.Label(root, text="College Fest Management System", font=("Arial", 16, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

# Main Buttons
tk.Button(root, text="Student Registration", command=open_registration_page, width=20).pack(pady=10)
tk.Button(root, text="Student Login", command=open_login_page, width=20).pack(pady=10)

root.mainloop()