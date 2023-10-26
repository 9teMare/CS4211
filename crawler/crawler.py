from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import os
import pandas as pd
import re

# Define the starting URL for your web crawler
sofifa_url = "https://sofifa.com/player/232284/mark-travers/?r=190075&set=true"


# Define the function to crawl a page
def crawl_overall_rating(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")

        meta_description = page_soup.find("meta", attrs={"name": "description"})
        description = meta_description["content"]
        overall_rating = re.search(
            r"overall rating is (\d+)", description, re.IGNORECASE
        )
        if overall_rating:
            return int(overall_rating.group(1))
        else:
            print(f"No meta description found for {url}")
            return None
    except Exception as e:
        print("An error occurred:", e)


def get_players_with_missing_overall_rating():
    missing = {}

    RATINGS_DIR = "../Datasets/ratings"
    ratings = sorted(os.listdir(RATINGS_DIR))

    for filename in ratings:
        df = pd.read_csv(f"{RATINGS_DIR}/{filename}")
        for _, row in df.iterrows():
            if pd.isnull(row["overall"]):
                if filename not in missing:
                    missing[filename] = {}
                if row["sofifa_id"] not in missing[filename]:
                    missing[filename][row["sofifa_id"]] = row["player_url"]

    return missing


def crawl_plyers(data):
    missing_overall_rating = {}

    for filename in data:
        missing_overall_rating[filename] = {}
        for sofifa_id in data[filename]:
            if sofifa_id not in missing_overall_rating[filename]:
                missing_overall_rating[filename][sofifa_id] = crawl_overall_rating(
                    data[filename][sofifa_id]
                )
    return missing_overall_rating


def write_to_csv(data: dict[dict[str, int]]):
    for filename in data:
        df = pd.read_csv(f"../Datasets/ratings/{filename}")
        for sofifa_id_to_update in data[filename]:
            new_overall_rating = data[filename][sofifa_id_to_update]
            df.loc[
                df["sofifa_id"] == sofifa_id_to_update, "overall"
            ] = new_overall_rating
        df.to_csv(f"../Datasets/ratings/{filename}", index=False)


# Start crawling from the initial URL

players = get_players_with_missing_overall_rating()
missing_overall_ratings = crawl_plyers(players)
print(missing_overall_ratings)
write_to_csv(missing_overall_ratings)
