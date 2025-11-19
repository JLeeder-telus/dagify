# DAGify Project Brief

## Overview
DAGify is a highly extensible, template-driven migration accelerator that helps organizations convert their enterprise scheduler workflows (primarily from Control-M) to Apache Airflow and Google Cloud Composer. The tool aims to significantly reduce the effort required for developers to convert native enterprise scheduler formats into Python code in Apache Airflow DAG format.

## Core Requirements

1. **Conversion Capability**
   - Convert Control-M XML job definitions to Apache Airflow Python DAGs
   - Support for Automic job definitions (in development)
   - Maintain job dependencies and relationships in the converted DAGs
   - Preserve scheduling information where possible

2. **Extensibility**
   - Template-driven architecture for mapping different job types
   - Customizable rules engine for field transformations
   - Support for adding new templates and job types

3. **Usability**
   - Command-line interface for batch processing
   - Web-based UI for interactive use
   - Detailed conversion reports
   - Docker container support for portable deployment

4. **Performance**
   - Handle large XML files with many job definitions
   - Support for splitting large workflows into multiple DAGs

## Project Goals

1. **Migration Acceleration**
   - Reduce manual effort in migration projects
   - Automate the conversion of common job patterns
   - Provide clear reporting on what was converted and what needs manual attention

2. **Flexibility**
   - Support various Control-M job types through templates
   - Allow customization of the conversion process
   - Enable extension to other scheduler platforms

3. **Quality Assurance**
   - Generate valid, well-formatted Airflow DAGs
   - Provide detailed reports on the conversion process
   - Highlight areas requiring manual review

## Non-Goals

1. **100% Automated Migration**
   - The tool does not aim to automatically convert 100% of existing scheduler workflows
   - Some complex or specialized job types will require manual conversion

2. **Runtime Execution**
   - DAGify is a conversion tool, not a runtime execution environment
   - It does not execute the workflows, only converts their definitions

## Success Criteria

1. Successfully convert common Control-M job types to Airflow operators
2. Maintain job dependencies and relationships in the converted DAGs
3. Provide clear reporting on conversion success rates and areas requiring attention
4. Enable customization through templates and configuration
