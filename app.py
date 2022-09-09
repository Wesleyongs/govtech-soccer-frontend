import streamlit as st
import pandas as pd
import numpy as np
from utils import requests_post, get_inputs, request_delete
import datetime as dt
import requests

URL="http://localhost:8000/Soccer/"
HELP_MESSAGE="Data only persist after pressing submit, try changing some values, press submit and refresh the page"
# registrations_text="teamA 01/04 1\nteamB 02/05 1\nteamC 03/06 1\nteamD 04/06 1\nteamE 05/06 1\nteamF 15/06 1\nteamG 14/06 2\nteamH 13/06 2\nteamI 12/06 2\nteamJ 11/06 2\nteamK 10/06 2\nteamL 27/06 2\n"
# matches_text="teamA teamB 0 1\nteamA teamC 1 3\nteamA teamD 2 2\nteamA teamE 2 4\nteamA teamF 3 3\nteamB teamC 0 1\nteamB teamD 2 2\nteamB teamE 4 0\nteamB teamF 0 0\nteamC teamD 2 0\nteamC teamE 0 0\nteamC teamF 1 0\nteamD teamE 0 3\nteamD teamF 2 1\nteamE teamF 3 4\nteamG teamH 3 2\nteamG teamI 0 4\nteamG teamJ 1 0\nteamG teamK 1 4\nteamG teamL 1 4\nteamH teamI 2 0\nteamH teamJ 3 0\nteamH teamK 3 4\nteamH teamL 0 1\nteamI teamJ 2 1\nteamI teamK 3 0\nteamI teamL 1 3\nteamJ teamK 1 4\nteamJ teamL 0 3\nteamK teamL 0 0\n"

def app():
    st.title('Home')
    
    st.write("This is a sample home page in the mutliapp.")
    st.write("See `apps/home.py` to know how to use it.")

    registrations_text = get_inputs(URL, "Registration/")
    matches_text = get_inputs(URL, "Match/")

    registrations_input = st.text_area("Registration data", value=registrations_text, help=HELP_MESSAGE)
    matches_input = st.text_area("Match data", height=300, value=matches_text, placeholder=matches_text, help=HELP_MESSAGE)

    get_results = st.button("Submit")
    delete_all =  st.button("Delete All")
    
    if get_results:
        results = requests_post(URL+"Result", {"registrations_text":registrations_input, "matches_text":matches_input})
        df = pd.DataFrame(results)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%d-%m')
        st.write(df[['group_number',"team_name",'normal_score','team_score','alternate_score','date']].sort_values(by=['group_number','normal_score','team_score','alternate_score','date'], ascending=[True,False,False,False,True]))
        registrations_text = get_inputs(URL, "Registration/")
        matches_text = get_inputs(URL, "Match/")
        
    if delete_all:
        request_delete(URL+"Registration", "all registration data")
        request_delete(URL+"Match", "all match data")
        
        
    st.markdown("### Sample Data")
    st.write('Navigate to `Data Stats` page to visualize the data')

app()