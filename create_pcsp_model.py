import os
from typing import Dict

TEMPLATE_FILENAME = 'template.pcsp'

REQUIRED_KEYS = [
  "ak_shortPass", "ak_longPass",
  "ard_shortPass", "ard_longPass", "ard_probLoseBall",
  "acrd_shortPass", "acrd_longPass", "acrd_probLoseBall",
  "acld_shortPass", "acld_longPass", "acld_probLoseBall",
  "ald_shortPass", "ald_longPass", "ald_probLoseBall",
  "arm_shortPass", "arm_longPass", "arm_longShot", "arm_probLoseBall",
  "acm_shortPass", "acm_longPass", "acm_longShot", "acm_probLoseBall",
  "alm_shortPass", "alm_longPass", "alm_longShot", "alm_probLoseBall",
  "arf_finish", "arf_longShot", "arf_volley", "arf_header", "arf_probLoseBall",
  "acf_finish", "acf_longShot", "acf_volley", "acf_header", "acf_probLoseBall",
  "alf_finish", "alf_longShot", "alf_volley", "alf_header", "alf_probLoseBall",
  "dk_gkRating"
]

def create_pcsp_model(filename: str, data: Dict[str, int]) -> None:
  # Validate data to check if it has the relevant data 
  if not validate_data(data):
    print("Data dictionary passed is not valid, please check.")
    return
  
  # Check if template file exists
  if not os.path.exists(TEMPLATE_FILENAME):
    print("Template file not found")
    return

  with open(TEMPLATE_FILENAME, 'r') as file:
    template = file.read()
  
  # Replace placeholders with actual data
  content = template.format(**data)

  # Check if target file exists to avoid overwriting
  if os.path.exists(filename):
    print(f"{filename} already exists. Choose a different name or path.")
    return

  # Write to the new file
  with open(filename, 'w') as file:
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
