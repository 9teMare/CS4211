#!/usr/bin/env python3
# For macOS with mono installed

import os
import subprocess
import re

def gen_prob(model_file_path):
    output_file_name = model_file_path.replace("/", "_") + ".output"
    output_file_path = "pat_cli/" + output_file_name
    command = ["mono", "pat_cli/PAT3.Console.exe", "-pcsp", model_file_path, output_file_name]
    
    try:
        if not os.path.isfile(output_file_path):
            subprocess.run(command, check=True)
            
        with open(output_file_path, 'r') as f:
            output = f.read()

        pattern = r'Probability \[(\d+\.\d+), (\d+\.\d+)\]'
        match = re.search(pattern, output)
        if match:
            return (float(match.group(1)) + float(match.group(2))) / 2
        else:
            print("Probability not found in PAT output.")
            return None
    except subprocess.CalledProcessError as e:
        print("Error during PAT execution:", e)
        return None
    except FileNotFoundError as e:
        print("Output file not found. Make sure the PAT command is generating the output file correctly.")
        return None

# Example usage
# prob = gen_prob("20152016_12115_AFC_Bournemouth_Aston_Villa_home")
# print(prob)
