from datetime import date
import streamlit as st
import pandas as pd

League_Name = "Great Lakes Championship Series"
League_Abbreviation = "GLCS"
League_Season_Number = 1
League_Season_Type = "REG"

# streamlit run .\app.py

def View_Data(Team_Game_Data, Player_Game_Data, current_date,num):
    with st.expander("View / Download Uploaded Data"):
        Team_CheckBox = st.checkbox("Show All Team Game Data",key=f"show_team_data_after_form{num}")
        if Team_CheckBox:
            st.dataframe(Team_Game_Data.style.hide(axis="index"))

        Player_CheckBox = st.checkbox("Show Player Data", key=f"show_player_data_after_form{num}")
        if Player_CheckBox:
            st.dataframe(Player_Game_Data.style.hide(axis="index"))

        Download_Data(current_date,1)

def Download_Data(current_date,num):
    if not st.session_state.Team_Game_Data.empty:
            csv_team_data = (st.session_state.Team_Game_Data.to_csv(index=False).encode("utf-8"))
            st.download_button("Download Raw_Team_Data as CSV",csv_team_data,f"Raw_Team_Data-{current_date}.csv","text/csv",key=f"download_team_data_button_{num}")

    if not st.session_state.Player_Game_Data.empty:
        csv_player_data = (st.session_state.Player_Game_Data.to_csv(index=False).encode("utf-8-sig"))
        st.download_button("Download Raw_Player_Data as CSV",csv_player_data,f"Raw_Player_Data-{current_date}.csv","text/csv",key=f"download_player_data_button_{num}",)

