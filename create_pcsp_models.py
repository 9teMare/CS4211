import os
import pandas as pd
from multiprocessing import Pool, cpu_count
from create_pcsp_model import (
  MATCHES_DIR,
  RATINGS_DIR,
  get_csv_files_in_folder,
  get_match_name,
  get_match_sofifa_ids,
  generate_data_dict,
  create_pcsp_model
)

LOGS_FOLDER = "./logs"


if __name__ == "__main__":
  all_seasons = get_csv_files_in_folder(MATCHES_DIR)
  all_ratings = get_csv_files_in_folder(RATINGS_DIR)

  for i in range(0, len(all_seasons)):
    season_idx = i
    season_file_name = all_seasons[season_idx]
    ratings_file_name = all_ratings[season_idx]

    matches_df = pd.read_csv(f"{MATCHES_DIR}/{season_file_name}")
    ratings_df = pd.read_csv(f"{MATCHES_DIR}/{ratings_file_name}")

    selected_season = season_file_name[-12:-4]

    for match_idx, row in matches_df.iterrows():
      match_name = get_match_name(matches_df, match_idx)

      players_in_match = get_match_sofifa_ids(matches_df, match_idx)

      home_data_dict, away_data_dict = generate_data_dict(rating_df, players_in_match)

      if home_data_dict is None or away_data_dict is None:
        print(f"Could not generate data for match {match_idx}, {match_name} of season {selected_season}.")
        continue
      
      base_file_name = f"{selected_season}__{match_name}"

      create_pcsp_model(f"{base_file_name}_home.pcsp", home_data_dict)
      create_pcsp_model(f"{base_file_name}_away.pcsp", away_data_dict)








