import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)

@st.cache_data(ttl= 30)
def load_runs():
    query = "SELECT drift_score, diagnosis, action_taken, ran_at FROM sentinel_runs ORDER BY ran_at ASC"
    return pd.read_sql(query, engine)

st.title("Sentinel - ML Guardian Dashboard")
st.markdown("Autonomous drift detection and model remediation")



df = load_runs()

if df.empty:
    st.warning("No runs yet. Hit POST /sentinel/run first.")
    st.stop()
col1, col2, col3 = st.columns(3)
col1.metric("Total Runs", len(df))
col2.metric("Avg Drift Score", f"{df['drift_score'].mean():.3f}")
col3.metric("Retrains Triggered", len(df[df['action_taken'].str.contains("Retraining")]))

st.subheader("Drift Score Over Time")
fig = px.line(df, x="ran_at", y="drift_score", title="Model Drift Score Over Time", markers=True)
fig.add_hline(y=0.3, line_dash="dash", line_color="red", annotation_text="Threshold (0.3)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Recent Agent Decisions")
st.dataframe(df[["ran_at", "drift_score", "action_taken"]].sort_values("ran_at", ascending=False).head(10))

st.subheader("Latest Diagnosis")
st.write(df.iloc[-1]["diagnosis"])