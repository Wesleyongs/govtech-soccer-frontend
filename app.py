import streamlit as st
import pandas as pd
import numpy as np
from utils import requests_post, get_inputs, request_delete
import datetime as dt
import requests

URL="http://localhost:8000/Soccer/"
HELP_MESSAGE="Data only persist after pressing submit, try changing some values, press submit and refresh the page"

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