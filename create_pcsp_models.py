#!/usr/bin/env python3
import sys
import os
import pandas as pd
from multiprocessing import cpu_count, Pool
from create_pcsp_model import (
  DEFAULT_TEMPLATE_FILENAME,
  MATCHES_DIR,
  RATINGS_DIR,
  get_csv_files_in_folder,
  get_match_name,
  get_match_sofifa_ids,
  generate_data_dict,
  create_pcsp_model,
)

CPU_COUNT = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", cpu_count()))
THREAD_TO_CPU_RATIO = 2
MAX_WORKERS = CPU_COUNT * THREAD_TO_CPU_RATIO

def process_single_match(matches_df, ratings_df, match_idx, selected_season, template_filename):
  match_name = get_match_name(matches_df, match_idx)
  players_in_match = get_match_sofifa_ids(matches_df, match_idx)

  try:
    home_data_dict, away_data_dict = generate_data_dict(ratings_df, players_in_match)
  except Exception as e:
    print(f"Error occurred for {selected_season} {match_idx} {match_name}: {e}", flush=True)
    return

  base_file_name = f"{selected_season}__{match_name}"

  try:
    create_pcsp_model(f"{base_file_name}_home.pcsp", home_data_dict, selected_season, template_filename)
    create_pcsp_model(f"{base_file_name}_away.pcsp", away_data_dict, selected_season, template_filename)
  except Exception as e:
    print(f"Error occurred for {selected_season} {match_idx} {match_name}: {e}", flush=True)
    return

  print(f"Generated models for match {match_idx}, {match_name} of season {selected_season}.", flush=True)

def wrapper(args):
  return process_single_match(*args)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    template_filename = sys.argv[1]
  else:
    template_filename = DEFAULT_TEMPLATE_FILENAME

  all_seasons = get_csv_files_in_folder(MATCHES_DIR)
  all_ratings = get_csv_files_in_folder(RATINGS_DIR)

  tasks = []

  for i in range(0, len(all_seasons)):
    season_idx = i
    season_file_name = all_seasons[season_idx]
    ratings_file_name = all_ratings[season_idx]

    matches_df = pd.read_csv(f"{MATCHES_DIR}/{season_file_name}")
    ratings_df = pd.read_csv(f"{RATINGS_DIR}/{ratings_file_name}")

    selected_season = season_file_name[-12:-4]

    for match_idx, row in matches_df.iterrows():
      task = (matches_df, ratings_df, match_idx, selected_season, template_filename)
      tasks.append(task)
  

  with Pool(processes=MAX_WORKERS) as pool:
    pool.map(wrapper, tasks)
