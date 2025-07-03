import asyncio
import yaml
import os
import pandas as pd
import sys, traceback
from gt7.writer.motec_exporter import export_to_ld

def handle_uncaught(exc_type, exc_value, tb):
    print(f"[UNEXPECTED ERROR] {exc_value}")
    sys.exit(1)

sys.excepthook = handle_uncaught

CONFIG_FILE = 'config.yml'
CONFIG_EXAMPLE_FILE = 'config.yml.example'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"'{CONFIG_FILE}' not found, copying from '{CONFIG_EXAMPLE_FILE}'")
        import shutil
        shutil.copy(CONFIG_EXAMPLE_FILE, CONFIG_FILE)
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

async def main():
    config = load_config()

    # Placeholder for UDP listeners
    print("UDP listeners would be started here.")

    # Example of processing a sample file
    # In a real scenario, this would come from the UDP listener
    if os.path.exists('samples/packet_a.bin'):
        print("Processing sample file...")
        # This is a placeholder for the full decryption and parsing pipeline
        # For now, we'll create a dummy dataframe
        data = {
            'timestamp': [0, 0.01, 0.02],
            'throttle': [0, 10, 50],
            'brake': [100, 90, 20]
        }
        df = pd.DataFrame(data)

        metadata = {
            'vehicle': 'Placeholder Vehicle',
            'venue': 'Placeholder Track',
            'event': 'Placeholder Event'
        }

        output_path = config.get('log_output_path', './logs/session.ld')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        export_to_ld(df, metadata, output_path)
        print(f"Successfully generated .ld file at {output_path}")
    else:
        print("Sample file not found, skipping processing.")

    print("Async core running")
    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())