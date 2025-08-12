# Config Generator Conveyor Belt 🔧⚙️

A streamlined Python-based configuration generator that transforms CSV data into network device configurations using Jinja2 templates. This "conveyor belt" approach enables rapid, automated generation of consistent configuration files for multiple network devices.

## 🚀 Features

- **CSV-to-Config Pipeline**: Convert CSV parameter files into device configurations
- **Jinja2 Template Engine**: Flexible templating for various network device types
- **Batch Processing**: Generate multiple configurations in one run
- **Regional Support**: Organized templates and data for different regions (Central, North, South)
- **Error Handling**: Robust error handling with detailed feedback
- **Type Safety**: Modern Python with type hints for better code reliability

## 📁 Project Structure

```
ConfigGenConveyorBelt/
├── data/                       # Sample CSV data files
│   └── example-data.csv
├── template/                   # Jinja2 template files
│   └── example-jinja.j2
├── scripts-src/               # Main Python scripts
│   └── nbpconfigs.py         # Core configuration generator
├── _output/                   # Generated configuration files
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ConfigGenConveyorBelt.git
cd ConfigGenConveyorBelt
```

### 2. Create Virtual Environment

#### Using `venv` (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### Using `conda` (Alternative)

```bash
# Create conda environment
conda create -n config-generator python=3.9

# Activate environment
conda activate config-generator
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python scripts-src/nbpconfigs.py --help
```

## 🏃‍♂️ Quick Start

### Basic Usage

1. **Prepare your data**: Create a CSV file with device parameters
   ```csv
   hostname;ip_address;interface;vlan_id
   router01;192.168.1.1;GigabitEthernet0/1;100
   router02;192.168.1.2;GigabitEthernet0/1;200
   ```

2. **Create a Jinja2 template**: Define your configuration template
   ```jinja2
   hostname {{ hostname }}
   !
   interface {{ interface }}
    ip address {{ ip_address }} 255.255.255.0
    switchport access vlan {{ vlan_id }}
   !
   ```

3. **Run the generator**:
   ```bash
   cd scripts-src
   python nbpconfigs.py
   ```

4. **Check output**: Generated configurations will be in the `_output` directory

### Advanced Usage

#### Custom Template and Data Files

Modify the configuration in `nbpconfigs.py`:

```python
def main():
    template_file = "your-template.j2"      # Your Jinja2 template
    csv_file = "your-data.csv"              # Your CSV data file
    output_directory = "custom_output"       # Custom output directory
    
    generate_configurations(
        template_file=template_file,
        csv_file=csv_file,
        output_dir=output_directory
    )
```

#### Using Different Delimiters

The script supports different CSV delimiters:

```python
# For comma-separated values
config_parameters = read_csv_to_dict(csv_file, delimiter=",")

# For tab-separated values  
config_parameters = read_csv_to_dict(csv_file, delimiter="\t")
```

## 📋 Example Workflow

### Step-by-Step Example

1. **Create sample data** (`data/routers.csv`):
   ```csv
   hostname;mgmt_ip;loopback_ip;as_number;description
   R1-NYC;10.1.1.1;1.1.1.1;65001;New York Core Router
   R2-LA;10.1.1.2;2.2.2.2;65001;Los Angeles Core Router
   R3-CHI;10.1.1.3;3.3.3.3;65001;Chicago Core Router
   ```

2. **Create template** (`template/router-base.j2`):
   ```jinja2
   ! {{ description }}
   hostname {{ hostname }}
   !
   ip domain-name company.com
   !
   interface Loopback0
    ip address {{ loopback_ip }} 255.255.255.255
   !
   interface Management0
    ip address {{ mgmt_ip }} 255.255.255.0
   !
   router bgp {{ as_number }}
    bgp router-id {{ loopback_ip }}
    network {{ loopback_ip }} mask 255.255.255.255
   !
   end
   ```

3. **Update script configuration**:
   ```python
   template_file = "router-base.j2"
   csv_file = "../data/routers.csv"
   ```

4. **Execute**:
   ```bash
   python scripts-src/nbpconfigs.py
   ```

5. **Result**: Three configuration files created:
   - `_output/R1-NYC.cfg`
   - `_output/R2-LA.cfg`
   - `_output/R3-CHI.cfg`

## 🧪 Development Setup

### Install Development Dependencies

```bash
pip install black flake8 mypy
```

### Code Quality Checks

```bash
# Format code
black scripts-src/

# Lint code
flake8 scripts-src/

# Type checking
mypy scripts-src/
```

## 📚 CSV File Format

The CSV files should follow this structure:

- **Headers**: First row contains variable names (used in Jinja2 templates)
- **Delimiter**: Semicolon (`;`) by default, configurable
- **Encoding**: UTF-8
- **Required field**: `hostname` (used for output filename)

### Example CSV Structure:
```csv
hostname;variable1;variable2;variable3
device1;value1;value2;value3
device2;value1;value2;value3
```

## 🎯 Use Cases

- **Network Device Configuration**: Routers, switches, firewalls
- **Server Configuration**: Web servers, database servers
- **Cloud Infrastructure**: AWS, Azure, GCP resource configurations
- **Configuration Management**: Ansible, Puppet, Chef templates
- **Documentation Generation**: Network diagrams, inventory lists

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Template not found**:
   ```
   FileNotFoundError: Template file not found: template.j2
   ```
   - Ensure template file exists in the correct directory
   - Check file path and name spelling

2. **CSV parsing errors**:
   ```
   ValueError: Error reading CSV file
   ```
   - Verify CSV file format and delimiter
   - Check for encoding issues (use UTF-8)

3. **Missing hostname field**:
   ```
   KeyError: 'hostname'
   ```
   - Ensure CSV has a 'hostname' column
   - Check column name spelling

### Getting Help

- Create an issue on GitHub
- Check existing issues for solutions
- Review the example files in `data/` and `template/`

## 🔮 Future Enhancements

- [ ] Web-based interface
- [ ] Multiple output formats (JSON, YAML, XML)
- [ ] Configuration validation
- [ ] Integration with network management tools
- [ ] Real-time configuration deployment
- [ ] Configuration version control

---

**Built with ❤️ for Network Engineers**
