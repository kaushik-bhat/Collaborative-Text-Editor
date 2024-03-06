# client_side.py
import socket
import ssl
from gui import CollaborativeTextEditor
import threading
import tkinter as tk

def create_client_context():
    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile="client.crt", keyfile="client.key")
    context.load_verify_locations(cafile="server.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    return context

def main():
    context = create_client_context()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")

    try:
        secure_socket.connect(('localhost', 12345))
        print("Connected to the server.")
        
        # Launch the GUI
        app = CollaborativeTextEditor.get_instance(secure_socket)
        app.protocol("WM_DELETE_WINDOW", app.on_close)
        app.mainloop()
    except Exception as e:
        print(f"Error connecting to the server: {e}")
    finally:
        secure_socket.close()

if __name__ == "__main__":
    main()
