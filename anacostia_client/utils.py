import socket
import subprocess
import time


def find_available_port():
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))     # Bind to a random port on localhost
    _, port = sock.getsockname()    # Get the assigned port
    sock.close()                    # Close the socket
    return port


def establish_connection() -> str:

    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    start_time = time.time()
    elapsed_time = 0
    ip_address = None

    while ip_address is None:

        ip_address = get_ip_address()

        time.sleep(0.5)
        elapsed_time = int(time.time() - start_time)
        formatted_time = format_time(elapsed_time)
        print(f"\rTrying to establish connection {formatted_time}", end="", flush=True)
    
    print(f"\nEstablished connection to host IP: {ip_address}")
    return ip_address


def get_ip_address():
    # note that on linux, ifconfig is deprecated and ip addr is the new command
    command = "ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}'"

    try:
        output = subprocess.check_output(command, shell=True)
        ip_address = output.decode('utf-8').strip()

        if ip_address == "":
            return None
        else:
            return ip_address

    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
        return None


def is_port_available(port):
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to bind to the port
        sock.bind(('localhost', port))

        # Port is available
        return True

    except socket.error as e:
        # Port is not available
        return False

    finally:
        # Close the socket
        sock.close()