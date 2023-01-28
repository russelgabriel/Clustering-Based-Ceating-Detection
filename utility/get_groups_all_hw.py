import os
from find_groups import find_groups
import json

homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
groups_dict = {}
for homework in homeworks:
  groups = find_groups(homework, 0.7, 10.0, 10.0)
  groups_dict.setdefault(homework, groups)

groups = json.dumps(groups_dict, indent=4, default=str)

with open("./clean_data/groups.json", "w") as f:
  f.write(groups)
  
  