import streamlit as st
import pandas as pd

League_Name = "Great Lakes Championship Series"
League_Abbreviation = "GLCS"

def Test_Page():
    st.title("Hockey Goal Tracker")

    # Initialize session state
    if "goals" not in st.session_state:
        st.session_state.goals = []  # list of dicts

    st.subheader("Game info")
    home_team = st.text_input("Home team", "Warriors")
    away_team = st.text_input("Away team", "Mariners")

    st.markdown("---")
    st.subheader("Add goal")

    # Simple fields: period, scorer, up to 2 assists, note like G1 / PP / PK
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        goal_label = st.text_input("Goal label", "G1")  # e.g. G1, G2
    with col2:
        scorer = st.text_input("Scorer", "Nem")
    with col3:
        assist1 = st.text_input("Assist 1", "Liability")
    with col4:
        assist2 = st.text_input("Assist 2", "")

    note = st.text_input("Extra note (e.g. PK line)", "")

    if st.button("Add goal"):
        st.session_state.goals.append(
            {
                "label": goal_label,
                "scorer": scorer,
                "assist1": assist1,
                "assist2": assist2,
                "note": note,
            }
        )

    st.markdown("---")
    st.subheader("Goals log")

    # Render in the “G1: scorer (a1, a2)” style
    for i, g in enumerate(st.session_state.goals, start=1):
        label = g["label"] or f"G{i}"
        pieces = []
        if g["assist1"] or g["assist2"]:
            assists = ", ".join([x for x in [g["assist1"], g["assist2"]] if x])
            pieces.append(f"{g['scorer']} ({assists})")
        else:
            pieces.append(g["scorer"])

        line = f"{label}: " + ", ".join(pieces)
        if g["note"]:
            line += f"  — {g['note']}"
        st.write(line)

    # Optional: show as a table too
    if st.session_state.goals:
        st.markdown("### Goals table")
        st.dataframe(st.session_state.goals)


def game_tracker():
    # Access shared dataframes in session state
    League_Teams = st.session_state.get('League_Teams', pd.DataFrame())
    League_Roster = st.session_state.get('League_Roster', pd.DataFrame())

    # Initialize session state
    if "team1_data" not in st.session_state:
        st.session_state.team1_data = []
    if "tracking_active" not in st.session_state:
        st.session_state.tracking_active = True

    cols = st.columns(2)
    Team1_Selection = cols[0].selectbox(
        "Choose Team #1",
        League_Teams['Team_Name'],
        index=None,
        placeholder="Please Select Team",
        key="Team1_Selection",
    )
    Team2_Selection = cols[1].selectbox(
        "Choose Team #2",
        League_Teams['Team_Name'],
        index=None,
        placeholder="Please Select Team",
        key="Team2_Selection",
    )

    filtered_team1 = League_Teams.loc[League_Teams['Team_Name'] == Team1_Selection, 'Team_Code']
    filtered_team2 = League_Teams.loc[League_Teams['Team_Name'] == Team2_Selection, 'Team_Code']
    Team1_code = filtered_team1.values[0] if not filtered_team1.empty else None
    Team2_code = filtered_team2.values[0] if not filtered_team2.empty else None

    with st.form("Game_Tracker_Form"):
        cols = st.columns([2, 1.75, 1.75, 1.75])

        Team_Selection = cols[0].selectbox(
            "Select Team",
            [Team1_Selection, Team2_Selection],
            index=None,
            placeholder="Please Select Team",
            key="Team_Selection_For_Roster",
        )

        Roster = League_Roster.loc[
            League_Roster['Team_Name'] == Team_Selection
        ].sort_values("Skater_Name")

        Goal_Scorer = cols[1].selectbox(
            "Goal Scorer",
            Roster["Skater_Name"],
            index=None,
            key="Goal_Scorer",
        )
        Primary_Assist = cols[2].selectbox(
            "Primary Assist",
            Roster["Skater_Name"],
            index=None,
            key="Primary_Assist",
        )
        Secondary_Assist = cols[3].selectbox(
            "Secondary Assist",
            Roster["Skater_Name"],
            index=None,
            key="Secondary_Assist",
        )

        submitted = st.form_submit_button("Submit Goal")

    # "Loop": each submit adds one more row while tracking is active
    if submitted and st.session_state.tracking_active:
        team_code = Team1_code if Team_Selection == Team1_Selection else Team2_code
        line = f"{team_code}: {Goal_Scorer}, ({Primary_Assist}), ({Secondary_Assist})"
        st.session_state.team1_data.append(line)

    if st.button("Reset Tracker"):
        st.session_state.team1_data = []
        st.session_state.tracking_active = True


    st.subheader("Output")

    for i in range(st.session_state.team1_data.__len__()):
        st.text(f"{st.session_state.team1_data[i]}\n")


def main():
    st.markdown(f"<h1 style='text-align: center;'>{League_Name} Game Tracker</h1>", unsafe_allow_html=True)
    game_tracker()
if __name__ == "__main__":
    main()