from datetime import datetime as dt
from datetime import timedelta
import json
import math

"""
- Group by similarity of grade breakdown
- within those groups, group by start and end time
"""


def find_groups(hw="HW01", sim=0.7, start=20.0, end=10.0):
  student_info = {}

  SIMILARITY_CUTOFF = sim # Float percentage
  START_TIME_BUFFER = start # Float minutes
  END_TIME_BUFFER = end # Float minutes

  with open("./clean_data/students.json") as f:
    student_info = json.load(f)
    
  # Array of groups
  groups = []
  # Array of students already in a group (used to check if student alrady in group)
  grouped_students = []

  # Split students into groups of students with similar grade breakdowns
  for id, info in student_info.items():
    student_grade_breakdown = info['homeworks'][hw]["Grade breakdown"]
    student_id = id
    
    # Check if student has already been put into group
    if student_id not in grouped_students:
      group = set()
      group.add(student_id)
      
      # Compare our student with all other students in class
      for id, info in student_info.items():
        compare_student_grade_breakdown = info['homeworks'][hw]["Grade breakdown"]
        compare_student_id = id
        
        hw_len = len(student_grade_breakdown)
        match_counter = 0
        
        # Check if the scores for each question are similar
        # and count the number of similar scores
        for i in range(hw_len):
          if math.isclose(student_grade_breakdown[i], compare_student_grade_breakdown[i], rel_tol=0.5):
            match_counter += 1
            
        # Check to see if over 70% of the answers match
        if ((match_counter / hw_len) > SIMILARITY_CUTOFF and abs(sum(student_grade_breakdown) - sum(compare_student_grade_breakdown)) < 2):
          group.add(compare_student_id)
          grouped_students.append(compare_student_id)
        
      groups.append(group)
      
  # for group in groups:
  #   print(group)
  #   print("\n")
    
  # Split groups into subgroups of students with similar
  # start and end times
  # Finding type 1 groups
  all_groups = []
  for group in groups:
    new_groups = []
    checked_students = []
    format = "%Y-%m-%d %H:%M:%S"
    for student in group:
      sub_group = set()
      
      student_start_time = student_info[student]["homeworks"][hw]["Start time"]
      student_time_taken = student_info[student]["homeworks"][hw]["Time taken"]
      
      if student in checked_students:
        continue
      
      try:
        student_start_time = dt.strptime(student_start_time, format)
        student_end_time = student_start_time + timedelta(minutes=student_time_taken)
      except:
        checked_students.append(student)
        continue
      
      for compare_student in group:
        compare_student_start_time = student_info[compare_student]["homeworks"][hw]["Start time"]
        compare_student_time_taken = student_info[compare_student]["homeworks"][hw]["Time taken"]

        try:
          compare_student_start_time = dt.strptime(compare_student_start_time, format)
          compare_student_end_time = compare_student_start_time + \
                                      timedelta(minutes=compare_student_time_taken)
        except:
          
          continue
        
        start_time_difference = abs(student_start_time - compare_student_start_time).total_seconds() / 60.0
        end_time_difference = abs(student_end_time - compare_student_end_time).total_seconds() / 60.00
        
        if (start_time_difference < START_TIME_BUFFER and end_time_difference < END_TIME_BUFFER):
          sub_group.add(compare_student)
          checked_students.append(compare_student)
      
      # Add our main student to the group
      sub_group.add(student)
      checked_students.append(student)   
      
      # Can change min size of group
      if len(sub_group) > 1:
        new_groups.append(sub_group)
        
    all_groups += new_groups
    
  # Remove duplicate groups
  all_groups = list(set([tuple(set(i)) for i in all_groups]))
  all_groups = [set(i) for i in all_groups]

  # for group in all_groups:
  #   print(group)
  #   print("\n")
    
  return all_groups

  