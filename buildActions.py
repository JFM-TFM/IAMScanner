from iam_actions import actions
from json import dumps
from os import getenv
ACTIONS_FILE = getenv("ACTIONS_FILE", "actions.json")
sorted_actions = {}

# Iterate through all services and their actions
for service_name, service_actions in actions.items():
    sorted_actions[service_name] = {
        "Permissions management": [],
        "Sensitive": [],
        "Write": [],
        "Read": [],
        "List": [],
        "Tagging": []
    }
    for action_name, action_details in service_actions.items():
        access_level = action_details["access_level"]
        if access_level == "Undocumented":
            if "Tag" in action_name:
                access_level = "Tagging"
            elif action_name.startswith("List"):
                access_level = "List"
            elif action_name.startswith("Get") or action_name.startswith("Describe") or action_name.startswith("Lookup") or action_name.startswith("Read"):
                access_level = "Read"
            else:
                access_level = "Write"
        
        if "Token" in action_name or "Secret" in action_name or "Authorization" in action_name:
            access_level = "Sensitive"


        sorted_actions[service_name][access_level].append(action_name)


with open(ACTIONS_FILE, "w") as actions_file:
    actions_file.write(dumps(sorted_actions, indent=4))