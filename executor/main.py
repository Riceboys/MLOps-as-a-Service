import yaml
from config import get_tools


if __name__ == "__main__":

    # in the future, also handle cases for *.yml or *.yaml
    with open("/host_dir/mlops.yaml", "r") as yaml_file:
        yaml_text = yaml_file.read()
        yaml_data = yaml.safe_load(yaml_text)

        tools = get_tools(yaml_data=yaml_data)