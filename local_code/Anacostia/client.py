import sys
import anyio
import dagger
import socket
import functools


class AnacostiaComponent:

    def __init__(self, host_ip: str = None, export_image: bool = False) -> None:
        if host_ip == None:
            hostname = socket.gethostname()
            self.host_ip = socket.gethostbyname(hostname)
        else:
            self.host_ip = host_ip

        self.export_image = export_image
        
    def is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.host_ip, port))
                return False
            except socket.error:
                raise Exception(f"Port {port} is already in use, please assign a different port for this pipeline component.")

    async def create_container(self):
        raise NotImplementedError("Subclasses must implement abstract_method")


class AnacostiaExecutor(AnacostiaComponent):
    
    def __init__(
        self, 
        inbound_port: int, 
        outbound_port: int,
        client: dagger.Client,
        host_ip: str = None, 
        export_image: bool = False, 
        tag: str = "latest"
    ) -> None:

        self.client = client
        self.image_link = f"mdo6180/anacostia-executor:{tag}"
        super().__init__(host_ip, export_image)
        
        if self.is_port_in_use(inbound_port) == False:
            self.inbound_port = inbound_port
        
        if self.is_port_in_use(outbound_port) == False:
            self.outbound_port = outbound_port

    async def create_container(self):
        executor_container = await (
            self.client.container()
            .from_(self.image_link)
            .with_directory("/tmp", self.client.host().directory("/tmp"))  
        )


        """
        executor_service_container = await (
            self.client.container()
            .from_("python:3.9-slim")
            .with_service_binding("anacostia-executor", executor_container)
        )
        """

        await executor_container.stdout()
        hostname = await executor_container.endpoint(scheme="http")
        print(hostname)

        #http_endpoint = await executor_container.endpoint(scheme="http")
        #print(http_endpoint)

        # log output of container to terminal
        """
        await executor_container.stdout()

        if self.export_image == True:
            # export container image (pulled from Docker Hub and built by Dagger) to local Docker Engine 
            # https://docs.dagger.io/252029/load-images-local-docker-engine
            image = await executor_container.export("/tmp/anacostia-executor.tar")
            print(f"Exported image: {image}")
        """


def anacostia_pipeline(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        async def run_async_func():
            print("Building your MLOps pipeline...")
            result = await func(*args, **kwargs)
            print("Done building MLOps pipeline.")
            return result

        return anyio.run(run_async_func)

    return wrapper


@anacostia_pipeline
async def pipeline():
    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:
        component = await AnacostiaExecutor(inbound_port=8000, outbound_port=12345, client=client).create_container() 

    # see this tutorial for container-to-container networking with Dagger
    # https://docs.dagger.io/757394/use-service-containers

if __name__ == "__main__":
    pipeline()