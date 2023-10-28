#!/usr/bin/env python3
import sys
import os
import pandas as pd
from typing import Dict
from threading import Lock
from generate_player_probLoseBall import generate_player_probLoseBall
import re

MODELS_DIR = "./models"
GENERATED_MODELS_DIR = "./generated_models"
DEFAULT_TEMPLATE_FILENAME = "template.pcsp"

PLAYER_RATINGS_GENERATOR = {
    "shortPass": (lambda player: player["attacking_short_passing"]),
    "longPass": (lambda player: player["skill_long_passing"]),
    "probLoseBall": (
        lambda player_for, player_against: generate_player_probLoseBall(
            player_for, player_against
        )
    ),
    "longShot": (lambda player: player["power_long_shots"]),
    "finish": (lambda player: player["attacking_finishing"]),
    "volley": (lambda player: player["attacking_volleys"]),
    "header": (lambda player: player["attacking_heading_accuracy"]),
    "dk_gkRating": (lambda def_keeper: int(def_keeper["overall"])),
}

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

KEEPER_POSITIONS = ["GK"]
DEFENDER_POSITIONS = ["RD", "CRD", "CLD", "LD"]
MIDFIELDER_POSITIONS = ["RM", "CM", "LM"]
FORWARD_POSITIONS = ["RF", "CF", "LF"]

DEFENDING_POSITION_MAPPER = {
    "RD": "LM",
    "CRD": "LF",
    "CLD": "CF",
    "LD": "RF",
    "RM": "CM",
    "CM": "RM",
    "LM": "RD",
    "RF": "LD",
    "CF": "CLD",
    "LF": "CRD",
}

class DataValidationError(Exception):
    pass

class TemplateNotFoundError(Exception):
    pass

class FileExistsError(Exception):
    pass

def create_pcsp_model(filename: str, data: Dict[str, int], selected_season: str, template_file_name: str) -> None:
  # Validate data to check if it has the relevant data
  if not validate_data(data):
    raise DataValidationError("Data dictionary passed is not valid, please check.")

  # Check if template file exists
  if not os.path.exists(f"{MODELS_DIR}/{template_file_name}"):
    raise TemplateNotFoundError("Template file not found")

  with open(f"{MODELS_DIR}/{template_file_name}", "r") as file:
    template = file.read()

  # Replace placeholders with actual data
  try:
    content = template.format(**data)
  except KeyError as e:
    raise KeyError(f"Key error: {e} not found in data.")

  # Define the sub-folder path
  sub_folder_path = f"{MODELS_DIR}/{GENERATED_MODELS_DIR}/{selected_season}"

  # Atomically create sub-folder if it does not exist
  os.makedirs(sub_folder_path, exist_ok=True)

  # Combine the sub-folder path with the desired filename
  file_path = os.path.join(sub_folder_path, filename)

  # Check if target file exists to avoid overwriting.
  # Files do not have to be written to atomically since we guarantee
  # unique file paths
  if os.path.exists(file_path):
    raise FileExistsError(f"{file_path} already exists. Choose a different name or path.")

  # Write to the new file
  with open(file_path, "w") as file:
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


def get_player_rating_by_sofifa_id(rating_df: pd.DataFrame, sofifa_id) -> pd.Series:
    for _, row in rating_df.iterrows():
        if "sofifa_id" in row and int(float(row["sofifa_id"])) == sofifa_id:
            # get_player_statistics(row)
            return row


def get_player_statistics(row):
    print(row["short_name"] if pd.notna(row["short_name"]) else row["long_name"])
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


def get_match_name(matches_df: pd.DataFrame, match_id: int):
    home_team_name = matches_df.iloc[match_id]["home_team"]
    away_team_name = matches_df.iloc[match_id]["away_team"]

    return f"{home_team_name}_{away_team_name}"


def print_players(rating_df: pd.DataFrame, players_in_match):
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


