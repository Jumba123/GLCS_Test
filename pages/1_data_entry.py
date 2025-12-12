from datetime import date
import streamlit as st
import pandas as pd

League_Name = "Great Lakes Championship Series"
League_Abbreviation = "GLCS"
League_Season_Number = 1
League_Season_Type = "REG"

def Team_Data_Entry_Form(current_date):
    st.title(f"{League_Abbreviation} Team Results ",width='stretch',)
    # Get session state keys if they exist
    Team_Game_Data = st.session_state.get('Team_Game_Data', pd.DataFrame())
    League_Teams = st.session_state.get('League_Teams', pd.DataFrame())

    # Team Inputs Needed Before Submitting Team Data
    team_cols = st.columns(2)
    with team_cols[0]:
        team1_selection = st.selectbox(f"Choose {League_Abbreviation} Team #1", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team1_Select")
        # team1_code = League_Teams.loc[League_Teams['Team_Name'] == team1_selection, 'Team_Code'].values[0] if team1_selection else None
    with team_cols[1]:
        team2_selection = st.selectbox(f"Choose {League_Abbreviation} Team #2", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team2_Select")
        # team2_code = League_Teams.loc[League_Teams['Team_Name'] == team2_selection, 'Team_Code'].values[0] if team2_selection else None

    """
    """
    Game_Result = ('Win_Reg', 'Win_OT', 'Loss_Reg', 'Loss_OT')
    if team1_selection and team2_selection:
        # # Initialize session state keys if they don't exist
        # for key in ['team1_shutout', 'team2_shutout']:
        #     if key not in st.session_state:
        #         st.session_state[key] = None if 'result' in key else "No"

        with st.form("game_stats_form"):
            st.markdown(f"<h3 style='text-align: center;'>Enter Week and Game Number</h3>", unsafe_allow_html=True)

            # Week and Game Number Inputs Needed Before Submitting Team Data
            detail_cols = st.columns(2)
            with detail_cols[0]:
                Week = st.number_input("Week", min_value=1, max_value=52, step=1)
            with detail_cols[1]:
                Game_Number = st.number_input("Game Number", min_value=1, step=1)

            st.markdown(f"<h3 style='text-align: center;'>Enter Game Stats</h3>", unsafe_allow_html=True)

            stats_cols = st.columns(2)

            with stats_cols[0]:
                st.subheader(f"{team1_selection if team1_selection else 'Team #1'}")
                team1_goals = st.number_input("Goals", min_value=0, step=1, key="team1_goals")
                team1_assists = st.number_input("Assists", min_value=0, step=1, key="team1_assists")
                team1_shots = st.number_input("Shots", min_value=0, step=1, key="team1_shots")
                team1_saves = st.number_input("Saves", min_value=0, step=1, key="team1_saves")
                team1_result = st.selectbox(f"{team1_selection}'s Game Result", Game_Result, index=None, placeholder="Please Select Result", key="team1_result")

            with stats_cols[1]:
                st.subheader(f"{team2_selection if team2_selection else 'Team #2'}")
                team2_goals = st.number_input("Goals", min_value=0, step=1, key="team2_goals")
                team2_assists = st.number_input("Assists", min_value=0, step=1, key="team2_assists")
                team2_shots = st.number_input("Shots", min_value=0, step=1, key="team2_shots")
                team2_saves = st.number_input("Saves", min_value=0, step=1, key="team2_saves")
                team2_result = st.selectbox(f"{team2_selection}'s Game Result", Game_Result, index=None, placeholder="Please Select Result", key="team2_result")

            submitted = st.form_submit_button("Submit")
        # Shutout logic (can be inside form or just after submit)
        if submitted:
            team1_code = League_Teams.loc[League_Teams['Team_Name'] == team1_selection, 'Team_Code'].values[0] if team1_selection else None
            team2_code = League_Teams.loc[League_Teams['Team_Name'] == team2_selection, 'Team_Code'].values[0] if team2_selection else None

            team1_conf = League_Teams.loc[League_Teams['Team_Name'] == team1_selection, 'Conference'].values[0] if team1_selection else None
            team2_conf = League_Teams.loc[League_Teams['Team_Name'] == team2_selection, 'Conference'].values[0] if team2_selection else None

            team1_div = League_Teams.loc[League_Teams['Team_Name'] == team1_selection, 'Division'].values[0] if team1_selection else None
            team2_div = League_Teams.loc[League_Teams['Team_Name'] == team2_selection, 'Division'].values[0] if team2_selection else None

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

            if Team_Game_Data.empty:
                Game_ID = 1
            else:
                Game_ID = Team_Game_Data['GAME_ID'].max() + 1  

            data = [
                {
                    "GAME_ID": Game_ID,
                    "Team_Name": team1_selection,
                    "Team_Code": team1_code,
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
                    "Shoutout": team1_shutout,
                    "Plus/Minus": team1_goals - team2_goals,
                    "Away_Team_Name": team2_selection,
                    "Away_Team_Code": team2_code,
                    "Away_Team_Goals": team2_goals,
                    "Away_Team_Assists": team2_assists,
                    "Away_Team_Shots": team2_shots,
                    "Away_Team_Saves": team2_saves,
                },
                {
                    "GAME_ID": Game_ID,
                    "Team_Name": team2_selection,
                    "Team_Code": team2_code,
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
                    "Shoutout": team2_shutout,
                    "Plus/Minus": team2_goals - team1_goals,
                    "Away_Team_Name": team1_selection,
                    "Away_Team_Code": team1_code,
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
            st.success("Team game data was added! - Newest Team Game Data Shown Below")

            Newest_Team_Data_Added = st.session_state['Team_Game_Data'].tail(2)
            st.dataframe(Newest_Team_Data_Added.style.hide(axis="index"))
            
        # Prepare CSV data without index for download
        csv_data = st.session_state['Team_Game_Data'].to_csv(index=False).encode('utf-8')
      
        # Show updated team_game_data if wanted`
        Team_CheckBox = st.checkbox("Show All Team Game Data", key="show_team_data_after form")
        if Team_CheckBox:
            st.dataframe(Team_Game_Data.style.hide(axis="index")) 

        st.download_button(
            label="Download Raw_Team_Data as CSV",
            data=csv_data,
            file_name=f'Raw_Team_Data-{current_date}.csv',
            mime='text/csv',
        )
        
    else:
        st.warning("Please select both teams, week, and game number to continue.")

def Player_Data_Entry_Form(current_date):
    st.title("Player Game Submission")
    
    # Access shared dataframes in session state
    League_Teams = st.session_state.get('League_Teams', pd.DataFrame())
    League_Roster = st.session_state.get('League_Roster', pd.DataFrame())
    Team_Game_Data = st.session_state.get('Team_Game_Data', pd.DataFrame())
    Player_Game_Data = st.session_state.get('Player_Game_Data', pd.DataFrame())
    # if 'Player_Game_Data' not in st.session_state:
    #     st.session_state.Player_Game_Data = pd.DataFrame()
    
    # Inputs Needed Before Submitting Player Data
    team_cols = st.columns(2)
    with team_cols[0]:
        player_team1_selection = st.selectbox("Choose Team #1", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team1_Player_Select")
        Week = st.number_input("Week", min_value=1, max_value=52, step=1, key="Player_Data_Week_Input")
        
    with team_cols[1]:
        player_team2_selection = st.selectbox("Choose Team #2", League_Teams['Team_Name'], index=None, placeholder="Please Select Team", key="Team2_Player_Select")
        Game_Number = st.number_input("Game Number", min_value=1, step=1, key="Player_Data_Game_Number_Input")
        
    filtered_team1 = League_Teams.loc[League_Teams['Team_Name'] == player_team1_selection, 'Team_Code']
    filtered_team2 = League_Teams.loc[League_Teams['Team_Name'] == player_team2_selection, 'Team_Code']
    player_team1_code = filtered_team1.values[0] if not filtered_team1.empty else None
    player_team2_code = filtered_team2.values[0] if not filtered_team2.empty else None
    Team_1_Roster = League_Roster.loc[League_Roster['Team_Name'] == player_team1_selection].sort_values("Skater_Name")
    Team_2_Roster = League_Roster.loc[League_Roster['Team_Name'] == player_team2_selection].sort_values("Skater_Name")

    Puck_Positions = ('LW', 'C', 'RW', 'LD', 'RD', 'G')
    if player_team1_selection and player_team2_selection and Week and Game_Number:
        filter_condition_team1 = (
            (Team_Game_Data['Team_Code'] == player_team1_code) &
            (Team_Game_Data['Week'] == Week) &
            (Team_Game_Data['Game_Number'] == Game_Number))
        filter_condition_team2 = (
            (Team_Game_Data['Team_Code'] == player_team2_code) &
            (Team_Game_Data['Week'] == Week) &
            (Team_Game_Data['Game_Number'] == Game_Number))

        Team1_Game_Data = Team_Game_Data.loc[filter_condition_team1]
        Team2_Game_Data = Team_Game_Data.loc[filter_condition_team2]
        team1_goals = Team1_Game_Data['Goals'].iloc[0]
        team2_goals = Team2_Game_Data['Goals'].iloc[0]
        Team1_Game_Result = Team1_Game_Data['Game_Result'].iloc[0]
        Team2_Game_Result = Team2_Game_Data['Game_Result'].iloc[0]
        
        st.markdown(f"<h3 style='text-align: center;'>Game Result - {player_team1_code}({team1_goals}) - {player_team2_code}({team2_goals})</h3>", unsafe_allow_html=True)

        # Initialize row counts if needed
        if 'team1_rows' not in st.session_state:
            st.session_state.team1_rows = 4
        if 'team2_rows' not in st.session_state:
            st.session_state.team2_rows = 4

        def add_team1_row():
            st.session_state.team1_rows += 1

        def add_team2_row():
            st.session_state.team2_rows += 1
    
        Team1_Key = f"{player_team1_code}_player_"
        Team2_Key = f"{player_team2_code}_player_"
        
        Combined_Skaters = pd.concat([
            Team_1_Roster[['Team_Code', 'Skater_Name']], 
            Team_2_Roster[['Team_Code', 'Skater_Name']]], ignore_index=True).drop_duplicates().sort_values(['Team_Code', 'Skater_Name']).reset_index(drop=True)
        
        # Combined form for both teams
        with st.form("Combined_Scoreboard_Form"):
            team1_data = []
            team2_data = []

            st.header(f"{player_team1_selection}")
            for i in range(st.session_state.team1_rows):
                cols = st.columns([1, 2, 1.5, 1.5, 1.5])
                Team1_Skater_Position = cols[0].selectbox("Position", Puck_Positions, key=f"{Team1_Key}Skater_Position{i}")
                Team1_Skater_Name = cols[1].selectbox(f"Skater #{i+1}", Team_1_Roster["Skater_Name"], key=f"{Team1_Key}Skater_Name{i}")
                Team1_Goals = cols[2].number_input("Goals", min_value=0, step=1, key=f"{Team1_Key}Goals{i}")
                Team1_Assists = cols[3].number_input("Assists", min_value=0, step=1, key=f"{Team1_Key}Assists{i}")
                Team1_SOG = cols[4].number_input("SOG", min_value=0, step=1, key=f"{Team1_Key}Shots_On_Goal{i}")
                
                team1_conf = League_Teams.loc[League_Teams['Team_Name'] == player_team1_selection, 'Conference'].values[0] if player_team1_selection else None
                team1_div = League_Teams.loc[League_Teams['Team_Name'] == player_team1_selection, 'Division'].values[0] if player_team1_selection else None
                
                Team1_Skater_Type = League_Roster.loc[League_Roster['Skater_Name'] == Team1_Skater_Name]['Skater_Type'].values[0]
                Team1_Plus_Minus = Team1_Game_Data['Plus/Minus'].iloc[0]
                Team1_Shoutout = Team1_Game_Data['Shoutout'].iloc[0]
                Team1_ID = Team1_Game_Data['GAME_ID'].iloc[0]

                team1_data.append({
                    "Skater_Name": Team1_Skater_Name,
                    "GAME_ID": Team1_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team1_conf,
                    "Division":team1_div,   
                    "Skater_Type": Team1_Skater_Type,
                    "Position": Team1_Skater_Position,
                    "Team_Name": player_team1_selection,
                    "Team_Code": player_team1_code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Team1_Goals,
                    "Assists": Team1_Assists,
                    "SOG": Team1_SOG,
                    "GWG": None,
                    "Game_Result": Team1_Game_Result,
                    "Shoutout": Team1_Shoutout,
                    "Plus/Minus": Team1_Plus_Minus,
                    "Goalie_Goals_Allowed": None,
                    "Goalie_Shots_Allowed": None,
                    "Goalie_Saves": None,
                    
                })
            """
            """
            #Team 2 inputs
            
            st.header(f"{player_team2_selection}")

            for i in range(st.session_state.team2_rows):
                cols = st.columns([1, 2, 1.5, 1.5, 1.5])
                Team2_Skater_Position = cols[0].selectbox("Position", Puck_Positions, key=f"{Team2_Key}Skater_Position{i}")
                Team2_Skater_Name = cols[1].selectbox(f"Skater #{i+1}", Team_2_Roster["Skater_Name"], key=f"{Team2_Key}Skater_Name{i}")
                Team2_Goals = cols[2].number_input("Goals", min_value=0, step=1, key=f"{Team2_Key}Goals{i}")
                Team2_Assists = cols[3].number_input("Assists", min_value=0, step=1, key=f"{Team2_Key}Assists{i}")
                Team2_SOG = cols[4].number_input("SOG", min_value=0, step=1, key=f"{Team2_Key}Shots_On_Goal{i}")

                team2_conf = League_Teams.loc[League_Teams['Team_Name'] == player_team2_selection, 'Conference'].values[0] if player_team2_selection else None
                team2_div = League_Teams.loc[League_Teams['Team_Name'] == player_team2_selection, 'Division'].values[0] if player_team2_selection else None
                
                Team2_Skater_Type = League_Roster.loc[League_Roster['Skater_Name'] == Team2_Skater_Name]['Skater_Type'].values[0]
                Team2_Plus_Minus = Team2_Game_Data['Plus/Minus'].iloc[0]
                Team2_Shoutout = Team2_Game_Data['Shoutout'].iloc[0]
                Team2_ID = Team2_Game_Data['GAME_ID'].iloc[0]
                
                team2_data.append({
                    "Skater_Name": Team2_Skater_Name,
                    "GAME_ID": Team2_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team2_conf,
                    "Division":team2_div,     
                    "Skater_Type": Team2_Skater_Type,
                    "Position": Team2_Skater_Position,
                    "Team_Name": player_team2_selection,
                    "Team_Code": player_team2_code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Team2_Goals,
                    "Assists": Team2_Assists,
                    "SOG": Team2_SOG,
                    "GWG": None,
                    "Game_Result": Team2_Game_Result,
                    "Shoutout": Team2_Shoutout,
                    "Plus/Minus": Team2_Plus_Minus,
                    "Goalie_Goals_Allowed": None,
                    "Goalie_Shots_Allowed": None,
                    "Goalie_Saves": None,    
                })

                
            st.markdown(f"<h1 style='text-align: center;'>Goalie Entry</h1>", unsafe_allow_html=True)
            
            cols = st.columns([2, 1.5, 1.5, 1.5])
            Team1_Goalie_Name = cols[0].selectbox(f"{player_team1_selection} - Goalie Data Entry", Team_1_Roster["Skater_Name"], key=f"Team1_Goalie_Name1")
            Team1_Checkbox = cols[0].checkbox(f"Use {player_team1_code} Results For Goalie Stats", key="Goalie_Stats_From_Team1", help="If checked, Goalie Stats will be auto-filled from Team Results")
            Goalie1_Goals_Allowed = cols[1].number_input("GA - Goalie Only", min_value=0, step=1,key=f"Goalie1_Goals_Allowed{i}")
            Goalie1_Shots_Allowed = cols[2].number_input("SA - Goalie Only", min_value=0, step=1,key=f"Goalie1_Shots_Allowed{i}")
            Goalie1_Saves = cols[3].number_input("Saves - Goalie Only", min_value=0, step=1,key=f"Goalie1_Saves")
            
            if Team1_Checkbox:
                Goalie1_Goals_Allowed = Team1_Game_Data['Goals'].iloc[0]
                Goalie1_Shots_Allowed = Team1_Game_Data['Shots'].iloc[0]
                Goalie1_Saves = Team1_Game_Data['Saves'].iloc[0]
            
            Goalie1_Goals = cols[1].number_input("Goals", min_value=0, step=1, key=f"Team1_Goalie_Goals{i}")
            Goalie1_Assists = cols[2].number_input("Assists", min_value=0, step=1, key=f"Team1_Goalie_Assists{i}")
            Goalie1_SOG = cols[3].number_input("SOG", min_value=0, step=1, key=f"Team1_Goalie_Shots_On_Goal{i}")
            
            team1_g_conf = League_Teams.loc[League_Teams['Team_Name'] == player_team1_selection, 'Conference'].values[0] if player_team1_selection else None
            team1_g_div = League_Teams.loc[League_Teams['Team_Name'] == player_team1_selection, 'Division'].values[0] if player_team1_selection else None
            
            Team1_g_Shoutout = Team1_Game_Data['Shoutout'].iloc[0]
            Team1_g_Plus_Minus = Team1_Game_Data['Plus/Minus'].iloc[0]
            Team1_G_ID = Team1_Game_Data['GAME_ID'].iloc[0]
            
            team1_data.append({
                    "Skater_Name": Team1_Goalie_Name,
                    "GAME_ID": Team1_G_ID,
                    "League": League_Abbreviation,
                    "Season": League_Season_Number,
                    "Season_Type": League_Season_Type,
                    "Conference": team1_g_conf,
                    "Division":team1_g_div,   
                    "Skater_Type": "Goalie",
                    "Position": "G",
                    "Team_Name": player_team1_selection,
                    "Team_Code": player_team1_code,
                    "Week": Week,
                    "Game_Number": Game_Number,
                    "Goals": Goalie1_Goals,
                    "Assists": Goalie1_Assists,
                    "SOG": Goalie1_SOG,
                    "GWG": None,
                    "Game_Result": Team1_Game_Result,
                    "Shoutout": Team1_g_Shoutout,
                    "Plus/Minus": Team1_g_Plus_Minus,
                    "Goalie_Goals_Allowed": Goalie1_Goals_Allowed,
                    "Goalie_Shots_Allowed": Goalie1_Shots_Allowed,
                    "Goalie_Saves": Goalie1_Saves,
                    
                })
            
            cols = st.columns([2, 1.5, 1.5, 1.5])
            Team2_Goalie_Name = cols[0].selectbox(f"{player_team2_selection} - Goalie Data Entry", Team_2_Roster["Skater_Name"], key=f"Team2_Goalie_Name2")
            Team2_Checkbox = cols[0].checkbox(f"Use {player_team2_code} Results For Goalie Stats", key="Goalie_Stats_From_Team2", help="If checked, Goalie Stats will be auto-filled from Team Results")
            Goalie2_Goals_Allowed = cols[1].number_input("GA - Goalie Only", min_value=0, step=1,key=f"Goalie2_Goals_Allowed{i}")
            Goalie2_Shots_Allowed = cols[2].number_input("SA - Goalie Only", min_value=0, step=1,key=f"Goalie2_Shots_Allowed{i}")
            Goalie2_Saves = cols[3].number_input("Saves - Goalie Only", min_value=0, step=1,key=f"Goalie2_Saves")
            if Team2_Checkbox:
                Goalie2_Goals_Allowed = Team2_Game_Data['Goals'].iloc[0]
                Goalie2_Shots_Allowed = Team2_Game_Data['Shots'].iloc[0]
                Goalie2_Saves = Team2_Game_Data['Saves'].iloc[0] 
            Goalie2_Goals = cols[1].number_input("Goals", min_value=0, step=1, key=f"Team2_Goalie_Goals{i}")
            Goalie2_Assists = cols[2].number_input("Assists", min_value=0, step=1, key=f"Team2_Goalie_Assists{i}")
            Goalie2_SOG = cols[3].number_input("SOG", min_value=0, step=1, key=f"Team2_Goalie_Shots_On_Goal{i}")
            
            team2_g_conf = League_Teams.loc[League_Teams['Team_Name'] == player_team2_selection, 'Conference'].values[0] if player_team2_selection else None
            team2_g_div = League_Teams.loc[League_Teams['Team_Name'] == player_team2_selection, 'Division'].values[0] if player_team2_selection else None
            
            Team2_g_Shoutout = Team1_Game_Data['Shoutout'].iloc[0]
            Team2_g_Plus_Minus = Team1_Game_Data['Plus/Minus'].iloc[0]
            Team2_G_ID = Team2_Game_Data['GAME_ID'].iloc[0]
            
            team2_data.append({
                "Skater_Name": Team2_Goalie_Name,
                "GAME_ID": Team2_G_ID,
                "League": League_Abbreviation,
                "Season": League_Season_Number,
                "Season_Type": League_Season_Type,
                "Conference": team2_g_conf,
                "Division":team2_g_div,   
                "Skater_Type": "Goalie",
                "Position": "G",
                "Team_Name": player_team2_selection,
                "Team_Code": player_team2_code,
                "Week": Week,
                "Game_Number": Game_Number,
                "Goals": Goalie2_Goals,
                "Assists": Goalie2_Assists,
                "SOG": Goalie2_SOG,
                "GWG": None,
                "Game_Result": Team2_Game_Result,
                "Shoutout": Team2_g_Shoutout,
                "Plus/Minus": Team2_g_Plus_Minus,
                "Goalie_Goals_Allowed": Goalie2_Goals_Allowed,
                "Goalie_Shots_Allowed": Goalie2_Shots_Allowed,
                "Goalie_Saves": Goalie2_Saves,
                
            })
            st.markdown("---")

            Combined_Skaters['Display_Name'] = Combined_Skaters['Team_Code'].astype(str) + ' - ' + Combined_Skaters['Skater_Name']

            GWG_Player = st.selectbox("Select Game Winning Goal Scorer", Combined_Skaters['Display_Name'], index=None, placeholder="Please Select GWG Scorer", key="GWG_Player_Select")
            
            # Assign GWG to the selected player
            if GWG_Player:
                selected_skater_name = GWG_Player.split(' - ')[-1]
                for player_data in team1_data:
                    if player_data['Skater_Name'] == selected_skater_name:
                        player_data['GWG'] = "Yes"
                for player_data in team2_data:
                    if player_data['Skater_Name'] == selected_skater_name:
                        player_data['GWG'] = "Yes"

            # Buttons to add rows for each team
            col_add_row = st.columns(2)
            with col_add_row[0]:
                add_row_team_1 = st.form_submit_button("Add Another Player to Team 1", on_click=add_team1_row)
            with col_add_row[1]:
                add_row_team_2 = st.form_submit_button("Add Another Player to Team 2", on_click=add_team2_row)



            # Submit button for all players
            submitted = st.form_submit_button("Submit Players")

        if submitted:
            new_data = pd.concat([pd.DataFrame(team1_data), pd.DataFrame(team2_data)], ignore_index=True)
            st.session_state.Player_Game_Data = pd.concat([st.session_state.Player_Game_Data, new_data], ignore_index=True)
            st.success("Player game data was added! - Newest Player Game Data Shown Below")
            Newest_Player_Data_Added = st.session_state['Player_Game_Data'].tail(12)
            st.dataframe(Newest_Player_Data_Added.style.hide(axis="index"))

        Player_CheckBox = st.checkbox("Show Player Data", key="show_player_data_after form")
        if Player_CheckBox:
            st.dataframe(Player_Game_Data.style.hide(axis="index")) 

        if not st.session_state.Player_Game_Data.empty:
            csv = st.session_state.Player_Game_Data.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="Download Raw_Player_Data as CSV",
                data=csv,
                file_name=f"Raw_Player_Data-{current_date}.csv",
                mime="text/csv"
            )
    else:
        st.warning("Please select both teams, week, and game number to continue.")

def Test(current_date):
    pass

def main():
    current_date = date.today()

    if all([
    'League_Teams' in st.session_state and not st.session_state['League_Teams'].empty,
    'League_Roster' in st.session_state and not st.session_state['League_Roster'].empty,
    ]):
        # Test( current_date)
        Team_Data_Entry_Form(current_date)
        Player_Data_Entry_Form(current_date)
    else:
        st.warning("Go Back to the app page to load the files or please upload all 4 required CSV files to proceed.")

if __name__ == "__main__":
    main()

# streamlit run .\1_data_entry.py
# streamlit run e:/Python Programs/New_PHL/app.py

