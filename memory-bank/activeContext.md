# DAGify Active Context

## Current Focus

DAGify is currently in a stable state with core functionality for converting Control-M workflows to Apache Airflow DAGs. The project has established a solid foundation with the following capabilities:

1. **Control-M Conversion**: Robust support for converting Control-M XML job definitions to Airflow DAGs
2. **Template System**: Flexible template-based conversion for different job types
3. **Dependency Handling**: Preservation of job dependencies within and across DAGs
4. **Reporting**: Detailed conversion reports highlighting successes and areas needing attention
5. **Multiple Interfaces**: Both CLI and web-based UI for different usage scenarios

## Recent Changes

Recent development has focused on:

1. **Airflow Variable Integration**: Implemented support for loading g_ variables from Airflow Variable.get() instead of environment variables, making DAGs more configurable through the Airflow UI
2. **Dynamic ORDERID Generation**: Added functionality to replace ORDERID variable with a datetime-based value (now.strftime("%Y%m%d%H%M%S")) for better runtime flexibility
3. **Airflow 3.1 Compatibility**: Updated DAG template to use `schedule` instead of `schedule_interval` for compatibility with Airflow 3.1
4. **Post-Processing Pipeline**: Created a post-processing script to replace Variable.get() calls with local variable references in bash_command strings, improving code readability and performance
5. **Control-M Syntax Cleanup**: Added functionality to clean up Control-M concatenation syntax (periods used for concatenation) in the generated DAG files, ensuring proper Python syntax
6. **DAG Owner from RUN_AS**: Added functionality to set the DAG owner from the RUN_AS attribute in the Control-M XML file, ensuring proper ownership in Airflow
7. **Operator-Level Queue Settings**: Improved queue mapping by moving queue settings from DAG-level to operator-level, allowing different tasks within the same DAG to use different queues
8. **Server-Based Queue Mapping**: Enhanced the queue mapping logic to intelligently assign queue values based on server numbers in NODEID (e.g., "OMG_BATCH2_SVR" maps to "kidc" queue due to the number "2"), ensuring proper workload distribution
9. **Improved L_ Variable Handling**: Enhanced handling of L_ variables to source them exclusively from libmemsym files rather than Airflow Variables, ensuring better environment isolation
10. **LibMemSym File Format Support**: Enhanced the `read_libmemsym_file` function to handle variable names with double percent sign (%%) prefixes, ensuring compatibility with the TELUS libmemsym file format (e.g., %%L_GCP_UID=value)
11. **telus_data Protection**: Added a file access restriction rule to prevent editing of files in the telus_data directory, preserving the integrity of source Control-M job definitions
12. **Environment Variable Handling**: Enhanced the `rule_env_var_to_python` method to properly handle Control-M environment variables in Python code, including special handling for variables ending with `_prefix` followed by a period
6. **Control-M Job Template**: Updated the template to convert Control-M jobs with TASKTYPE="Job" to Airflow SSHOperator with proper f-string formatting for environment variables
7. **Proxy Configuration**: Enhanced documentation for TELUS network proxy requirements, adding explicit instructions for Cline to run proxy configuration commands when starting a new terminal
8. **PowerShell Syntax**: Documented PowerShell syntax requirements for Windows environments
9. **VM Setup Guide**: Created a comprehensive guide for setting up DAGify on a GCP VM
10. **Airflow Integration**: Fixed Pylance warnings by properly installing Apache Airflow dependencies
11. **Automic Support**: Initial implementation of support for Automic job definitions
12. **Web UI Improvements**: Enhanced user experience in the web interface
13. **Report Generation**: More comprehensive reporting capabilities
14. **Docker Integration**: Improved containerization for easier deployment
15. **Documentation**: Better documentation of usage patterns and extension points

## Current Challenges

The project is currently addressing several challenges:

1. **Template Coverage**: Expanding the range of templates to cover more job types
2. **Complex Dependencies**: Handling complex dependency patterns between jobs
3. **Scheduling Translation**: Accurately translating scheduling information between platforms
4. **Performance Optimization**: Improving performance for large XML files
5. **Error Handling**: More robust error handling and reporting

## Active Decisions

Several key decisions are currently being considered or have recently been made:

1. **Template Standardization**: Establishing consistent patterns for template development
2. **Configuration Simplification**: Making the configuration process more intuitive
3. **Validation Enhancement**: Improving validation of templates and configurations
4. **Extension Mechanism**: Formalizing the approach for extending the tool
5. **Testing Strategy**: Enhancing the testing framework for better coverage

## Next Steps

The immediate roadmap includes:

1. **Template Expansion**: Develop additional templates for other common job types
2. **Automic Support Enhancement**: Improve and expand support for Automic
3. **Documentation Improvement**: Create more comprehensive documentation
4. **Error Handling**: Enhance error reporting and recovery
5. **Performance Optimization**: Optimize memory usage for large files
6. **Parameter Handling**: Enhance parameter handling in templates

## Current Limitations

Current known limitations that are being addressed:

1. **Complex Job Types**: Some specialized job types are not yet fully supported
2. **Custom Logic**: Complex custom logic in workflows may not be fully captured
3. **Scheduling Differences**: Some scheduling patterns don't translate directly
4. **Large File Performance**: Very large XML files may cause performance issues
5. **External Dependencies**: Limited handling of dependencies on external systems

## Integration Points

Key integration points with other systems:

1. **Apache Airflow**: Generated DAGs need to be compatible with Airflow's expectations
2. **Google Cloud Composer**: Ensuring compatibility with Google Cloud Composer
3. **CI/CD Pipelines**: Integration with deployment pipelines for automated conversion
4. **Version Control**: Workflow for managing converted DAGs in version control
5. **Monitoring Systems**: Potential integration with monitoring for conversion processes

## User Feedback

Recent user feedback has highlighted:

1. **Template Customization**: Need for more guidance on customizing templates
2. **Error Messages**: Requests for more descriptive error messages
3. **Conversion Reports**: Appreciation for detailed conversion reports
4. **Web UI**: Positive response to the web interface
5. **Documentation**: Requests for more examples and tutorials
