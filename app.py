import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from supabase import create_client, Client

# Create Supabase client
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)

@st.cache_resource()
def get_supabase_client():
    return init_supabase()

st.session_state.supabase = get_supabase_client()

data, count = st.session_state.supabase.table('T_F_BODY_WEIGHT').select('Date', 'Weight').execute()
data = pd.DataFrame(data[1])
# st.line_chart(data, x="Date", y="Weight")

min_weight = data['Weight'].min()
max_weight = data['Weight'].max()

# Create Altair line chart
chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%Y-%m-%d')),
    y=alt.Y('Weight:Q', scale=alt.Scale(domain=[min_weight, max_weight])),  # Set y-axis limits
).properties(
    title='Weight Over Time'
)

# Render the chart in Streamlit
st.altair_chart(chart, use_container_width=True)