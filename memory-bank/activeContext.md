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

1. **Environment Variable Handling**: Enhanced the `rule_env_var_to_python` method to properly handle Control-M environment variables in Python code, including special handling for variables ending with `_prefix` followed by a period
2. **Control-M Job Template**: Updated the template to convert Control-M jobs with TASKTYPE="Job" to Airflow SSHOperator with proper f-string formatting for environment variables
3. **Proxy Configuration**: Enhanced documentation for TELUS network proxy requirements, adding explicit instructions for Cline to run proxy configuration commands when starting a new terminal
4. **PowerShell Syntax**: Documented PowerShell syntax requirements for Windows environments
5. **VM Setup Guide**: Created a comprehensive guide for setting up DAGify on a GCP VM
6. **Airflow Integration**: Fixed Pylance warnings by properly installing Apache Airflow dependencies
7. **Automic Support**: Initial implementation of support for Automic job definitions
8. **Web UI Improvements**: Enhanced user experience in the web interface
9. **Report Generation**: More comprehensive reporting capabilities
10. **Docker Integration**: Improved containerization for easier deployment
11. **Documentation**: Better documentation of usage patterns and extension points

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
