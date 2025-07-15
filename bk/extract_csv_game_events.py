import pandas as pd

def extract_game_data(file_path: str) -> pd.DataFrame:
    """
    Extracts game event data from a CSV file.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned game event DataFrame.
    """
    try:
        df = pd.read_csv(file_path, parse_dates=["event_time"])
        print(f"✅ Successfully loaded {len(df)} game event records.")
        return df
    except Exception as e:
        print(f"❌ Error reading game event data: {e}")
        return pd.DataFrame()