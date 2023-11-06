#!/usr/bin/env python3
import os
import csv
import subprocess
from multiprocessing import cpu_count, Pool
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
# Used below imports to test
# from gen_prob_stubs import gen_prob, gen_softmax_home_prob
from gen_prob import gen_prob
from gen_softmax_home_prob import gen_softmax_home_prob

CPU_COUNT = cpu_count()
THREAD_TO_CPU_RATIO = 2
MAX_PROCESS_WORKERS = CPU_COUNT * THREAD_TO_CPU_RATIO
MAX_THREAD_WORKERS = MAX_PROCESS_WORKERS * THREAD_TO_CPU_RATIO

# Each process handles probability generation for 1 model, 1 season
# Form subtasks of model type, season
# Within 1 model type, 1 season, use thread pooling to handle concurrent probability generation
# Add to thread safe buffer protected by a lock
# At the end, wait for threads and then write to csv

def generate_match_url(model_name):
  model_name_parts = model_name.split('_')
  match_id = model_name_parts[1]
  return f'https://www.premierleague.com/match/{match_id}'

def process_model(model, season_directory_path, lock, season_data):
  if model.endswith('_home.pcsp'):
    away_model = model.replace('_home.pcsp', '_away.pcsp')
    away_path = os.path.join(season_directory_path, away_model)

    if not os.path.isfile(away_path):
      print(f"Error: {away_path} does not exist, skipping.")
      return

    home_path = os.path.join(season_directory_path, model)

    home_prob = gen_prob(home_path, model)
    print("home_prob: {0}".format(home_prob))
    away_prob = gen_prob(away_path, away_model)
    print("away_prob: {0}".format(away_prob))
    softmax_prob = gen_softmax_home_prob(home_prob, away_prob)
    print("softmax_home_prob: {0}".format(softmax_prob))

    match_url = generate_match_url(model)

    with lock:
      season_data.append([match_url, softmax_prob])

def write_to_csv(subdir, season, output_directory, season_data):
  output_directory_to_check = os.path.join(output_directory, subdir)
  # Atomically make directory if not exist, else don't error
  os.makedirs(output_directory_to_check, exist_ok=True)
  
  csv_filename = os.path.join(output_directory_to_check, f'{season}.csv')

  with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['match_url', 'home_prob_softmax'])
    for match_url, prob in season_data:
      csv_writer.writerow([match_url, prob])

def process_single_season(subdir, subdir_path, season, output_directory):
  season_directory_path = os.path.join(subdir_path, season)
  season_data = []
  season_data_lock = Lock()

  if os.path.isdir(season_directory_path):
    models = sorted(os.listdir(season_directory_path))

    with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as executor:
      futures = [executor.submit(process_model, model, season_directory_path, season_data_lock, season_data) for model in models]
      wait(futures)
  
  if len(season_data):
    write_to_csv(subdir, season, output_directory, season_data)

def wrapper(args):
  return process_single_season(*args)

if __name__ == '__main__':
  models_directory = 'models/generated_models'
  output_directory = 'betting_simulation/generated_probabilities'
  subprocess.run(['rm', '-rf', output_directory])
  
  # Break problem into sub tasks for problems
  tasks = []

  for subdir in os.listdir(models_directory):
    subdir_path = os.path.join(models_directory, subdir)

    if not os.path.isdir(subdir_path):
      continue

    for season in os.listdir(subdir_path):
      task = (subdir, subdir_path, season, output_directory)
      tasks.append(task)
  
  with Pool(processes=MAX_PROCESS_WORKERS) as pool:
    pool.map(wrapper, tasks)
