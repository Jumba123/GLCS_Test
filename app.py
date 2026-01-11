import streamlit as st
import pandas as pd

# streamlit run .\app.py

League_Name = "Great Lakes Championship Series"
League_Abbreviation = "GLCS"

def Pre_Process_CSV(df):
    df['Skaters'] = df['Skaters'].str.title()
    df['Games Played'] = df['Games Played'].astype(int)
    df['Goals'] = df['Goals'].astype(int)
    df['Assists'] = df['Assists'].astype(int)
    df['Goals Allowed'] = df['Goals Allowed'].astype(int)
    df['Win'] = df['Win'].astype(int)
    df['Loss'] = df['Loss'].astype(int)
    df['Week'] = df['Week'].astype(int)

    df["Points"] = df["Goals"] + df["Assists"]
    df.insert(5, "Points", df.pop("Points"))

    df["GAA"] = df["Goals Allowed"] / df["Games Played"]
    df["GAA"] = df["GAA"].round(2)
    df.insert(6, "GAA", df.pop("GAA"))
    
    df = df[['Skater_ID','Skaters', 'Position', 'Games Played', 'Goals', 'Assists', 'Points','Win', 'Loss', 'Goals Allowed', 'Week', 'Team']]
    
    return df

def Home_Page (df):
    Options = ["Points","PPG","Goals", "Assists"]
    Rank_Choice = st.pills("Rank By:", Options, default=Options[0], selection_mode="single")

    for option in Options:
        if Rank_Choice == option:
            df_temp = df.copy()
            
            # Group and sort by the selected stat
            df_temp = df_temp.groupby("Skaters", as_index=False).sum("Points")
            
            df_temp["PPG"] = df_temp["Points"] / df_temp["Games Played"]
            df_temp["PPG"] = df_temp["PPG"].round(2)
            df_temp.insert(7, "PPG", df_temp.pop("PPG"))
            df_temp = df_temp.drop(columns=["Skater_ID", "Week","Goals Allowed"])
            df_temp = df_temp.sort_values(option, ascending=False)


            # Games played filter
            slider_gp = st.slider("Games Played", 0, df_temp['Games Played'].max().round(0).astype(int), 0)
            df_temp = df_temp[df_temp['Games Played'] >= slider_gp]

            # Rank and display
            df_temp['Rank'] = df_temp[option].rank(method='dense', ascending=False)
            df_temp.insert(0, f"Rank ({option})", df_temp.pop("Rank"))
            df_temp = df_temp.set_index(f"Rank ({option})")
            st.dataframe(df_temp)
            break  # Stop after the matching option is processed

def URL_CSV(url, session_key):
    df = pd.read_csv(url)
    st.session_state[session_key] = df
    st.session_state[f"{session_key}_filename"] = url
    return st.session_state[session_key]

def Upload_CSV(label, session_key):
    uploaded_file = st.file_uploader(label, type=["csv"])
    if uploaded_file is not None:
        # Reload if new file or different filename from currently loaded
        if (session_key not in st.session_state or 
            st.session_state.get(f"{session_key}_filename", None) != uploaded_file.name):
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state[session_key] = df
                st.session_state[f"{session_key}_filename"] = uploaded_file.name
                st.success(f"'{uploaded_file.name}' loaded successfully.")
            except Exception as e:
                st.error(f"Error loading CSV: {e}")
    else:
        if session_key not in st.session_state:
            st.session_state[session_key] = pd.DataFrame()

    return st.session_state[session_key]

