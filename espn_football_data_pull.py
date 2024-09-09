from espn_api.football import League
import json
import secrets

# Function to initialize the league with authentication (private league)
def initialize_league(league_id, year, espn_s2, swid):
    """
    Initializes the league object with authentication for a private league.
    
    Args:
        league_id (int): The ID of the ESPN Fantasy League.
        year (int): The year of the league.
        espn_s2 (str): The ESPN S2 cookie for authentication.
        swid (str): The SWID cookie for authentication.

    Returns:
        League object: Initialized ESPN Fantasy Football league object.
    """
    return League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

# Function to extract detailed league data
def extract_league_data(league):
    """
    Extracts detailed data from the league such as standings, matchups, transactions, and waivers.
    
    Args:
        league (League): ESPN Fantasy Football League object.

    Returns:
        dict: A dictionary containing detailed league data.
    """
    league_data = {
        "teams": [{
            "team_name": team.team_name,
            "owner": team.owners,
            "wins": team.wins,
            "losses": team.losses,
            "points_for": team.points_for,
            "points_against": team.points_against,
            "roster": [{
                "player_name": player.name,
                "position": player.position,
                "total_points": player.total_points,
                "injured": player.injured
            } for player in team.roster]
        } for team in league.teams],
        "matchups": [{
            "home_team": matchup.home_team.team_name,
            "away_team": matchup.away_team.team_name,
            "home_score": matchup.home_score,
            "away_score": matchup.away_score,
        } for matchup in league.scoreboard()],
        "transactions": [{
            "type": transaction.transaction_type,
            "team_involved": transaction.team,
            "players": [player.name for player in transaction.players],
        } for transaction in league.get_transactions()],
        "waivers": [{
            "player_name": player.name,
            "position": player.position,
            "total_points": player.total_points
        } for player in league.free_agents(size=10)]  # Top 10 free agents
    }
    return league_data

# Function to extract detailed team data
def extract_team_data(my_team):
    """
    Extracts detailed data for a specific team, including roster, bench, and schedule.
    
    Args:
        my_team (Team): ESPN Fantasy Football Team object.

    Returns:
        dict: A dictionary containing detailed team data.
    """
    team_data = {
        "name": my_team.team_name,
        "record": {
            "wins": my_team.wins,
            "losses": my_team.losses
        },
        "points_for": my_team.points_for,
        "points_against": my_team.points_against,
        "roster": [{
            "player_name": player.name,
            "position": player.position,
            "total_points": player.total_points,
            "injured": player.injured,
            "projected_points": player.projected_points
        } for player in my_team.roster],
        "bench": [{
            "player_name": player.name,
            "position": player.position,
            "total_points": player.total_points,
        } for player in my_team.roster if not player.starter],  # Only bench players
        "schedule": [{
            "week": week + 1,  # Week numbering starts from 1
            "opponent": game.opponent.team_name,
            "result": game.result
        } for week, game in enumerate(my_team.schedule)],
    }
    return team_data

# Function to save data to JSON file
def save_data_to_json(data, filename):
    """
    Saves the given data to a JSON file.
    
    Args:
        data (dict): Data to be saved.
        filename (str): The name of the JSON file.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Main function to execute the process
def main(league_id, year, my_team_id, espn_s2, swid):
    """
    Main function to extract league and team data, and save them to JSON files.
    
    Args:
        league_id (int): The ID of the ESPN Fantasy League.
        year (int): The year of the league.
        my_team_id (int): The ID of your team in the league.
    """
    # Step 1: Initialize the league
    league = initialize_league(league_id, year, espn_s2, swid)

    #print welcome message with basic team info
    print(f"\nChecking stats for {league.teams[my_team_id-1].team_name}!")
    print("\n...\n")
    
    # Step 2: Extract league data
    league_data = extract_league_data(league)

    # Step 3: Get your specific team from the league
    my_team = next(team for team in league.teams if team.team_id == my_team_id)

    # Step 4: Extract detailed team data
    team_data = extract_team_data(my_team)

    # Step 5: Save the data to JSON files
    save_data_to_json(league_data, 'granular_league_data.json')
    save_data_to_json(team_data, 'granular_team_data.json')

# Example of how to call the main function
if __name__ == '__main__':
    league_id = 1339216694  # Replace with your league ID
    year = 2024  # Replace with the current year, e.g., 2024
    my_team_id = 2  # Replace with your team ID
    main(league_id, year, my_team_id, secrets.espn_s2, secrets.SWID)
