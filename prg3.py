import sqlite3
from collections import defaultdict
import pandas as pd

rows = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

# 1. Plain Python: running sum and count
acc = defaultdict(lambda: [0.0, 0])

for station, day, pm25 in rows:
    acc[(station, day)][0] += pm25
    acc[(station, day)][1] += 1

loop_result = {k: v[0] / v[1] for k, v in acc.items()}

# 2. pandas groupby
df = pd.DataFrame(rows, columns=["station", "day", "pm25"])

pandas_result = df.groupby(["station", "day"])["pm25"].mean().to_dict()

# 3. SQL GROUP BY
con = sqlite3.connect(":memory:")

con.execute(
    "CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)"
)

con.executemany(
    "INSERT INTO aq VALUES (?, ?, ?)",
    rows
)

sql_result = {
    (station, day): mean
    for station, day, mean in con.execute(
        "SELECT station, day, AVG(pm25) FROM aq GROUP BY station, day"
    )
}

con.close()
