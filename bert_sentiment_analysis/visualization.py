import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
import json
from datetime import datetime

with open("object_list.json", "r", encoding="utf-8") as dataFile:
    data = json.loads(dataFile.read())

dataFile.close()

keyWords = ["electric", "hydrogen", "natural_gas"]

optimism = sorted(data, key=lambda d: d["optimism"])

positive = sorted(data, key=lambda d: d["positive"])

# Lists to store dates and scores
encountered = {}
encountered1 = {}

e_pos = []
e_opt = []
e_dates = []
e_dates1 = []
h_pos = []
h_opt = []
h_dates = []
h_dates1 = []
n_pos = []
n_opt = []
n_dates = []
n_dates1 = []

for each in positive:
    if each["created_at"] not in encountered:
        if each["keyword"] == "electric":
            encountered[each["created_at"]] = True
            e_dates.append(each["created_at"])
            e_pos.append(each["positive"])
        if each["keyword"] == "hydrogen":
            encountered[each["created_at"]] = True
            h_dates.append(each["created_at"])
            h_pos.append(each["positive"])
        if each["keyword"] == "natural_gas":
            encountered[each["created_at"]] = True
            n_dates.append(each["created_at"])
            n_pos.append(each["positive"])

for each in optimism:
    if each["created_at"] not in encountered1:
        if each["keyword"] == "electric":
            encountered1[each["created_at"]] = True
            e_dates1.append(each["created_at"])
            e_opt.append(each["optimism"])
        if each["keyword"] == "hydrogen":
            encountered1[each["created_at"]] = True
            h_dates1.append(each["created_at"])
            h_opt.append(each["optimism"])
        if each["keyword"] == "natural_gas":
            encountered1[each["created_at"]] = True
            n_dates1.append(each["created_at"])
            n_opt.append(each["optimism"])

# Convert date strings (e.g. 2014-10-18 10:22:30) to datetime
e_dates = [pd.to_datetime(d) for d in e_dates]
h_dates = [pd.to_datetime(d) for d in h_dates]
n_dates = [pd.to_datetime(d) for d in n_dates]

e_x = np.array(e_dates)
e_y = np.array(e_pos)
h_x = np.array(h_dates)
h_y = np.array(h_pos)
n_x = np.array(n_dates)
n_y = np.array(n_pos)

plt.scatter(e_x, e_y, s=5, c="green", label='electric')
plt.scatter(h_x, h_y, s=5, c="blue", label='hydrogen')
plt.scatter(n_x, n_y, s=5, c="red", label='natural gas')
plt.xlabel("Dates")
plt.ylabel("Scores")
plt.title("Positive Scores Scatter-plot (all)")
plt.legend(loc="center left")
plt.show()

e_dates1 = [pd.to_datetime(d) for d in e_dates1]
h_dates1 = [pd.to_datetime(d) for d in h_dates1]
n_dates1 = [pd.to_datetime(d) for d in n_dates1]

e_x1 = np.array(e_dates1)
e_y1 = np.array(e_opt)
h_x1 = np.array(h_dates1)
h_y1 = np.array(h_opt)
n_x1 = np.array(n_dates1)
n_y1 = np.array(n_opt)

plt.scatter(e_x1, e_y1, s=5, c="green", label='electric')
plt.scatter(h_x1, h_y1, s=5, c="blue", label='hydrogen')
plt.scatter(n_x1, n_y1, s=5, c="red", label='natural gas')
plt.xlabel("Dates")
plt.ylabel("Scores")
plt.title("Optimism Scores Scatter-plot (all)")
plt.legend(loc="center left")
plt.show()

# for frequency charts
"""
# Choose some nice levels
levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates) / 6)))[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
ax.set(title="Frequency of Powertrain Mentions")

ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
ax.plot(dates, np.zeros_like(dates), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.

# annotate lines
for d, l, r in zip(dates, levels, pos):
    ax.annotate('', xy=(d, l),
                xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top")

# format x-axis with 4-month intervals
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y-axis and spines
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right"]].set_visible(False)

ax.margins(y=0.1)
plt.show()
"""
