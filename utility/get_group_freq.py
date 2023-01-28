import json

def get_group_freq():
  processed_groups = {}
  all_groups = set()
  group_count = {}
  group_freq_dict = {x:{"Groups":[], "Total":0} for x in range(1, 11)}

  json_groups = {}
  with open("./clean_data/groups.json", "r") as f:
    json_groups = json.load(f)

  # Get correct datatype for processed_groups
  for homework, groups in json_groups.items():
    set_groups = []
    for group in groups:
      set_groups.append(frozenset(eval(group)))
    processed_groups[homework] = set_groups

  # Store all distinct groups found
  for homework, groups in processed_groups.items():
    for group in groups:
      all_groups.add(frozenset(group))

  # Count how many times each group shows up in all homeworks
  homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
  for homework in homeworks:
    for group in processed_groups[homework]:
      group_count.setdefault(group, 0)
      group_count[group] += 1

  # Lists groups based on frequency
  for group, freq in group_count.items():
    group_freq_dict[freq]["Groups"].append(group)
  for key in group_freq_dict.keys():
    group_freq_dict[key]["Total"] = len(group_freq_dict[key]["Groups"])
    # print("{}: {}".format(key, len(group_freq_dict[key]["Groups"])))

  # print(len(all_groups))
  # print(len(group_freq_dict[1]["Groups"]))

  # # Remove groups that only appear once from all groups
  # for group in group_freq_dict[1]["Groups"]:
  #   all_groups.remove(group)
    
  # print(len(all_groups))

  
  return group_freq_dict
    
