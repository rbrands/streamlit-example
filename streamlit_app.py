import os
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import blob
import yaml
import streamlit_authenticator as auth
from io import StringIO

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
# Read environment configuration. See https://github.com/theskumar/python-dotenv
load_dotenv(find_dotenv(), override=False)
st.write("Environment variable `APP_CONFIG_KEY` is:", os.getenv("APP_CONFIG_KEY"))    

# Read authentication config from Azure BLOB storage
auth_config = blob.read_authentication_config().decode("utf-8")
auth_config = yaml.safe_load(auth_config)

authenticator = auth.Authenticate(
    auth_config['credentials'], 
    auth_config['cookie']['name'],
    auth_config['cookie']['key'],
    auth_config['cookie']['expiry_days'],
    auth_config['preauthorized']
)

# Simple graphics with Streamlit

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
    
"""
## Simple authentication

Demo how to implement a very simple authentication mechanism: 
Username/passwords are stored in a config file in blob storage.

"""

authenticator.login('Login', 'main')
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='logout_unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Protected Content')
    """
    This part of the page is only visible if the user has been authenticated.
    """
    uploaded_file = st.file_uploader('Upload File', accept_multiple_files=False)
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        blob.write_blob(uploaded_file.name, bytes_data)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
