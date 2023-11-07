import os

main_directory = 'betting_simulation/generated_probabilities'

def rename_files(subdir):
  for filename in os.listdir(subdir):
    if filename.endswith('.csv') and filename.startswith('20'):
      new_filename = filename[2:4] + filename[6:8] + '.csv'
      old_file = os.path.join(subdir, filename)
      new_file = os.path.join(subdir, new_filename)
      os.rename(old_file, new_file)
      print(f"Renamed {old_file} to {new_file}")

for folder in os.listdir(main_directory):
  # Construct the full path to the subdirectory
  subdir_path = os.path.join(main_directory, folder)
  # Check if it is indeed a directory
  if os.path.isdir(subdir_path):
    rename_files(subdir_path)