def Data_Entry(League_Teams, League_Roster,Team_Game_Data, Player_Game_Data, current_date):
    # Dropping Free Agent Row if Present
    League_Teams = League_Teams.drop(index=0)
    # Team Inputs Needed Before Submitting Team Data
    team_cols = st.columns(2)
    with team_cols[0]:
        Team_1_Selection = st.selectbox(f"Choose {League_Abbreviation} Team #1", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team1_Select")
        Team_1_Code = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Team_Code'].values[0] if Team_1_Selection else None
    with team_cols[1]:
        Team_2_Selection = st.selectbox(f"Choose {League_Abbreviation} Team #2", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team2_Select")
        Team_2_Code = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Team_Code'].values[0] if Team_2_Selection else None
    
    Team_1_Roster = League_Roster.loc[League_Roster['Team_Name'] == Team_1_Selection].sort_values("Skater_Name")
    Team_2_Roster = League_Roster.loc[League_Roster['Team_Name'] == Team_2_Selection].sort_values("Skater_Name")
    Game_Result = ('Win_Reg', 'Win_OT', 'Loss_Reg', 'Loss_OT')
    Puck_Positions = ('LW', 'C', 'RW', 'LD', 'RD', 'G')
    """
    """
    
    if Team_1_Selection and Team_2_Selection:
        with st.form("game_stats_form", clear_on_submit=True):
            # Determine the next GAME_ID
            if Team_Game_Data.empty:
                Game_ID = 1
            else:
                Game_ID = Team_Game_Data['GAME_ID'].max() + 1 
            # Week and Game Number Inputs
            st.markdown(f"<h4 style='text-align: center;'>1. Enter Week and Game Number</h4>", unsafe_allow_html=True)
            weekandgamenumber_columns = st.columns(2)
            with weekandgamenumber_columns[0]:
                Week = st.number_input("Week", min_value=1, max_value=52, step=1)
            with weekandgamenumber_columns[1]:
                Game_Number = st.number_input("Game Number", min_value=1, step=1)
            
            # Game Results Inputs
            st.markdown(f"<h4 style='text-align: center;'>2. Enter the Game Results for Both Teams</h4>", unsafe_allow_html=True)
            game_result_columns = st.columns(2)
            with game_result_columns[0]:
                team1_result = st.selectbox(f"{Team_1_Selection}'s Game Result", Game_Result, index=None, placeholder="Please Select Result", key="team1_result")
                
            with game_result_columns[1]:
                team2_result = st.selectbox(f"{Team_2_Selection}'s Game Result", Game_Result, index=None, placeholder="Please Select Result", key="team2_result")

            # Game Winning Goal Scorer Selection
            st.markdown(f"<h4 style='text-align: center;'>3. Select Game Winning Goal Scorer</h4>", unsafe_allow_html=True)
            Combined_Skaters = pd.concat([
                Team_1_Roster[['Team_Code', 'Skater_Name']], 
                Team_2_Roster[['Team_Code', 'Skater_Name']]], ignore_index=True).drop_duplicates().sort_values(['Team_Code', 'Skater_Name']).reset_index(drop=True)
            
            Combined_Skaters['Display_Name'] = Combined_Skaters['Team_Code'].astype(str) + ' - ' + Combined_Skaters['Skater_Name']
            GWG_Player = st.selectbox("Select Game Winning Goal Scorer", Combined_Skaters['Display_Name'], index=None, placeholder="Please Select GWG Scorer", key="GWG_Player_Select")
            
            st.markdown(f"<h3 style='text-align: center;'>Enter Game Data</h3>", unsafe_allow_html=True)
            # Initialize row counts if needed
            if 'team1_rows' not in st.session_state:
                st.session_state.team1_rows = 4
            if 'team2_rows' not in st.session_state:
                st.session_state.team2_rows = 4

            def add_team1_row():
                st.session_state.team1_rows += 1

            def add_team2_row():
                st.session_state.team2_rows += 1

            team1_data = []
            team2_data = []

            Team1_Key = f"{Team_1_Code}_player_"
            Team2_Key = f"{Team_2_Code}_player_"
            
            st.header(f"{Team_1_Selection}")
            for i in range(st.session_state.team1_rows):
                # """
                # ==================== Team 1 inputs ====================
                # """
                cols = st.columns([1, 2, 1.5, 1.5, 1.5])
                Team1_Skater_Position = cols[0].selectbox("Position", Puck_Positions, key=f"{Team1_Key}Skater_Position{i}")
                Team1_Skater_Name = cols[1].selectbox(f"Skater #{i+1}", Team_1_Roster["Skater_Name"], key=f"{Team1_Key}Skater_Name{i}")
                Team1_Goals = cols[2].number_input("Goals", min_value=0, step=1, key=f"{Team1_Key}Goals{i}")
                Team1_Assists = cols[3].number_input("Assists", min_value=0, step=1, key=f"{Team1_Key}Assists{i}")
                Team1_Points = Team1_Goals + Team1_Assists
                Team1_SOG = cols[4].number_input("SOG", min_value=0, step=1, key=f"{Team1_Key}Shots_On_Goal{i}")
                
                team1_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Conference'].values[0] if Team_1_Selection else None
                team1_div = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Division'].values[0] if Team_1_Selection else None
                
                Team1_Skater_Type = League_Roster.loc[League_Roster['Skater_Name'] == Team1_Skater_Name]['Skater_Type'].values[0]
                # Team1_Plus_Minus = Team1_Game_Data['Plus/Minus'].iloc[0]
                # Team1_Shoutout = Team1_Game_Data['Shoutout'].iloc[0]
                # Team1_ID = Team1_Game_Data['GAME_ID'].iloc[0]

                team1_data.append({
                    "Skater_Name": Team1_Skater_Name,
                    "GAME_ID": Game_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team1_conf,
                    "Division":team1_div,   
                    "Skater_Type": Team1_Skater_Type,
                    "Position": Team1_Skater_Position,
                    "Team_Name": Team_1_Selection,
                    "Team_Code": Team_2_Code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Team1_Goals,
                    "Assists": Team1_Assists,
                    "Points": Team1_Points,
                    "SOG": Team1_SOG,
                    "GWG": None,
                    "Game_Result": team1_result,
                    "Shoutout": None,
                    "Plus/Minus": None,
                    "Goalie_Goals_Allowed": None,
                    "Goalie_Shots_Allowed": None,
                    "Goalie_Saves": None,
                    
                })
            # """
            # ==================== Team 2 inputs ====================
            # """
            st.header(f"{Team_2_Selection}")

            for i in range(st.session_state.team2_rows):
                cols = st.columns([1, 2, 1.5, 1.5, 1.5])
                Team2_Skater_Position = cols[0].selectbox("Position", Puck_Positions, key=f"{Team2_Key}Skater_Position{i}")
                Team2_Skater_Name = cols[1].selectbox(f"Skater #{i+1}", Team_2_Roster["Skater_Name"], key=f"{Team2_Key}Skater_Name{i}")
                Team2_Goals = cols[2].number_input("Goals", min_value=0, step=1, key=f"{Team2_Key}Goals{i}")
                Team2_Assists = cols[3].number_input("Assists", min_value=0, step=1, key=f"{Team2_Key}Assists{i}")
                Team2_Points = Team2_Goals + Team2_Assists
                Team2_SOG = cols[4].number_input("SOG", min_value=0, step=1, key=f"{Team2_Key}Shots_On_Goal{i}")

                team2_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Conference'].values[0] if Team_2_Selection else None
                team2_div = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Division'].values[0] if Team_2_Selection else None
                
                Team2_Skater_Type = League_Roster.loc[League_Roster['Skater_Name'] == Team2_Skater_Name]['Skater_Type'].values[0]
                # Team2_Plus_Minus = Team2_Game_Data['Plus/Minus'].iloc[0]
                # Team2_Shoutout = Team2_Game_Data['Shoutout'].iloc[0]
                # Team2_ID = Team2_Game_Data['GAME_ID'].iloc[0]
                
                team2_data.append({
                    "Skater_Name": Team2_Skater_Name,
                    "GAME_ID": Game_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team2_conf,
                    "Division":team2_div,     
                    "Skater_Type": Team2_Skater_Type,
                    "Position": Team2_Skater_Position,
                    "Team_Name": Team_2_Selection,
                    "Team_Code": Team_2_Code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Team2_Goals,
                    "Assists": Team2_Assists,
                    "Points": Team2_Points,
                    "SOG": Team2_SOG,
                    "GWG": None,
                    "Game_Result": team2_result,
                    "Shoutout": None,
                    "Plus/Minus": None,
                    "Goalie_Goals_Allowed": None,
                    "Goalie_Shots_Allowed": None,
                    "Goalie_Saves": None,    
                })

            # """
            # ==================== Team 1 Goalie inputs ====================
            # """
            st.markdown(f"<h1 style='text-align: center;'>Goalie Entry</h1>", unsafe_allow_html=True)
            
            cols = st.columns([2, 1.5, 1.5, 1.5])
            Team1_Goalie_Name = cols[0].selectbox(f"{Team_1_Selection} - Goalie Data Entry", Team_1_Roster["Skater_Name"], key=f"Team1_Goalie_Name1")
            
            Goalie1_Goals = cols[1].number_input("Goals", min_value=0, step=1, key=f"Team1_Goalie_Goals{i}")
            Goalie1_Assists = cols[2].number_input("Assists", min_value=0, step=1, key=f"Team1_Goalie_Assists{i}")
            Goalie1_Points = Goalie1_Goals + Goalie1_Assists
            Goalie1_SOG = cols[3].number_input("SOG", min_value=0, step=1, key=f"Team1_Goalie_Shots_On_Goal{i}")
            
            team1_g_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Conference'].values[0] if Team_1_Selection else None
            team1_g_div = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Division'].values[0] if Team_1_Selection else None
        
            team1_data.append({
                    "Skater_Name": Team1_Goalie_Name,
                    "GAME_ID": Game_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team1_g_conf,
                    "Division":team1_g_div,   
                    "Skater_Type": "Goalie",
                    "Position": "G",
                    "Team_Name": Team_1_Selection,
                    "Team_Code": Team_1_Code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Goalie1_Goals,
                    "Assists": Goalie1_Assists,
                    "Points": Goalie1_Points,
                    "SOG": Goalie1_SOG,
                    "GWG": None,
                    "Game_Result": team1_result,
                    "Shoutout": None,
                    "Plus/Minus": None,
                    "Goalie_Goals_Allowed": None,
                    "Goalie_Shots_Allowed": None,
                    "Goalie_Saves": None,
                    
                })
            
            # """
            # ==================== Team 2 Goalie inputs ====================
            # """
            cols = st.columns([2, 1.5, 1.5, 1.5])
            Team2_Goalie_Name = cols[0].selectbox(f"{Team_2_Selection} - Goalie Data Entry", Team_2_Roster["Skater_Name"], key=f"Team2_Goalie_Name2")

            Goalie2_Goals = cols[1].number_input("Goals", min_value=0, step=1, key=f"Team2_Goalie_Goals{i}")
            Goalie2_Assists = cols[2].number_input("Assists", min_value=0, step=1, key=f"Team2_Goalie_Assists{i}")
            Goalie2_Points = Goalie2_Goals + Goalie2_Assists
            Goalie2_SOG = cols[3].number_input("SOG", min_value=0, step=1, key=f"Team2_Goalie_Shots_On_Goal{i}")
            
            team2_g_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Conference'].values[0] if Team_2_Selection else None
            team2_g_div = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Division'].values[0] if Team_2_Selection else None
            
            # Team2_g_Shoutout = Team1_Game_Data['Shoutout'].iloc[0]
            # Team2_g_Plus_Minus = Team1_Game_Data['Plus/Minus'].iloc[0]
            # Team2_G_ID = Team2_Game_Data['GAME_ID'].iloc[0]
            
            team2_data.append({
                "Skater_Name": Team2_Goalie_Name,
                "GAME_ID": Game_ID,
                "League": League_Abbreviation,
                "Season": League_Season_Number,
                "Season_Type": League_Season_Type,
                "Conference": team2_g_conf,
                "Division":team2_g_div,   
                "Skater_Type": "Goalie",
                "Position": "G",
                "Team_Name": Team_2_Selection,
                "Team_Code": Team_2_Code,
                "Week": Week,
                "Game_Number": Game_Number,
                "Goals": Goalie2_Goals,
                "Assists": Goalie2_Assists,
                "Points": Goalie2_Points,
                "SOG": Goalie2_SOG,
                "GWG": None,
                "Game_Result": team2_result,
                "Shoutout": None,
                "Plus/Minus": None,
                "Goalie_Goals_Allowed": None,
                "Goalie_Shots_Allowed": None,
                "Goalie_Saves": None,
                
            })
            st.markdown("---")
            # Buttons to add rows for each team
            col_add_row = st.columns(2)
            with col_add_row[0]:
                add_row_team_1 = st.form_submit_button("Add Another Player to Team 1", on_click=add_team1_row)
            with col_add_row[1]:
                add_row_team_2 = st.form_submit_button("Add Another Player to Team 2", on_click=add_team2_row)

            # Submit button for all players
            submitted = st.form_submit_button("Submit Players")

        if submitted:
            # Convert team data lists to DataFrames
            team1_data_DF = pd.DataFrame(team1_data)
            team2_data_DF = pd.DataFrame(team2_data)
            # Assign GWG to the selected player
            if GWG_Player:
                selected_skater_name = GWG_Player.split(' - ')[-1]
                for df in [team1_data_DF, team2_data_DF]:
                    df.loc[df['Skater_Name'] == selected_skater_name, 'GWG'] = "Yes"


            # Shutout logic (can be inside form or just after submit)
            team1_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Conference'].values[0] if Team_1_Selection else None
            team2_conf = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Conference'].values[0] if Team_2_Selection else None

            team1_div = League_Teams.loc[League_Teams['Team_Name'] == Team_1_Selection, 'Division'].values[0] if Team_1_Selection else None
            team2_div = League_Teams.loc[League_Teams['Team_Name'] == Team_2_Selection, 'Division'].values[0] if Team_2_Selection else None

            team1_goals = team1_data_DF['Goals'].sum()  
            team2_goals = team2_data_DF['Goals'].sum()  # Sum goals from all players including goalie

            team1_assists = team1_data_DF['Assists'].sum()  # Sum assists from all players including goalie
            team2_assists = team2_data_DF['Assists'].sum()  # Sum assists from all players including goalie 
            team1_shots = team1_data_DF['SOG'].sum()  # Sum shots from all players including goalie
            team2_shots = team2_data_DF['SOG'].sum()  # Sum shots from all players including goalie
            team1_plus_minus = team1_goals - team2_goals
            team2_plus_minus = team2_goals - team1_goals

            team1_saves = team2_shots - team2_goals
            team2_saves = team1_shots - team1_goals  # Goalie saves
            # Shutout logic
            if team1_goals == 0 and team2_goals > 0:
                team1_shutout = "No"
                team2_shutout = "Yes"
            elif team2_goals == 0 and team1_goals > 0:
                team1_shutout = "Yes"
                team2_shutout = "No"
            else:
                team1_shutout = "No"
                team2_shutout = "No"
            # Points logic
            if team1_result == "Win_Reg":
                team1_points = 2
                team2_points = 0
            elif team1_result == "Win_OT":
                team1_points = 2
                team2_points = 1
            elif team1_result == "Loss_Reg":
                team1_points = 0
                team2_points = 2
            elif team1_result == "Loss_OT":
                team1_points = 1
                team2_points = 2



            # set the same value for all rows
            team1_data_DF["Shoutout"] = team1_shutout 
            team2_data_DF["Shoutout"] = team2_shutout
            team1_data_DF["Plus/Minus"] = team1_plus_minus
            team2_data_DF["Plus/Minus"] = team2_plus_minus


            #Update Goalie Stats
            team1_goalie_only = team1_data_DF['Position'] == "G"
            team1_data_DF.loc[team1_goalie_only, 'Goalie_Goals_Allowed'] = team2_goals
            team1_data_DF.loc[team1_goalie_only, 'Goalie_Shots_Allowed'] = team2_shots
            team1_data_DF.loc[team1_goalie_only, 'Goalie_Saves'] = team1_saves

            team2_goalie_only = team2_data_DF['Position'] == "G"
            team2_data_DF.loc[team2_goalie_only, 'Goalie_Goals_Allowed'] = team1_goals
            team2_data_DF.loc[team2_goalie_only, 'Goalie_Shots_Allowed'] = team1_shots
            team2_data_DF.loc[team2_goalie_only, 'Goalie_Saves'] = team2_saves

            data = [
                {
                    "GAME_ID": Game_ID,
                    "Team_Name": Team_1_Selection,
                    "Team_Code": Team_1_Code,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team1_conf,
                    "Division":team1_div,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": team1_goals,
                    "Assists": team1_assists,
                    "Shots": team1_shots,
                    "Saves": team1_saves,
                    "Game_Result": team1_result,
                    "Points": team1_points,
                    "Shoutout": team1_shutout,
                    "Plus/Minus": team1_plus_minus,
                    "Away_Team_Name": Team_2_Selection,
                    "Away_Team_Code": Team_2_Code,
                    "Away_Team_Goals": team2_goals,
                    "Away_Team_Assists": team2_assists,
                    "Away_Team_Shots": team2_shots,
                    "Away_Team_Saves": team2_saves,
                },
                {
                    "GAME_ID": Game_ID,
                    "Team_Name": Team_2_Selection,
                    "Team_Code": Team_2_Code,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team2_conf,
                    "Division":team2_div,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": team2_goals,
                    "Assists": team2_assists,
                    "Shots": team2_shots,
                    "Saves": team2_saves,
                    "Game_Result": team2_result,
                    "Points": team2_points,
                    "Shoutout": team2_shutout,
                    "Plus/Minus": team2_plus_minus,
                    "Away_Team_Name": Team_1_Selection,
                    "Away_Team_Code": Team_1_Code,
                    "Away_Team_Goals": team1_goals,
                    "Away_Team_Assists": team1_assists,
                    "Away_Team_Shots": team1_shots,
                    "Away_Team_Saves": team1_saves,
                }
            ]
            new_df = pd.DataFrame(data)

            if Team_Game_Data.empty:
                st.session_state['Team_Game_Data'] = new_df
            else:
                st.session_state['Team_Game_Data'] = pd.concat([Team_Game_Data, new_df], ignore_index=True)

            st.session_state['Team_Game_Data'] = st.session_state['Team_Game_Data'].reset_index(drop=True)
            new_data = pd.concat([pd.DataFrame(team1_data_DF), pd.DataFrame(team2_data_DF)], ignore_index=True)
            st.session_state.Player_Game_Data = pd.concat([st.session_state.Player_Game_Data, new_data], ignore_index=True)
            
            st.session_state.team1_rows = 4
            st.session_state.team2_rows = 4
            st.rerun()
            
        else:    
            # Show Newest Team Data Added
            Download_Data(current_date,2)
            show_newest_team_data = st.checkbox("Show Newest Team Data (Last 2)", key="show_newest_team_after_submit")
            if show_newest_team_data:
                Newest_Team_Data_Added = st.session_state['Team_Game_Data'].tail(2)
                st.dataframe(Newest_Team_Data_Added.style.hide(axis="index"))    
            
            # Show Newest Player Data Added
            show_newest_player_data = st.checkbox("Show Newest Player Data (Last 12)", key="show_newest_player_after_submit")
            if show_newest_player_data:
                Newest_Player_Data_Added = st.session_state['Player_Game_Data'].tail(12)
                st.dataframe(Newest_Player_Data_Added.style.hide(axis="index"))
            
        
def main():
    current_date = date.today()

    League_Teams = st.session_state.get('League_Teams', pd.DataFrame())
    League_Roster = st.session_state.get('League_Roster', pd.DataFrame())
    Team_Game_Data = st.session_state.get('Team_Game_Data', pd.DataFrame())
    Player_Game_Data = st.session_state.get('Player_Game_Data', pd.DataFrame())

    if all([
    'League_Teams' in st.session_state and not st.session_state['League_Teams'].empty,
    'League_Roster' in st.session_state and not st.session_state['League_Roster'].empty,
    ]):
        st.title(f"{League_Abbreviation} Team Results ",width='stretch',)
        View_Data(Team_Game_Data, Player_Game_Data, current_date,1)
        Data_Entry(League_Teams, League_Roster,Team_Game_Data, Player_Game_Data, current_date)
        
    else:
        st.warning("Go Back to the app page to load the files or please upload all 4 required CSV files to proceed.")

if __name__ == "__main__":
    main()

# streamlit run .\1_data_entry.py
# streamlit run .\app.py

