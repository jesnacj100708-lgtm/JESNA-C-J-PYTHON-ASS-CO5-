import csv
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
    """Return (station, date, pm25) tuples for valid PM2.5 only."""
    rows = []
    reader = csv.DictReader(StringIO(text))
    required = {"station", "date", "pm25"}

    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError("CSV must contain station, date and pm25 columns")

    for row in reader:
        raw_value = (row.get("pm25") or "").strip()

        if raw_value.upper() in ("", "NA", "N/A", "NULL"):
            continue

        try:
            pm25 = float(raw_value)
        except ValueError:
            continue

        if pm25 < 0 or pm25 > 999:
            continue

        station = (row.get("station") or "").strip()
        date = (row.get("date") or "").strip()

        if not station or not date:
            continue

        rows.append((station, date, pm25))

    return rows


def min_max(values):
    """Scale values to 0..1 and round to 3 decimal places."""
    if not values:
        return []

    low, high = min(values), max(values)

    if high == low:
        return [0.0 for _ in values]

    return [round((v - low) / (high - low), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
