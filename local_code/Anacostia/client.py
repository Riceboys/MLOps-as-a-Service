import sys
import anyio
import dagger
import socket


class AnacostiaComponent:

    def __init__(self, port: int, host_ip: str = None, export_image: bool = False) -> None:
        if host_ip == None:
            hostname = socket.gethostname()
            self.host_ip = socket.gethostbyname(hostname)
        else:
            self.host_ip = host_ip

        if self.is_port_in_use(port) == False:
            self.port = port
        
        self.export_image = export_image
        
        self.container = anyio.run(self.create_container)
    
    def is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.host_ip, port))
                return False
            except socket.error:
                raise Exception(f"Port {port} is already in use, please assign a different port for this pipeline component.")

    async def create_container(self) -> dagger.Container:
        raise NotImplementedError("Subclasses must implement abstract_method")


class AnacostiaExecutor(AnacostiaComponent):
    
    def __init__(self, port: int, host_ip: str = None, export_image: bool = False, tag: str = "latest") -> None:
        self.image_link = f"mdo6180/anacostia-executor:{tag}"
        super().__init__(port, host_ip, export_image)

    async def create_container(self) -> dagger.Container:
        config = dagger.Config(log_output=sys.stdout)

        # initialize Dagger client
        async with dagger.Connection(config) as client: 
            executor_container = (
                client.container()
                .from_(self.image_link)
                .with_exposed_port(self.port)
                .with_env_variable("HOST", self.host_ip)
                .with_env_variable("PORT", f"{self.port}")
            )
        
            # log output of container to terminal
            await executor_container.stdout()
            
            if self.export_image == True:
                # export container image (pulled from Docker Hub and built by Dagger) to local Docker Engine 
                # https://docs.dagger.io/252029/load-images-local-docker-engine
                image = await executor_container.export("/tmp/anacostia-executor.tar")
                print(f"Exported image: {image}")

            return executor_container


if __name__ == "__main__":
    component = AnacostiaExecutor(port=12345, export_image=True)
