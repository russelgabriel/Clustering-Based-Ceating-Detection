import pandas as pd
from utility.create_df import create_df
import plotly.express as px

homeworks = ["HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]

df = create_df("HW01")
for homework in homeworks:
  df = pd.concat([df, create_df(homework)])

legend = {
  "blue": "Class",
  "green": "Grouped", 
  "red": "Cheaters"
}

colors = {
  "red": "#E70A0A",
  "green": "#2FB351", 
  "blue": "#0DACE7"
}

fig = px.box(df, y="Total", x="Homework type", color="Grouped", color_discrete_map=colors)
for idx, trace in enumerate(fig["data"]):
  trace["name"] = legend[trace["name"]]
fig.update_layout(title="Summary Statistics for Each Type of Student in Each Homework")
fig.update_layout(legend_title_text="Type of Student")
fig.update_yaxes(title_text="Total grade")
fig.show()