# Proxy Settings for TELUS Network

## Required Proxy Configuration

**IMPORTANT: Always set proxy environment variables before running DAGify or installing packages.**

When testing, installing packages, or accessing external resources within the TELUS network environment, you must set the proxy environment variables first. This is mandatory for proper connectivity.

### PowerShell Command Format

Always use this exact format when running DAGify:

```powershell
$env:HTTPS_PROXY="http://webproxystatic-on.tsl.telus.com:8080"; $env:HTTP_PROXY="http://webproxystatic-on.tsl.telus.com:8080"; python DAGify.py [options]
```

For example, to convert a Control-M XML file:

```powershell
$env:HTTPS_PROXY="http://webproxystatic-on.tsl.telus.com:8080"; $env:HTTP_PROXY="http://webproxystatic-on.tsl.telus.com:8080"; python DAGify.py -s telus_data/BIL-EXF.DRF.xml -o telus_data/output/
```

### Important Notes

1. **Always Set Proxy**: The TELUS network requires these proxy settings for any external connections.
  
2. **PowerShell Syntax**: Remember that PowerShell uses semicolons (`;`) to chain commands and `$env:VARIABLE_NAME` for environment variables.

3. **Session Scope**: These settings are only applied for the current PowerShell session. If you open a new terminal, you'll need to set them again.

4. **Applies to All External Commands**: This proxy configuration is required for all tools that access the internet, including:
   - pip (for package installation)
   - git (for repository operations)
   - curl/wget (for downloading resources)
   - Any API calls made by DAGify
