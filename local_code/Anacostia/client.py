import docker
import socket


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
        hostname = socket.gethostname()
        self.host_ip = socket.gethostbyname(hostname)

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
                f"HOST={self.host_ip}",
                f"IN_PORT={host_inbound_port}",
                f"OUT_PORT={host_outbound_port}"
            ],
            detach=True
        )


if __name__ == "__main__":
    executor = AnacostiaExecutor(host_inbound_port=8000, host_outbound_port=12345)
