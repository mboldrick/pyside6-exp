import ast
import datetime
import functools
import json
import os
import time
import calendar
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
import requests
import seaborn as sns
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

API_URL = "https://api.monday.com/v2"
API_KEY = os.environ.get("API_KEY")
HEADERS = {"Authorization": API_KEY}
MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        print(f"{func.__name__!r} Execution started...")
        start_time = time.perf_counter()  # also time.process_time()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Ran {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def post_query(query, variables=None, retries=5, backoff_factor=0.5):
    data = {"query": query, "variables": variables}
    for attempt in range(retries):
        response = requests.post(url=API_URL, json=data, headers=HEADERS)

        if response.status_code == 200:
            response_json = response.json()
            if "errors" in response_json:
                raise ValueError(f"API returned errors: {response_json['errors']}")
            return response_json.get("data", None)

        if attempt < retries - 1:
            sleep_time = backoff_factor * (2**attempt)
            time.sleep(sleep_time)
            continue

        else:
            raise ValueError(
                f"Hit maximum # retries / last staus was " f"{response.status_code}"
            )


def get_users():
    query = "{ users (limit: 9999) { id name } }"
    data = post_query(query)
    with open("users.json", "w") as f:
        json.dump(data, f)
    return data


@timer
def get_all_board_ids_from_workspaces(workspace_ids):
    query = """
    query {
            boards (state: active, limit:9999) {
            workspace_id
            id
        }
    }
    """
    data = post_query(query)
    boards = data.get("boards", [])
    filtered_boards = [
        board["id"] for board in boards if board["workspace_id"] in workspace_ids
    ]
    print(f"Number of boards: {len(filtered_boards)}")

    return filtered_boards


@timer
def get_all_item_ids_from_board(board_id):
    query = (
        """
    query {
      boards(ids: %s) {
        items (limit:9999) {
          id
        }
      }
    }
    """
        % board_id
    )
    data = post_query(query)

    return [item["id"] for item in data["boards"][0]["items"]]


def get_all_column_values_from_board(board_id):
    query = (
        """
    query {
            boards(ids: %s) {
                columns {
                    archived
                    title
                    type
                    settings_str
                    description
                }
            }
    }
    """
        % board_id
    )
    data = post_query(query)
    columns = data["boards"][0]["columns"]
    return columns


def get_item(item_id):
    query = f"""
    query {{
        items(ids: {item_id}) {{
            id
            name
            column_values {{
                title
                text
                value
            }}
        }}
    }}
    """
    data = post_query(query)
    return data["items"][0]


@timer
def process_new_items(item_ids):
    items_data = []
    subitems_data = []

    for item_id in item_ids:
        item_data = get_item(item_id)
        items_data.append(item_data)

        linked_subitem_ids = get_linked_pulse_ids(item_data)
        for subitem_id in linked_subitem_ids:
            subitem_data = get_item(subitem_id)
            subitem_data["parent_item_id"] = item_data["id"]

            subitem_column_values = {}
            for column_value in subitem_data["column_values"]:
                subitem_column_values[column_value["title"]] = column_value["text"]

            subitem_column_values["parent_item_id"] = subitem_data["parent_item_id"]
            subitem_column_values["id"] = subitem_data["id"]

            subitems_data.append(subitem_column_values)

    return items_data, subitems_data


@timer
def process_items(board_ids, board_types):
    items_data = []
    subitems_data = []
    old_items_data = []

    for board_id in board_ids:
        item_ids = get_all_item_ids_from_board(board_id)
        print(f"board_id: {board_id} Length: {len(item_ids)}")

        if item_ids:
            if board_types[board_id] == "old":
                continue
            else:
                new_data, new_subitems_data = process_new_items(item_ids)
                items_data.extend(new_data)
                subitems_data.extend(new_subitems_data)

    return items_data, subitems_data, old_items_data


@timer
def extract_columns(data, columns_to_keep=None):
    columns_data = {}
    for item in data:
        for column_value in item["column_values"]:
            column_title = column_value["title"]
            if columns_to_keep is None or column_title in columns_to_keep:
                column_text = column_value["text"]
                columns_data[column_title] = column_text
        item.update(columns_data)
        del item["column_values"]
    return data


@timer
def create_dataframes(items_data, subitems_data, old_items_data):
    items_data = extract_columns(items_data)

    items_df = pd.DataFrame(items_data)
    subitems_df = pd.DataFrame(subitems_data)
    old_items_df = pd.DataFrame(old_items_data)

    return items_df, subitems_df, old_items_df


