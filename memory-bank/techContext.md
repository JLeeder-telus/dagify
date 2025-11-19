# DAGify Technical Context

## Technology Stack

### Core Technologies

1. **Python 3**
   - Primary programming language
   - Used for all core functionality, parsing, and generation

2. **XML Processing**
   - `xml.etree.ElementTree` for parsing Control-M XML files
   - `lxml` for additional XML processing capabilities

3. **YAML**
   - Used for configuration files and templates
   - `PyYAML` for parsing and loading YAML files
   - `yamale` for YAML schema validation

4. **Jinja2**
   - Template engine for generating Airflow DAG code
   - Used in the DAG template system

5. **Click**
   - Command-line interface framework
   - Handles command-line arguments and options

### Web Interface

1. **FastAPI**
   - Modern, high-performance web framework
   - Provides the backend for the web UI

2. **Jinja2 Templates**
   - Used for server-side rendering of HTML

3. **Bootstrap**
   - Frontend framework for responsive design
   - Provides UI components and styling

4. **JavaScript**
   - Client-side validation and interactivity

### Development Tools

1. **autopep8**
   - Code formatting for generated Python files
   - Ensures consistent code style

2. **Make**
   - Build automation
   - Manages development environment setup

3. **Docker**
   - Containerization for portable deployment
   - Simplifies environment setup and distribution

## Dependencies

### Core Dependencies

```
PyYAML
yamale
Jinja2
Click
lxml
autopep8
prettytable
```

### Web UI Dependencies

```
FastAPI
uvicorn
python-multipart
```

## Development Environment

### Setup

1. **Virtual Environment**
   - Created and managed through `make clean`
   - Installs all required dependencies

2. **Configuration**
   - Default configuration in `config.yaml`
   - Templates in `dagify/templates/`
   - Schema validation in `dagify/converter/yaml_validator/`

3. **Docker**
   - Dockerfile for containerized deployment
   - Environment variables configurable through `.env.example`

### Running Locally

1. **From Source**
   ```bash
   make clean
   python3 DAGify.py --source-path=[SOURCE-XML-FILE]
   ```

2. **With Custom Configuration**
   ```bash
   python3 DAGify.py --source-path=[SOURCE-XML-FILE] --output-path=[OUTPUT-PATH] --config-file=[CONFIG-YAML]
   ```

3. **With Web UI**
   ```bash
   cd ui
   uvicorn app:app --reload
   ```

4. **From Docker**
   ```bash
   docker build -t localhost/dagify:source .
   docker run -p 8000:8000 -it --env-file=.env.example -v $(pwd):/app localhost/dagify:source
   ```

## File Structure

```
dagify/
├── __init__.py
├── setup.py
├── converter/
│   ├── __init__.py
│   ├── automic.py
│   ├── controlm.py
│   ├── engine.py
│   ├── report_generator.py
│   ├── rules.py
│   ├── uf.py
│   ├── utils.py
│   ├── templates/
│   │   └── dag.tmpl
│   └── yaml_validator/
│       ├── __init__.py
│       ├── custom_validator.py
│       └── schema.yaml
├── templates/
│   ├── automic-dummy-to-airflow-dummy.yaml
│   ├── control-m-command-to-airflow-bash.yaml
│   ├── control-m-command-to-airflow-gke-start-job.yaml
│   ├── control-m-command-to-airflow-python.yaml
│   ├── control-m-command-to-airflow-ssh-gce.yaml
│   ├── control-m-command-to-airflow-ssh.yaml
│   └── control-m-dummy-to-airflow-dummy.yaml
└── test/
    ├── __init__.py
    ├── test_converter.py
    ├── test_utils.py
    └── integration/
        ├── regenerate_int_tests.sh
        ├── run_integration-tests.sh
        ├── test_data/
        └── test_references/

ui/
├── app.py
├── static/
│   ├── style.css
│   └── assets/
│       └── img/
└── templates/
    └── index.html

sample_data/
└── control-m/
    ├── 001-tfatf.xml
    └── 002-tftf.xml
```

## Key Technical Concepts

### 1. Universal Format (UF)

The Universal Format is an internal representation of workflow definitions that abstracts away source-specific details. It consists of:

- **UFTask**: Represents a job or task in the workflow
- **UFTaskVariable**: Represents a variable associated with a task
- **UFTaskInCondition**: Represents an input condition for a task
- **UFTaskOutCondition**: Represents an output condition for a task
- **UFTaskShout**: Represents a notification or alert associated with a task

The UF provides a common model for all supported schedulers, enabling the system to handle multiple source formats.

### 2. Template System

Templates define the mapping between source job types and Airflow operators. Each template includes:

- **Metadata**: Information about the template (name, version, author)
- **Source**: Details about the source platform and operator
- **Target**: Details about the target platform and operator
- **Mappings**: Field mappings between source and target
- **Structure**: Jinja2 template for generating Airflow operator code

Templates are stored as YAML files and loaded at runtime based on the configuration.

### 3. Rules Engine

The rules engine applies transformations to field values during conversion. Rules are Python functions that can be applied to field values through template configuration. Examples include:

- **python_variable_safe**: Ensures a string is a valid Python variable name
- **escape_quotes**: Escapes quotes in strings
- **lowercase**: Converts a string to lowercase
- **replace**: Replaces characters in a string

### 4. DAG Division

DAGify supports splitting large workflows into multiple DAGs based on configurable criteria:

- **FOLDER**: Divides by Control-M folder
- **APPLICATION**: Divides by Control-M application
- **SUB_APPLICATION**: Divides by Control-M sub-application

This improves the manageability of large workflows in Airflow.

### 5. Dependency Handling

DAGify preserves dependencies between tasks, including:

- **Internal Dependencies**: Dependencies between tasks in the same DAG
- **External Dependencies**: Dependencies between tasks in different DAGs

External dependencies are handled using Airflow's ExternalTaskSensor and ExternalTaskMarker.

## Technical Constraints

1. **XML Structure**: The tool expects Control-M XML files to follow a specific structure. Variations in the XML format may cause parsing issues.

2. **Template Availability**: The conversion process depends on the availability of templates for specific job types. Unsupported job types will be converted to dummy operators.

3. **Python Version**: The tool is designed to work with Python 3.6+. Earlier versions may not be compatible.

4. **Memory Usage**: Large XML files with many job definitions may require significant memory during processing.

5. **Airflow Compatibility**: Generated DAGs are designed for compatibility with recent versions of Apache Airflow (2.0+). Older versions may require adjustments.
