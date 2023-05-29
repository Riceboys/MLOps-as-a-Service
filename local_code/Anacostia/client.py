import sys
import anyio
import dagger
import os
import socket


async def main():

    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:

        # set secret as string value
        # secret = client.set_secret("password", DOCKER_HUB_PASSWORD)

        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        port = 12345

        executor_container = (
            client.container()
            .from_("mdo6180/anacostia-executor:latest")
            .with_exposed_port(port)
            .with_env_variable("HOST", host_ip)
            .with_env_variable("PORT", f"{port}")
        )

        # log output of container to terminal
        await executor_container.stdout()

        # export container image (pulled from Docker Hub and built by Dagger) to local Docker Engine 
        # https://docs.dagger.io/252029/load-images-local-docker-engine
        image = await executor_container.export("/tmp/anacostia-executor.tar")
        print(f"Exported image: {image}")


if __name__ == "__main__":
    anyio.run(main)