def generate_data_dict_for_team(for_stats, against_stats):
    data = {}

    # keeper stats
    try:
      data["ak_shortPass"] = PLAYER_RATINGS_GENERATOR["shortPass"](
          for_stats[KEEPER_POSITIONS[0]]
      )
    except Exception as e:
      raise Exception(f"Could not get shortPass rating for keeper -> {against_stats[KEEPER_POSITIONS[0]][0]}, sofifa id: {against_stats[KEEPER_POSITIONS[0]]['sofifa_id']}")
    try:
      data["ak_longPass"] = PLAYER_RATINGS_GENERATOR["longPass"](
          for_stats[KEEPER_POSITIONS[0]]
      )
    except Exception as e:
      raise Exception(f"Could not get longPass rating for keeper -> {against_stats[KEEPER_POSITIONS[0]][0]}, sofifa id: {against_stats[KEEPER_POSITIONS[0]]['sofifa_id']}")
    try:
      data["dk_gkRating"] = PLAYER_RATINGS_GENERATOR["dk_gkRating"](
          against_stats[KEEPER_POSITIONS[0]]
      )
    except Exception as e:
      raise Exception(f"Could not get overall rating for keeper -> {against_stats[KEEPER_POSITIONS[0]][0]}, sofifa id: {against_stats[KEEPER_POSITIONS[0]]['sofifa_id']}")
    

    # defender stats
    for position in DEFENDER_POSITIONS:
        for_player = for_stats[position]
        against_player = against_stats[DEFENDING_POSITION_MAPPER[position]]

        short_pass_rating = PLAYER_RATINGS_GENERATOR["shortPass"](for_player)
        long_pass_rating = PLAYER_RATINGS_GENERATOR["longPass"](for_player)
        try:
          prob_lose_ball = PLAYER_RATINGS_GENERATOR["probLoseBall"](
              for_player, against_player
          )
        except Exception as e:
          raise Exception(f"Could not prob_lose_ball (for DEFENDER -> {for_player[0]}, sofifa id: {for_player['sofifa_id']}, against player -> {against_player[0]}, sofifa id: {against_player['sofifa_id']}). Error: {e}.")

        data[f"a{position.lower()}_shortPass"] = short_pass_rating
        data[f"a{position.lower()}_longPass"] = long_pass_rating
        data[f"a{position.lower()}_probLoseBall"] = prob_lose_ball

    # midfielder stats
    for position in MIDFIELDER_POSITIONS:
        for_player = for_stats[position]
        against_player = against_stats[DEFENDING_POSITION_MAPPER[position]]

        short_pass_rating = PLAYER_RATINGS_GENERATOR["shortPass"](for_player)
        long_pass_rating = PLAYER_RATINGS_GENERATOR["longPass"](for_player)
        long_shot_rating = PLAYER_RATINGS_GENERATOR["longShot"](for_player)
        try:
          prob_lose_ball = PLAYER_RATINGS_GENERATOR["probLoseBall"](
              for_player, against_player
          )
        except Exception as e:
          raise Exception(f"Could not prob_lose_ball (for MIDFIELDER -> {for_player[0]}, sofifa id: {for_player['sofifa_id']}, against player -> {against_player[0]}, sofifa id: {against_player['sofifa_id']}). Error: {e}.")
        data[f"a{position.lower()}_shortPass"] = short_pass_rating
        data[f"a{position.lower()}_longPass"] = long_pass_rating
        data[f"a{position.lower()}_longShot"] = long_shot_rating
        data[f"a{position.lower()}_probLoseBall"] = prob_lose_ball

    for position in FORWARD_POSITIONS:
        for_player = for_stats[position]
        against_player = against_stats[DEFENDING_POSITION_MAPPER[position]]

        finish_rating = PLAYER_RATINGS_GENERATOR["finish"](for_player)
        volley_rating = PLAYER_RATINGS_GENERATOR["volley"](for_player)
        long_shot_rating = PLAYER_RATINGS_GENERATOR["longShot"](for_player)
        header_rating = PLAYER_RATINGS_GENERATOR["header"](for_player)
        try:
          prob_lose_ball = PLAYER_RATINGS_GENERATOR["probLoseBall"](
              for_player, against_player
          )
        except Exception as e:
          raise Exception(f"Could not prob_lose_ball (for FORWARD -> {for_player[0]}, sofifa id: {for_player['sofifa_id']}, against player -> {against_player[0]}, sofifa id: {against_player['sofifa_id']}). Error: {e}.")
        data[f"a{position.lower()}_finish"] = finish_rating
        data[f"a{position.lower()}_longShot"] = long_shot_rating
        data[f"a{position.lower()}_volley"] = volley_rating
        data[f"a{position.lower()}_header"] = header_rating
        data[f"a{position.lower()}_probLoseBall"] = prob_lose_ball

    return data


