import requests
import streamlit as st
import json

def requests_post(url, params):
    x = requests.post(url, params=params)
    
    if x.status_code==200:
        st.success("Here are the results")
        return x.json()
    else:
        st.warning("There was an error")
        st.exception(x.text)
        
# get persistent inputs from db
def get_inputs(url, endpoint):
    res = json.loads(requests.get(url+endpoint).text)
    
    try:
        if endpoint == "Registration/":
            rows = [" ".join([i['team_name'],i['date'],str(i['group_number'])]) for i in res]
        elif endpoint == "Match/":
            rows = [" ".join([i['team_1_name'],i['team_2_name'],str(i['team_1_score']), str(i['team_2_score'])]) for i in res]
        return "\n".join(rows)
    except: # no data or valid data in db
        return ""
    
def request_delete(url, message):
    res = requests.delete(url)
    if res.status_code == 200:
        st.success("Sucessfully Deleted")
    else:
        st.warning(res.status_code, message)