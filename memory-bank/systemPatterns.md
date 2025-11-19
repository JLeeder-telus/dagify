# DAGify System Patterns

## Architecture Overview

DAGify follows a modular architecture with clear separation of concerns. The system is designed around the following key components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Source Parser  │────▶│ Universal Format│────▶│  DAG Generator  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Configuration  │     │    Templates    │     │  Report Generator│
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Key Components

### 1. Source Parser
- Parses Control-M XML or Automic job definitions
- Extracts job attributes, dependencies, and scheduling information
- Converts source-specific formats into the Universal Format

### 2. Universal Format (UF)
- Internal representation of workflow definitions
- Abstracts away source-specific details
- Provides a common model for all supported schedulers
- Consists of tasks, variables, conditions, and dependencies

### 3. DAG Generator
- Converts Universal Format to Airflow DAGs
- Applies templates to transform job types to Airflow operators
- Handles dependencies and scheduling
- Generates Python code with proper formatting

### 4. Templates
- YAML-based definition of mapping between source job types and Airflow operators
- Contains metadata, source/target information, field mappings, and structure
- Uses Jinja2 templating for dynamic code generation
- Allows for customization and extension

### 5. Rules Engine
- Applies transformations to field values during conversion
- Supports operations like variable name sanitization, string escaping, etc.
- Extensible through Python functions

### 6. Configuration
- YAML-based configuration of job type mappings
- Defines which templates to use for each job type
- Controls the conversion process

### 7. Report Generator
- Creates detailed reports on the conversion process
- Provides statistics on conversion success rates
- Identifies jobs requiring manual attention
- Outputs in both text and JSON formats

### 8. User Interfaces
- Command-line interface for batch processing
- Web-based UI for interactive use
- Docker container for portable deployment

## Key Technical Decisions

### 1. Template-Driven Conversion
- **Decision**: Use templates to define mappings between source job types and Airflow operators
- **Rationale**: Enables extensibility, customization, and separation of conversion logic from core code
- **Implementation**: YAML templates with Jinja2 for code generation

### 2. Universal Format
- **Decision**: Create an intermediate representation of workflows
- **Rationale**: Decouples source parsing from DAG generation, enabling support for multiple schedulers
- **Implementation**: Python classes representing tasks, conditions, and dependencies

### 3. Rules Engine
- **Decision**: Implement a rules system for field transformations
- **Rationale**: Allows for customization of field conversions without changing core code
- **Implementation**: Python functions applied through template configuration

### 4. DAG Division
- **Decision**: Support splitting large workflows into multiple DAGs
- **Rationale**: Improves manageability of large workflows in Airflow
- **Implementation**: Configurable division based on folder, application, or sub-application

### 5. Report Generation
- **Decision**: Generate detailed reports on the conversion process
- **Rationale**: Provides transparency and guidance for manual interventions
- **Implementation**: Text and JSON reports with statistics and details

## Data Flow

1. **Input**: Control-M XML or Automic job definitions
2. **Parsing**: Source-specific parser extracts job information
3. **Transformation**: Conversion to Universal Format
4. **Template Application**: Job types mapped to Airflow operators via templates
5. **Rule Application**: Field values transformed according to rules
6. **DAG Generation**: Python code generated for Airflow DAGs
7. **Report Generation**: Conversion statistics and details compiled
8. **Output**: Airflow DAG Python files and reports

## Design Patterns

### 1. Adapter Pattern
- Used to convert between different formats (Control-M to Universal Format to Airflow)
- Enables support for multiple source and target platforms

### 2. Template Method Pattern
- Defines the skeleton of the conversion process
- Allows specific steps to be overridden for different scheduler types

### 3. Strategy Pattern
- Rules engine implements different strategies for field transformations
- Templates define strategies for converting job types

### 4. Factory Pattern
- Creates appropriate parser and generator instances based on configuration
- Simplifies handling of different source and target formats

## Extension Points

1. **New Job Types**: Add new templates for unsupported job types
   - Example: The Control-M Job to SSHOperator template (control-m-job-to-airflow-ssh.yaml) was added to support Control-M jobs with TASKTYPE="Job"
2. **New Schedulers**: Implement new parsers for additional scheduler platforms
3. **New Rules**: Add new transformation rules for field values

## Template Development

### Template Structure
Templates follow a standardized YAML structure:
```yaml
metadata:
  id: <unique_id>
  name: <template_name>
  version: <version>
  author:
    name: <author_name>
    email: <author_email>
  description-short: <short_description>
  description: <detailed_description>
  tags:
    - <tag1>
    - <tag2>
source:
  platform: 
    id: <source_platform_id>
    name: <source_platform_name>
  operator: 
    id: <source_operator_id>
target:
  platform: 
    id: <target_platform_id>
    name: <target_platform_name>
  operator: 
    id: <target_operator_id>
    name: <target_operator_name>
    docs: <documentation_url>
    imports: 
      - package: <package_name>
        imports:
          - <import1>
          - <import2>
mappings:
  - source: <source_field>
    target: <target_field>
    rules:
      - rule: <rule_name>
structure: |
  <jinja2_template_for_code_generation>
```

### Template Validation
Templates are validated against a schema to ensure correctness:
- The `id` field must be an integer between 0 and 5
- Required fields must be present
- Field types must match expected types

### Template Configuration
Templates are configured in `config.yaml` to map job types to templates:
```yaml
config: 
  mappings: 
    - job_type: <job_type>
      template_name: <template_name>
```

### Template Development Process
1. Identify a job type that needs conversion
2. Create a new template file in the `dagify/templates` directory
3. Define the metadata, source, target, mappings, and structure
4. Add the template to `config.yaml`
5. Test the template with sample XML files
6. Refine the template based on testing results
