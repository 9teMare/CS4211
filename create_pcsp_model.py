import os
import pandas as pd
from typing import Dict
import re

TEMPLATE_FILENAME = "template.pcsp"

REQUIRED_KEYS = [
    "ak_shortPass",
    "ak_longPass",
    "ard_shortPass",
    "ard_longPass",
    "ard_probLoseBall",
    "acrd_shortPass",
    "acrd_longPass",
    "acrd_probLoseBall",
    "acld_shortPass",
    "acld_longPass",
    "acld_probLoseBall",
    "ald_shortPass",
    "ald_longPass",
    "ald_probLoseBall",
    "arm_shortPass",
    "arm_longPass",
    "arm_longShot",
    "arm_probLoseBall",
    "acm_shortPass",
    "acm_longPass",
    "acm_longShot",
    "acm_probLoseBall",
    "alm_shortPass",
    "alm_longPass",
    "alm_longShot",
    "alm_probLoseBall",
    "arf_finish",
    "arf_longShot",
    "arf_volley",
    "arf_header",
    "arf_probLoseBall",
    "acf_finish",
    "acf_longShot",
    "acf_volley",
    "acf_header",
    "acf_probLoseBall",
    "alf_finish",
    "alf_longShot",
    "alf_volley",
    "alf_header",
    "alf_probLoseBall",
    "dk_gkRating",
]

SRC_DIR = "./Datasets"
MATCHES_DIR = f"{SRC_DIR}/matches"
RATINGS_DIR = f"{SRC_DIR}/ratings"


def create_pcsp_model(filename: str, data: Dict[str, int]) -> None:
    # Validate data to check if it has the relevant data
    if not validate_data(data):
        print("Data dictionary passed is not valid, please check.")
        return

    # Check if template file exists
    if not os.path.exists(TEMPLATE_FILENAME):
        print("Template file not found")
        return

    with open(TEMPLATE_FILENAME, "r") as file:
        template = file.read()

    # Replace placeholders with actual data
    content = template.format(**data)

    # Check if target file exists to avoid overwriting
    if os.path.exists(filename):
        print(f"{filename} already exists. Choose a different name or path.")
        return

    # Write to the new file
    with open(filename, "w") as file:
        file.write(content)

    return


def validate_data(data: Dict[str, int]) -> bool:
    # Check if data has necessary fields
    for key in REQUIRED_KEYS:
        if key not in data:
            return False

    for key, value in data.items():
        if not (isinstance(value, int) and 0 <= value <= 100):
            return False

    return True


def get_csv_files_in_folder(dir):
    matches = os.listdir(dir)
    return sorted(matches)


def get_match_sofifa_ids(matches_df: pd.DataFrame, matchId):
    home_team_sofifa_ids_column = "home_xi_sofifa_ids"
    away_team_sofifa_ids_column = "away_xi_sofifa_ids"
    home_team_column = "home_team"
    away_team_column = "away_team"

    row = matches_df.loc[matchId]
    home_sofifa_ids = [
        int(float(id)) for id in row[home_team_sofifa_ids_column].split(",")
    ]
    away_sofifa_ids = [
        int(float(id)) for id in row[away_team_sofifa_ids_column].split(",")
    ]

    return {
        "home_team": row[home_team_column],
        "away_team": row[away_team_column],
        "home_team_sofifa_ids": {
            "goalkeeper": home_sofifa_ids[:1],
            "defenders": home_sofifa_ids[1:5],
            "midfielders": home_sofifa_ids[5:8],
            "forwards": home_sofifa_ids[8:11],
        },
        "away_team_sofifa_ids": {
            "goalkeeper": away_sofifa_ids[:1],
            "defenders": away_sofifa_ids[1:5],
            "midfielders": away_sofifa_ids[5:8],
            "forwards": away_sofifa_ids[8:11],
        },
    }


def get_player_rating_by_sofifa_id(rating_df: pd.DataFrame, sofifa_id):
    for index, row in rating_df.iterrows():
        if "sofifa_id" in row and int(float(row["sofifa_id"])) == sofifa_id:
            get_player_statistics(row)


def get_player_statistics(row):
    print(row["short_name"])
    return


def get_seasons_cli():
    season_pattern = r"\d{8}"
    available_seasons = []
    for i, season in enumerate(seasons, start=1):
        value = "".join(re.findall(season_pattern, season))
        available_seasons.append(f"{i}. {value}")
    return available_seasons


def get_matches_cli(matches_df: pd.DataFrame):
    matches = []
    for index, row in matches_df.iterrows():
        name = str(index + 1) + ". " + row["home_team"] + " VS " + row["away_team"]
        matches.append(name)
    return matches


def print_player(rating_df: pd.DataFrame, players_in_match):
    print("\nHome Team")
    print("\nGoalkeeper")
    for player in players_in_match["home_team_sofifa_ids"]["goalkeeper"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nDefenders")
    for player in players_in_match["home_team_sofifa_ids"]["defenders"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nMidfielders")
    for player in players_in_match["home_team_sofifa_ids"]["midfielders"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nForwards")
    for player in players_in_match["home_team_sofifa_ids"]["forwards"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nAway Team")
    print("\nGoalkeeper")
    for player in players_in_match["away_team_sofifa_ids"]["goalkeeper"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nDefenders")
    for player in players_in_match["away_team_sofifa_ids"]["defenders"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nMidfielders")
    for player in players_in_match["away_team_sofifa_ids"]["midfielders"]:
        get_player_rating_by_sofifa_id(rating_df, player)

    print("\nForwards")
    for player in players_in_match["away_team_sofifa_ids"]["forwards"]:
        get_player_rating_by_sofifa_id(rating_df, player)


if __name__ == "__main__":
    seasons = get_csv_files_in_folder(MATCHES_DIR)
    ratings = get_csv_files_in_folder(RATINGS_DIR)

    available_seasons = "\n".join(get_seasons_cli())
    season = input(f"Select a season and hit enter\n{available_seasons}")

    if not season.isdigit() or int(season) > len(seasons):
        print("Invalid season selected")
        exit()

    season_file_name = seasons[int(season) - 1]
    print(f"Selected season matches file: {season_file_name}")
    rating_file_name = ratings[int(season) - 1]
    print(f"Selected season ratings file: {rating_file_name}\n")

    matches_df = pd.read_csv(f"{MATCHES_DIR}/{season_file_name}")
    rating_df = pd.read_csv(f"{RATINGS_DIR}/{rating_file_name}")

    matches = "\n".join(get_matches_cli(matches_df))
    matchId = input(f"Select a match from {season_file_name} and hit enter\n{matches}")

    players_in_match = get_match_sofifa_ids(matches_df, int(matchId) - 1)

    print_player(rating_df, players_in_match)
