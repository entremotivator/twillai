import streamlit as st
from twilio.rest import Client
from datetime import datetime, timedelta

# Twilio credentials
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Database to store client information
client_database = []

# Streamlit app
def main():
    st.title("Twilio Automation App")

    # Create tabs
    tabs = ["Text Message Automation", "Client Calling", "Client Info"]
    choice = st.sidebar.selectbox("Select Tab", tabs)

    if choice == "Text Message Automation":
        text_message_automation()

    elif choice == "Client Calling":
        client_calling()

    elif choice == "Client Info":
        client_info()

# Text Message Automation tab
def text_message_automation():
    st.subheader("Text Message Automation")

    # Get user input
    phone_number = st.text_input("Enter client's phone number:")
    message_content = st.text_area("Enter message content:")

    # Schedule message
    scheduled_time = st.text_input("Schedule message (YYYY-MM-DD HH:MM):")
    if scheduled_time:
        scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")

    # Send message button
    if st.button("Send Message"):
        send_text_message(phone_number, message_content, scheduled_time)

# Function to send text message using Twilio
def send_text_message(phone_number, message_content, scheduled_time=None):
    try:
        if scheduled_time and scheduled_time > datetime.now():
            twilio_client.messages.create(
                to=phone_number,
                from_=TWILIO_PHONE_NUMBER,
                body=message_content,
                date_sent=scheduled_time
            )
            st.success(f"Message scheduled for {scheduled_time} successfully!")
        else:
            twilio_client.messages.create(
                to=phone_number,
                from_=TWILIO_PHONE_NUMBER,
                body=message_content
            )
            st.success("Message sent successfully!")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Client Calling tab
def client_calling():
    st.subheader("Client Calling")

    # Get client to call
    client_to_call = st.selectbox("Select client to call:", [client['name'] for client in client_database])

    # Display client notes
    client_notes = get_client_notes(client_to_call)
    st.write(f"### Notes for {client_to_call}:")
    st.text_area("Add new note:", key=f"{client_to_call}_note")
    st.text_area("Client Notes:", value=client_notes, key=f"{client_to_call}_notes", height=150)

    # Call timer
    timer_running = st.checkbox("Start Call Timer")
    if timer_running:
        call_timer(client_to_call)

# Function to get client notes
def get_client_notes(client_name):
    for client in client_database:
        if client['name'] == client_name:
            return client.get('notes', '')

# Function to update client notes
def update_client_notes(client_name, new_note):
    for client in client_database:
        if client['name'] == client_name:
            if 'notes' in client:
                client['notes'] += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')}: {new_note}"
            else:
                client['notes'] = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {new_note}"

# Function to handle call timer
def call_timer(client_name):
    start_time = datetime.now()
    elapsed_time = datetime.now() - start_time

    while st.checkbox("Stop Call Timer"):
        elapsed_time = datetime.now() - start_time
        st.write(f"Call Duration: {elapsed_time}")
        st.sleep(1)

    # Update client notes with call duration
    update_client_notes(client_name, f"Call duration: {elapsed_time}")

# Client Info tab
def client_info():
    st.subheader("Client Info")

    # Display client information
    if client_database:
        st.write("### Client List:")
        for i, client in enumerate(client_database, 1):
            st.write(f"{i}. Name: {client['name']}, Phone: {client['phone']}")
    else:
        st.info("No clients in the database.")

    # Add new client
    st.header("Add New Client")
    new_name = st.text_input("Enter client's name:")
    new_phone = st.text_input("Enter client's phone number:")

    if st.button("Add Client"):
        add_client(new_name, new_phone)

# Function to add a new client to the database
def add_client(name, phone):
    client_database.append({'name': name, 'phone': phone})
    st.success(f"Client {name} added successfully!")

# Run the app
if __name__ == "__main__":
    main()
