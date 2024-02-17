# utils.py

import socket

def check_internet_connection():
    try:
    
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        return True
    except OSError:
        return False
