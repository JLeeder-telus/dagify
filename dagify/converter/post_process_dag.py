import os
import re
import sys
import datetime
import json

def read_libmemsym_file(file_path, variable_name):
    """
    Read a specific variable from a libmemsym file.

    Args:
        file_path: Path to the libmemsym file
        variable_name: Name of the variable to retrieve

    Returns:
        Value of the variable, or None if not found
    """
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().lstrip('%')  # Strip leading % characters
                    if key.strip() == variable_name:
                        return value.strip()
        print(f"Variable {variable_name} not found in {file_path}")
        return None
    except Exception as e:
        print(f"Error reading libmemsym file {file_path}: {e}")
        return None

def clean_control_m_concat(content):
    """
    Clean up Control-M concatenation syntax in the content.
    
    In Control-M, a period (.) is used for concatenation, but in Python,
    we should remove the period. For example:
    APP_HOME={g_app_home_prefix}.omg/vpop -> APP_HOME={g_app_home_prefix}omg/vpop
    
    Args:
        content: The content to clean up
        
    Returns:
        The cleaned content
    """
    # Pattern to match variable references with concatenation
    pattern = r'(\{[^}]+\})\.([a-zA-Z0-9_/]+)'
    
    # Replace with proper Python syntax
    return re.sub(pattern, r'\1\2', content)

def generate_libmemsym_code(content):
    """
    Generate code to read variables from the libmemsym file.
    
    Args:
        content: The content of the DAG file
        
    Returns:
        Tuple containing:
        - A string with code to be inserted after variables section
        - List of L_ variables that should be read from the libmemsym file
        - Dictionary mapping each L_ variable Python name to its environment variable name
    """
    # Find the component name and locals path
    locals_path_pattern = r"(\w+)_locals_path = f\"(.+)\""
    locals_path_match = re.search(locals_path_pattern, content)
    
    if not locals_path_match:
        print("No locals_path found in the DAG file.")
        return "", [], {}
    
    component_name = locals_path_match.group(1)
    
    # Find all L_ variables - both those using Variable.get() and those already set to None
    l_var_pattern_get = r"l_(\w+) = Variable\.get\(\"L_([^\"]+)\"\)"
    l_var_pattern_none = r"l_(\w+) = None\s+"
    
    l_var_matches_get = re.findall(l_var_pattern_get, content)
    l_var_matches_none = re.findall(l_var_pattern_none, content)
    
    # Combine matches, assuming the variable name is the same as the environment variable name for None-initialized variables
    l_var_matches = l_var_matches_get + [(var, var.upper()) for var in l_var_matches_none]
    
    if not l_var_matches:
        print("No L_ variables found in the DAG file.")
        return "", [], {}
    
    # Generate code to read each L_ variable from the libmemsym file
    code_lines = [
        f"\n    # Read L_ variables from the {component_name} locals file",
        f"    print(f\"Reading variables from {{{{ {component_name}_locals_path }}}}\") "
    ]
    
    l_vars = []
    l_var_mapping = {}
    
    for python_var, env_var in l_var_matches:
        l_vars.append(f"L_{env_var}")
        l_var_mapping[f"l_{python_var}"] = f"L_{env_var}"
        code_line = f"    l_{python_var} = read_libmemsym_file({component_name}_locals_path, \"L_{env_var}\") or l_{python_var}"
        code_lines.append(code_line)
    
    return "\n".join(code_lines), l_vars, l_var_mapping

def remove_libmemsym_from_bash_commands(content):
    """
    Remove libmemsym references from BashOperator bash_command strings.
    
    This function finds all instances of {g_libmemsym_prefix}/{g_env}/VPOPBatch/locals
    in bash_command strings and removes them.
    
    Args:
        content: The content of the DAG file
        
    Returns:
        The cleaned content with libmemsym references removed
    """
    # Pattern to match libmemsym references in bash_command strings
    pattern = r'(bash_command=f".*?)(\{g_libmemsym_prefix\}/\{g_env\}/\w+/locals)(\s+)'
    
    # Replace with just a space
    modified_content = re.sub(pattern, r'\1\3', content)
    
    # Count replacements
    count = content.count('{g_libmemsym_prefix}/{g_env}') - modified_content.count('{g_libmemsym_prefix}/{g_env}')
    
    if count > 0:
        print(f"Removed {count} libmemsym references from bash_command strings")
    
    return modified_content

