from espn_api.football import League
import json
import pyperclip
import datetime
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Try to import secrets.py; if it fails, handle the error
try:
    import secrets
    espn_s2 = secrets.espn_s2
    swid = secrets.SWID
except ImportError:
    espn_s2 = None
    swid = None
    messagebox.showerror("Error", "Missing secrets.py! Please ensure that secrets.py exists and contains your ESPN S2 and SWID cookies.")

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
    """
    with open("prompt.txt", "r") as file:
        prompt_text = file.read()

    # Copy the text to the clipboard
    pyperclip.copy(prompt_text)
    print("The Fantasy Football Coach ChatGPT prompt has been copied to your clipboard!\n")

def run_export_data(league_id, year, my_team_id, espn_s2, swid, status_label, team_label, week_label):
    try:
        # Check if espn_s2 and swid are available
        if not espn_s2 or not swid:
            raise ValueError("Missing ESPN S2 or SWID cookies. Please ensure secrets.py is correctly configured.")
        
        # Initialize the league and export data
        league = initialize_league(league_id, year, espn_s2, swid)
        week = league.current_week
        team_name = league.teams[my_team_id - 1].team_name
        
        # Export league data
        export_all_league_data(league, my_team_id, week)

        # Update the status, team name, and week number
        status_label.config(text=f"Data for Week {week} exported successfully!", bootstyle="success")
        team_label.config(text=f"Team: {team_name}", bootstyle="warning")
        week_label.config(text=f"Week: {week}", bootstyle="warning")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {str(e)}")

def copy_gpt_prompt(status_label):
    try:
        # Copy prompt to clipboard
        copy_prompt_to_clipboard()
        status_label.config(text="ChatGPT prompt copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy prompt: {str(e)}")

# GUI setup
def create_gui():
    root = ttk.Window(themename="superhero")  # You can choose different themes here
    root.title("Fantasy Football Data Exporter")
    root.geometry("400x450")  # Set window size
    
    # Title label
    title_label = ttk.Label(root, text="Fantasy Football Data Exporter", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    # Labels and Entries for league_id, year, team_id, espn_s2, swid
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="League ID:", font=("Helvetica", 12), bootstyle="info").grid(row=0, column=0, padx=5, pady=5)
    league_id_entry = ttk.Entry(input_frame, width=20)
    league_id_entry.grid(row=0, column=1, padx=5, pady=5)
    league_id_entry.insert(0, str(1339216694))  # Prefill with existing data

    ttk.Label(input_frame, text="Year:", font=("Helvetica", 12), bootstyle="info").grid(row=1, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(input_frame, width=20)
    year_entry.grid(row=1, column=1, padx=5, pady=5)
    year_entry.insert(0, "2024")  # Prefill with existing data
    
    ttk.Label(input_frame, text="Team ID:", font=("Helvetica", 12), bootstyle="info").grid(row=2, column=0, padx=5, pady=5)
    team_id_entry = ttk.Entry(input_frame, width=20)
    team_id_entry.grid(row=2, column=1, padx=5, pady=5)
    team_id_entry.insert(0, str(2))  # Prefill with existing data
    
    ttk.Label(input_frame, text="ESPN S2:", font=("Helvetica", 12), bootstyle="info").grid(row=3, column=0, padx=5, pady=5)
    espn_s2_entry = ttk.Entry(input_frame, width=20)
    espn_s2_entry.grid(row=3, column=1, padx=5, pady=5)
    espn_s2_entry.insert(0, espn_s2 if espn_s2 else "")  # Prefill with data from secrets.py
    
    ttk.Label(input_frame, text="SWID:", font=("Helvetica", 12), bootstyle="info").grid(row=4, column=0, padx=5, pady=5)
    swid_entry = ttk.Entry(input_frame, width=20)
    swid_entry.grid(row=4, column=1, padx=5, pady=5)
    swid_entry.insert(0, swid if swid else "")  # Prefill with data from secrets.py
    
    # Team name and week number labels
    team_label = ttk.Label(root, text="Team: ", font=("Helvetica", 12), bootstyle="warning")
    team_label.pack(pady=5)

    week_label = ttk.Label(root, text="Week: ", font=("Helvetica", 12), bootstyle="warning")
    week_label.pack(pady=5)
    
    # Status label
    status_label = ttk.Label(root, text="", font=("Helvetica", 12), bootstyle="success")
    status_label.pack(pady=5)

    # Buttons with custom styling
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    export_button = ttk.Button(button_frame, text="Export Data", command=lambda: run_export_data(
        int(league_id_entry.get()), int(year_entry.get()), int(team_id_entry.get()),
        espn_s2_entry.get(), swid_entry.get(), status_label, team_label, week_label))
    export_button.grid(row=0, column=0, padx=10, pady=10)

    copy_button = ttk.Button(button_frame, text="Copy ChatGPT Prompt", command=lambda: copy_gpt_prompt(status_label))
    copy_button.grid(row=0, column=1, padx=10, pady=10)

    # Start the GUI loop
    root.mainloop()

# Main function to execute the process
'''def main(league_id, year, my_team_id, espn_s2, swid):
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
''' 
# Run Script
if __name__ == '__main__':
    create_gui()
    """
    y = input("Press Enter to exit...")
    league_id = 1339216694  # Replace with your league ID
    year = 2024  # Replace with the current year, e.g., 2024
    my_team_id = 2  # Replace with your team ID
    main(league_id, year, my_team_id, secrets.espn_s2, secrets.SWID)"""