def generate_data_dict(rating_df: pd.DataFrame, players_in_match: Dict[str, dict]):
    home_stats = {}
    away_stats = {}

    positions = [
        ("goalkeeper", KEEPER_POSITIONS),
        ("defenders", DEFENDER_POSITIONS),
        ("midfielders", MIDFIELDER_POSITIONS),
        ("forwards", FORWARD_POSITIONS)
    ]

    for position, position_constants in positions:
        for i, player_id in enumerate(players_in_match["home_team_sofifa_ids"][position]):
            home_stats[position_constants[i]] = get_player_rating_by_sofifa_id(rating_df, player_id)
            
        for i, player_id in enumerate(players_in_match["away_team_sofifa_ids"][position]):
            away_stats[position_constants[i]] = get_player_rating_by_sofifa_id(rating_df, player_id)

    try:
        home_data_dict = generate_data_dict_for_team(home_stats, away_stats)
        away_data_dict = generate_data_dict_for_team(away_stats, home_stats)

        return (home_data_dict, away_data_dict)
    except Exception as e:
        raise Exception(f"An error occurred while generating data dict: {str(e)}") from e


if __name__ == "__main__":
    if len(sys.argv) > 1:
      template_filename = sys.argv[1]
    else:
      template_filename = DEFAULT_TEMPLATE_FILENAME

    seasons = get_csv_files_in_folder(MATCHES_DIR)
    ratings = get_csv_files_in_folder(RATINGS_DIR)

    available_seasons = "\n".join(get_seasons_cli())
    season = input(f"Select a season and hit enter\n{available_seasons}\n")

    if not season.isdigit() or int(season) > len(seasons):
        print("Invalid season selected")
        exit()

    season_file_name = seasons[int(season) - 1]
    print(f"Selected season matches file: {season_file_name}")
    rating_file_name = ratings[int(season) - 1]
    print(f"Selected season ratings file: {rating_file_name}\n")
    selected_season = season_file_name[-12:-4]

    matches_df = pd.read_csv(f"{MATCHES_DIR}/{season_file_name}")
    rating_df = pd.read_csv(f"{RATINGS_DIR}/{rating_file_name}")

    matches = "\n".join(get_matches_cli(matches_df))
    matchId = input(
        f"Select a match from {season_file_name} and hit enter\n{matches}\n"
    )

    match_name = get_match_name(matches_df, int(matchId) - 1)

    print(match_name)

    players_in_match = get_match_sofifa_ids(matches_df, int(matchId) - 1)

    print_players(rating_df, players_in_match)

    try:
        home_data_dict, away_data_dict = generate_data_dict(rating_df, players_in_match)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

    base_file_name = f"{selected_season}__{match_name}"

    try:
        create_pcsp_model(f"{base_file_name}_home.pcsp", home_data_dict, selected_season, template_filename)
        create_pcsp_model(f"{base_file_name}_away.pcsp", away_data_dict, selected_season, template_filename)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

    print(f"Generated models for {base_file_name} successfully.")

