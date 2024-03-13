import matplotlib.pyplot as plt
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
from nba_api.stats.static import players

# Function to retrieve player career statistics
def get_player_career_stats(player_id):
    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id) 
    player_data = player_stats.get_data_frames()[0]
    player_data = player_data.sort_values(by='SEASON_ID')  # Sort by season
    return player_data

# Function to get player's name
def get_player_name(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info = player_info.get_data_frames()[0]
    player_name = player_info['DISPLAY_FIRST_LAST'].iloc[0]
    return player_name

# Function to plot selected statistic for a player
def plot_statistic(player_data, statistic, player_name):
    seasons = player_data['SEASON_ID']
    stat_values = player_data[statistic]
    
    plt.plot(seasons, stat_values, marker='o', label=player_name)

# Function to prompt user for player selection
def select_players():
    # Initialize lists to store player names and IDs
    player_names = []
    player_ids = []

    # Ask user for the number of players
    num_players = 2

    # Prompt user for player names
    for i in range(num_players):
        player_name = input(f"Enter the full name of player {i+1}: ")
        player_names.append(player_name)

    # Find player IDs for the given names
    for player_name in player_names:
        player_dict = players.find_players_by_full_name(player_name)
        if player_dict:
            player_ids.append(player_dict[0]['id'])
        else:
            print(f"Player '{player_name}' not found.")
            return None, None

    return player_names, player_ids

# Function to compare statistics between two players
def compare_players():
    # Ask user for the statistic to plot
    statistic = input("Enter the statistic you want to plot (e.g., 'PTS', 'REB', 'AST'): ")

    # Select players
    player_names, player_ids = select_players()
    if player_names is None or player_ids is None:
        return

    # Plot the selected statistic for each player
    plt.figure(figsize=(10, 6))
    for player_id, player_name in zip(player_ids, player_names):
        player_data = get_player_career_stats(player_id)
        plot_statistic(player_data, statistic, player_name)

    # Customize the plot
    plt.xlabel('Season')
    plt.ylabel(statistic)
    plt.title(f'{statistic} by Season')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Show plot
    plt.show()

# Main function
def main():
    compare_players()

if __name__ == "__main__":
    main()
