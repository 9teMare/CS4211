from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import os
import pandas as pd
from crawlers import (
    CrawlerType,
    crawl_overall_rating,
    crawl_defending_marking_rating,
)


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


def get_players_with_missing_defending_marking_rating():
    missing = {}

    RATINGS_DIR = "../Datasets/ratings"
    ratings = sorted(os.listdir(RATINGS_DIR))

    for filename in ratings:
        df = pd.read_csv(f"{RATINGS_DIR}/{filename}")
        for _, row in df.iterrows():
            if pd.isnull(row["defending_marking"]):
                if filename not in missing:
                    missing[filename] = {}
                if row["sofifa_id"] not in missing[filename]:
                    missing[filename][row["sofifa_id"]] = row["player_url"]

    return missing


def crawl_data(data, type=CrawlerType):
    missing_data = {}

    for filename in data:
        missing_data[filename] = {}
        for sofifa_id in data[filename]:
            if sofifa_id not in missing_data[filename]:
                if type == CrawlerType.DEFENDING_MARKING_RATING:
                    missing_data[filename][sofifa_id] = crawl_defending_marking_rating(
                        data[filename][sofifa_id]
                    )
                elif type == CrawlerType.OVERALL_RATING:
                    missing_data[filename][sofifa_id] = crawl_overall_rating(
                        data[filename][sofifa_id]
                    )
    return missing_data


def write_to_csv(data: [dict[dict[str, int]]]):
    for filename in data[0]:
        df = pd.read_csv(f"../Datasets/ratings/{filename}")
        for sofifa_id_to_update in data[0][filename]:
            new_overall_rating = data[0][filename][sofifa_id_to_update]
            df.loc[
                df["sofifa_id"] == sofifa_id_to_update, "overall"
            ] = new_overall_rating
        df.to_csv(f"../Datasets/ratings/{filename}", index=False)

    for filename in data[1]:
        df = pd.read_csv(f"../Datasets/ratings/{filename}")
        for sofifa_id_to_update in data[1][filename]:
            new_defending_marking_rating = data[1][filename][sofifa_id_to_update]
            df.loc[
                df["sofifa_id"] == sofifa_id_to_update, "defending_marking"
            ] = new_defending_marking_rating
        df.to_csv(f"../Datasets/ratings/{filename}", index=False)


if __name__ == "__main__":
    players_without_overall_rating = get_players_with_missing_overall_rating()

    players_without_defending_marking_rating = (
        get_players_with_missing_defending_marking_rating()
    )

    missing_ratings = [
        crawl_data(players_without_overall_rating, CrawlerType.OVERALL_RATING),
        crawl_data(
            players_without_defending_marking_rating,
            CrawlerType.DEFENDING_MARKING_RATING,
        ),
    ]
    print(missing_ratings)
    write_to_csv(missing_ratings)
