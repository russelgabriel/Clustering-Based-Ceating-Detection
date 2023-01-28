import pandas as pd
from utility.create_df import create_df

def find_cheaters_per_hw(df):
  homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
  homework_cheaters = {}
  for homework in homeworks:
    homework_cheaters.setdefault(homework, [])

  for index, row in df.iterrows():
    if row["Grouped"] == "red":
      homework_cheaters[row["Homework type"]].append(row["ID"])
  
  return homework_cheaters

def find_all_cheaters(df):
  cheaters = set()
  for index, row in df.iterrows():
    if row["Grouped"] == "red":
      cheaters.add(row["ID"])
  
  return cheaters

def get_cheater_freq(cheaters, hw_cheaters):
  cheater_count = {x:0 for x in range(1, 11)}
  for cheater in cheaters:
    freq = 0
    for cheater_list in hw_cheaters.values():
      if cheater in cheater_list:
        freq += 1
    cheater_count[freq] += 1
    
  return cheater_count

def student_cheat_freq(cheaters, hw_cheaters):
  student_id = []
  cheat_freq = []
  for cheater in cheaters:
    freq = 0
    for cheater_list in hw_cheaters.values():
      if cheater in cheater_list:
        freq += 1
    student_id.append(cheater)
    cheat_freq.append(freq)
  # print(len(student_id))
  # print(len(cheat_freq))
  dict = {"ID": student_id, "Cheat Frequency": cheat_freq}
  df = pd.DataFrame(dict)
  return df
  
  
