 College Fest Management System

This is a **College Fest Management System** designed to help manage various aspects of a college fest, including event management, attendee registration, guest and winner management, and more. The system allows fest organizers and attendees to manage and interact with the event details, guests, and winners for a smooth fest experience.

## Features

- **Fest Management**: Create and manage fest details (name, venue, date, expenditure).
- **Event Management**: Create and manage events within a fest, add guests, and handle winners.
- **Attendee Management**: Register attendees and assign them to events. Attendees can log in, explore fests, and join events.
- **Guest Management**: Add and view event guests (including remuneration and contact details).
- **Winner Management**: Add winners to events and assign prize money.
- **Expenditure Management**: Track the estimated and actual expenditure for each fest.

## Technologies Used

- **Programming Language**: Python
- **Database**: SQLite
- **GUI Library**: Tkinter (for the graphical user interface)

## Prerequisites

- Python 3.x installed on your machine.
- The `sqlite3` library (this comes pre-installed with Python).
  
## Installation

1. **Clone the repository**:
   
   git clone https://github.com/yourusername/college-fest-management.git
   

2. **Navigate to the project directory**:
   
   cd college-fest-management
   

3. **Run the application**:
   
   python main.py
   

   This will launch the GUI application. You can start managing your college fest by creating fests, adding events, and registering attendees.

## Database Structure

The database college_fest.db consists of the following tables:

- **Fest**: Stores information about each fest (e.g., name, date, venue).
- **Event**: Stores event details under each fest (e.g., event name, event head).
- **Attendees**: Stores information about attendees and their registered events.
- **Guest**: Stores details of the guests invited to the events.
- **Winners**: Stores details about winners of the events, including prize money.
- **Expenditure**: Tracks estimated and actual expenditures for the fest.
- **Students**: Stores basic details about students (name, email).

## Features Breakdown

### 1. **Fest Management**
   - Create and manage fest details like name, venue, and date.
   - Calculate the total number of events and the total expenditure.

### 2. **Event Management**
   - Add new events to the fest.
   - View and manage guests for each event.
   - View and add winners for each event.
   - Add a registration fee for events.

### 3. **Attendee Management**
   - Register attendees with details like name, phone number, email, semester, branch, and college.
   - Attendees can log in with their name and ID, view the fests, and join events.
   - On joining an event, their attendee ID and event ID are linked.

### 4. **Guest Management**
   - Add guests to events with their remuneration and contact details.
   - View the guest list for each event.

### 5. **Winner Management**
   - Assign winners for each event and award them with prize money.
   - View the list of winners for each event.

### 6. **Expenditure Management**
   - Track estimated and actual expenditure for each fest.

## Database Schema

### Tables:

- **Fest**:
  - Fid: Fest ID (Primary Key)
  - Fname: Fest name
  - Organisations: Organizing body
  - Coordinator: Fest coordinator
  - No_events: Number of events
  - Total_expenditure: Total expenditure of the fest
  - Date: Date of the fest
  - Venue: Venue of the fest

- **Event**:
  - Fid: Fest ID (Foreign Key)
  - Eid: Event ID (Primary Key)
  - Event_name: Name of the event
  - Event_head: Event head
  - Reg_fee: Registration fee for the event

- **Attendees**:
  - Fid: Fest ID (Foreign Key)
  - Aid: Attendee ID (Primary Key)
  - Eid: Event ID (Foreign Key)
  - Name: Attendee name
  - Phone_no: Attendee phone number
  - Mail_id: Attendee email address
  - Semester: Attendee semester
  - Branch: Attendee branch
  - College: Attendee college name

- **Guest**:
  - Eid: Event ID (Foreign Key)
  - Gid: Guest ID (Primary Key)
  - Guest_name: Name of the guest
  - Guest_remuneration: Remuneration for the guest
  - Guest_contact_number: Contact number of the guest

- **Winners**:
  - Eid: Event ID (Foreign Key)
  - Aid: Attendee ID (Foreign Key)
  - Prize_money: Prize money awarded to the winner

- **Expenditure**:
  - Fid: Fest ID (Foreign Key)
  - Type: Type of expenditure (e.g., infrastructure, refreshments)
  - Tid: Transaction ID (Primary Key)
  - Amount_estimated: Estimated expenditure
  - Actual_expenditure: Actual expenditure

## Future Improvements

- Add the ability to edit or delete events, guests, and attendees.
- Implement user authentication for fest coordinators and attendees.
- Provide detailed reports on expenditure and event participation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

