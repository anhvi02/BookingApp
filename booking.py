import sqlite3
import streamlit as st
import datetime

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

# Streamlit UI
def display_bookings():
    st.title("Hệ thống đặt lịch Spa")
    
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



    if st.button("Đặt lịch hẹn"):
        # Combine date and time into a single string
        datetime_str = f"{date} {time}"
        # Insert booking into the database
        insert_booking(client_name, people, phone, datetime_str, service)
        st.success("Đặt lịch thành công!")
    
    # Display current bookings in a table format
    st.subheader("Các lịch hẹn hiện tại")
    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()
    # Display the bookings in a table format
    st.table(bookings)

if __name__ == "__main__":
    display_bookings()

# Close the database connection
conn.close()
