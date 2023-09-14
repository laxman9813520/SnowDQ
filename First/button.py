import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_searchbar import streamlit_searchbar
from sqlalchemy.orm import sessionmaker
from snowflake.connector import connect


from sqlalchemy import create_engine, Column,String,Integer,Float

#import pandas as pd

#from streamlit_option_menu import option_menu

from snowflake.sqlalchemy import URL   

from sqlalchemy.exc import OperationalError


import time

st.set_page_config(
    layout = "wide",
)
col1,col2 = st.columns((1,8))
with col1:
   st.image("logo.png", width=140)

with col2:

    page_selected = option_menu(

                menu_title = None,

                options = ['Projects', 'Suites', 'Expectations','Datasets'],

                default_index = 0,

                icons=['stack','bounding-box','file-earmark-text','folder2'],

                menu_icon=None,

                orientation='horizontal',

                styles={

                "container": {"padding": "0!important", "background-color": "#fafafa"},

                # "icon": {"color": "orange", "font-size": "25px"},

                "icon":{"display":"inline-block"},

                "nav": {"background-color":"#f2f5f9"},

                "nav-link": {"font-size": "15px",

                "font-weight":"bold",

                "color":"#00568D",

                "border-right":"1.5px solid #00568D",

                "border-left":"1.5px solid #00568D",

                "border-top":"1.5px solid #00568D",

                "border-bottom":"1.5px solid #00568D",

                "padding":" 7px",

                "text-transform": "uppercase",

                "border-radius":"5px",

                "margin":"0.4px",

                "--hover-color": "#e1e1e1"},

                "nav-link-selected": {"background-color":"#4682B4", "color":"#ffffff"},

                }

)

snowflake_config = {
    "user": "SNOWDQ",
    "password": "SnowDQ@202308",
    "account": "anblicksorg_aws.us-east-1",
    "database": "SNOWDQ_DB",
    "schema": "public",
    "warehouse":"SNOWDQ_WH",
    "role": "SNOWDQ_ARL",
    }
url = URL(**snowflake_config)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
sess = Session()
query  =  "select * from real_table"
data = sess.execute(query).fetchall()
df = pd.DataFrame(data)
query1 = "select distinct(name) from dq_project"
data1 = sess.execute(query1).fetchall()
df1 = pd.DataFrame(data1)
query2 = "select res:group_name::varchar as Suite,res:checkpoint_name::varchar as checkpoint,res:run_name::varchar as RunName,res:total_records_passed::int as Success,res:total_records_failed::int as Failed,res:success_percentage::float as DQscore,res:run_date_time::varchar as RunDate from results_json"
data2 = sess.execute(query2).fetchall()
df2 = pd.DataFrame(data2)
col1, col2 = st.columns([2, 6])
with col1:
        st.title("")
        c1,c2=st.columns([1,1])
        with c1:
            decent = """
            <html>
            <body>
                    <div class="search-container">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" class="search-input" placeholder="Search Project">
                    </div>
                    <!-- Include Font Awesome for the search icon -->
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
                    </body>
                    <style>
                                    .search-container {
                                        display: flex;
                                        align-items: center;
                                        width: 145px; /* Adjust the width as needed */
                                        border: 1px solid #ccc;
                                        border-radius: 5px;
                                        padding: 5px;
                                        height: 40px;
                                    }

                                    .search-input {
                                    border: none;
                                    width: 100%;
                                    padding: 5px;
                                    outline: none;
                                    }

                                    .search-icon {
                                        padding:5px;
                                        color: #777;
                                    }
                        </style>
                        </html>"""
            st.markdown(decent, unsafe_allow_html=True)
        with c2:
            st.write(f'<style>div.stButton > button {{background-color: #002366;color: white;}}</style>',unsafe_allow_html=True,)
            st.markdown( """<style>
                        .stButton>button {
                      margin-top: -50px;
                      margin-left: -10px;
                        position: absolute;
                        top: 20px
                                 }
                            </style> """, unsafe_allow_html=True,)
            if st.button("Add Project"):
                    right_popup_content = """
                        <div id="rightPopup" style="position: fixed; top: 0; right: 0; width: 300px; z-index: 9999; height: 100%; background-color: white; box-shadow: -5px 0 5px rgba(0, 0, 0, 0.2);">
                            <h5 style="padding: 20px;">Add New Project</h5>
                            <form id="project-form">
                                <label for="projectname">Project Name:</label><br>
                                <input type="text_input" id="projectname" ><br><br>
                                <label for="description>Description:</label><br>
                                <textarea id="description" name="description" rows='4' cols='30'></textarea><br><br>
                                <button style="margin: 10px;" type="button" onclick="addProject()">Add Project</button>
                                <button style="margin: 10px;" type="button" onclick="closePopup()">Cancel</button>
                            </form>
                        </div>
                        <script>
                        function addProject() {
                        var projectname = document.getElementById("projectname").value;
                        var projectdescription = document.getElementById("description").value;
                        Streamlit.setComponentValue({ "projectName": projectname, "description": description });
                            }
                        <script>
                        function closePopup() {
                                document.querySelector('#rightPopup').style.display = 'none';
                            }
                        </script>
                    """
                    st.markdown(right_popup_content, unsafe_allow_html=True)
                    projectname = st.get_last_component_value()

            
                st.write(" ")
        for i in df1.index:
             st.write(df1['name'][i])

with col2: 
        st.markdown('<h1 style="font-size: 24px;">Sales Data Quality Check</h1>', unsafe_allow_html=True)
        st.write("Sales Data Quality Check")
        html_code = """
                <style>
                /* Define the CSS for the boxes and container */
                .container {
                display: flex;
                justify-content: space-between;
                }
                .box {
                background-color: #E6E8E8;
                width: 2000px;
                height: 120px;
                padding: 20px;
                margin: 15px;
                </style>
                <div class="container">
                <div class="box">
                <p>Average DQ Score</p>
                <p1 style="font-size: 24px;">80</p1>
                </div>
                <div class="box">
                <p>Total Records</p>
                <p1 style="font-size: 24px;">12699</p1>
                </div>
                <div class="box">
                <p>Failed</p>
                <p1 style="color:red;"> 6 </p1>
                </div>
                <div class="box">
                <p>Success</p>
                <p1 style="color:green;">12693</p1>
                </div>
                </div>"""
        st.markdown(html_code , unsafe_allow_html=True)
        cola,colb = st.columns([10,2])
        with cola:
            st.markdown("**Last 10 Executed Runs**")
        with colb:
            st.markdown(":blue[View all runs →]")
        st.write(df)

        
        
        