def Load_Files_Needed():
    # #CSV Uploaded Files Through Google Sheets
    #Google URLs
    sheet_id = "1R-Fkeb_wFCaxUWALr0yTamREO0AMpn8jfXnKyoL3rfw"
    GLCS_Teams = "GLCS_Teams"
    GLCS_Roster = "GLCS_Roster"
    Team_Game_Data = "Raw_Team_Data"
    Player_Game_Data = "Raw_Player_Data"

    League_Team_URL = (f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?"
    f"tqx=out:csv&sheet={GLCS_Teams}")
    League_Roster_URL = (f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?"
    f"tqx=out:csv&sheet={GLCS_Roster}")
    Team_Game_Data_URL = (f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?"
    f"tqx=out:csv&sheet={Team_Game_Data}")  
    Player_Game_Data_URL = (f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?"
    f"tqx=out:csv&sheet={Player_Game_Data}")


    # # #CSV Uploaded Files Through GitHub
    # # #CSV URLs
    # League_Team_URL = "https://raw.githubusercontent.com/Jumba123/GLCS_Test/refs/heads/main/GLCS_Teamsv1.csv"
    # League_Roster_URL = "https://raw.githubusercontent.com/Jumba123/GLCS_Test/refs/heads/main/GLCS_Rosterv1.csv"
    # Team_Game_Data_URL = "https://raw.githubusercontent.com/Jumba123/PHL_Data_Entry_App/refs/heads/main/PHL_Roster.csv"
    # Player_Game_Data_URL = "https://raw.githubusercontent.com/Jumba123/PHL_Data_Entry_App/refs/heads/main/PHL_Roster.csv"
    
    # #Load or initialize CSVs
    League_Teams = URL_CSV(League_Team_URL, "League_Teams")
    League_Roster = URL_CSV(League_Roster_URL, "League_Roster")
    Team_Game_Data = URL_CSV(Team_Game_Data_URL, "Team_Game_Data")
    Player_Game_Data = URL_CSV(Player_Game_Data_URL, "Player_Game_Data")
    """
    """
    #Upload 4 csv files and store in session_state
    # League_Teams = Upload_CSV(f"Upload {League_Abbreviation} Team CSV", "League_Teams")
    # League_Roster = Upload_CSV(f"Upload {League_Abbreviation} Roster CSV", "League_Roster")
    st.markdown("---")  # horizontal separator
    # Team_Game_Data = Upload_CSV(f"Upload Raw_Team_Data CSV", "Team_Game_Data")
    # Player_Game_Data = Upload_CSV(f"Upload Raw_Player_Data CSV", f"Player_Game_Data")

    st.markdown("---")  # horizontal separator

    # Optionally show the uploaded CSV preview
    if not League_Teams.empty:
        if st.checkbox(f"Show {League_Abbreviation} Team CSV ", key=f"show_{League_Abbreviation}_Teams_preview"):
            st.dataframe(League_Teams.style.hide(axis="index"))
    if not League_Roster.empty:
        if st.checkbox(f"Show {League_Abbreviation} Roster CSV", key=f"show_{League_Abbreviation}_Roster_preview"):
            st.dataframe(League_Roster.style.hide(axis="index"))
    if not Team_Game_Data.empty:
        if st.checkbox("Show Team Game Data CSV", key="show_team_data_preview"):
            st.dataframe(Team_Game_Data.style.hide(axis="index"))
    if not Player_Game_Data.empty:
        if st.checkbox("Show Player Game Data CSV", key="show_player_data_preview"):
            st.dataframe(Player_Game_Data.style.hide(axis="index"))

def main():
    # df = Pre_Process_CSV(df)
    st.markdown(f"<h1 style='text-align: center;'>GLCS - Great Lakes Championship Series Website</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Season 1 - Version 1.1</h2>", unsafe_allow_html=True)

    Load_Files_Needed()

    Data_Entry_Link, Skater_Link, Goalie_Link, Weekly_Link, Stat_Track_Link= st.columns(5,border=True, gap="small")
    with Data_Entry_Link:
        Data_Entry_Link = st.button("Data Entry")
    with Skater_Link:
        Skater_Link = st.button("Skater")
    with Goalie_Link:
        Goalie_Link = st.button("Goalie")
    with Weekly_Link:
        Weekly_Link = st.button("Weekly")
    with Stat_Track_Link:
        Stat_Track_Link = st.button("Stat Track")
    if Data_Entry_Link:
        st.switch_page("pages/1_data_entry.py")
    if Skater_Link:
        st.switch_page("pages/2_skater_stats.py")
    if Goalie_Link:
        st.switch_page("pages/3_goalie_stats.py")
    if Weekly_Link:
        st.switch_page("pages/4_weekly_stats.py")
    if Stat_Track_Link:
        st.switch_page("pages/5_stat_track.py")
        

if __name__ == "__main__":
    main()


# streamlit run .\app.py
