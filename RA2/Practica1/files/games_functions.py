import os

from funcions import open_file

games=open_file("../data", "vgsales.csv")
if games is None or (isinstance(games, int) and games == 0):
	raise SystemExit("Error: file 'vgsales.csv' could not be opened or is empty.")

print("\n=== Change column name Global_Sales to Total_Sales ===")
change_name = games.rename(columns={"Global_Sales": "Total_Sales"}, inplace = True)
print(games.head(5))

print("\n=== Count games by platform ===")
games_platform = games['Platform'].value_counts()
print(games_platform)

print("\n=== Count games by genre sorted from smallest to largest ===")
games_genre = games['Genre'].value_counts().sort_values()
print(games_genre)

print("\n=== Count games by year ===")
games_per_year = games['Year'].value_counts().sort_index()
print(games_per_year)

print("\n=== 5 best-selling games in the USA ===")
games_usa = games.sort_values('NA_Sales', ascending=False).head(5)
print(games_usa)

print("\n=== Platform with the highest total sales ===")
platform_with_highest_sales = games.groupby('Platform')['Total_Sales'].sum().idxmax()
print(platform_with_highest_sales)

print("\n=== Sum of sales by region ===")
sum_sales_regions = games[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
print(sum_sales_regions)

print("\n=== Publisher with the most games published and the number ===")
top_publisher = games['Publisher'].value_counts().idxmax()
num_games = games['Publisher'].value_counts().max()
print(f"{top_publisher} with {num_games} games\n")

print("\n=== Best-selling Action game globally ===")
best_selling_action_game = games[games['Genre'] == 'Action'].sort_values('Total_Sales', ascending=False).head(1)
print(best_selling_action_game)

print("\n=== Average global sales in absolute value ===")
average_global_sales = games['Total_Sales'].mean()
print(abs(average_global_sales))

base_dir = os.path.dirname(__file__)
output_path = os.path.join(base_dir, "..", "data", "JuncosaDavid_games_results.txt")
with open(output_path, "w", encoding='utf-8') as export_txt:
	export_txt.write(f"""
    === Games Data Analysis Results === \n
	=== Change column name Global_Sales to Total_Sales === \n
    {games.head(5)} \n
    === Count games by platform === \n
	{games_platform} \n
    === Count games by genre sorted from smallest to largest === \n
    {games_genre} \n
    === Count games by year === \n
    {games_per_year} \n
    === 5 best-selling games in the USA === \n
    {games_usa} \n
    === Platform with the highest total sales === \n
    {platform_with_highest_sales} \n
    === Sum of sales by region === \n
    {sum_sales_regions} \n
    === Publisher with the most games published and the number === \n
    {top_publisher} with {num_games} games \n
    === Best-selling Action game globally === \n
    {best_selling_action_game} \n
    === Average global sales in absolute value === \n
    {abs(average_global_sales)} \n
""")