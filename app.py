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
    

    # Create Students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        Student_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    
    # Create Winners table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Winners (
                        Eid INTEGER,
                        Aid INTEGER,
                        Prize_money REAL,
                        FOREIGN KEY (Eid) REFERENCES Event(Eid),
                        FOREIGN KEY (Aid) REFERENCES Attendees(Aid),
                        PRIMARY KEY (Eid, Aid))''')
    
    
    
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
            # Attendee details fetched successfully
            messagebox.showinfo("Login Successful", f"Welcome {result[3]}!")
            # Now open fest details window
            open_fest_details(result)
        else:
            messagebox.showerror("Error", "Attendee not found.")
    
    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)

# Open Fest Details window
def open_fest_details(attendee):
    fid = attendee[2]  # Current Fest ID of the Attendee
    name = attendee[3]  # Attendee's Name
    
    # Open new window for fest details
    fest_window = tk.Toplevel(root)
    fest_window.title(f"{name} - Fests")
    fest_window.geometry("400x300")
    
    # Fetch all fests from the database
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Fest")
    fests = cursor.fetchall()
    
    conn.close()
    
    if fests:
        tk.Label(fest_window, text="Explore Fests", font=("Arial", 14, "bold")).pack(pady=10)
        for fest in fests:
            fest_id = fest[0]
            fest_name = fest[1]
            
            fest_frame = tk.Frame(fest_window)
            fest_frame.pack(pady=5)
            
            tk.Label(fest_frame, text=f"Fest ID: {fest_id} - {fest_name}").pack(side=tk.LEFT, padx=5)
            
            # Explore Fest button
            tk.Button(fest_frame, text="Explore Fest", command=lambda fid=fest_id: explore_fest(fid, attendee)).pack(side=tk.RIGHT)

    else:
        tk.Label(fest_window, text="No fests available.", font=("Arial", 10)).pack(pady=10)


# Open Event Details for a selected Fest
def explore_fest(fid, attendee):
    name = attendee[3]  # Attendee's Name
    
    # Open new window for events in the selected fest
    event_window = tk.Toplevel(root)
    event_window.title(f"{name} - Events in Fest {fid}")
    event_window.geometry("500x400")
    
    # Fetch events for the selected fest from the database
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event WHERE Fid = ?", (fid,))
    events = cursor.fetchall()
    conn.close()

    if events:
        tk.Label(event_window, text="Event Details", font=("Arial", 12, "bold")).grid(row=0, columnspan=4, pady=5)
        
        # Display column headers
        tk.Label(event_window, text="Event ID").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(event_window, text="Event Name").grid(row=1, column=1, padx=5, pady=5)
        tk.Label(event_window, text="Event Head").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(event_window, text="Reg Fee").grid(row=1, column=3, padx=5, pady=5)

        # Display each event's details with a 'Join' button
        for i, event in enumerate(events, start=2):
            tk.Label(event_window, text=event[1]).grid(row=i, column=0, padx=5, pady=5)  # Event ID
            tk.Label(event_window, text=event[2]).grid(row=i, column=1, padx=5, pady=5)  # Event Name
            tk.Label(event_window, text=event[3]).grid(row=i, column=2, padx=5, pady=5)  # Event Head
            tk.Label(event_window, text=event[4]).grid(row=i, column=3, padx=5, pady=5)  # Registration Fee
            
            # Join button for each event
            tk.Button(event_window, text="Join", command=lambda eid=event[0], fid=event[1], attendee=attendee: join_event(eid, fid, attendee)).grid(row=i, column=4, padx=5, pady=5)

    else:
        tk.Label(event_window, text="No events found for this fest.", font=("Arial", 10)).pack(pady=10)

# Join the selected event
def join_event(eid, fid, attendee):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()

    # Update the attendee's Fid and Eid in the database
    cursor.execute("UPDATE Attendees SET Fid = ?, Eid = ? WHERE Aid = ?", (fid, eid, attendee[1]))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Event Joined", f"You have successfully joined Event ID {eid} in Fest ID {fid}.")


# Open Admin Login Page
def open_admin_login():
    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Admin Login")
    admin_login_window.geometry("300x200")
    
    tk.Label(admin_login_window, text="Username").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(admin_login_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(admin_login_window, text="Password").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(admin_login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)
    
    # Admin credentials
    admin_username = "admin2024"
    admin_password = "1234"
    
    # Login button
    def admin_login():
        if entry_username.get() == admin_username and entry_password.get() == admin_password:
            admin_login_window.destroy()
            open_admin_page()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    tk.Button(admin_login_window, text="Login", command=admin_login).grid(row=2, columnspan=2, pady=10)

# Generate a new unique Fest ID
def generate_fid():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Fid) FROM Fest")
    max_fid = cursor.fetchone()[0]
    conn.close()
    return max_fid + 1 if max_fid is not None else 1  # Start FID at 1 if the table is empty

# Open Fest Registration page
def open_fest_registration():
    fest_window = tk.Toplevel(root)
    fest_window.title("Fest Registration")
    fest_window.geometry("500x500")
    
    # Generate a new unique Fest ID
    fid = generate_fid()

    # Display the auto-generated Fest ID
    tk.Label(fest_window, text="Fest ID (auto-generated)").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(fest_window, text=fid).grid(row=0, column=1, padx=10, pady=5)
    
    # Form labels and entry fields for other Fest table details
    tk.Label(fest_window, text="Fest Name").grid(row=1, column=0, padx=10, pady=5)
    entry_fname = tk.Entry(fest_window)
    entry_fname.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Organisations").grid(row=2, column=0, padx=10, pady=5)
    entry_organisations = tk.Entry(fest_window)
    entry_organisations.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Coordinator").grid(row=3, column=0, padx=10, pady=5)
    entry_coordinator = tk.Entry(fest_window)
    entry_coordinator.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Number of Events").grid(row=4, column=0, padx=10, pady=5)
    entry_no_events = tk.Entry(fest_window)
    entry_no_events.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Total Expenditure").grid(row=5, column=0, padx=10, pady=5)
    entry_total_expenditure = tk.Entry(fest_window)
    entry_total_expenditure.grid(row=5, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Date").grid(row=6, column=0, padx=10, pady=5)
    entry_date = tk.Entry(fest_window)
    entry_date.grid(row=6, column=1, padx=10, pady=5)
    
    tk.Label(fest_window, text="Venue").grid(row=7, column=0, padx=10, pady=5)
    entry_venue = tk.Entry(fest_window)
    entry_venue.grid(row=7, column=1, padx=10, pady=5)
    
    # Function to register fest in the database
    def register_fest():
        fname = entry_fname.get()
        organisations = entry_organisations.get()
        coordinator = entry_coordinator.get()
        no_events = entry_no_events.get()
        total_expenditure = entry_total_expenditure.get()
        date = entry_date.get()
        venue = entry_venue.get()
        
        # Insert fest data into Fest table
        conn = sqlite3.connect('college_fest.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''INSERT INTO Fest (Fid, Fname, Organisations, Coordinator, No_events, Total_expenditure, Date, Venue)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (fid, fname, organisations, coordinator, no_events, total_expenditure, date, venue))
            conn.commit()
            messagebox.showinfo("Success", f"Fest '{fname}' registered successfully with Fest ID: {fid}!")
            fest_window.destroy()  # Close the fest registration window
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Fest registration failed due to an integrity error.")
        finally:
            conn.close()

    # Register button
    tk.Button(fest_window, text="Register", command=register_fest).grid(row=8, columnspan=2, pady=20)

# Generate a unique Event ID
def generate_eid():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Eid) FROM Event")
    max_eid = cursor.fetchone()[0]
    conn.close()
    return max_eid + 1 if max_eid is not None else 1  # Start Eid at 1 if table is empty


# Generate a unique Guest ID
def generate_gid():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Gid) FROM Guest")
    max_gid = cursor.fetchone()[0]
    conn.close()
    return max_gid + 1 if max_gid is not None else 1  # Start Gid at 1 if table is empty

# Open Manage Event page
def open_manage_event_page():
    manage_event_window = tk.Toplevel(root)
    manage_event_window.title("Manage Event")
    manage_event_window.geometry("300x200")
    
    tk.Label(manage_event_window, text="Enter Event ID").grid(row=0, column=0, padx=10, pady=5)
    entry_eid = tk.Entry(manage_event_window)
    entry_eid.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(manage_event_window, text="Enter Event Name").grid(row=1, column=0, padx=10, pady=5)
    entry_event_name = tk.Entry(manage_event_window)
    entry_event_name.grid(row=1, column=1, padx=10, pady=5)
    
    def open_event_options():
        eid = entry_eid.get()
        event_name = entry_event_name.get()
        
        if not eid or not event_name:
            messagebox.showerror("Error", "Please enter both Event ID and Event Name.")
            return
        
        try:
            eid = int(eid)
            # Open the Event Management Options window
            event_options_window = tk.Toplevel(manage_event_window)
            event_options_window.title("Event Management Options")
            event_options_window.geometry("400x400")
            
            tk.Label(event_options_window, text=f"Managing Event: {event_name} (ID: {eid})", font=("Arial", 14, "bold")).pack(pady=10)
            
            # Buttons for event management options
            tk.Button(event_options_window, text="View Event Details", command=lambda: view_event_details(eid)).pack(pady=10)
            tk.Button(event_options_window, text="Add Guest", command=lambda: open_add_guest_page(eid)).pack(pady=10)
            tk.Button(event_options_window, text="Add Winners", command=lambda: open_add_winner_page(eid)).pack(pady=10)
            tk.Button(event_options_window, text="View Guest", command=lambda: view_guest_details(eid)).pack(pady=10)
            tk.Button(event_options_window, text="View Winners", command=lambda: view_winner_details(eid)).pack(pady=10)
            tk.Button(event_options_window, text="View Attendees", command=lambda: view_attendee_details(eid)).pack(pady=10)
        

        except ValueError:
            messagebox.showerror("Error", "Invalid Event ID format. Please enter a numeric Event ID.")
    
    tk.Button(manage_event_window, text="Submit", command=open_event_options).grid(row=2, columnspan=2, pady=10)



# View Event Details
def view_event_details(eid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event WHERE Eid = ?", (eid,))
    event_details = cursor.fetchone()
    conn.close()
    
    if event_details:
        details = f"Event ID: {event_details[1]}\nName: {event_details[2]}\nHead: {event_details[3]}\nRegistration Fee: {event_details[4]}"
        messagebox.showinfo("Event Details", details)
    else:
        messagebox.showerror("Error", "Event not found.")

# Open Add Guest page
def open_add_guest_page(eid):
    guest_window = tk.Toplevel(root)
    guest_window.title("Add Guest")
    guest_window.geometry("400x400")
    
    gid = generate_gid()  # Auto-generate a unique Guest ID
    
    # Display auto-generated Guest ID and provided Event ID
    tk.Label(guest_window, text="Guest ID (auto-generated)").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(guest_window, text=gid).grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(guest_window, text="Event ID").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(guest_window, text=eid).grid(row=1, column=1, padx=10, pady=5)
    
    # Form labels and entry fields for Guest table details
    tk.Label(guest_window, text="Guest Name").grid(row=2, column=0, padx=10, pady=5)
    entry_guest_name = tk.Entry(guest_window)
    entry_guest_name.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(guest_window, text="Remuneration").grid(row=3, column=0, padx=10, pady=5)
    entry_guest_remuneration = tk.Entry(guest_window)
    entry_guest_remuneration.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(guest_window, text="Contact Number").grid(row=4, column=0, padx=10, pady=5)
    entry_guest_contact = tk.Entry(guest_window)
    entry_guest_contact.grid(row=4, column=1, padx=10, pady=5)
    
    # Function to add guest to the database
    def add_guest():
        guest_name = entry_guest_name.get()
        remuneration = entry_guest_remuneration.get()
        contact_number = entry_guest_contact.get()
        
        conn = sqlite3.connect('college_fest.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''INSERT INTO Guest (Eid, Gid, Guest_name, Guest_remuneration, Guest_contact_number)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (eid, gid, guest_name, remuneration, contact_number))
            conn.commit()
            messagebox.showinfo("Success", f"Guest '{guest_name}' added successfully with Guest ID: {gid}!")
            guest_window.destroy()  # Close the guest registration window
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Failed to add guest due to an integrity error.")
        finally:
            conn.close()
    
    # Register button for adding guest
    tk.Button(guest_window, text="Add Guest", command=add_guest).grid(row=5, columnspan=2, pady=20)

# View Guest Details
def view_guest_details(eid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guest WHERE Eid = ?", (eid,))
    guests = cursor.fetchall()
    conn.close()
    
    if guests:
        guest_info = "\n".join([f"Guest ID: {guest[1]}, Name: {guest[2]}, Remuneration: {guest[3]}, Contact: {guest[4]}" for guest in guests])
        messagebox.showinfo("Guest Details", guest_info)
    else:
        messagebox.showinfo("Guest Details", "No guests found for this event.")

# Open Add Winner page
def open_add_winner_page(eid):
    winner_window = tk.Toplevel(root)
    winner_window.title("Add Winner")
    winner_window.geometry("400x300")
    
    # Display Event ID label
    tk.Label(winner_window, text="Event ID (auto-filled)").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(winner_window, text=eid).grid(row=0, column=1, padx=10, pady=5)
    
    # Form labels and entry fields for Winner details
    tk.Label(winner_window, text="Attendee ID").grid(row=1, column=0, padx=10, pady=5)
    entry_aid = tk.Entry(winner_window)
    entry_aid.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(winner_window, text="Prize Money").grid(row=2, column=0, padx=10, pady=5)
    entry_prize_money = tk.Entry(winner_window)
    entry_prize_money.grid(row=2, column=1, padx=10, pady=5)
    
    # Function to add winner to the database
    def add_winner():
        aid = entry_aid.get()
        prize_money = entry_prize_money.get()
        
        conn = sqlite3.connect('college_fest.db')
        cursor = conn.cursor()
        
        try:
            # Insert the winner details
            cursor.execute('''INSERT INTO Winners (Eid, Aid, Prize_money)
                              VALUES (?, ?, ?)''', 
                           (eid, aid, prize_money))
            conn.commit()
            messagebox.showinfo("Success", f"Winner with Attendee ID {aid} added successfully!")
            winner_window.destroy()  # Close the add winner window
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Failed to add winner. Check Attendee ID or ensure this winner has not been added for this event.")
        finally:
            conn.close()
    
    # Register button for adding winner
    tk.Button(winner_window, text="Submit", command=add_winner).grid(row=3, columnspan=2, pady=20)

# View Winner Details
def view_winner_details(eid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Winners WHERE Eid = ?", (eid,))
    winners = cursor.fetchall()
    conn.close()
    
    if winners:
        winner_info = "\n".join([f"Attendee ID: {winner[1]}, Prize Money: {winner[2]}" for winner in winners])
        messagebox.showinfo("Winner Details", winner_info)
    else:
        messagebox.showinfo("Winner Details", "No winners found for this event.")

# View Attendee Details
def view_attendee_details(eid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    
    # Query to fetch attendees who are registered for this event
    cursor.execute("SELECT Aid, Name FROM Attendees WHERE Eid = ?", (eid,))
    attendees = cursor.fetchall()
    conn.close()

    if attendees:
        attendee_info = "\n".join([f"Attendee ID: {attendee[0]}, Name: {attendee[1]}" for attendee in attendees])
        messagebox.showinfo("Attendee Details", attendee_info)
    else:
        messagebox.showinfo("Attendee Details", "No attendees found for this event.")



# Open Fest Management page
def open_fest_management_page():
    fest_mgmt_window = tk.Toplevel(root)
    fest_mgmt_window.title("Fest Management")
    fest_mgmt_window.geometry("300x200")
    
    tk.Label(fest_mgmt_window, text="Enter Fest ID").grid(row=0, column=0, padx=10, pady=5)
    entry_fid = tk.Entry(fest_mgmt_window)
    entry_fid.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(fest_mgmt_window, text="Enter Fest Name").grid(row=1, column=0, padx=10, pady=5)
    entry_fname = tk.Entry(fest_mgmt_window)
    entry_fname.grid(row=1, column=1, padx=10, pady=5)
    
    def open_management_options():
        fid = entry_fid.get()
        fname = entry_fname.get()
        
        if not fid or not fname:
            messagebox.showerror("Error", "Please enter both Fest ID and Fest Name.")
            return
        
        try:
            fid = int(fid)
            # Open the Management Options window
            management_window = tk.Toplevel(fest_mgmt_window)
            management_window.title("Fest Management Options")
            management_window.geometry("400x300")
            
            tk.Label(management_window, text=f"Managing Fest: {fname} (ID: {fid})", font=("Arial", 14, "bold")).pack(pady=10)
            
            # Buttons for fest management options
            tk.Button(management_window, text="Add Event", command=lambda: open_add_event_page(fid)).pack(pady=10)
            tk.Button(management_window, text="Manage Event", command=lambda: open_manage_event_page()).pack(pady=10)
            tk.Button(management_window, text="Add Expense", command=lambda: open_add_expense_page(fid)).pack(pady=10)
            tk.Button(management_window, text="View Expense", command=lambda: view_expense_details(fid)).pack(pady=10)
            tk.Button(management_window, text="List Events", command=lambda: list_events(fid)).pack(pady=10)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid Fest ID format. Please enter a numeric Fest ID.")
    
    tk.Button(fest_mgmt_window, text="Submit", command=open_management_options).grid(row=2, columnspan=2, pady=10)

# Open Add Event page
def open_add_event_page(fid):
    event_window = tk.Toplevel(root)
    event_window.title("Add Event")
    event_window.geometry("400x400")
    
    # Generate a new unique Event ID
    eid = generate_eid()
    
    # Display auto-generated Event ID and Fest ID
    tk.Label(event_window, text="Event ID (auto-generated)").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(event_window, text=eid).grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(event_window, text="Fest ID").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(event_window, text=fid).grid(row=1, column=1, padx=10, pady=5)
    
    # Form labels and entry fields for Event table details
    tk.Label(event_window, text="Event Name").grid(row=2, column=0, padx=10, pady=5)
    entry_event_name = tk.Entry(event_window)
    entry_event_name.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(event_window, text="Event Head").grid(row=3, column=0, padx=10, pady=5)
    entry_event_head = tk.Entry(event_window)
    entry_event_head.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(event_window, text="Registration Fee").grid(row=4, column=0, padx=10, pady=5)
    entry_reg_fee = tk.Entry(event_window)
    entry_reg_fee.grid(row=4, column=1, padx=10, pady=5)
    
    # Function to register event in the database
    def register_event():
        event_name = entry_event_name.get()
        event_head = entry_event_head.get()
        reg_fee = entry_reg_fee.get()
        
        # Insert event data into Event table
        conn = sqlite3.connect('college_fest.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''INSERT INTO Event (Fid, Eid, Event_name, Event_head, Reg_fee)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (fid, eid, event_name, event_head, reg_fee))
            conn.commit()
            messagebox.showinfo("Success", f"Event '{event_name}' registered successfully with Event ID: {eid}!")
            event_window.destroy()  # Close the event registration window
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Event registration failed due to an integrity error.")
        finally:
            conn.close()
    
    # Register button
    tk.Button(event_window, text="Register", command=register_event).grid(row=5, columnspan=2, pady=20)

# Function to generate unique Tid
def generate_tid():
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Tid) FROM Expenditure")
    max_tid = cursor.fetchone()[0]
    conn.close()
    return max_tid + 1 if max_tid is not None else 1  # Start Tid at 1 if table is empty

# Open Add Expense page
def open_add_expense_page(fid):
    expense_window = tk.Toplevel(root)
    expense_window.title("Add Expense")
    expense_window.geometry("400x300")
    
    # Display Fest ID label
    tk.Label(expense_window, text="Fest ID (auto-filled)").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(expense_window, text=fid).grid(row=0, column=1, padx=10, pady=5)
    
    # Form labels and entry fields for Expense details
    tk.Label(expense_window, text="Type").grid(row=1, column=0, padx=10, pady=5)
    entry_type = tk.Entry(expense_window)
    entry_type.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(expense_window, text="Amount Estimated").grid(row=2, column=0, padx=10, pady=5)
    entry_amount_estimated = tk.Entry(expense_window)
    entry_amount_estimated.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(expense_window, text="Actual Expenditure").grid(row=3, column=0, padx=10, pady=5)
    entry_actual_expenditure = tk.Entry(expense_window)
    entry_actual_expenditure.grid(row=3, column=1, padx=10, pady=5)
    
    # Function to add expense to the database
    def add_expense():
        tid = generate_tid()  # Generate unique Tid
        expense_type = entry_type.get()
        amount_estimated = entry_amount_estimated.get()
        actual_expenditure = entry_actual_expenditure.get()
        
        conn = sqlite3.connect('college_fest.db')
        cursor = conn.cursor()
        
        try:
            # Insert the expense details
            cursor.execute('''INSERT INTO Expenditure (Fid, Tid, Type, Amount_estimated, Actual_expenditure)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (fid, tid, expense_type, amount_estimated, actual_expenditure))
            conn.commit()
            messagebox.showinfo("Success", f"Expense with ID {tid} added successfully!")
            expense_window.destroy()  # Close the add expense window
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
        finally:
            conn.close()
    
    # Register button for adding expense
    tk.Button(expense_window, text="Submit", command=add_expense).grid(row=4, columnspan=2, pady=20)

