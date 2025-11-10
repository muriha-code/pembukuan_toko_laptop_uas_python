import csv
from pathlib import Path

# Folder data sejajar dengan folder modules
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def read_csv(filename):
    path = DATA_DIR / filename
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(filename, data, fieldnames):
    path = DATA_DIR / filename
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
