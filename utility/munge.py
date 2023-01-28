import pandas as pd
import json
from conversions import *

homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
labs = ["LB01", "LB04", "LB05", "LB06", "LB07", "LB08", "LB09", "LB10", "LB11"]
students = {}
assignment_info = {}

# Get information from each assignment
assignment_info["homeworks"], assignment_info["labs"] = get_assignment_info()

# Get student IDs
df = pd.read_csv("./raw_data/HW/HW03.csv")
df.drop(df.tail(1).index,inplace=True)
df = df.reset_index()
for i in range(len(df["ID number"])):
  students[str(int(df["ID number"][i]))] = None
  
# Set schema for students
for key, value in students.items():
  students[key] = {
    "homeworks": {},
    "labs": {},
    "final": None
  }

# Get homeworks
for homework in homeworks:
  df = pd.read_csv("./raw_data/HW/{}.csv".format(homework))
  df.drop(df.tail(1).index,inplace=True)
  df = df.reset_index()
  
  # Get individual homework
  for index, row in df.iterrows():
    id = str(int(row["ID number"]))
    students[id]["homeworks"][homework] = {}
    
    # Get time taken
    time = get_time_taken(str(row["Time taken"]))
    
    # Get start time
    start_time = get_datetime(row["Started on"], 0) if str(row["Started on"]) != "-" else 0
    
    # Get grade breakdowns
    grade_breakdown = []
    num_of_cols = len(df.columns)
    for i in range(10, num_of_cols):
      if row[i] == '-':
        grade_breakdown.append(0)
      else:
        grade_breakdown.append(float(row[i]))
    
    students[id]["homeworks"][homework] = {}
    students[id]["homeworks"][homework]['Time taken'] = time
    students[id]["homeworks"][homework]['Start time'] = start_time
    students[id]["homeworks"][homework]['Grade breakdown'] = grade_breakdown
    students[id]["homeworks"][homework]['Total'] = sum(grade_breakdown)
    
# Get labs
for lab in labs:
  df = pd.read_csv("./raw_data/LB/{}.csv".format(lab))
  df.drop(df.tail(1).index,inplace=True)
  df = df.reset_index()

  # Get individual labs
  for index, row in df.iterrows():
    id = str(int(row["ID number"]))
    students[id]["labs"][lab] = {}
    
    # Get time taken
    time = get_time_taken(str(row["Time taken"]))
    
    # Get start time
    start_time = get_datetime(row["Started on"], 0) if str(row["Started on"]) != "-" else 0
    
    # Get grade breakdowns
    grade_breakdown = []
    num_of_cols = len(df.columns)
    for i in range(10, num_of_cols):
      if row[i] == '-':
        grade_breakdown.append(0)
      else:
        grade_breakdown.append(float(row[i]))
        
    students[id]["labs"][lab] = {}
    students[id]["labs"][lab]['Time taken'] = time
    students[id]["labs"][lab]['Start time'] = start_time
    students[id]["labs"][lab]['Grade breakdown'] = grade_breakdown
        
# Output clean data
student_info = json.dumps(students, indent=4, default=str)
assignment_info = json.dumps(assignment_info, indent=4, default=str)

with open("./clean_data/students.json", "w") as f:
  f.write(student_info)
with open("./clean_data/assignments.json", "w") as f:
  f.write(assignment_info)


