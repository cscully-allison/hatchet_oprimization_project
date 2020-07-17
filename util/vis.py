import pandas as pd
import altair
import json
from db import MetadataDB

db = MetadataDB()
data = {}

with open("/usr/WS1/scullyal/hatchet_optimization_project/profiling/Abhinav_Runs/a_vis.json", "r") as f:
    data = json.loads(f.read())

df = pd.DataFrame(data)
df = df.set_index("id").join(db.p_md)

chart = altair.Chart(df).mark_point().encode(
    y=altair.Y("runtime", axis=altair.Axis(title="Runtime (s)"), scale=altair.Scale(type='log')),
    x=altair.X("callsites", axis=altair.Axis(title="Callsites")),
    color=altair.Color("optim:N", legend=altair.Legend(title="Optimization Level"))
).interactive().properties(width=800)

chart.save("Abhinav_Runs/scaled_vis.html")
