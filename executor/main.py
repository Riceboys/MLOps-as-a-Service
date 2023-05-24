import yaml
from config import MLOpsYAML


if __name__ == "__main__":

    mlops_yaml_obj = MLOpsYAML()
    print(mlops_yaml_obj.get_tools())