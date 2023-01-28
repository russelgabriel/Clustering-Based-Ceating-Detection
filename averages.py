import pandas as pd
import plotly.express as px
import json
from utility.create_df import create_df
import numpy
from utility.find_cheaters import *
  
# print(json.dumps(groups, indent=4, default=str))
# print(json.dumps(student_info, indent=4, default=str))

def get_average(hw):
  df = create_df(hw)

  group_scores = []
  non_group_scores = []
  cheater_scores = []
  all_scores = []

  for index, row in df.iterrows():
    total_score = sum(row["Breakdown"])
    if row["Grouped"] == "green":
      group_scores.append(total_score)
    elif row["Grouped"] == "red":
      cheater_scores.append(total_score)
    else:
      non_group_scores.append(total_score)
    all_scores.append(total_score)
    
  class_average = round((numpy.mean(all_scores)/20)*100, 2)
  groups_average = round((numpy.mean(group_scores)/20)*100, 2)
  non_group_average = round((numpy.mean(non_group_scores)/20)*100, 2)
  cheater_average = round((numpy.mean(cheater_scores)/20)*100, 2)

  # print("Group average: {0:.2f}".format((numpy.mean(group_scores)/20)*100))
  # print("Non-group average: {0:.2f}".format((numpy.mean(non_group_scores)/20)*100))
  # print("Class average: {0:.2f}".format((numpy.mean(all_scores)/20)*100))
  
  return (class_average, groups_average, non_group_average, cheater_average)

def final_exam_averages():
  homeworks = ["HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
  df = create_df("HW01")
  for homework in homeworks:
    df = pd.concat([df, create_df(homework)])
  cheaters = find_all_cheaters(df)
  
  df = create_df("HW03")
  group_scores = []
  non_group_scores = []
  cheater_scores = []
  all_scores = []
  
  for index, row in df.iterrows():
    score = row["Final"]
    if row["Grouped"] == "green":
      group_scores.append(score)
    elif row["ID"] in cheaters:
      cheater_scores.append(score)
    else:
      non_group_scores.append(score)
    all_scores.append(score)
    
  class_average = round((numpy.mean(all_scores)/20)*100, 2)
  groups_average = round((numpy.mean(group_scores)/20)*100, 2)
  non_group_average = round((numpy.mean(non_group_scores)/20)*100, 2)
  cheater_average = round((numpy.mean(cheater_scores)/20)*100, 2)
  
  return (class_average, groups_average, non_group_average, cheater_average)
    

homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
averages = {}

for homework in homeworks:
  hw_avgs = get_average(homework)
  averages.setdefault(homework, {
    "Class": None,
    "Group": None,
    "Non Group": None,
    "Cheaters": None

    })
  averages[homework]["Class"] = hw_avgs[0]
  averages[homework]["Group"] = hw_avgs[1]
  averages[homework]["Non Group"] = hw_avgs[2]
  averages[homework]["Cheaters"] = hw_avgs[3]

# print(json.dumps(averages, indent=4, default=str))
df = pd.DataFrame.from_dict(averages)
df = df.transpose()
df.loc["Averages"] = df.mean()

print(df)
print(final_exam_averages())