def post_process_dag_file(file_path):
    """
    Post-process a DAG file to replace Variable.get calls with local variables.
    
    This function:
    1. Reads the content of a DAG file
    2. Identifies all Variable.get calls in bash_command strings
    3. Ensures corresponding variable declarations exist in the variables section
    4. Replaces Variable.get calls with the local variable references
    5. Adds code to read L_ variables from the libmemsym file
    6. Removes libmemsym references from BashOperator bash_command strings
    
    Args:
        file_path: Path to the DAG file to process
    """
    print(f"Post-processing DAG file: {file_path}")
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all Variable.get calls in bash_command strings
    variable_get_pattern = r"Variable\.get\('([^']+)'\)"
    matches = re.findall(variable_get_pattern, content)
    
    # Get unique variable names
    unique_vars = set(matches)
    
    # Find L_ variables
    l_var_pattern = r"l_\w+ = Variable\.get\(\"L_[^\"]+\"\)"
    has_l_vars = bool(re.search(l_var_pattern, content))
    
    # Check if we need to make any changes
    if not unique_vars and not has_l_vars:
        print("No Variable.get calls found in bash_command strings or L_ variables. No changes needed.")
        return
    
    # Find the variables section
    variables_section_pattern = r"(# Get variables from Airflow Variables\s*\n)"
    variables_section_match = re.search(variables_section_pattern, content)
    
    if not variables_section_match:
        print("Variables section not found. Cannot proceed with post-processing.")
        return
    
    # Check which variables are already declared
    declared_vars_pattern = r"(\w+) = Variable\.get\(\"([^\"]+)\"\)"
    declared_vars_matches = re.findall(declared_vars_pattern, content)
    
    # Create a mapping of variable names to their Python variable names
    declared_vars = {var_name: python_var for python_var, var_name in declared_vars_matches}
    
    # Add missing variable declarations
    new_declarations = []
    for var_name in unique_vars:
        if var_name not in declared_vars:
            # Convert to snake_case for Python variable name
            python_var = var_name.lower()
            declared_vars[var_name] = python_var
            new_declarations.append(f"\n    {python_var} = Variable.get(\"{var_name}\")")
    
    # Sort the new declarations to ensure consistent ordering
    new_declarations.sort()
    
    if new_declarations:
        # Insert new declarations after the variables section
        insert_position = variables_section_match.end()
        content = content[:insert_position] + "".join(new_declarations) + content[insert_position:]
    
    # Special handling for ORDERID - replace with datetime
    orderid_pattern = r'(\s*orderid = Variable\.get\("ORDERID"\))'
    orderid_match = re.search(orderid_pattern, content)
    if orderid_match:
        # Replace with datetime
        now_line = '    now = datetime.datetime.now()'
        orderid_replacement = '    orderid = now.strftime("%Y%m%d%H%M%S")'
        # Insert the now line before the orderid line
        content = content.replace(orderid_match.group(1), now_line + '\n' + orderid_replacement + '\n')
    
    # Replace Variable.get calls with local variable references
    for var_name, python_var in declared_vars.items():
        pattern = r"Variable\.get\('" + var_name + r"'\)"
        replacement = python_var
        content = re.sub(pattern, replacement, content)
    
    # Fix any formatting issues with variable declarations
    # Ensure there's a newline between variable declarations
    content = re.sub(r'(Variable\.get\([^\)]+\))(\s*)(\w+\s*=)', r'\1\n\n    \3', content)
    
    # Clean up Control-M concatenation syntax
    content = clean_control_m_concat(content)
    
    # Remove libmemsym references from bash_command strings
    content = remove_libmemsym_from_bash_commands(content)
    
    # Replace L_ variables with None
    l_var_pattern = r"(l_\w+) = Variable\.get\(\"(L_[^\"]+)\"\)"
    l_var_replacements = re.findall(l_var_pattern, content)
    replaced_l_vars_count = len(l_var_replacements)
    content = re.sub(l_var_pattern, r"\1 = None", content)
    
    # Generate code to read variables from the libmemsym file
    libmemsym_code, l_vars, l_var_mapping = generate_libmemsym_code(content)
    
    if libmemsym_code:
        # Find the position to insert the libmemsym code
        # Insert after the component locals path declaration
        component_locals_path_pattern = r"(\w+)_locals_path = f\"(.+)\"\n"
        component_locals_path_match = re.search(component_locals_path_pattern, content)
        
        if component_locals_path_match:
            insert_position = component_locals_path_match.end()
            content = content[:insert_position] + "\n" + libmemsym_code + content[insert_position:]
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Successfully post-processed DAG file: {file_path}")
    print(f"Added {len(new_declarations)} new variable declarations")
    print(f"Replaced {len(declared_vars)} Variable.get calls with local variable references")
    if replaced_l_vars_count > 0:
        print(f"Replaced {replaced_l_vars_count} L_ variables with None")
    if l_vars:
        print(f"Added code to read {len(l_vars)} variables from libmemsym file")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_process_dag.py <dag_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    post_process_dag_file(file_path)
