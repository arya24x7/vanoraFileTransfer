import streamlit as st
import paramiko
from scp import SCPClient
import os
import subprocess

def send_file_and_run_command(local_path, remote_path, hostname, username, password, command):
    try:
        # Set up SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        # Use SCP to send the file
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, remote_path)

        st.success("File sent successfully!")

        # Run the command on the remote system
        _, stdout, stderr = ssh.exec_command(command)

        # Display the command output in the Streamlit UI
        st.text("Command Output:")
        st.text(stdout.read().decode('utf-8'))

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        ssh.close()

def main():
    st.title("Vanora file Transfer")

    # File selection
    uploaded_file = st.file_uploader("Choose a file", type=["ino"])

    if uploaded_file is not None:
        # Display file details
        st.write("Selected File:", uploaded_file.name)

        # Hostname, username, and password input
        hostname = "192.168.29.10"
        username = "vanora"
        password = "vanora"

        # Command to run on the remote system
        command = "python flash.py"

        # Send button
        if st.button("Send File and Run Command"):
            # Save the uploaded file locally
            local_path = os.path.join(".", uploaded_file.name)
            with open(local_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Rename file to vanora.ino
            # new_local_path = os.path.join(".", "vanora.ino")
            # os.rename(local_path, new_local_path)

            # Send the renamed file and run the command on the server
            # send_file_and_run_command(new_local_path, "~/vanora.ino", hostname, username, password, command)
            send_file_and_run_command(local_path, "~/vanora.ino", hostname, username, password, command)

            # Remove the local file after sending

if __name__ == "__main__":
    main()
