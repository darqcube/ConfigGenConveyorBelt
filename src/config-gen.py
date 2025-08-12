#!/usr/bin/env python3
"""
Configuration Generator

This script generates network configuration files from CSV data using Jinja2 templates.
It reads CSV parameters and generates configuration files for network devices.

Author: Salman Khan, Chief Infrastructure & Security Architect
License: MIT
"""

import csv
import os
import sys
from pathlib import Path
from typing import Dict, List

import jinja2


def read_csv_to_dict(csv_file_path: str, delimiter: str = ";") -> List[Dict[str, str]]:
    """
    Read CSV file and convert it to a list of dictionaries.

    Args:
        csv_file_path: Path to the CSV file
        delimiter: CSV delimiter (default: semicolon)

    Returns:
        List of dictionaries where keys are CSV headers and values are row data

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the CSV file is empty or malformed
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    config_parameters = []

    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            config_parameters = list(csv_reader)

        if not config_parameters:
            raise ValueError("CSV file is empty or has no data rows")

    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    return config_parameters


def create_jinja_environment(template_dir: str = ".") -> jinja2.Environment:
    """
    Create and configure Jinja2 environment.

    Args:
        template_dir: Directory containing Jinja2 templates

    Returns:
        Configured Jinja2 environment
    """
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def ensure_output_directory(output_dir: str) -> None:
    """
    Ensure the output directory exists, create if it doesn't.

    Args:
        output_dir: Path to the output directory
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def generate_configurations(
    template_file: str,
    csv_file: str,
    output_dir: str = "_output",
    template_dir: str = ".",
) -> None:
    """
    Generate configuration files from CSV data using Jinja2 templates.

    Args:
        template_file: Name of the Jinja2 template file
        csv_file: Path to the CSV file containing parameters
        output_dir: Directory to save generated configurations
        template_dir: Directory containing Jinja2 templates
    """
    print(f"Reading CSV parameter file: {csv_file}...")
    config_parameters = read_csv_to_dict(csv_file)
    print(f"Found {len(config_parameters)} configuration entries")

    print("Creating Jinja2 environment...")
    env = create_jinja_environment(template_dir)

    try:
        template = env.get_template(template_file)
    except jinja2.TemplateNotFound:
        raise FileNotFoundError(f"Template file not found: {template_file}")

    print(f"Ensuring output directory exists: {output_dir}")
    ensure_output_directory(output_dir)

    print("Generating configuration files...")
    for i, parameter in enumerate(config_parameters, 1):
        try:
            result = template.render(parameter)
            hostname = parameter.get("hostname", f"config_{i}")
            config_filename = f"{hostname}.cfg"
            config_path = os.path.join(output_dir, config_filename)

            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write(result)

            print(f"  [{i}/{len(config_parameters)}] Created: {config_filename}")

        except Exception as e:
            print(f"  Error generating config for entry {i}: {e}")
            continue

    print("Configuration generation completed!")


def main():
    """Main function to run the configuration generator."""
    # Configuration parameters
    template_file = "./template/example-jinja.j2"
    csv_file = "./data/example-data.csv"
    output_directory = "_output"

    try:
        generate_configurations(
            template_file=template_file, csv_file=csv_file, output_dir=output_directory
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
