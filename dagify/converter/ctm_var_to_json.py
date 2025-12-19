#!/usr/bin/env python3
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script to convert Control-M variable files to JSON format.
This script reads a Control-M variable file (with %%\ prefix) and converts it to JSON.
"""

import argparse
import json
import os
import sys


def convert_ctm_var_to_json(input_file, output_file=None, pretty=False):
    """
    Convert a Control-M variable file to JSON format.
    
    Args:
        input_file (str): Path to the Control-M variable file
        output_file (str, optional): Path to the output JSON file. If None, prints to stdout.
        pretty (bool, optional): Whether to format the JSON output with indentation. Defaults to False.
    
    Returns:
        dict: The converted variables as a dictionary
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    variables = {}
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('%%\\'):
                continue
            
            # Remove the %%\ prefix and split by the first equals sign
            line = line[3:]  # Remove '%%\'
            if '=' not in line:
                continue
                
            key, value = line.split('=', 1)
            variables[key] = value
    
    # Output the JSON
    indent = 4 if pretty else None
    json_output = json.dumps(variables, indent=indent)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(json_output)
    else:
        print(json_output)
    
    return variables


def main():
    parser = argparse.ArgumentParser(description='Convert Control-M variable file to JSON')
    parser.add_argument('input_file', help='Path to the Control-M variable file')
    parser.add_argument('-o', '--output', help='Path to the output JSON file (default: stdout)')
    parser.add_argument('-p', '--pretty', action='store_true', help='Format JSON with indentation')
    
    args = parser.parse_args()
    
    try:
        convert_ctm_var_to_json(args.input_file, args.output, args.pretty)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

# python dagify/converter/ctm_var_to_json.py telus_data/config/ctmvar_it04.txt -o telus_data/output/ctmvar_it04.json -p