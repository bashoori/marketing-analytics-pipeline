import pandas as pd

def transform_and_join(game_df: pd.DataFrame, campaign_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms and joins game events with campaign data to produce aggregated insights.

    Steps:
    - Removes invalid/null records from both datasets
    - Aggregates total playtime and revenue per user from game events
    - Left-joins campaign clicks with game activity using 'user_id'
    - Fills in missing values for users with no activity

    Parameters:
        game_df (pd.DataFrame): DataFrame containing raw game event data
        campaign_df (pd.DataFrame): DataFrame containing campaign click data

    Returns:
        pd.DataFrame: Final joined and cleaned dataset ready for loading to database
    """
    # Step 1: Drop rows with missing essential fields
    game_df = game_df.dropna(subset=["user_id", "session_id", "event_time"])
    campaign_df = campaign_df.dropna(subset=["user_id", "campaign_name", "source", "clicked_at"])

    # Step 2: Aggregate game data by user_id (sum playtime and revenue)
    agg_game = game_df.groupby("user_id").agg(
        total_playtime=("playtime_minutes", "sum"),
        total_revenue=("revenue", "sum")
    ).reset_index()

    # Step 3: Join campaign data with aggregated game data
    # We use a LEFT JOIN to keep all campaign records even if no gameplay happened
    final_df = pd.merge(
        campaign_df,
        agg_game,
        on="user_id",
        how="left"
    )

    # Step 4: Fill NaNs with 0 for users who clicked but never played
    final_df["total_playtime"] = final_df["total_playtime"].fillna(0)
    final_df["total_revenue"] = final_df["total_revenue"].fillna(0)

    print(f"✅ Transformed data: {len(final_df)} records after join and aggregation.")
    return final_df