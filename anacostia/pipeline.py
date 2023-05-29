import sys
import anyio
import dagger
from dagger.api.gen import BuildArg
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
        secret = client.set_secret("password", DOCKER_HUB_PASSWORD)

        # set build context
        context_dir = client.host().directory("./mlflow")

        # build using Dockerfile in ./mlflow directory
        image_ref = await context_dir.docker_build()
        
        mlflow_container_name = await (
            image_ref
            .with_registry_auth("docker.io", DOCKER_HUB_USERNAME, secret)
            .publish(f"{DOCKER_HUB_USERNAME}/anacostia:latest")
        )

        mlflow_container = (
            client.container()
            .from_(f"{DOCKER_HUB_USERNAME}/anacostia:latest")
            .with_exec(["mlflow", "--version"])
        )

        version = await mlflow_container.stdout()

        # print output
        print(f"Hello from Dagger and mlflow version {version}")


if __name__ == "__main__":
    anyio.run(main)