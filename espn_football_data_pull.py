from espn_api.football import League
import json
import secrets
import pyperclip
import datetime
import os

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

def export_team_info(league, my_team_id):
    team = league.teams[my_team_id - 1]
    team_data = {
        "team_name": team.team_name,
        "wins": team.wins,
        "losses": team.losses,
        "points_for": team.points_for,
        "points_against": team.points_against,
        "acquisitions": team.acquisitions,
        "acquisition_budget_spent": team.acquisition_budget_spent,
        "roster": [{
            "player_name": player.name,
            "position": player.position,
            "points": player.total_points,
            "projected_points": player.projected_total_points,
            "injured": player.injured
        } for player in team.roster]
    }
    return team_data

def export_player_info(league, my_team_id):
    team = league.teams[my_team_id - 1]
    players = [{
        "name": player.name,
        "position": player.position,
        "total_points": player.total_points,
        "avg_points": player.avg_points,
        "projected_total_points": player.projected_total_points,
        "injury_status": player.injuryStatus
    } for player in team.roster]
    return players

def export_matchup_info(league, week):
    box_scores = league.box_scores(week)
    matchups = [{
        "home_team": box.home_team.team_name,
        "away_team": box.away_team.team_name,
        "home_score": box.home_score,
        "away_score": box.away_score,
        "home_projected": box.home_projected,
        "away_projected": box.away_projected,
        "home_lineup": [{
            "player_name": player.name,
            "points": player.points,
            "projected_points": player.projected_points
        } for player in box.home_lineup],
        "away_lineup": [{
            "player_name": player.name,
            "points": player.points,
            "projected_points": player.projected_points
        } for player in box.away_lineup]
    } for box in box_scores]
    return matchups

def export_free_agents(league, position=None, size=10):
    if position:
        free_agents = league.free_agents(size=size, position=position)
    else:
        free_agents = league.free_agents(size=size)
    
    agents = [{
        "name": player.name,
        "position": player.position,
        "total_points": player.total_points,
        "projected_points": player.projected_total_points
    } for player in free_agents]
    return agents

def export_power_rankings(league, week):
    rankings = league.power_rankings(week)
    return [{"team_name": team[1].team_name, "score": team[0]} for team in rankings]

def export_recent_activity(league, size=25, msg_type=None):
    """
    Export recent activity (news) from the league.
    
    Args:
        league (League): The fantasy league object.
        size (int): The number of recent activities to fetch.
        msg_type (str): The type of message to filter, e.g., 'TRADED', 'WAIVER', etc.
        
    Returns:
        List of recent activity in the league.
    """
    # Fetch recent activity from the league
    if msg_type:
        activity = league.recent_activity(size=size, msg_type=msg_type)
    else:
        activity = league.recent_activity(size=size)

    # Format recent activity data
    recent_activity_data = [{
        "date": act.date,
        "actions": [{
            "team": action[0].team_name,
            "action_type": action[1],
            "player_name": action[2].name
        } for action in act.actions]
    } for act in activity]

    return recent_activity_data

def get_date_info(league):
    """
    Get the current date and time information for the league.
    
    Args:
        league (League): The fantasy league object.
        
    Returns:
        Dictionary containing the current date and time information.
    """
    date_info = {
        "current_day of the week": datetime.datetime.now().strftime("%A"),
        "current_week": league.current_week,
    }
    return date_info


def export_all_league_data(league, my_team_id, week):
    team_info = export_team_info(league, my_team_id)
    player_info = export_player_info(league, my_team_id)
    matchup_info = export_matchup_info(league, week)
    free_agents = export_free_agents(league)
    power_rankings = export_power_rankings(league, week)
    recent_activity = export_recent_activity(league)
    date_info = get_date_info(league)

    data = {
        "date_info": date_info,
        "team_info": team_info,
        "player_info": player_info,
        "matchup_info": matchup_info,
        "free_agents": free_agents,
        "power_rankings": power_rankings,
        "recent_activity": recent_activity
    }
    
    # Save to JSON in a subfolder

    folder_path = os.path.dirname(os.path.abspath(__file__)) + "/data_exports"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = f"{folder_path}/league_data_week_{week}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"Exporting data to: {file_path}")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return data

