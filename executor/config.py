import yaml
from typing import List

def get_tools(yaml_data) -> List[str]:
    tools = []

    for stages, _ in yaml_data["pipeline"]["stages"]:
        for tool, _ in stages["tools"]:
            tools.append(tool)
    
    print(tools)
    return tools