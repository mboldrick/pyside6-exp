import pandas as pd
import datetime
from mapping_2023 import *


def collect_column_names():
    column_names = [
        key.lower()  # Convert to lowercase
        for key, value in globals().items()
        if type(value) == int and not key.startswith("__")
    ]
    return column_names


def main():
    # Set the Excel filename, inlcuding the path
    filename = "data/Ironman workouts test.xlsx"

    # Loop through data worksheets

    # Get the column names for this worksheet
    colnames = collect_column_names()
    print(f"Number of columns: {len(colnames)}")

    # Read the Excel worksheet into a dataframe
    df = pd.read_excel(
        filename,
        sheet_name="2023",
        skiprows=3,
        skipfooter=6,
        dtype_backend="pyarrow",
        names=colnames,
    )

    # Print the dataframe info
    print(df.info())

    # Convert the time fields (swim time, bike time, etc.) to timedelta
    df["swim_time"] = pd.to_timedelta(df["swim_time"], errors="coerce")
    df["bike_time"] = pd.to_timedelta(df["bike_time"], errors="coerce")
    df["run_time"] = pd.to_timedelta(df["run_time"], errors="coerce")
    df["abs_time_1"] = pd.to_timedelta(df["abs_time_1"], errors="coerce")
    df["abs_time_2"] = pd.to_timedelta(df["abs_time_2"], errors="coerce")
    df["abs_time_3"] = pd.to_timedelta(df["abs_time_3"], errors="coerce")
    df["abs_time_total"] = pd.to_timedelta(df["abs_time_total"], errors="coerce")
    df["core_time"] = pd.to_timedelta(df["core_time"], errors="coerce")
    df["meditate_time"] = pd.to_timedelta(df["meditate_time"], errors="coerce")
    df["strength_time_total"] = pd.to_timedelta(
        df["strength_time_total"], errors="coerce"
    )
    df["combined_time_total"] = pd.to_timedelta(
        df["combined_time_total"], errors="coerce"
    )
    df["sleep_time"] = pd.to_timedelta(df["sleep_time"], errors="coerce")
    df["swim_time_total"] = pd.to_timedelta(df["swim_time_total"], errors="coerce")
    df["bike_time_total"] = pd.to_timedelta(df["bike_time_total"], errors="coerce")
    df["run_time_total"] = pd.to_timedelta(df["run_time_total"], errors="coerce")
    df["strength_time_total_2"] = pd.to_timedelta(
        df["strength_time_total_2"], errors="coerce"
    )
    df["combined_time_total_2"] = pd.to_timedelta(
        df["combined_time_total_2"], errors="coerce"
    )

    # Print the dataframe info
    print(df.info())

    # Print the first and last 10 rows of the dataframe
    print(df.head(10))
    print(df.tail(10))

    # # Store the dataframe in a CSV file
    # df.to_csv(f"data/{sheet_name}.csv", index=False)
    # # Store the dataframe in an Excel file
    # df.to_excel(f"data/{sheet_name}.xlsx", index=False)


if __name__ == "__main__":
    main()
