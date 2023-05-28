import sys
import anyio
import dagger
from dotenv import load_dotenv
import os


async def main():

    load_dotenv("./.env")
    DOCKER_HUB_USERNAME = os.getenv("DOCKER-HUB-USERNAME")
    DOCKER_HUB_PASSWORD = os.getenv("DOCKER-HUB-PASSWORD")

    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:

        # set secret as string value
        #secret = client.set_secret("password", DOCKER_HUB_PASSWORD)

        executor_container = (
            client.container()
            .from_(f"{DOCKER_HUB_USERNAME}/anacostia-executor:latest")
            .with_exposed_port(12345)
        )

        version = await executor_container.stdout()


if __name__ == "__main__":
    anyio.run(main)