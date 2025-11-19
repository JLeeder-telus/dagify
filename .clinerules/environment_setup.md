# Environment Setup Guidelines

## Proxy Configuration

When installing packages or accessing external resources, always set the proxy environment variables first. This is required for connectivity in the TELUS network environment.

### PowerShell Syntax

Always use PowerShell syntax for terminal commands. PowerShell uses different syntax than bash/cmd for environment variables and command chaining.

```powershell
# Setting proxy environment variables in PowerShell
$env:HTTPS_PROXY="http://webproxystatic-on.tsl.telus.com:8080"
$env:HTTP_PROXY="http://webproxystatic-on.tsl.telus.com:8080"

# Example: Installing packages with pip
pip install -r requirements.txt
```

### Important Notes

1. **Command Chaining**: 
   - PowerShell uses semicolons (`;`) to chain commands, not `&&` as in bash
   - Example: `$env:HTTPS_PROXY="http://webproxystatic-on.tsl.telus.com:8080"; pip install package-name`

2. **Environment Variables**:
   - PowerShell uses `$env:VARIABLE_NAME` syntax, not `export VARIABLE_NAME` as in bash
   - Variables set this way are only available in the current PowerShell session

3. **Always Set Proxy Before Package Installation**:
   - Set proxy variables before running any `pip install` commands
   - This applies to all package installations, including requirements.txt

4. **Package Installation Best Practices**:
   - Always use `-r requirements.txt` when installing project dependencies
   - For individual packages not in requirements.txt, document them for future reference
