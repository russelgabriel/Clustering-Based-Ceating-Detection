import json
import numpy

def get_class_average(hw):
  
  with open("./clean_data/students.json", "r") as f:
    student_info = json.load(f)
  
  all_grades = []
  for id, info in student_info.items():
    grade = info["homeworks"][hw]["Total"]
    if grade > 0:
      all_grades.append(grade)
  
  return numpy.mean(all_grades)
  