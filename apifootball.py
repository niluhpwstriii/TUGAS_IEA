import streamlit as st
import requests
import pandas as pd

st.title('Football Information Dashboard')

api_key = '3ed8d4507aa2d3f525072bd1cfef25b64a3aa4bdd9f0cc1b080f73705414d433'

# Function to fetch countries
st.cache_data.clear()
def fetch_countries():
    url = f'https://apiv3.apifootball.com/?action=get_countries&APIkey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error('Failed to fetch countries.')
        return pd.DataFrame()

countries_df = fetch_countries()
country_list = countries_df['country_name'].tolist()
selected_country = st.selectbox('Select a Country', country_list)

if selected_country:
    selected_country_id = countries_df[countries_df['country_name'] == selected_country]['country_id'].iloc[0]

    # Function to fetch competitions for the selected country
    st.cache_data.clear()
    def fetch_competitions(country_id):
        url = f'https://apiv3.apifootball.com/?action=get_leagues&country_id={country_id}&APIkey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error('Failed to fetch competitions.')
            return pd.DataFrame()

    competitions_df = fetch_competitions(selected_country_id)
    competition_list = competitions_df['league_name'].tolist()
    selected_competition = st.selectbox('Select a Competition', competition_list)

    if selected_competition:
        selected_league_id = competitions_df[competitions_df['league_name'] == selected_competition]['league_id'].iloc[0]

        # Function to fetch teams for the selected competition
        st.cache_data.clear()
        def fetch_teams(league_id):
            url = f'https://apiv3.apifootball.com/?action=get_teams&league_id={league_id}&APIkey={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                teams_data = response.json()
                # Flatten the data if teams come nested with player details
                for team in teams_data:
                    if 'players' in team:
                        team['players'] = str(len(team['players'])) + " players"
                return pd.DataFrame(teams_data)
            else:
                st.error('Failed to fetch teams.')
                return pd.DataFrame()

        teams_df = fetch_teams(selected_league_id)
        team_list = teams_df['team_name'].tolist()
        selected_team = st.selectbox('Select a Team', team_list)

        if selected_team:
            selected_team_key = teams_df[teams_df['team_name'] == selected_team]['team_key'].iloc[0]
            
            # Function to fetch players for the selected team
            st.cache_data.clear()
            def fetch_players(team_key):
                url = f'https://apiv3.apifootball.com/?action=get_teams&team_id={team_key}&APIkey={api_key}'
                response = requests.get(url)
                if response.status_code == 200:
                    team_data = response.json()[0] 
                    players_data = team_data['players']
                    return pd.DataFrame(players_data)
                else:
                    st.error('Failed to fetch players.')
                    return pd.DataFrame()

            players_df = fetch_players(selected_team_key)
            player_names = players_df['player_name'].tolist()
            selected_player = st.selectbox('Select a Player', player_names)

            if selected_player:
                # Displaying selected player details
                selected_player_details = players_df[players_df['player_name'] == selected_player].iloc[0]
                st.image(selected_player_details['player_image'], width=200)
                st.dataframe(selected_player_details.drop('player_image'))