import csv


def total_amount(path):
    total = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            total += int(row["amount"])
    return total


if __name__ == "__main__":
    print("Total:", total_amount("data.csv"))
