import pandas as pd
import sys
import os

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(repo_root, "third_party"))

from motec_log_generator.motec_log import MoTeCLog

def export_to_ld(df, metadata, output_path):
    """Exports a pandas DataFrame to a MoTeC .ld file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        metadata (dict): A dictionary of metadata for the log file.
        output_path (str): The path to write the .ld file to.
    """
    try:
        log = MoTeCLog.from_dataframe(df, **metadata)
        log.write(output_path)
    except Exception:
        print("[EXPORT ERROR] Could not export to .ld file.")
        sys.exit(1)