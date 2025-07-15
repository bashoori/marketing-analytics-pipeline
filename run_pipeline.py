# run_pipeline.py

from bk.extract_csv_game_events import extract_game_data
from bk.extract_csv_campaigns import extract_campaign_data
from transform.transform_data import transform_and_join
from load.load_to_postgres import load_to_postgres
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    print("🔹 Extracting game events...")
    game_df = extract_game_data("data/game_events.csv")

    print("🔹 Extracting campaigns...")
    campaign_df = extract_campaign_data("data/campaigns.csv")

    print("🔹 Transforming and joining data...")
    final_df = transform_and_join(game_df, campaign_df)

    print("🔹 Loading to PostgreSQL...")
    load_to_postgres(final_df)

    print("✅ Pipeline complete!")

if __name__ == "__main__":
    main()