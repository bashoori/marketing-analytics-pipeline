from bk.extract_csv_game_events import extract_game_data


df = extract_game_data("data/game_events.csv")
print(df.head())