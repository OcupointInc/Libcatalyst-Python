import csv

def remove_duplicates(input_csv, output_csv):
    # Use a set to track seen rows and a list to maintain order
    seen = set()
    unique_rows = []

    # Read the input CSV file
    with open(input_csv, "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            # Convert the row to a tuple for hashable comparison
            row_tuple = tuple(row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)

    # Write the output CSV file
    with open(output_csv, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(unique_rows)

# Example usage
input_csv = "sleep.csv"
output_csv = "sleep.csv"
remove_duplicates(input_csv, output_csv)
print(f"Duplicate-free CSV written to {output_csv}")
