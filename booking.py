import sqlite3
import streamlit as st
import datetime
import pandas as pd

# Path to SQLite database
db_path = 'data/bookings.db'

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create the table (if not already created)
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS bookings (
#         name TEXT NOT NULL,
#         numberofpeople INTEGER NOT NULL, 
#         phone TEXT NOT NULL,
#         time TEXT NOT NULL,
#         service TEXT NOT NULL
#     )
# ''')

# Insert booking into the database
def insert_booking(name, numberofpeople, phone, time, service):
    cur.execute("INSERT INTO bookings (name, numberofpeople, phone, time, service) VALUES (?, ?, ?, ?, ?)",
                (name, numberofpeople, phone, time, service))
    conn.commit()

# Check if a time overlaps with any existing bookings by less than 1 hour
def check_time_availability(new_time):
    cur.execute("SELECT time FROM bookings")
    existing_times = cur.fetchall()
    
    # Convert the new time into a datetime object
    try:
        new_time_obj = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M")  # User input time format
    except ValueError:
        # In case user input includes seconds, handle that
        new_time_obj = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")

    for existing_time in existing_times:
        existing_time = existing_time[0]
        # Try parsing the existing time with both formats (with and without seconds)
        try:
            existing_time_obj = datetime.datetime.strptime(existing_time, "%Y-%m-%d %H:%M")  # For time without seconds
        except ValueError:
            # If that fails, try the format with seconds
            existing_time_obj = datetime.datetime.strptime(existing_time, "%Y-%m-%d %H:%M:%S")  # Format in the database

        # Calculate the difference between the existing time and the new time
        time_difference = abs(existing_time_obj - new_time_obj)
        
        # If the time difference is less than 1 hour, return False
        if time_difference < datetime.timedelta(hours=1):
            return False
    return True



# Streamlit UI
def display_bookings():
    st.title("BETTY SPA")
    st.subheader("Hệ thống đặt lịch")
    
    # Client name input
    client_name = st.text_input("Nhập tên của bạn")
    
    # Phone number input
    phone = st.text_input("Số điện thoại")
    
    # Number of people with session state handling
    people = st.number_input("Số người", min_value=1, max_value=10, value=1)
    
    # Date picker
    date = st.date_input("Chọn ngày", min_value=datetime.date.today())
    
    # Time picker
    time = st.time_input("Chọn giờ", datetime.time(9, 0))

    # Service selection (optional)
    service = st.selectbox("Dịch vụ", ["Facial", "Massage", "Manicure", "Pedicure"])

    # Combine date and time into a single string for storing in the database
    datetime_str = f"{date} {time}"

    if st.button("Đặt lịch hẹn"):
        # Check if the time is available (at least 1 hour away from any existing appointment)
        if not check_time_availability(datetime_str):
            st.error("Lịch đã có người đặt trong vòng 1 giờ. Vui lòng chọn thời gian khác.")
        else:
            # Insert booking into the database if the time is available
            insert_booking(client_name, people, phone, datetime_str, service)
            st.success("Đặt lịch thành công!")

    # Display current bookings in a table format with custom column names
    st.subheader("Các lịch hẹn hiện tại")
    
    # Fetch data from the database, sorted by time in ascending order
    cur.execute("SELECT name, numberofpeople, phone, time, service FROM bookings ORDER BY time ASC")
    bookings = cur.fetchall()

    # Define column names for the table
    column_names = ["Tên khách hàng", "Số người", "Số điện thoại", "Thời gian", "Dịch vụ"]
    
    # Display the bookings without changing the time format
    formatted_bookings = []
    for booking in bookings:
        name, numberofpeople, phone, time, service = booking
        formatted_bookings.append([name, numberofpeople, phone, time, service])
    
    # Display the bookings with custom column names using a DataFrame
    bookings_df = pd.DataFrame(formatted_bookings, columns=column_names)
    st.table(bookings_df)

if __name__ == "__main__":
    display_bookings()

# Close the database connection
conn.close()