# View Expense Details
def view_expense_details(fid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Expenditure WHERE Fid = ?", (fid,))
    expenses = cursor.fetchall()
    conn.close()
    
    if expenses:
        expense_info = "\n".join([f"Type: {expense[1]}, Estimated: {expense[2]}, Actual: {expense[3]}" for expense in expenses])
        messagebox.showinfo("Expense Details", expense_info)
    else:
        messagebox.showinfo("Expense Details", "No expenses found for this fest.")

# Function to list all events for a specific fest
# Function to list all events for a specific fest in a new window
def list_events(fid):
    conn = sqlite3.connect('college_fest.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event WHERE Fid = ?", (fid,))
    events = cursor.fetchall()
    conn.close()
    
    # Create a new window to show event details
    event_window = tk.Toplevel(root)
    event_window.title(f"Events for Fest ID {fid}")
    event_window.geometry("500x400")
    
    # Display event details in this new window
    if events:
        tk.Label(event_window, text="Event Details", font=("Arial", 12, "bold")).grid(row=0, columnspan=4, pady=5)
        
        # Display column headers
        tk.Label(event_window, text="Event ID").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(event_window, text="Event Name").grid(row=1, column=1, padx=5, pady=5)
        tk.Label(event_window, text="Event Head").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(event_window, text="Reg Fee").grid(row=1, column=3, padx=5, pady=5)

        # Display each event's details
        for i, event in enumerate(events, start=2):
            tk.Label(event_window, text=event[1]).grid(row=i, column=0, padx=5, pady=5)  # Event ID
            tk.Label(event_window, text=event[2]).grid(row=i, column=1, padx=5, pady=5)  # Event Name
            tk.Label(event_window, text=event[3]).grid(row=i, column=2, padx=5, pady=5)  # Event Head
            tk.Label(event_window, text=event[4]).grid(row=i, column=3, padx=5, pady=5)  # Registration Fee
    else:
        tk.Label(event_window, text="No events found for this fest.", font=("Arial", 10)).pack(pady=10)


# Open Admin Page
def open_admin_page():
    admin_page_window = tk.Toplevel(root)
    admin_page_window.title("College Fest Management System - Admin")
    admin_page_window.geometry("400x200")
    
    tk.Label(admin_page_window, text="College Fest Management System", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Admin options
    tk.Button(admin_page_window, text="Fest Registration", width=20, command=open_fest_registration).pack(pady=10)
    tk.Button(admin_page_window, text="Fest Management", width=20, command=open_fest_management_page).pack(pady=10)


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
tk.Button(root, text="Admin Login", command=open_admin_login, width=20).pack(pady=10)

root.mainloop()