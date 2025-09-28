import csv
import os
from collections import Counter

def find_interest_column(header):
    """Find the interest rate column from possible names."""
    possible_names = ['interest_rate', 'int_rate', 'Rate', 'APR', 'apr', 'Interest', 'interest']
    for name in possible_names:
        if name in header:
            return name
    return None

def clean_interest_rate(value):
    """
    Convert interest rate values to a float percentage rounded to 2 decimals.
    Handles formats like '13.49%', '0.1349', '13.49'.
    Returns None if value is invalid.
    """
    if not value:
        return None
    value = value.strip().replace(',', '')
    try:
        if value.endswith('%'):
            num = float(value.rstrip('%'))
        else:
            num = float(value)
            if num < 1:  # e.g., 0.1349 means 13.49%
                num *= 100
        return round(num, 2)
    except ValueError:
        return None

def read_interest_rates(filename):
    """Read and clean interest rates from the CSV file."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return None

    rates = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rate_col = find_interest_column(reader.fieldnames)
            if not rate_col:
                print("Error: Interest rate column not found.")
                return None
            for row in reader:
                rate = clean_interest_rate(row.get(rate_col, ''))
                if rate is not None:
                    rates.append(rate)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    return rates

def print_top_rates(rates, top_n=3):
    """Print the top N most common interest rates with counts and percentages."""
    total = len(rates)
    counter = Counter(rates)
    most_common = counter.most_common(top_n)
    print(f"Top {top_n} Most Common Loan Interest Rates:")
    for rate, count in most_common:
        percent = (count / total) * 100
        print(f"{rate:.2f}%: {count} loans ({percent:.2f}%)")

def main():
    filename = input("Enter CSV filename: ").strip()
    rates = read_interest_rates(filename)
    if not rates:
        print("No valid interest rate data found.")
        return
    print_top_rates(rates)

if __name__ == "__main__":
    main()