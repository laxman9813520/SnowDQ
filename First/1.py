
import streamlit as st

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column,String,Integer,Float

import pandas as pd

from streamlit_option_menu import option_menu

from snowflake.sqlalchemy import URL

 
st.set_page_config(
    layout = "wide",
)
# connect to database

url = URL(

            user="PavanKumarreddy",

            password="P@van@2001",

            account="gg26504.ap-southeast-1",

            database="task_db",

            schema="task_sc",

            warehouse="compute_wh",

            role="ACCOUNTADMIN"

        )

engine = create_engine(url)

Session = sessionmaker(bind=engine)

sess = Session()

a,b = st.columns([15,120])
with a:
    logo = st.image("media\\logo.png")
with b:
    selected2 = option_menu(None, ["Project", "Suits", "Expectations", 'Datasets'],  
    default_index=0, orientation="horizontal")

if selected2 == "Expectations":

    search = st.text_input("search expectation")

    if search:
        query = f"""SELECT RULE,TAGS,ARGS,DESCRIPTION,OWNER,CATEGORY,STATUS,SUPPORTED_BACKEND FROM DQ_RULES where RULE ILIKE '%{search}%' """
        data = sess.execute(query).fetchall()
        df = pd.DataFrame(data)
        # st.write(df)
        for index in range(len(df.index)):
            col1, col2, col3, col4, col5, col6 = st.columns([35, 20, 20, 20 ,20 ,15])
            with col1: 
                st.write(df['rule'][index])
                st.text(df['description'][index])
            with col2:
                st.write("Owner")
                st.write(df["owner"][index])
            with col3: 
                st.write("Category")
                st.write(df["category"][index])
            with col4:
                st.write("Tags")
                st.write(df["tags"][index])

            with col5: 
                st.write("Backend support")
                st.write(df["supported_backend"][index])
            with col6:
                st.write("Status")
                st.success(df["status"][index])
            st.markdown("""---""")
    else:
        query = '''SELECT RULE,TAGS,ARGS,DESCRIPTION,OWNER,CATEGORY,STATUS,SUPPORTED_BACKEND FROM DQ_RULES'''
        data = sess.execute(query).fetchall()
        df = pd.DataFrame(data)
        for index in range(len(df.index)):

            col1, col2, col3, col4, col5, col6 = st.columns([35, 20, 20, 20 ,20 ,15])
            with col1: 
                st.write(df['rule'][index])
                st.text(df['description'][index])
            with col2:
                st.write("Owner")
                st.write(df["owner"][index])
            with col3: 
                st.write("Category")
                st.write(df["category"][index])
            with col4:
                st.write("Tags")
                st.write(df["tags"][index])

            with col5: 
                st.write("Backend support")
                st.write(df["supported_backend"][index])
            with col6:
                st.write("Status")
                st.success(df["status"][index])
            st.markdown("""---""")