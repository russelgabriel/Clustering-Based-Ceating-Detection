import json
import pandas as pd
import plotly.express as px
from utility.create_df import create_df
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
groups = {}
student_info = {}

with open("clean_data/groups.json", "r") as f:
  groups = json.load(f)
with open("clean_data/students.json", "r") as f:
  student_info = json.load(f)

df = create_df("HW01")
for homework in homeworks:
  df = pd.concat([df, create_df(homework)])
  
num_groups = {}
for key, value in groups.items():
  num_groups.setdefault(key, {"Group Count": len(value)})

num_grouped = {}
for homework in homeworks:
  df = create_df(homework)
  data = {
    "Group": len(df.loc[df["Grouped"].eq("green")]),
    "Non Group": len(df.loc[df["Grouped"].eq("blue")]),
    "Cheater": len(df.loc[df["Grouped"].eq("red")])
  }
  num_grouped.setdefault(homework, data)
  

# print(json.dumps(num_groups, indent=4, default=str))
# print(json.dumps(num_grouped, indent=4, default=str))

num_groups = (pd.DataFrame(num_groups)).transpose()
num_grouped = (pd.DataFrame(num_grouped)).transpose()

# print(num_groups)
# print(num_grouped)

colors = {
  "Cheater": "#E70A0A",
  "Group": "#2FB351", 
  "Non Group": "#0DACE7"
}

fig1 = px.bar(num_groups, y="Group Count", text_auto=True)
fig1.update_layout(title="Number of Groups per Homework")
fig1.update_xaxes(title_text="Homework")

fig2 = px.bar(num_grouped, y=["Non Group", "Group", "Cheater"], text_auto=True, color_discrete_map=colors)
fig2.update_yaxes(title_text="Number of students")
fig2.update_xaxes(title_text="Homework")
fig2.update_layout(legend_title_text="Type of Student")
fig2.update_layout(title="Student Type Breakdown")
fig1.show()
fig2.show()

