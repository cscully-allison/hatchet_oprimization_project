import pandas as pd
import altair
import json

data = {}

with open("vis_data_5_trials.json", "r") as f:
    data = json.loads(f.read())

df = pd.DataFrame(data)

chart = altair.Chart(df).mark_bar(size = 20).encode(
    y="runtime",
    x="records",
    color=altair.Color('profile', legend=altair.Legend(title="Profile"))
).interactive().properties(width=800)

chart.save("runtimes_mod.html")
