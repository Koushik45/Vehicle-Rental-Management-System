import streamlit as st
import mysql.connector
from mysql.connector import Error

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Function to create a database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='root',
            password=''
        )
        if connection.is_connected():
            #print("Connection established")
            return connection
        else:
            st.error("Connection failed.")
    except Error as e:
        st.error(f"Error: {e}")
    return connection


# Function to fetch user data
def fetch_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users_data = cursor.fetchall()
    return users_data

# Function to fetch vehicle data
def fetch_vehicles(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Vehicles")
    vehicles_data = cursor.fetchall()
    return vehicles_data

# Function to create a new user
def create_user(connection, first_name, last_name, email, phone_number, username, password):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (FirstName, LastName, Email, PhoneNumber, Username, Password) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, email, phone_number, username, password))
        connection.commit()
        st.success("User created successfully.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to create a new vehicle
def create_vehicle(connection, vehicle_type, brand, model, price):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Vehicles (VehicleType, Brand, Model, Price) VALUES (%s, %s, %s, %s)",
                       (vehicle_type, brand, model, price))
        connection.commit()
        st.success("Vehicle created successfully.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to update an existing user
def update_user(connection, user_id, first_name, last_name, email, phone_number, username, password):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Users SET FirstName=%s, LastName=%s, Email=%s, PhoneNumber=%s, Username=%s, Password=%s WHERE UserID=%s",
                       (first_name, last_name, email, phone_number, username, password, user_id))
        connection.commit()
        st.success("User updated successfully.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to update an existing vehicle
def update_vehicle(connection, vehicle_id, vehicle_type, brand, model, price):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Vehicles SET VehicleType=%s, Brand=%s, Model=%s, Price=%s WHERE VehicleID=%s",
                       (vehicle_type, brand, model, price, vehicle_id))
        connection.commit()
        st.success("Vehicle updated successfully.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete an existing user
def delete_user(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Users WHERE UserID=%s", (user_id,))
        connection.commit()
        st.success("User deleted successfully.")
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete an existing vehicle
def delete_vehicle(connection, vehicle_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Vehicles WHERE VehicleID=%s", (vehicle_id,))
        connection.commit()
        st.success("Vehicle deleted successfully.")
    except Error as e:
        st.error(f"Error: {e}")
     
     
        
def fetch_reservations(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            Reservations.ResID,
            Users.FirstName AS UserName,
            Vehicles.Brand AS VehicleBrand,
            Vehicles.Model AS VehicleModel,
            Reservations.StartDate,
            Reservations.EndDate
        FROM
            Reservations
        JOIN Users ON Reservations.UserID = Users.UserID
        JOIN Vehicles ON Reservations.VehicleID = Vehicles.VehicleID            
    """)
    reservations_data = cursor.fetchall()                                                                                 # JOIN 
    return reservations_data

# Function to update an existing reservation
def update_reservation(connection, res_id, start_date, end_date):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Reservations SET StartDate=%s, EndDate=%s WHERE ResID=%s",
                       (start_date, end_date, res_id))
        connection.commit()
        st.success("Reservation updated successfully.")
    except Error as e:
        st.error(f"Error: {e}")
# Administrator Interface

# Function to fetch reservation data with column headers
def fetch_reservations_with_headers(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Reservations")
    reservations_data = cursor.fetchall()
    headers = [i[0] for i in cursor.description]  # Get column headers
    return headers, reservations_data


def admin_interface():
    st.title("Vehicle Rental System - Administrator Interface")

    # Sidebar menu for selecting CRUD operation
    operation = st.sidebar.radio("Select Operation", ["Read Users", "Read Vehicles", "Create User", "Create Vehicle", "Update User", "Update Vehicle", "Delete User", "Delete Vehicle", "Read Reservations", "Update Reservation", "Cancel Reservation"])

    connection = create_connection()
    
    if operation == "Cancel Reservation":
        st.header("Cancel Reservation")
        res_id_to_cancel = st.number_input("Reservation ID to Cancel", step=1)

        if st.button("Cancel"):
            cancel_reservation(connection, res_id_to_cancel)

    if operation.startswith("Read"):
        # Read Users or Vehicles
        if operation == "Read Users":
            st.header("User Information")
            users_data = fetch_users(connection)
            st.table(users_data)
        elif operation == "Read Vehicles":
            st.header("Vehicle Information")
            vehicles_data = fetch_vehicles(connection)
            st.table(vehicles_data)
        elif operation == "Read Reservations":
            st.header("Reservation Information")
            reservations_data = fetch_reservations(connection)
            st.table(reservations_data)

    elif operation.startswith("Create"):
        # Create User or Vehicle
        if operation == "Create User":
            st.header("Create User")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            #username = st.text_input("Username")
            username = st.text_input("Username", key="unique_key_for_username_input")
            password = st.text_input("Password", type="password", key="create_user_password")
            if st.button("Create"):
                create_user(connection, first_name, last_name, email, phone_number, username, password)

        elif operation == "Create Vehicle":
            st.header("Create Vehicle")
            vehicle_type = st.text_input("Vehicle Type")
            brand = st.text_input("Brand")
            model = st.text_input("Model")
            price = st.number_input("Price", step=1.0)
            if st.button("Create"):
                create_vehicle(connection, vehicle_type, brand, model, price)

    elif operation.startswith("Update"):
        # Update User or Vehicle
        if operation == "Update User":
            st.header("Update User")
            user_id = st.number_input("User ID", step=1)
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            #username = st.text_input("Username")
            username = st.text_input("Username", key="unique_key_for_username_input_Update")
            password = st.text_input("Password", type="password", key="update_user_password")
            if st.button("Update"):
                update_user(connection, user_id, first_name, last_name, email, phone_number, username, password)

        elif operation == "Update Vehicle":
            st.header("Update Vehicle")
            vehicle_id = st.number_input("Vehicle ID", step=1)
            vehicle_type = st.text_input("Vehicle Type")
            brand = st.text_input("Brand")
            model = st.text_input("Model")
            price = st.number_input("Price", step=1.0)
            if st.button("Update"):
                update_vehicle(connection, vehicle_id, vehicle_type, brand, model, price)
        
        elif operation == "Update Reservation":
            st.header("Update Reservation")
            res_id = st.number_input("Reservation ID", step=1)
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            if st.button("Update"):
                update_reservation(connection, res_id, start_date, end_date)

    elif operation.startswith("Delete"):
        # Delete User or Vehicle
        if operation == "Delete User":
            st.header("Delete User")
            user_id = st.number_input("User ID", step=1)
            if st.button("Delete"):
                delete_user(connection, user_id)

        elif operation == "Delete Vehicle":
            st.header("Delete Vehicle")
            vehicle_id = st.number_input("Vehicle ID", step=1)
            if st.button("Delete"):
                delete_vehicle(connection, vehicle_id)
    
    # Close the database connection when the app is done
    if connection:
        connection.close()

def fetch_available_vehicles(connection, vehicle_type):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Vehicles WHERE VehicleType=%s AND Available = 1", (vehicle_type,))
    available_vehicles_data = cursor.fetchall()
    return available_vehicles_data



# Function to book a vehicle
def book_vehicle(connection, user_id, vehicle_id, start_date, end_date):
    try:
        # Check if the UserID exists in the Users table
        cursor = connection.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE UserID = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            # UserID exists, proceed with the reservation
            cursor.execute("UPDATE Vehicles SET Available = 0 WHERE VehicleID = %s", (vehicle_id,))
            cursor.execute("INSERT INTO Reservations (UserID, VehicleID, StartDate, EndDate) VALUES (%s, %s, %s, %s)",
                           (user_id, vehicle_id, start_date, end_date))
            connection.commit()
            st.success("Vehicle booked successfully.")
        else:
            st.error("UserID does not exist in the Users table.")

    except Error as e:
        st.error(f"Error: {e}")


# Function to fetch all unique vehicle types
def fetch_all_vehicle_types(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT VehicleType FROM Vehicles")
        vehicle_types = cursor.fetchall()
        return [type[0] for type in vehicle_types]
    except Error as e:
        st.error(f"Error: {e}")
        return []

def user_booking_interface():
    st.title("Vehicle Rental System - User Booking Interface")

    user_id = st.text_input("User ID", key="user_id")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    connection = create_connection()

    # Create a dropdown menu for selecting the vehicle type
    vehicle_type = st.selectbox("Select Vehicle Type", fetch_all_vehicle_types(connection))

    available_vehicles_data = fetch_available_vehicles(connection, vehicle_type)

    st.header("Available Vehicles")

    # Display column headers
    st.write("Brand | Model | Price")

    # Display available vehicles with brand, model, and price
    for vehicle in available_vehicles_data:
        try:
            price = float(vehicle[3].replace(',', ''))  # Remove commas from the price before conversion
            formatted_price = f"${price:,.2f}"
        except ValueError:
            formatted_price = vehicle[4]


    # Use st.selectbox to select a vehicle
    selected_vehicle_option = st.selectbox("Select a Vehicle", [f"{vehicle[2]} | {vehicle[3]} | {vehicle[4]}" for vehicle, formatted_price in zip(available_vehicles_data, [f"${float(vehicle[3].replace(',', '')):,.2f}" if vehicle[3].replace(',', '').replace('.', '').isdigit() else vehicle[3] for vehicle in available_vehicles_data])])

    # Find the selected vehicle ID
    selected_vehicle_id = None
    for vehicle in available_vehicles_data:
        try:
            price = float(vehicle[3].replace(',', ''))  # Remove commas from the price before conversion
            formatted_price = f"${price:,.2f}"
        except ValueError:
            formatted_price = vehicle[4]

        option = f"{vehicle[2]} | {vehicle[3]} | {formatted_price}"
        if selected_vehicle_option == option:
            selected_vehicle_id = vehicle[0]
            break

    if selected_vehicle_id is not None:
        if st.button("Book"):
            book_vehicle(connection, user_id, selected_vehicle_id, start_date, end_date)
    else:
        st.warning("Selected vehicle option not found. Please try again.")

    # Close the database connection when the app is done
    if connection:
        connection.close()


def fetch_user_reservations_with_total(connection):                                                     # NESTED QUERY
    cursor = connection.cursor()
    cursor.execute("""
        SELECT UserID, FirstName, LastName, (
            SELECT COUNT(*)
            FROM Reservations
            WHERE UserID = Users.UserID
        ) AS TotalReservations
        FROM Users
    """)
    user_reservations_data = cursor.fetchall()
    return user_reservations_data


# Function to cancel a reservation
def cancel_reservation(connection, res_id):
    try:
        cursor = connection.cursor()
        cursor.callproc("CancelReservation", (res_id,))                                                  # PROCEDURE
        connection.commit()
        st.success("Reservation canceled successfully.")
    except Error as e:
        st.error(f"Error: {e}")


def authenticate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE Username=%s AND Password=%s", (username, password))
    user_data = cursor.fetchone()
    connection.close()
    return user_data

def authenticate_admin(username, password):
    if username=="admin" and password=="admin@123":
        admin_data=("admin","admin_data")
    return admin_data


def register_user(first_name, last_name, email, phone_number, username, password, role='user'):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (FirstName, LastName, Email, PhoneNumber, Username, Password, Role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (first_name, last_name, email, phone_number, username, password, role))
    connection.commit()
    connection.close()
    

# Function to get the user session state
def get_user_session():
    if not hasattr(st.session_state, 'user_session'):
        st.session_state.user_session = SessionState(login_status=False, user_data=None)
    return st.session_state.user_session

def get_admin_session():
    if not hasattr(st.session_state, 'admin_session'):
        st.session_state.admin_session = SessionState(login_status=False, admin_data=None)
    return st.session_state.admin_session

# Function to set the user session state
def set_user_session(login_status, user_data=None):
    user_session = get_user_session()
    user_session.login_status = login_status
    user_session.user_data = user_data

def set_admin_session(login_status, admin_data=None):
    admin_session = get_admin_session()
    admin_session.login_status = login_status
    admin_session.admin_data = admin_data

# Function to check if the user is logged in
def is_user_logged_in():
    return get_user_session().login_status

def is_admin_logged_in():
    return get_admin_session().login_status

# Function to log out the user
def logout_user():
    set_user_session(login_status=False, user_data=None)

def logout_admin():
    set_admin_session(login_status=False, admin_data=None)

# ... (remaining code)


def login_page():
    st.title("Login")
    # username = st.text_input("Username")
    username = st.text_input("Username", key="unique_key_for_username_input_login")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_data = authenticate_user(username, password)
        #admin_data = ("admin","admin@123")
                
        if username=="admin" and password=="admin@123":
            set_admin_session(login_status=True,admin_data=("admin","admin@123"))
            st.success("Admin Login successful.")
            admin_interface()
        elif user_data:
            set_user_session(login_status=True,user_data=user_data)
            st.success("User Login successful.")
            user_booking_interface()
            
        

def registration_page():
    st.title("User Registration")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    #username = st.text_input("Username")
    username = st.text_input("Username", key="unique_key_for_username_input_register")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        register_user(first_name, last_name, email, phone_number, username, password)
        st.success("Registration successful. Please log in.")


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Login", "Registration"])

    if page == "Login":
        login_page()
    elif page == "Registration":
        registration_page()

    user_session = get_user_session()
    admin_session = get_admin_session()

    if user_session.login_status and not admin_session.login_status:
        user_booking_interface()
    elif admin_session.login_status and not user_session.login_status:
        admin_interface()
        
        


if __name__ == "__main__":
    main()


