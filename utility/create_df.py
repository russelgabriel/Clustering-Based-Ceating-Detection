from datetime import datetime as dt
from datetime import timedelta
import json
import pandas as pd
from utility.get_group_freq import get_group_freq
import numpy

def group_check():
  group_freq = get_group_freq()
  grouped_students = set()
  for i in range(2,11):
    for allowed in group_freq[i]["Groups"]:
      for person in allowed:
        grouped_students.add(person)
  return grouped_students

def average_duration(student_info, hw_num):
  all_times = []
  for id, info in student_info.items():
    time_taken = info["homeworks"][hw_num]["Time taken"]
    if time_taken > 0:
      all_times.append(time_taken)
  return sum(all_times) / len(all_times)

def get_class_average(student_info, hw):
  all_grades = []
  for id, info in student_info.items():
    grade = info["homeworks"][hw]["Total"]
    if grade > 0:
      all_grades.append(grade)
  
  return sum(all_grades) / len(all_grades)
  

def create_df(hw):
  group_freq = get_group_freq()
  student_info = {}
  group_info = {}
  student_ids = []
  start_times = []
  end_times = []
  totals = []
  breakdowns = []
  type = []
  hw_num = []
  final_exam = []


  with open("./clean_data/students.json") as f:
    student_info = json.load(f)
  with open("./clean_data/assignments.json") as f:
    assignment_info = json.load(f)
  with open("./clean_data/groups.json") as f:
    group_info = json.load(f)
    
  average_time = average_duration(student_info, hw)
  average_grade = get_class_average(student_info, hw)
  # print("{}        {}        {}".format(hw, round(average_time, 2), round(average_grade, 2)))

  for key, value in student_info.items():
    marked_flag = False
    group_flag = False
    cheater_flag = False
    time_taken = value["homeworks"][hw]["Time taken"]
    total = sum(value["homeworks"][hw]["Grade breakdown"])
    if time_taken == 0:
      continue
    student_ids.append(key)
    format = "%Y-%m-%d %H:%M:%S"
    start_time = dt.strptime(value["homeworks"][hw]["Start time"], format)
    start_times.append(start_time)
    end_time = start_time + timedelta(minutes=time_taken)
    end_times.append(end_time)
    totals.append(total)
    breakdowns.append(value["homeworks"][hw]["Grade breakdown"])
    

    
    if (time_taken < 0.25 * average_time) and (total > average_grade):
      cheater_flag = True
      
    # Check if student is in a group that has worked together
    # for more than one homework
    valid_grouped_students = group_check()

    for group in group_info[hw]:

      # Check if student is in a group for more than one homework
      # Only allow students if they are a part of a group that
      # appears more than once
      # change to group if we want to include groups that
      # only appear once, otherwise use valid_grouped_students
      if key in group:
        group_flag = True
      if key in group and valid_grouped_students:
        type.append("green")
        marked_flag = True
        cheater_flag = False
        break
        
    if not marked_flag and not cheater_flag:
      type.append("blue")
    elif not marked_flag and cheater_flag:
      type.append("red")
      
    hw_num.append(hw)
    
    if value["final"] == None:
      final_exam.append(0)
    else:
      final_exam.append(value["final"])

  dict = {"ID": student_ids, "Start times": start_times, "End times": end_times, "Total": totals, "Breakdown": breakdowns, "Grouped": type, "Homework type": hw_num, "Final": final_exam}
  df = pd.DataFrame(dict)
  df = df.sort_values(by="Start times")

  return df
