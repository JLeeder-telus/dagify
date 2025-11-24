import os
import sys
import re

# Add the dagify directory to the Python path
sys.path.append('.')

# Import the Rule class from dagify.converter.rules
from dagify.converter.rules import Rule

def test_env_var_to_python():
    """Test the env_var_to_python rule with various inputs."""
    rule = Rule()
    
    # Test cases
    test_cases = [
        "%%G_COMMON_SCRIPT_HOME/fw-SFTX.sh",
        "ctmfw '%%G_DATA_HOME_PREFIX.bil/exf/data/inbox/%%L_BILL_EC_FP_SUB_NS/%%L_BILL_EC_FP_PAT_LOW' CREATE 0 600 10 3 1380",
        "Simple string with no env vars",
        "%%VAR1 and %%VAR2 in the same string",
        "%%VAR1",
    ]
    
    print("Testing env_var_to_python rule:")
    print("-" * 50)
    
    for test_case in test_cases:
        result = rule.run(["env_var_to_python", test_case])
        print(f"\nInput:  {test_case}")
        print(f"Output: {result}")
        
        # Demonstrate how it would work in a real command
        if '%%' in test_case:
            print("\nIn a real command:")
            # Set some environment variables for testing
            os.environ['G_COMMON_SCRIPT_HOME'] = '/path/to/scripts'
            os.environ['G_DATA_HOME_PREFIX'] = '/data'
            os.environ['L_BILL_EC_FP_SUB_NS'] = 'subdir'
            os.environ['L_BILL_EC_FP_PAT_LOW'] = 'pattern'
            os.environ['VAR1'] = 'value1'
            os.environ['VAR2'] = 'value2'
            
            # Evaluate the result as a Python expression if possible
            try:
                # For f-string format
                if result.startswith("f\"") or result.startswith("f'"):
                    # Set environment variables for testing
                    os.environ['G_COMMON_SCRIPT_HOME'] = '/path/to/scripts'
                    os.environ['G_DATA_HOME_PREFIX'] = '/data'
                    os.environ['L_BILL_EC_FP_SUB_NS'] = 'subdir'
                    os.environ['L_BILL_EC_FP_PAT_LOW'] = 'pattern'
                    os.environ['VAR1'] = 'value1'
                    os.environ['VAR2'] = 'value2'
                    
                    # Extract variable names from the f-string
                    var_names = re.findall(r"{([^}]+)}", result)
                    
                    # Create a local dictionary with the variables
                    local_vars = {}
                    for var in var_names:
                        env_var = var.upper()
                        local_vars[var] = os.environ.get(env_var, '')
                    
                    # Evaluate the f-string
                    eval_result = eval(result, {}, local_vars)
                    print(f"Evaluated: {eval_result}")
                elif result.startswith("os.environ.get("):
                    # For backward compatibility with old format
                    eval_result = eval(result)
                    print(f"Evaluated: {eval_result}")
                else:
                    # For strings without environment variables
                    print(f"Evaluated: {result}")
            except Exception as e:
                print(f"Error evaluating: {e}")

if __name__ == "__main__":
    test_env_var_to_python()
