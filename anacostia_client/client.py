import docker
import socket
import time
import subprocess


class AnacostiaComponent:
    def __init__(self) -> None:
        pass
        
    def find_available_port(self):
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))  # Bind to a random port on localhost

        # Get the assigned port
        _, port = sock.getsockname()

        # Close the socket
        sock.close()

        return port
    
    def establish_connection(self) -> str:

        def format_time(seconds):
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
    
        start_time = time.time()
        elapsed_time = 0
        ip_address = None

        while ip_address is None:

            ip_address = self.get_ip_address()

            time.sleep(0.5)
            elapsed_time = int(time.time() - start_time)
            formatted_time = format_time(elapsed_time)
            print(f"\rTrying to establish connection {formatted_time}", end="", flush=True)
        
        print(f"\nEstablished connection to host IP: {ip_address}")
        return ip_address

    def get_ip_address(self):
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

    def is_port_available(self, port):
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


class AnacostiaExecutor(AnacostiaComponent):
    def __init__(self, host_inbound_port=None, host_outbound_port=None) -> None:
        host_ip = self.establish_connection()

        if host_inbound_port is not None:
            if self.is_port_available(host_inbound_port) is True:
                self.host_inbound_port = host_inbound_port
            else:
                raise Exception(f"Port {host_inbound_port} is not available, please select another port.")
        else:
            self.host_inbound_port = self.find_available_port()
        
        if host_outbound_port is not None:
            self.host_outbound_port = host_outbound_port
        else:
            self.host_outbound_port = self.find_available_port()

        self.image_name = "mdo6180/anacostia-executor"
        
        client = docker.from_env()

        # needs to pull images in the __init__() method
        try:
            client.images.get(self.image_name)

        except docker.errors.ImageNotFound:
            print(f"Pulling image {self.image_name} from Docker Hub.")
            client.images.pull(self.image_name)
            print(f"Done pulling image {self.image_name} from Docker Hub.")
        
        # needs to be ran in detach mode
        client.containers.run(
            image=self.image_name,
            ports={
                "8000":self.host_inbound_port,
                "12345":self.host_outbound_port
            },
            environment=[
                f"HOST={host_ip}",
                f"IN_PORT={host_inbound_port}",
                f"OUT_PORT={host_outbound_port}"
            ],
            detach=True
        )
        

if __name__ == "__main__":
    executor = AnacostiaExecutor(host_inbound_port=8000, host_outbound_port=12345)
