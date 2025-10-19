import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import sys

# pathlib (set base path to OYA folder)
from pathlib import Path

# The purpose of this python file is to retrieve data from the user's YouTube channel, and:
#  1. Display the top 5 best performing videos with how views, impressions, CTR, Watch Time in a table on the side dashboard with a refresh button
#  2. Train a machine learning algorithm to pick up on winning video patterns
#  3. Creator score data (% split between important success-determining data metrics)

# set directories (base, data, etc) (this will be present in each python file)
base = Path(__file__).resolve().parents[1]
print(base)

total_views = pd.read_csv(base / "data" / "raw" / "Totals.csv")
print(total_views)

# switch date formatting order
def date_format(total_views):
    month_list = []
    date_list = []
    year_list = []
    for date in total_views.iloc[:, 0]:
        year_list.append(date[0:4])
        month_list.append(date[5:7])
        date_list.append(date[8:])

    for i, date in enumerate(total_views.iloc[:, 0]):
        new_date = month_list[i] + "-" + date_list[i] + "-" + year_list[i]
        total_views.iloc[i, 0] = new_date
    return new_date

# data visualization
plt.plot(total_views.iloc[:, 0], total_views.iloc[:, 1])
plt.yticks([1000, 2000, 3000, 4000])
plt.xticks(total_views.iloc[::10, 0])
plt.xlabel("Date")
plt.ylabel("Total Views")
plt.title("Total Views per Day Graph")
plt.show()
# Code above is for learning purposes, code below is for 1. in first markdown

# Video score (Weighted CTR, Watch Time, Impressions) (combined value)
video_score = 0
raw_table = pd.read_csv(base / "data" / "raw" / "Table data.csv")


