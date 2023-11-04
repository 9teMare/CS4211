#!/usr/bin/env python3
import os
import csv
import subprocess
from gen_prob_stubs import gen_prob, gen_softmax_home_prob
# from gen_prob import gen_prob
# from gen_softmax_home_prob import gen_softmax_home_prob

def generate_match_url(model_name):
  # Split model_name by `_` separator
  model_name_parts = model_name.split('_')
  match_id = model_name_parts[1]
  return f'https://www.premierleague.com/match/{match_id}'

def go_through_season_directory(season_directory_path):
  season_data = []
  if os.path.isdir(season_directory_path):
    models = sorted(os.listdir(season_directory_path))

    for model in models:
      if model.endswith('_home.pcsp'):
        home_path = os.path.join(season_directory_path, model)
        away_path = home_path.replace('_home.pcsp', '_away.pcsp')

        home_prob = gen_prob(home_path)
        away_prob = gen_prob(away_path)

        softmax_prob = gen_softmax_home_prob(home_prob, away_prob)

        match_url = generate_match_url(model)

        season_data.append([match_url, softmax_prob])

  return season_data

def process_directory(directory_path):
  season_data_by_subdir = {}

  for subdir in os.listdir(directory_path):
    subdir_path = os.path.join(directory_path, subdir)
    if not os.path.isdir(subdir_path):
      continue

    # Initialize season's data structure
    season_data_by_subdir[subdir] = {}

    seasons = os.listdir(subdir_path)

    for season in seasons:
      season_data = go_through_season_directory(os.path.join(subdir_path, season))
      season_data_by_subdir[subdir][season] = season_data
      

  return season_data_by_subdir

def write_to_csv(season_data_by_subdir, directory_to_write_to):
  for subdir, subdir_seasons in season_data_by_subdir.items():
    for season, matches in subdir_seasons.items():
      # Create directory for the CSV file if it does not exist
      output_dir = os.path.join(directory_to_write_to, subdir)
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)

      csv_filename = os.path.join(output_dir, f'{season}.csv')
      with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['match_url', 'home_prob_softmax'])
        for match_url, prob in matches:
          csv_writer.writerow([match_url, prob])

if __name__ == '__main__':
  models_directory = 'models/generated_models'
  output_directory = 'betting_simulation/generated_probabilities'
  subprocess.run(['rm', '-rf', output_directory])
  data = process_directory(models_directory)
  write_to_csv(data, output_directory)


