import pandas as pd

def extract_game_events(file_path: str) -> pd.DataFrame:
 
    """
    Extracts game event data from a JSON file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        pd.DataFrame: Cleaned game event DataFrame.
    """
    try:
        # Load JSON into DataFrame and parse event_time column
        df = pd.read_json(file_path)
        df["event_time"] = pd.to_datetime(df["event_time"])
        
        print(f"✅ Successfully loaded {len(df)} game event records from JSON.")
        return df
    except Exception as e:
        print(f"❌ Error reading game event JSON data: {e}")
        return pd.DataFrame()