import pandas as pd
import sys
import os

# Add the third_party directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'third_party')))

from motec_log_generator import MoTeCLog

def export_to_ld(df, metadata, output_path):
    """Exports a pandas DataFrame to a MoTeC .ld file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        metadata (dict): A dictionary of metadata for the log file.
        output_path (str): The path to write the .ld file to.
    """
    log = MoTeCLog.from_dataframe(df, **metadata)
    log.write(output_path)