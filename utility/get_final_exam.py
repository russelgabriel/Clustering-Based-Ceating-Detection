import json
import pandas as pd
from find_cheaters import *

with open("./clean_data/students.json", "r") as f:
  student_info = json.load(f)
  
df = pd.read_csv("./raw_data/FE.csv")
for index, row in df.iterrows():
  try:
    student_info[str(int(row["ID"]))]["final"] = float(row["FE"])
  except:
    continue
student_info = json.dumps(student_info, indent=4, default=str)
with open("./clean_data/students.json", "w") as f:
  f.write(student_info)
  