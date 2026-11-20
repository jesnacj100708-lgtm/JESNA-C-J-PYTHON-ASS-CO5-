import csv
import sqlite3
from io import StringIO

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1200
"""


def load_clean(text):
    result = []
    reader = csv.DictReader(StringIO(text))
    required = {"station", "date", "pm25"}

    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError("Missing required columns")

    for row in reader:
        raw = (row.get("pm25") or "").strip()

        if raw.upper() in ("", "NA", "N/A", "NULL"):
            continue

        try:
            value = float(raw)
        except ValueError:
            continue

        if value < 0 or value > 999:
            continue


def min_max(values):
    if not values:
        return []

    lo, hi = min(values), max(values)

    return [0.0 if hi == lo else round((v-lo)/(hi-lo), 3)
            for v in values]


POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total, previous = 0, None

    for word in words:
                value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0

        if previous in NEGATORS:
            value *= -1

        total += value
        previous = word

    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


def main():
    cleaned = load_clean(RAW)
    print("Cleaned:", cleaned)
    print("Scaled:", min_max([r[2] for r in cleaned]))

    con = sqlite3.connect("air_quality.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("""CREATE TABLE IF NOT EXISTS aq(
        station TEXT NOT NULL,
        day TEXT NOT NULL,
        pm25 REAL NOT NULL,
        UNIQUE(station, day))""")

    con.executemany(
        "INSERT OR REPLACE INTO aq(station, day, pm25) VALUES (?, ?, ?)",
        cleaned
    )
    con.commit()

    row = con.execute(
        "SELECT AVG(pm25) FROM aq WHERE station = ?", ("Adyar",)
    ).fetchone()

    print("Adyar mean:", row[0])

    con.execute(
        "CREATE INDEX IF NOT EXISTS idx_aq_station_day ON aq(station, day)"
    )

    con.close()

    for complaint in [
        "Roads are clean and the bus was fast.",
        "Smoke from the factory, air is bad.",
        "The staff were not helpful.",
        "Not bad, service improved."
    ]:
        print(label(complaint), "|", complaint)


if __name__ == "__main__":
    main()
