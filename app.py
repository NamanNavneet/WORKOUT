import streamlit as st
import pandas as pd
import helper



st.sidebar.title("WORKOUTS")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Running Exercises','Mat Exercises','Stretching','Leg Day','Yoga','Dumbbells','Gym Exercise')
)

if user_menu == 'Mat Exercises':

    helper.mat()

if user_menu == 'Stretching':

    helper.stretch()

if user_menu == 'Leg Day':

    helper.leg()

if user_menu == 'Yoga':

    helper.yoga()

if user_menu == 'Running Exercises':

    helper.run()

if user_menu == 'Dumbbells':

    helper.dumbbells()

if user_menu == 'Gym Exercise':

    helper.gym()