def get_linked_pulse_ids(item_data):
    for column_value in item_data["column_values"]:
        if (
            column_value["title"] == "Subitems"
            and column_value["value"] is not None
            and "linkedPulseIds" in column_value["value"]
        ):
            value = json.loads(column_value["value"])
            return [entry["linkedPulseId"] for entry in value["linkedPulseIds"]]
    return []


def flatten_column_values(df):
    df["column_values"] = df["column_values"].apply(ast.literal_eval)
    new_columns = pd.DataFrame(df["column_values"].tolist())
    df.drop("column_values", axis=1, inplace=True)
    df = pd.concat([df, new_columns], axis=1)
    return df


def sum_list_of_strings(list_of_strings):
    return sum(
        [
            float(x.strip())
            for string in list_of_strings
            for x in string.split(",")
            if x.strip()
        ]
    )


def check_and_log_missing_column(df, column_name, board_id):
    if column_name not in df.columns:
        print(f"Column '{column_name}' is missing in board ID {board_id}")
        return False
    return True


def process_subitems_df(subitems_df):
    if "Date" in subitems_df.columns:
        subitems_df["Date"] = pd.to_datetime(subitems_df["Date"])

    subitems_df["Normal Business HRS"] = pd.to_numeric(
        subitems_df["Normal Business HRS"], errors="coerce"
    )
    subitems_df["Weekday After HRS"] = pd.to_numeric(
        subitems_df["Weekday After HRS"], errors="coerce"
    )
    subitems_df["Weekend HRS"] = pd.to_numeric(
        subitems_df["Weekend HRS"], errors="coerce"
    )

    return subitems_df


# def generate_filtered_df(subitems_df):
#     six_months_ago = pd.Timestamp.now() - pd.DateOffset(months=6)
#     filtered_df = subitems_df[subitems_df["Date"] >= six_months_ago].copy()

#     if "Date" in filtered_df.columns:
#         filtered_df["Week"] = filtered_df["Date"].dt.isocalendar().week
#         filtered_df["Month"] = filtered_df["Date"].dt.month

#     filtered_df.loc[:, "Week Ending"] = filtered_df["Date"] + pd.to_timedelta(
#         6 - filtered_df["Date"].dt.weekday, unit="d"
#     )

#     return filtered_df


def calculate_total_hours(filtered_df):
    filtered_df["Total Hours"] = (
        filtered_df["Normal Business HRS"].fillna(0)
        + filtered_df["Weekday After HRS"].fillna(0)
        + filtered_df["Weekend HRS"].fillna(0)
    )
    return filtered_df


def generate_new_pivot_df(filtered_df):
    pivot_df = filtered_df.pivot_table(
        index="Owner",
        columns="Month Name",
        values="Total Hours",
        aggfunc="sum",
        fill_value=0,
    )

    if not pivot_df.empty:
        pivot_df.loc["Grand Total"] = pivot_df.sum(numeric_only=True)

    # Sort columns by month name

    pivot_df = pivot_df.reindex(columns=MONTH_ORDER)

    return pivot_df


