from extract.extract_game_events import extract_game_events
from extract.extract_campaigns import extract_campaign_data
from transform.transform_data import transform_and_join
from load.load_to_postgres import load_to_postgres


game_df = extract_game_events("data/game_events.json")
print(game_df.head())

campaign_df = extract_campaign_data("data/campaigns.json")
print(campaign_df.head())

join_df = transform_and_join(game_df, campaign_df)
df=join_df
print(df.head())


load_to_postgres(df)






