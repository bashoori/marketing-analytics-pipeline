from extract.extract_game_events import extract_game_events
from extract.extract_campaigns import extract_campaign_data
from transform.transform_data import transform_and_join
from load.load_to_postgres import load_to_postgres

def main():
    print("🚀 Starting ETL pipeline...")

    # 1. Extract
    print("\n📥 Extracting game event data...")
    game_df = extract_game_events("data/game_events.json")

    print("\n📥 Extracting campaign data...")
    campaign_df = extract_campaign_data("data/campaigns.json")

    # 2. Transform
    print("\n🔄 Transforming and joining data...")
    final_df = transform_and_join(game_df, campaign_df)

    # 3. Load
    print("\n📦 Loading data into PostgreSQL...")
    load_to_postgres(final_df)

    print("\n✅ ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()

