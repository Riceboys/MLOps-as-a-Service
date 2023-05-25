from typing import List
import os
import yaml


class MLOpsYAML:

    def __init__(self, path="/host_dir", filename="mlops.yaml") -> None:
        self.stage_tags = ["load", "train", "validate", "test", "deploy", "monitor"]
        self.supported_tools = ["mlflow", "seldon core", "ama", "weave"]

        with open(os.path.join(path, filename), "r") as yaml_file:
            yaml_text = yaml_file.read()
            self.yaml_data = yaml.safe_load(yaml_text)
        
        self.__file_checker()
        self.__stage_checker()

    def __file_checker(self) -> None:
        check = 0
        try:
            self.yaml_data["version"]
            check += 1

            self.yaml_data["pipeline"]
            check += 1

            self.yaml_data["pipeline"]["stages"] 
            check += 1
        except:
            if check == 0:
                raise Exception("Need to specify 'version' tag in mlops.yaml")
            elif check == 1:
                raise Exception("Need to have 'pipeline' tag at the beginning of the mlops.yaml file.")
            elif check == 2:
                raise Exception("Need to have 'stages' tag under pipeline.")
        else:
            if self.yaml_data["pipeline"]["stages"] == None:
                raise Exception("Need to define at least one stage in your pipeline.")
            
    def __stage_checker(self):
        for stage in self.yaml_data["pipeline"]["stages"]:
            for stage_name in stage:
                if stage_name not in self.stage_tags:
                    raise Exception(f"'{stage_name}' is not a valid tag for a stage.")

    def get_tools(self) -> List[str]:
        tools = []

        for stage in self.yaml_data["pipeline"]["stages"]:
            for stage_info in stage.values():
                for tool in stage_info["tools"]:
                    for tool_name, tool_info in tool.items():
                        
                        required_var = []
                        for info, value in tool_info.items():
                            if (info == "environment") and (value not in ["local", "executor"]):
                                raise Exception(f"value of 'environment' tag under '{tool_name}' must be either 'local' or 'executor', not {value}")
                            required_var.append(info)
                        
                        if tool_name not in self.supported_tools:
                            raise Exception(f"'{tool_name}' is not a supported tool right now.")
                        
                        elif ("environment" not in required_var):
                            raise Exception("every tool must be provided with 'environment' tag")
                        
                        elif ("version" not in required_var):
                            raise Exception("every tool must be provided with 'version' tag")
                        
                        else:
                            if tool_name not in tools:
                                tools.append(tool_name)
        return tools