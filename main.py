import streamlit as st
from few_shot import FewShots
from post_generator import post_generator

st.title("Linkedin Post Generator")
col1,col2,col3 = st.columns(3)
few_shots = FewShots("data/processed_posts.json")
tags = few_shots.get_unique_tags()
language = list(set(few_shots.df["language"]))
length = list(set(few_shots.df["length"]))

with col1:
    selected_tag = st.selectbox("Topic",options = tags)

with col2:
    selected_language = st.selectbox("Language",options = language)

with col3:
    selected_length = st.selectbox("Length",options = length)

posts = few_shots.required_df(selected_language,selected_length,selected_tag)

post = post_generator(selected_language,selected_length,selected_tag)

if st.button("Generate"):
   st.write(post)