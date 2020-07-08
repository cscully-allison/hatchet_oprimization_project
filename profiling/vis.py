import pandas as pd
import altair
import json

data = {}

with open("/usr/workspace/scullyal/hatchet_optimization_project/profiling/vis_data_10_trials.json", "r") as f:
    data = json.loads(f.read())

df = pd.DataFrame(data)

chart = altair.Chart(df).mark_point(size = 20).encode(
    y="runtime",
    x="records",
    color=altair.Color('profile', legend=altair.Legend(title="Profile"))
).interactive().properties(width=800)

chart.save("runtimes_data.html")
