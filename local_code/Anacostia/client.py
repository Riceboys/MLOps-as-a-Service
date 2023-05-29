import sys
import anyio
import dagger
# from dotenv import load_dotenv
import os


async def main():

    # load_dotenv("./.env")
    # DOCKER_HUB_USERNAME = os.getenv("DOCKER-HUB-USERNAME")
    # DOCKER_HUB_PASSWORD = os.getenv("DOCKER-HUB-PASSWORD")

    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:

        # set secret as string value
        #secret = client.set_secret("password", DOCKER_HUB_PASSWORD)

        executor_container = (
            client.container()
            .from_("mdo6180/anacostia-executor:latest")
            .with_exposed_port(12345)
            .with_env_variable("HOST", "192.168.0.172")
            .with_env_variable("PORT", "12345")
        )

        # log output of container to terminal
        await executor_container.stdout()

        # export container image (pulled from Docker Hub and built by Dagger) to local Docker Engine 
        # https://docs.dagger.io/252029/load-images-local-docker-engine
        image = await executor_container.export("/tmp/anacostia-executor.tar")
        print(f"Exported image: {image}")


if __name__ == "__main__":
    anyio.run(main)