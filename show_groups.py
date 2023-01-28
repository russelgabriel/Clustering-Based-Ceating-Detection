import json
import pandas
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from utility.create_df import create_df
import sys
import numpy as np

def make_plot(hw_name, hw_num):
  assignment_info = {}  

  with open("clean_data/assignments.json") as f:
    assignment_info = json.load(f)
  
  df = create_df(hw_name)
  fig = px.timeline(df, x_start = "Start times", x_end = "End times", y = "ID", hover_data = ["Total", "Breakdown"])
  fig.update_xaxes(range = [assignment_info["homeworks"][hw_num]["open date"], assignment_info["homeworks"][hw_num]["close date"]])
  fig.update_yaxes(autorange="reversed")
  
  # Change trace colors
  colors = {
    "red": "#E70A0A",
    "green": "#2FB351", 
    "blue": "#0DACE7"
    } 
  colors_arr = df["Grouped"].to_numpy()
  for i in range(len(colors_arr)):
    colors_arr[i] = colors[colors_arr[i]]
  
  fig.update_traces(marker_color = colors_arr, showlegend = True)
  fig.update_layout(title="Start and End Times for Students for {}".format(hw_name))
  fig.update_xaxes(title_text="Time")
  fig.update_yaxes(title_text="Student ID")
  
  return fig

def one_group(hw_name, hw_num):
  make_plot(hw_name, str(hw_num)).show()

def all_groups():
  homeworks = [
  ("HW01", 1), 
  ("HW02", 2), 
  ("HW03", 3), 
  ("HW04", 4),
  ("HW05", 5),
  ("HW06", 6),
  ("HW07", 7),
  ("HW09", 9),
  ("HW10", 10),
  ("HW11", 11)
  ]
  for homework in homeworks:
    make_plot(homework[0], str(homework[1])).show()
    
if len(sys.argv) < 2:
  all_groups()
else:
  one_group(sys.argv[1], sys.argv[2])