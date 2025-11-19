# Setting Up DAGify on a GCP VM

This guide walks through the process of setting up DAGify on a Google Cloud Platform (GCP) Virtual Machine to convert Control-M job definitions to Apache Airflow DAGs.

## Prerequisites

- A GCP VM instance running Debian/Ubuntu
- Access to the DAGify source code (zip file)
- Control-M XML files to convert

## Setup Steps

### 1. Install Required Packages

First, install the necessary system packages:

```bash
# Install unzip to extract the DAGify source code
sudo apt install unzip

# Install make for build automation
sudo apt install make

# Install Python virtual environment package
sudo apt install python3.11-venv
```

### 2. Extract DAGify Source Code

Upload the DAGify zip file to your VM and extract it:

```bash
# Extract the zip file
unzip dagify-main.zip

# Remove the zip file (optional)
rm dagify-main.zip

# Navigate to the DAGify directory
cd dagify-main
```

### 3. Set Up Python Environment

Create and activate a Python virtual environment, then install dependencies:

```bash
# Clean and set up the environment using the provided Makefile
make dagify-clean

# This command:
# - Removes any existing output and venv directories
# - Creates a new Python virtual environment
# - Installs all dependencies from requirements.txt

# Activate the virtual environment
source venv/bin/activate
```

### 4. Verify Installation

Verify that DAGify is properly installed:

```bash
# Check the DAGify help information
python ./DAGify.py -h
```

You should see the usage information and available options for the DAGify tool.

### 5. Convert Control-M XML to Airflow DAGs

Run DAGify to convert your Control-M XML files to Airflow DAGs:

```bash
# Create directories for input and output files if they don't exist
mkdir -p telus/data
mkdir -p telus/output

# Copy your Control-M XML files to the telus/data directory

# Convert Control-M XML files to Airflow DAGs
python3 ./DAGify.py -s /home/[username]/dagify-main/telus/data/[your-file].DRF.xml -o /home/[username]/dagify-main/telus/output/
```

Replace `[username]` with your actual username and `[your-file]` with the name of your Control-M XML file.

### 6. Deploy DAGs to Google Cloud Composer

Upload the generated DAGs to your Google Cloud Composer environment's DAGs folder:

```bash
# Copy the generated DAGs to the Cloud Storage bucket associated with your Composer environment
gcloud storage cp -r /home/[username]/dagify-main/telus/output/[DAG_FOLDER]/* gs://[your-composer-bucket]/dags/
```

Replace:
- `[username]` with your actual username
- `[DAG_FOLDER]` with the folder containing your generated DAGs
- `[your-composer-bucket]` with your Cloud Composer bucket name

## Example Commands

Here are example commands for converting specific Control-M XML files and uploading them to Cloud Composer:

```bash
# Convert BIL-EXF.DRF.xml to Airflow DAGs
python3 ./DAGify.py -s /home/jeremy_leeder/dagify-main/telus/data/BIL-EXF.DRF.xml -o /home/jeremy_leeder/dagify-main/telus/output/

# Convert OMG-VPOP.DRF.xml to Airflow DAGs
python3 ./DAGify.py -s /home/jeremy_leeder/dagify-main/telus/data/OMG-VPOP.DRF.xml -o /home/jeremy_leeder/dagify-main/telus/output/

# Upload the generated DAGs to Cloud Composer
gcloud storage cp -r /home/jeremy_leeder/dagify-main/telus/output/BIL-EXF/* gs://northamerica-northeast1-bat-f6f9734c-bucket/dags/
gcloud storage cp -r /home/jeremy_leeder/dagify-main/telus/output/OMG-VPOP/* gs://northamerica-northeast1-bat-f6f9734c-bucket/dags/
```

## Troubleshooting

- If you encounter issues with the Python virtual environment, ensure you have installed `python3.11-venv` and that the virtual environment is properly activated.
- If DAGify fails to convert your Control-M XML files, check that the XML files are properly formatted and compatible with DAGify.
