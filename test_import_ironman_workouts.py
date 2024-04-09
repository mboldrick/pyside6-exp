import openpyxl
import pandas as pd

# hidden_cols = []
# for colLetter, colDimension in ws.column_dimensions.items():
#     if colDimension.hidden == True:
#         hidden_cols.append(colLetter)

# df = pd.read_excel(loc, skiprows=3, names=colnames)
# print(df.head(10))
# print(df.tail(10))


def iterating_over_values(path, sheet_name):
    colnames = [
        "week",
        "day_of_week",
        "date",
        "swim_time",
        "swim_meters",
        "swim_hr",
        "bike_time",
        "bike_miles",
        "bike_hr",
        "run_time",
        "run_miles",
        "run_hr",
        "pushups_1",
        "pushups_2",
        "pushups_3",
        "pushups_4",
        "pushups_5",
        "pushups_total",
        "abs_time_1",
        "abs_time_2",
        "abs_time_3",
        "abs_time_total",
        "core_time",
        "meditate_time",
        "strength_time_total",
        "combined_time_total",
        "rest_pulse",
        "bp",
        "sleep_time",
        "weight",
        "body_fat",
        "total_inches",
        "swim_time_total",
        "swim_meters_total",
        "bike_time_total",
        "bike_miles_total",
        "run_time_total",
        "run_miles_total",
        "strength_time_total",
        "combined_time_total",
        "notes",
        "nutrition",
        "meals",
    ]
    wb = openpyxl.load_workbook(filename=path)
    if sheet_name not in wb.sheetnames:
        print(f"'{sheet_name}' not found. Quitting.")
        return

    sheet = wb[sheet_name]
    print(f"{sheet_name}")
    print(f"Total number of rows: {sheet.max_row}")
    print(f"Total number of columns: {sheet.max_column}")

    for value in sheet.iter_rows(
        min_row=1, max_row=5, min_col=1, max_col=10, values_only=True
    ):
        print(value)


if __name__ == "__main__":
    iterating_over_values("data/Ironman workouts.xlsx", sheet_name="2024")
