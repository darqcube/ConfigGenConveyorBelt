#!/usr/bin/env python3
"""
Configuration Generator

This script generates network configuration files from CSV data using Jinja2 templates.
It reads CSV parameters and generates configuration files for network devices.

HOW TO USE:
1. Create a CSV file with device parameters (headers become template variables)
2. Create a Jinja2 template file with placeholders like {{ hostname }}
3. Update the file paths in the main() function
4. Run: python src/config-gen.py

EXAMPLE CSV FORMAT (semicolon-separated):
hostname;ip_address;interface
router01;192.168.1.1;eth0
router02;192.168.1.2;eth0

EXAMPLE TEMPLATE FORMAT:
hostname {{ hostname }}
interface {{ interface }}
ip address {{ ip_address }}

Author: Salman Khan, Chief Infrastructure & Security Architect
License: MIT
"""

# ========================================
# IMPORTS - Required Python modules
# ========================================
import csv  # For reading CSV files
import os  # For file system operations
import sys  # For system operations and exit codes
from pathlib import Path  # For cross-platform path handling
from typing import Dict, List  # For type hints

import jinja2  # For template processing


# ========================================
# CORE FUNCTIONS
# ========================================


def read_csv_to_dict(csv_file_path: str, delimiter: str = ";") -> List[Dict[str, str]]:
    """
    Read CSV file and convert it to a list of dictionaries.

    This function parses a CSV file where:
    - First row contains headers (these become dictionary keys)
    - Subsequent rows contain data (these become dictionary values)
    - Each row becomes one dictionary in the returned list

    Args:
        csv_file_path: Path to the CSV file
        delimiter: CSV delimiter (default: semicolon)

    Returns:
        List of dictionaries where keys are CSV headers and values are row data

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the CSV file is empty or malformed
    """
    # Check if the CSV file exists before trying to read it
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    config_parameters = []

    try:
        # Open the CSV file with UTF-8 encoding for international character support
        with open(csv_file_path, "r", encoding="utf-8") as file:
            # Use csv.DictReader to automatically convert CSV rows to dictionaries
            # This makes the first row (headers) the keys for all subsequent rows
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            config_parameters = list(csv_reader)

        # Validate that we actually have data to work with
        if not config_parameters:
            raise ValueError("CSV file is empty or has no data rows")

    except Exception as e:
        # Catch any file reading or parsing errors
        raise ValueError(f"Error reading CSV file: {e}")

    return config_parameters


def create_jinja_environment(template_dir: str = ".") -> jinja2.Environment:
    """
    Create and configure Jinja2 environment.

    Jinja2 Environment controls how templates are loaded and processed.
    We configure it with options that make templates cleaner and more readable.

    Args:
        template_dir: Directory containing Jinja2 templates

    Returns:
        Configured Jinja2 environment
    """
    return jinja2.Environment(
        # FileSystemLoader tells Jinja2 where to find template files
        loader=jinja2.FileSystemLoader(searchpath=template_dir),
        # trim_blocks removes newlines after block tags (like {% if %})
        trim_blocks=True,
        # lstrip_blocks removes leading whitespace from blocks
        lstrip_blocks=True,
    )


def ensure_output_directory(output_dir: str) -> None:
    """
    Ensure the output directory exists, create if it doesn't.

    Uses pathlib for cross-platform path handling and creates
    any necessary parent directories.

    Args:
        output_dir: Path to the output directory
    """
    # pathlib.Path provides cross-platform path handling
    # mkdir with parents=True creates parent directories if needed
    # exist_ok=True prevents errors if directory already exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def generate_configurations(
    template_file: str,
    csv_file: str,
    output_dir: str = "_output",
    template_dir: str = ".",
) -> None:
    """
    Generate configuration files from CSV data using Jinja2 templates.

    This is the main processing function that coordinates all the steps:
    1. Read CSV data
    2. Set up Jinja2 environment
    3. Load template
    4. Generate configs for each CSV row
    5. Save output files

    Args:
        template_file: Name of the Jinja2 template file
        csv_file: Path to the CSV file containing parameters
        output_dir: Directory to save generated configurations
        template_dir: Directory containing Jinja2 templates
    """
    # ========================================
    # STEP 1: READ AND VALIDATE CSV DATA
    # ========================================
    print(f"Reading CSV parameter file: {csv_file}...")
    config_parameters = read_csv_to_dict(csv_file)
    print(f"Found {len(config_parameters)} configuration entries")

    # ========================================
    # STEP 2: SETUP JINJA2 TEMPLATE ENGINE
    # ========================================
    print("Creating Jinja2 environment...")
    env = create_jinja_environment(template_dir)

    # Load the template file and handle any errors
    try:
        template = env.get_template(template_file)
    except jinja2.TemplateNotFound:
        raise FileNotFoundError(f"Template file not found: {template_file}")

    # ========================================
    # STEP 3: PREPARE OUTPUT DIRECTORY
    # ========================================
    print(f"Ensuring output directory exists: {output_dir}")
    ensure_output_directory(output_dir)

    # ========================================
    # STEP 4: GENERATE CONFIGURATION FILES
    # ========================================
    print("Generating configuration files...")
    for i, parameter in enumerate(config_parameters, 1):
        try:
            # Render the template with current row's data
            # This replaces all {{ variable }} placeholders with actual values
            result = template.render(parameter)

            # Get hostname from CSV data, or create a default name
            # Hostname is used as the filename for the generated config
            hostname = parameter.get("hostname", f"config_{i}")
            config_filename = f"{hostname}.cfg"
            config_path = os.path.join(output_dir, config_filename)

            # Write the rendered configuration to a file
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write(result)

            # Show progress to user
            print(f"  [{i}/{len(config_parameters)}] Created: {config_filename}")

        except Exception as e:
            # If there's an error with one config, continue with the rest
            print(f"  Error generating config for entry {i}: {e}")
            continue

    print("Configuration generation completed!")


def main():
    """Main function to run the configuration generator."""

    # ========================================
    # CONFIGURATION SECTION - MODIFY THESE VALUES
    # ========================================

    # Path to your Jinja2 template file (relative to project root)
    # Template defines the structure of your configuration files
    template_file = "./template/example-jinja.j2"

    # Path to your CSV data file containing device parameters (relative to project root)
    # CSV should have headers that match variables in your template
    csv_file = "./data/example-data.csv"

    # Directory where generated configuration files will be saved
    # Will be created automatically if it doesn't exist
    output_directory = "_output"

    # ========================================
    # EXECUTION SECTION - DO NOT MODIFY BELOW
    # ========================================

    try:
        # Run the configuration generation process
        generate_configurations(
            template_file=template_file, csv_file=csv_file, output_dir=output_directory
        )
    except Exception as e:
        # Handle any errors that occur during execution
        print(f"Error: {e}")
        sys.exit(1)


# ========================================
# SCRIPT ENTRY POINT
# ========================================
if __name__ == "__main__":
    # This ensures main() only runs when script is executed directly
    # (not when imported as a module)
    main()
