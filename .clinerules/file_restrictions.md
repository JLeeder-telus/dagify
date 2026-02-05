# File Access Restrictions

## Protected Directories

### telus_data

**IMPORTANT: Never edit any files in the 'telus_data' directory.**

The 'telus_data' directory contains sensitive Control-M job definitions and configuration files from TELUS production environments. These files are for reference and conversion purposes only and should never be modified directly.

#### Rationale

1. **Data Integrity**:
   - These files represent the source of truth for Control-M job definitions
   - Any modifications could lead to incorrect DAG conversions
   - Original files need to be preserved for comparison and validation

2. **Conversion Process**:
   - The proper workflow is to use DAGify to convert these files to Airflow DAGs
   - Any customizations should be made to the conversion templates or processes, not the source files

3. **Security and Compliance**:
   - These files may contain sensitive operational information
   - Preserving the original files is important for audit purposes

#### Correct Approach

If changes are needed in how these files are processed:
- Modify the conversion templates in `dagify/converter/templates/`
- Update conversion rules in `dagify/converter/rules.py`
- Create custom templates in `dagify/templates/`
