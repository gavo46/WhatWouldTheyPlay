import csv
import pandas as pd
from datetime import date, datetime
from collections import defaultdict
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def parse_show_date(show_str):
    return datetime.strptime(show_str, "%m.%d.%Y").date()

def bucket_4(m, c, n, r):
    return (c * m + r) / (c + n)

def get_global_mean_play_rate(data):
    total_plays = len(data)
    num_songs = data["Song"].nunique()
    num_shows = data["Date"].nunique()
    return total_plays / (num_songs * num_shows)

def get_prob(data, song, global_mean_rate):
    all_shows_sorted = sorted(data["Date"].unique())
    target_date = date.today()
    total_shows = data["Date"].nunique()
    filtered = data[data["Song"] == song]
    count = len(filtered)
    first_index = filtered.index[0]
    first_date = filtered["Date"].min()
    last_played_date = filtered["Date"].max()
    shows_elapsed = len([d for d in all_shows_sorted if last_played_date < d <= target_date])
    years_elapsed = (target_date - last_played_date).days / 365.25
    if years_elapsed >= 10 or shows_elapsed == 0: # Bucket 3: Irrelevant
        return 0 
    elif total_shows - sorted(data["Date"].unique()).index(first_date) <= 25 and count < 5: # bucket 4
        return bucket_4(global_mean_rate, 2.5, min(25, data[data["Date"] > first_date]["Date"].nunique()), count) 
    elif count < 5: # bucket 2
        plays = data.groupby("Song").size()
        deep = plays[plays <= 4]
        return (deep.sum() / data["Date"].nunique()) / len(deep) 
    else: # bucket 1
        last_15 = filtered.tail(15)
        gaps = last_15["Last Played"].tolist()
        # EWMA
        gap_series = pd.Series(gaps)
        G_expected = gap_series.ewm(alpha=0.3, adjust=False).mean().iloc[-1]
        decay = math.exp(-years_elapsed / 1.5)
        hazard = min(shows_elapsed / G_expected, 3)
        base_prob = sigmoid(2 * (hazard - 1.6))
        return base_prob * decay


    
def main():
    data = pd.read_csv("allshows.csv")
    data["Date"] = pd.to_datetime(data["Date"], format="%m.%d.%Y").dt.date
    data["Song"] = data["Song"].str.lower()  
    songs = data['Song'].unique()  
    global_mean_rate = get_global_mean_play_rate(data)

    while True:
        request = input("What song do you want to hear at the next show? ")
        cont = False
        if request.strip().lower() not in songs:
            want_to_cont = ""
            while want_to_cont != "Y" and want_to_cont != "N":
                want_to_cont = input("Sorry, that song is not in the database. Try another song! (Y/N) ")
            if want_to_cont == "Y":
                cont = True
        else:
            prob = get_prob(data, request.strip().lower(), global_mean_rate)
            want_to_cont = ""
            while want_to_cont != "Y" and want_to_cont != "N":
                want_to_cont = input(f"You have a {prob*100}% chance of hearing {request} at the next show! Try another song? (Y/N) ")
            if want_to_cont == "Y":
                cont = True
        if (not cont):
            break


if __name__ == "__main__":
    main()