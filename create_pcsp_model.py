import os
import csv
from typing import Dict

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
    return matches


def get_match_sofifa_ids(csv_file):
    home_team_sofifa_ids_column = "home_xi_sofifa_ids"
    away_team_sofifa_ids_column = "away_xi_sofifa_ids"
    home_team_column = "home_team"
    away_team_column = "away_team"

    sofifa_ids = []
    with open(f"{MATCHES_DIR}/{csv_file}", mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if (
                home_team_column in row
                and away_team_column in row
                and home_team_sofifa_ids_column in row
                and away_team_sofifa_ids_column in row
            ):
                home_sofifa_ids = [
                    int(float(id)) for id in row[home_team_sofifa_ids_column].split(",")
                ]
                away_sofifa_ids = [
                    int(float(id)) for id in row[away_team_sofifa_ids_column].split(",")
                ]
                sofifa_ids.append(
                    {
                        "home_team": row[home_team_column],
                        "away_team": row[away_team_column],
                        "home_team_sofifa_ids": {
                            "goalkeeper": home_sofifa_ids[0],
                            "defenders": home_sofifa_ids[1:5],
                            "midfielders": home_sofifa_ids[5:8],
                            "forwards": home_sofifa_ids[8:11],
                        },
                        "away_team_sofifa_ids": {
                            "goalkeeper": away_sofifa_ids[0],
                            "defenders": away_sofifa_ids[1:5],
                            "midfielders": away_sofifa_ids[5:8],
                            "forwards": away_sofifa_ids[8:11],
                        },
                    }
                )
            else:
                sofifa_ids.append(None)
    return sofifa_ids


def get_player_rating_by_sofifa_id(csv_file, sofifa_id):
    with open(f"{RATINGS_DIR}/{csv_file}", mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if "sofifa_id" in row and int(float(row["sofifa_id"])) == sofifa_id:
                get_player_statistics(row)
    return


def get_player_statistics(row):
    return


if __name__ == "__main__":
    matches = get_csv_files_in_folder(MATCHES_DIR)
    ratings = get_csv_files_in_folder(RATINGS_DIR)

    for match in matches:
        print(get_match_sofifa_ids(match))
