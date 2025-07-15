import pandas as pd

def extract_campaign_data(file_path: str) -> pd.DataFrame:
    """
    Extracts campaign data from a JSON file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        pd.DataFrame: Campaign data as a DataFrame.
    """
    try:
        df = pd.read_json(file_path)
        df["clicked_at"] = pd.to_datetime(df["clicked_at"])
        
        print(f"✅ Successfully loaded {len(df)} campaign records from JSON.")
        return df
    except Exception as e:
        print(f"❌ Error reading campaign JSON data: {e}")
        return pd.DataFrame()