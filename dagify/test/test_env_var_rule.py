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
                # For simple replacements
                if result.startswith("os.environ.get("):
                    eval_result = eval(result)
                    print(f"Evaluated: {eval_result}")
                else:
                    # For more complex strings with f-string syntax
                    # Extract the parts between ' + os.environ.get(...) + '
                    parts = re.findall(r"os\.environ\.get\('([^']+)'", result)
                    eval_result = test_case
                    for var in parts:
                        eval_result = eval_result.replace(f"%%{var}", os.environ.get(var, ''))
                    print(f"Evaluated: {eval_result}")
            except Exception as e:
                print(f"Error evaluating: {e}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    test_env_var_to_python()