def copy_prompt_to_clipboard():
    """
    Copies the detailed Fantasy Football Coach GPT prompt to the clipboard.
    
    Args:
        week (int): The current week of the fantasy football league.
        day (str): The current day of the week.
    """
    prompt_text = """
    ### Fantasy Football Coach GPT Prompt

    **Context:**  
    You are a Fantasy Football coach that helps analyze team performance, matchups, player statistics, and other league factors to recommend actions for managing a fantasy football team. I am providing you with a JSON file that contains data on my team’s performance, my players’ stats, upcoming matchups, recent league activities (trades, waiver wire changes, etc.), injury reports, free agents, power rankings, and more. Please carefully analyze the data and offer your best recommendations on what actions, if any, I should take to improve my team's performance.

    **Data Provided:**  
    Here’s a JSON file that includes detailed information about my team, the league, and other important data. Please analyze the following:
    1. **Team Information**: My team’s record, wins, losses, points scored and allowed, and overall performance.
    2. **Player Performance**: Current and projected points for each player on my roster, including injury statuses and positional rankings.
    3. **Injury Reports**: Information about any injured players on my team and how their injury status might affect my lineup.
    4. **Matchup Information**: Upcoming matchups, including the projected scores for both my team and my opponent, key players in the opponent’s lineup, and any potential advantages or disadvantages.
    5. **Free Agents and Waiver Wire**: Players available for acquisition, including their performance stats, projected points, and percent ownership in other leagues.
    6. **Power Rankings and Standings**: Where my team ranks in the league compared to others, and how my team is performing in relation to the rest of the competition.
    7. **Recent Activity**: Trades, player additions/drops, and any other recent activities within the league.
    8. **Roster News**: Any important roster updates or news related to my team.

    **Task:**  
    1. **Quick Overview**: Start by giving me a brief overview of how my team is looking this week. Highlight any key developments, trends, or interesting insights that I should be aware of. You can mention things like:
       - Any standout performances or slumps from players on my team.
       - Important injury news.
       - Projected outcomes of the upcoming matchup.
       - Recent league activity (e.g., trades, drops, waiver pickups) that may impact my team.
       - Anything else notable that stands out for the week.

    2. **Detailed Recommendations**: After the overview, please provide detailed and unbiased recommendations on the following:
       - **Lineup Adjustments**: Should I make any changes to my current starting lineup? If so, which players should I start or bench, and why? Consider player performance, injury risks, and matchups for the upcoming week.
       - **Waiver Wire or Free Agent Acquisitions**: Are there any players available in the free agent pool or on the waiver wire who I should consider adding to improve my team? If so, who should I drop from my roster, and why?
       - **Trades**: Based on my team's strengths and weaknesses, should I consider proposing any trades? If so, which players should I target or offer, and why? Be sure to consider both my team's needs and potential trade partners in the league.
       - **Long-Term Strategy**: Are there any long-term strategic decisions I should consider, such as preparing for the playoffs, trading for injured players who might recover, or acquiring players with favorable schedules later in the season?
       - **Matchup-Specific Strategies**: Do you notice any specific advantages or disadvantages in my upcoming matchup that I should exploit or be cautious about? Should I adjust my lineup to maximize my chances in this specific matchup?
       - **Power Rankings and League Position**: Based on my current standing in the league, what steps should I take to improve my position or maintain my lead? How can I optimize my chances for making the playoffs or securing a better seeding?

    **Important Considerations:**
    - Feel free to search the internet for additional information and context on what's going on right now in the league.
    - Please consider both short-term and long-term implications for any actions you recommend.
    - Take into account potential risks (e.g., injury-prone players, tough upcoming matchups) and rewards (e.g., breakout players, favorable schedules).
    - Provide detailed reasoning behind every recommendation, explaining why a specific change or action would be beneficial for my team.
    - Avoid bias based on my past decisions or current roster. Focus solely on the data provided and the best available actions to improve my team’s performance.
    - With the recommendations, pick one set of things I should do, and DON'T GIVE OPTIONS. Just tell me exactly what you think is the best course of action as concisely as possible.

    **JSON Input Format:**  
    The JSON file contains data in the following format (this is a sample structure to guide your analysis):
    '''json
    {
        "team_info": {
            "team_name": "My Team",
            "wins": 5,
            "losses": 3,
            "points_for": 1025,
            "points_against": 1000,
            ...
        },
        "player_info": [
            {
                "name": "Player 1",
                "position": "WR",
                "total_points": 150,
                "projected_points": 20,
                "injury_status": "Healthy",
                ...
            },
            ...
        ],
        "matchup_info": {
            "my_team_projected": 110,
            "opponent_team_name": "Opponent Team",
            "opponent_projected_score": 115,
            "opponent_key_players": [
                {
                    "name": "Opponent Player 1",
                    "points": 200,
                    "projected_points": 25
                },
                ...
            ]
        },
        "free_agents": [
            {
                "name": "Free Agent 1",
                "position": "RB",
                "total_points": 100,
                "projected_points": 12,
                ...
            },
            ...
        ],
        "recent_activity": [
            {
                "date": 1694032512000,
                "action_type": "ADDED",
                "player_name": "New Player",
                "position": "WR",
                ...
            },
            ...
        ],
        "power_rankings": [
            {
                "team_name": "Top Team",
                "score": 95.5
            },
            ...
        ],
        "injury_news": [
            {
                "name": "Player 2",
                "position": "RB",
                "injury_status": "Questionable",
                "projected_points": 15,
                ...
            }
        ]
    }
    '''

    **Output Format:**  
    Return your analysis in two sections:
    1. **Quick Overview**: A brief summary of how my team is looking this week, highlighting key developments.
    2. **Recommendations**: A detailed list of recommended actions, with explanations for each suggestion.
    """

    # Copy the text to the clipboard
    pyperclip.copy(prompt_text)
    print("The Fantasy Football Coach GPT prompt has been copied to your clipboard!\n")

# Main function to execute the process
def main(league_id, year, my_team_id, espn_s2, swid):
    """
    Main function to extract league and team data, and save them to JSON files.
    
    Args:
        league_id (int): The ID of the ESPN Fantasy League.
        year (int): The year of the league.
        my_team_id (int): The ID of your team in the league.
    """

    # Initialize the league
    league = initialize_league(league_id, year, espn_s2, swid)
    week = league.current_week

    # Export all league data
    exported_data = export_all_league_data(league, my_team_id, week)
    
    print(f"\nData for Week {week} has been exported successfully!\n")

    # Copy the GPT prompt to clipboard
    copy_prompt_to_clipboard()
 
# Call the main function
if __name__ == '__main__':
    league_id = 1339216694  # Replace with your league ID
    year = 2024  # Replace with the current year, e.g., 2024
    my_team_id = 2  # Replace with your team ID
    main(league_id, year, my_team_id, secrets.espn_s2, secrets.SWID)
