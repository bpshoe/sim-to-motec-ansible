# GT7 MoTeC Telemetry Logger

This project provides a complete pipeline for capturing Gran Turismo 7 (GT7) telemetry data, processing it, and exporting it to MoTeC .ld files for professional analysis.

## Architecture

The system consists of the following components:

- **UDP Listener:** Receives telemetry data packets from the PlayStation console.
- **Decryptor:** Decrypts the incoming data packets.
- **Parser:** Parses the decrypted data into a structured format.
- **Pandas DataFrame:** The parsed data is loaded into a pandas DataFrame for efficient manipulation.
- **MoTeC Log Generator:** The DataFrame is then used to generate a MoTeC .ld file.
- **FastAPI Backend:** A simple web backend provides a health check endpoint.

## Prerequisites

- Python 3.9+
- A Raspberry Pi or other Linux-based system

## Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This repo vendors MotecLogGenerator under third_party/. No pip install required.

3. **Configure the logger:**
   Copy `config.yml.example` to `config.yml` and edit the values to match your setup.

## Usage

- **Run the logger:**
  ```bash
  python gt7.py
  ```

- **Check the backend health:**
  ```bash
  curl http://localhost:8000/health
  ```

## Output Files

The generated .ld files will be saved to the path specified in `config.yml`.

## Sample Data

The `samples/` directory contains sample data packets that can be used for testing and development.

## Troubleshooting

- **`ModuleNotFoundError`:** If you encounter this error, make sure you have installed all the dependencies in `requirements.txt`.
- **No UDP data:** Ensure that your PlayStation and the system running the logger are on the same network and that the IP address in `config.yml` is correct.