import sqlite3
import streamlit as st
import datetime
import pandas as pd

st.set_page_config(layout = 'centered', page_title='Betty Spa Booking', page_icon='🧖‍♀️')

# Path to SQLite database
db_path = 'data/bookings.db'

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Insert booking into the database
def insert_booking(name, numberofpeople, phone, time, service):
    cur.execute("INSERT INTO bookings (name, numberofpeople, phone, time, service) VALUES (?, ?, ?, ?, ?)",
                (name, numberofpeople, phone, time, service))
    conn.commit()

# Check if a time overlaps with any existing bookings by less than 1 hour
def check_time_availability(new_time):
    cur.execute("SELECT time FROM bookings")
    existing_times = cur.fetchall()
    
    try:
        new_time_obj = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M")
    except ValueError:
        new_time_obj = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")

    for existing_time in existing_times:
        existing_time = existing_time[0]
        try:
            existing_time_obj = datetime.datetime.strptime(existing_time, "%Y-%m-%d %H:%M")
        except ValueError:
            existing_time_obj = datetime.datetime.strptime(existing_time, "%Y-%m-%d %H:%M:%S")
        
        time_difference = abs(existing_time_obj - new_time_obj)
        
        if time_difference < datetime.timedelta(hours=1):
            return False
    return True

# Streamlit UI
def display_bookings():
    st.title("Betty Spa")
    st.subheader("Hệ thống đặt lịch")
    st.text("Làm bởi Vĩ đẹp trai trong 1 tiếng nên chưa xài được, thông cảm")
    
    # Client name input
    client_name = st.text_input("Nhập tên của bạn")
    
    # Phone number input
    phone = st.text_input("Số điện thoại")
    
    # Create columns for date, time, number of people, and service
    col1, col2 = st.columns(2)
    
    with col1:
        # Date picker
        date = st.date_input("Chọn ngày", min_value=datetime.date.today())
    
    with col2:
        # Time picker
        time = st.time_input("Chọn giờ", datetime.time(9, 0))
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Number of people input
        people = st.number_input("Số người", min_value=1, max_value=10, value=1)
    
    with col4:
        # Service selection (optional)
        service = st.selectbox("Dịch vụ", ["Gội đầu", "Lấy mụn", "Lăn kim", "Ủ mặt"])

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
