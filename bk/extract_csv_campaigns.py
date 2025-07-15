import pandas as pd

def extract_campaign_data(file_path: str) -> pd.DataFrame:
    """
    Extracts marketing campaign data from a CSV file.

    Parameters:
        file_path (str): Path to the CSV file containing campaign data.

    Returns:
        pd.DataFrame: A DataFrame containing parsed campaign data.
                      Returns an empty DataFrame if there's an error.
    """
    try:
        # Read the campaign CSV file
        # Automatically parse 'clicked_at' column as datetime
        df = pd.read_csv(file_path, parse_dates=["clicked_at"])
        
        # Log success and record count
        print(f"✅ Successfully loaded {len(df)} campaign records.")
        
        return df

    except Exception as e:
        # Log error and return empty DataFrame if reading fails
        print(f"❌ Error reading campaign data: {e}")
        return pd.DataFrame()