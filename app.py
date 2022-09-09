import streamlit as st
import pandas as pd
import numpy as np
from utils import requests_post, get_inputs, request_delete, clear_text
import datetime as dt

URL = 'http://ec2-13-212-176-7.ap-southeast-1.compute.amazonaws.com/Soccer/'
HELP_MESSAGE = "Data only persist after pressing submit, try changing some values, press submit and refresh the page"
st.set_page_config(layout="wide", page_title="Govtech Soccer Event")


def app():

    # Heading
    st.write(
        """
    # Govtech Soccer App
    This simple app takes in the the registration and match details and outputs the top 4 teams based on the following logic:
    > 1. Highest total match points. A win is worth 3 points, a draw is worth 1 point, and a loss is worth 0 points.
    > 2. If teams are tied, highest total goals scored.
    > 3. If teams are still tied, highest alternate total match points. A win is worth 5 points, a draw is worth 3 points, and a loss is worth 1 point.
    > 4. If teams are still tied, earliest registration date.  \n
    Features:
    > 1. Initial input fields are loaded from db
    > 2. Upon submit, all inputs are saved to database and overwrite previous entries
    > 3. Delete will remove all entries from db, when refreshed input fields will be empty
    
    Created by [Wesley Ong](https://wesleyongs.com/).
    """
    )

    registrations_text = get_inputs(URL, "Registration/")
    matches_text = get_inputs(URL, "Match/")

    registrations_input = st.text_area(
        "Registration data",
        value=registrations_text,
        help=HELP_MESSAGE,
        key="registrations_input",
    )
    matches_input = st.text_area(
        "Match data",
        height=300,
        value=matches_text,
        help=HELP_MESSAGE,
        key="matches_input",
    )

    get_results = st.button("Submit")
    delete_all = st.button("Delete All", on_click=clear_text)

    if get_results:
        st.markdown("## Results")
        results = requests_post(
            URL + "Result",
            {"registrations_text": registrations_input, "matches_text": matches_input},
        )
        df = pd.DataFrame(results)
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = df["date"].dt.strftime("%d-%m")
        st.write(
            df[
                [
                    "group_number",
                    "team_name",
                    "normal_score",
                    "team_score",
                    "alternate_score",
                    "date",
                ]
            ].sort_values(
                by=[
                    "group_number",
                    "normal_score",
                    "team_score",
                    "alternate_score",
                    "date",
                ],
                ascending=[True, False, False, False, True],
            )
        )
        registrations_text = get_inputs(URL, "Registration/")
        matches_text = get_inputs(URL, "Match/")

    if delete_all:
        request_delete(URL + "Registration", "all registration data")
        request_delete(URL + "Match", "all match data")

app()

with st.sidebar:
    st.header("Some useful test cases below")
    st.markdown(
        "### Registrations  \nteamA 01/04 1  \nteamB 02/05 1  \nteamC 03/06 1  \nteamD 04/06 1  \nteamE 05/06 1  \nteamF 15/06 1  \nteamG 14/06 2  \nteamH 13/06 2  \nteamI 12/06 2  \nteamJ 11/06 2  \nteamK 10/06 2  \nteamL 27/06 2  \n"
    )
    st.markdown(
        "### Matches  \nteamA teamB 0 1  \nteamA teamC 1 3  \nteamA teamD 2 2  \nteamA teamE 2 4  \nteamA teamF 3 3  \nteamB teamC 0 1  \nteamB teamD 2 2  \nteamB teamE 4 0  \nteamB teamF 0 0  \nteamC teamD 2 0  \nteamC teamE 0 0  \nteamC teamF 1 0  \nteamD teamE 0 3  \nteamD teamF 2 1  \nteamE teamF 3 4  \nteamG teamH 3 2  \nteamG teamI 0 4  \nteamG teamJ 1 0  \nteamG teamK 1 4  \nteamG teamL 1 4  \nteamH teamI 2 0  \nteamH teamJ 3 0  \nteamH teamK 3 4  \nteamH teamL 0 1  \nteamI teamJ 2 1  \nteamI teamK 3 0  \nteamI teamL 1 3  \nteamJ teamK 1 4  \nteamJ teamL 0 3  \nteamK teamL 0 0  \n"
    )
    

