# For macOS with mono installed

import subprocess
import re

def gen_prob(model_file_name):
    model_file_path = "models/" + model_file_name
    output_file_name = model_file_name + ".output"
    output_file_path = "pat_cli/" + output_file_name
    command = ["mono", "pat_cli/PAT3.Console.exe", "-pcsp", model_file_path, output_file_name]
    
    try:
        subprocess.run(command, check=True)

        with open(output_file_path, 'r') as f:
            output = f.read()

        pattern = r'Probability \[(\d+\.\d+), (\d+\.\d+)\]'
        match = re.search(pattern, output)
        if match:
            return (float(match.group(1)), float(match.group(2)))
        else:
            print("Probability not found in PAT output.")
            return None
    except subprocess.CalledProcessError as e:
        print("Error during PAT execution:", e)
        return None
    except FileNotFoundError:
        print("Output file not found. Make sure the PAT command is generating the output file correctly.")
        return None

# Example usage:
# prob = gen_prob("sample.pcsp")
# print(prob)