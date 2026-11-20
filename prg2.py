import sqlite3

readings = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

con = sqlite3.connect(":memory:")

con.execute("""CREATE TABLE aq (
    station TEXT NOT NULL,
    day TEXT NOT NULL,
    pm25 REAL NOT NULL,
    UNIQUE(station, day)
)""")

con.executemany(
    "INSERT INTO aq(station, day, pm25) VALUES (?, ?, ?)",
    readings
)

con.commit()


def station_average(name):
    row = con.execute(
        "SELECT AVG(pm25) FROM aq WHERE station = ?",
        (name,)
    ).fetchone()

    return row[0]


print(station_average("Adyar"), station_average("Guindy"))
print(station_average("Adyar' OR '1'='1"))
con.close()
