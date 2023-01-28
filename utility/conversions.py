import pandas as pd
from datetime import datetime as dt

def get_time_taken(string):
  time = string.split()
  if time[0] == '-':
    return 0
  elif time[1] == "hour" or time[1] == "hours":
    # case that it took exactly one hour to complete
    if len(time) <= 2: 
      actual_time = 60 * int(time[0])
      return actual_time
    else:
      actual_time = (60 * int(time[0])) + int(time[2])
      return actual_time
  elif time[1] == "mins" or time[1] == "min":
    return int(time[0])
  
  return 0

def get_datetime(string, type):
  # Type 0 for students
  # Type 1 for assignments
  str_format = "%m/%d/%Y,%I:%M:%S %p" if type else "%d %B %Y  %I:%M %p"
  time = dt.strptime(string.replace("  ", " "), str_format)
  return time
    
def get_assignment_info():
  homeworks = {}
  labs = {}

  df = pd.read_csv("raw_data/moodle.csv")

  for index, row in df.iterrows():
    if row["Quiz type"] == "Homework":
      homeworks[row["Quiz number"]] = {}
      open_date = get_datetime(row["Open date"] + "," + row["Open time"], 1)
      close_date = get_datetime(row["Close date"] + "," + row["Close time"], 1)
      homeworks[row["Quiz number"]]["open date"] = open_date
      homeworks[row["Quiz number"]]["close date"] = close_date
      homeworks[row["Quiz number"]]["duration"] = row["Duration"]
    else:
      labs[row["Quiz number"]] = {}
      open_date = get_datetime(row["Open date"] + "," + row["Open time"], 1)
      close_date = get_datetime(row["Close date"] + "," + row["Close time"], 1)
      labs[row["Quiz number"]]["open date"] = open_date
      labs[row["Quiz number"]]["close date"] = close_date
      labs[row["Quiz number"]]["duration"] = row["Duration"]
      
  return homeworks, labs