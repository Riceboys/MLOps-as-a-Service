import sys
import anyio
import dagger
from dagger.api.gen import BuildArg


async def main():
    config = dagger.Config(log_output=sys.stdout)

    # initialize Dagger client
    async with dagger.Connection(config) as client:
        # set build context
        context_dir = client.host().directory("./mlflow")

        """
        # build using Dockerfile in ./mlflow directory
        image_ref = (
            await context_dir.docker_build()
            .publish("docker.io/anacostia/mlflow:0.1.0")
        )
        """

        mlflow_container = (
            client.container()
            .from_("docker.io/mlflow-image:latest")
            .with_exec(["python", "-V"])
        )

        version = await mlflow_container.stdout()

        # print output
        print(f"Hello from Dagger and mlflow version {version}")

        """
        # use a python:3.11-slim container
        # get version
        python = (
            client.container()
            .from_("python:3.11-slim")
            .with_exec(["python", "-V"])
        )

        # execute
        version = await python.stdout()

    # print output
    print(f"Hello from Dagger and {version}")
        """

if __name__ == "__main__":
    anyio.run(main)