@timer
def load_board_types(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@timer
def save_board_types(file_path, board_types):
    with open(file_path, "w") as file:
        json.dump(board_types, file)


@timer
def update_board_types(board_ids, file_path="board_types.json"):
    board_types = load_board_types(file_path)

    for board_id in board_ids:
        if board_id not in board_types:
            columns = get_all_column_values_from_board(board_id)
            is_old_timesheet = False
            for column in columns:
                if column["type"] == "duration":
                    is_old_timesheet = True
                    break

            board_type = "old" if is_old_timesheet else "new"
            board_types[board_id] = board_type
            save_board_types(file_path, board_types)

    return board_types


def filter_previous_week(df):
    today = datetime.date.today()
    # Calculate the start date of the previous week (Sunday of the previous week)
    start = today - datetime.timedelta(days=today.weekday() + 13)
    start = start - datetime.timedelta(days=7)
    # Calculate the end date of the previous week (Saturday of the previous week)
    end = start + datetime.timedelta(days=6)

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    start = pd.to_datetime("2023-03-26")
    end = pd.to_datetime("2023-04-01")

    filtered_df = df.loc[(df["Date"] >= start) & (df["Date"] <= end)]

    return filtered_df


def generate_previous_week_pivot_df(df):
    # previous_week_df = filter_previous_week(df)
    # change below to previous_week_df.pivot_table
    pivot_df = df.pivot_table(
        index="Owner",
        columns="Date",
        values="Total Hours",
        aggfunc="sum",
        fill_value=0,
    )

    pivot_df.loc["Grand Total"] = pivot_df.sum(numeric_only=True)

    return pivot_df


def group_by_week(df):
    end = df["Week Ending"].max()
    start = end - pd.Timedelta(days=6)

    weekly_dfs = []
    while start > df["Date"].min():
        week_df = df.loc[
            (df["Date"] >= pd.Timestamp(start)) & (df["Date"] <= pd.Timestamp(end))
        ]
        week_df["Week Ending"] = end
        weekly_dfs.append(week_df)
        end = start - pd.Timedelta(days=1)
        start = end - pd.Timedelta(days=6)

    return pd.concat(weekly_dfs, sort=False)


def filter_previous_7_days(filtered_df):
    today = pd.Timestamp.now()
    start_of_period = today - pd.to_timedelta(7, unit="d")

    previous_7_days_df = filtered_df[
        (filtered_df["Date"] >= start_of_period) & (filtered_df["Date"] < today)
    ]
    return previous_7_days_df


def generate_previous_7_days_pivot_df(filtered_df):
    filtered_df = filter_previous_7_days(filtered_df)
    pivot_df = filtered_df.pivot_table(
        index="Owner",
        columns="Date",
        values="Total Hours",
        aggfunc="sum",
        fill_value=0,
    )

    pivot_df.loc["Grand Total"] = pivot_df.sum(numeric_only=True)

    return pivot_df


def filter_last_n_months(filtered_df, n=3):
    today = pd.Timestamp.now()
    n_months_ago = today - pd.DateOffset(months=n)
    last_n_months_df = filtered_df[
        (filtered_df["Date"] >= n_months_ago) & (filtered_df["Date"] < today)
    ]
    return last_n_months_df


def add_month_name_column(filtered_df):
    filtered_df["Month Name"] = filtered_df["Month"].apply(
        lambda x: calendar.month_name[x]
    )
    return filtered_df


def process_subitems_and_generate_weekly_report(subitems_df):
    subitems_df = process_subitems_df(subitems_df)
    subitems_df.to_csv("subitems_df.csv")
    subitems_df = calculate_total_hours(subitems_df)
    subitems_df["Total Hours"] = subitems_df["Total Hours"].fillna(0)

    # Filter data for the last 4 complete weeks
    current_date = subitems_df["Date"].max()
    current_week = current_date.week
    four_weeks_ago_week = current_week - 4
    four_weeks_ago = current_date - pd.Timedelta(weeks=4)
    subitems_df = subitems_df.loc[
        (subitems_df["Date"] >= four_weeks_ago)
        & (subitems_df["Date"].dt.isocalendar().week >= four_weeks_ago_week)
        & (subitems_df["Date"].dt.isocalendar().week < current_week)
    ]

    total_hours_by_owner = (
        subitems_df.groupby(
            ["Owner", pd.Grouper(key="Date", freq="W-SAT", dropna=False)]
        )["Total Hours"]
        .sum()
        .reset_index()
    )
    total_hours_by_owner["Total Hours"] = total_hours_by_owner["Total Hours"].fillna(0)

    pivoted_df = total_hours_by_owner.pivot_table(
        values="Total Hours",
        index="Owner",
        columns=pd.Grouper(key="Date", freq="W-SAT"),
    )

    # Modify column labels
    column_labels = []
    for column in pivoted_df.columns:
        column_start = (column - pd.Timedelta(days=6)).strftime("%b %d")
        column_end = column.strftime("%b %d")
        column_label = f"{column_start} - {column_end}"
        column_labels.append(column_label)
    pivoted_df.columns = column_labels

    grand_totals = pd.DataFrame(pivoted_df.sum(), columns=["Grand Total"]).T
    pivoted_df = pd.concat([pivoted_df, grand_totals]).dropna(0)

    print(pivoted_df)
    pivoted_df.to_csv("previous_weeks_df.csv")


def main():
    # board_ids = get_all_board_ids_from_workspaces([974531])
    board_ids = [
        # "4107511682",
        # "3905301639",
        # "3937860982",
        # "2953214541",
        "3227946610",
        # "3725499406",
        # "4139926936",
    ]

    board_types = update_board_types(board_ids, "board_types.json")
    items_data, subitems_data, old_items_data = process_items(board_ids, board_types)
    items_df, subitems_df, old_items_df = create_dataframes(
        items_data, subitems_data, old_items_data
    )

    process_subitems_and_generate_weekly_report(subitems_df)

    subitems_df = process_subitems_df(subitems_df)

    # filtered_df = generate_filtered_df(subitems_df)
    filtered_df = calculate_total_hours(subitems_df)

    previous_days_df = filter_previous_7_days(filtered_df)

    previous_days_pivot = generate_previous_7_days_pivot_df(previous_days_df)

    previous_days_pivot.to_csv("previous_days_pivot.csv")
    print(previous_days_pivot)


if __name__ == "__main__":
    main()
