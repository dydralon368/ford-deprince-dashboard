import pandas as pd  
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="GIP Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"}
    )
# ---- MAINPAGE ----
st.image("https://ford.com.np/storage/pages/May2021/us0mtr4YC882z6b1BN7F.jpg")
st.title(":bar_chart: Jaarrekening Dashboard")
st.markdown("##")
# ---- READ EXCEL ACTIVA ----
@st.cache
def get_activa_from_excel():
    df = pd.read_excel(
        io="GIP_analyse van de jaarrekening_ford.xlsx",
        engine="openpyxl",
        sheet_name="verticale analyse balans",
        usecols="A:E",
        nrows=48,
        header=2
    )

    # filter row on column value
    activa = ["VASTE ACTIVA","VLOTTENDE ACTIVA"]
    df = df[df['ACTIVA'].isin(activa)]

    return df

df_activa = get_activa_from_excel()


# ---- READ EXCEL PASIVA ----
@st.cache
def get_passiva_from_excel():
    df = pd.read_excel(
        io="GIP_analyse van de jaarrekening_ford.xlsx",
        engine="openpyxl",
        sheet_name="verticale analyse balans",
        usecols="A:E",
        nrows=100,
        header=50
    )
    # filter row on column value
    passiva = ["EIGEN VERMOGEN","VOORZIENINGEN EN UITGESTELDE BELASTINGEN","SCHULDEN"]
    df = df[df['PASSIVA'].isin(passiva)]

    return df

df_passiva = get_passiva_from_excel()

# ---- READ EXCEL REV ----
@st.cache
def get_REV_from_excel():
    df = pd.read_excel(
        io="GIP_analyse van de jaarrekening_ford.xlsx",
        engine="openpyxl",
        sheet_name="REV",
        usecols="A:D",
        nrows=50,
        header=1
    )
   # change column names
    df.columns = ["Type","Boekjaar 1","Boekjaar 2","Boekjaar 3"]
    # filter row on column value
    REV = ["REV"]
    df = df[df["Type"].isin(REV)]

    df = df.T #Transponeren
    df = df.rename(index={"Boekjaar 1":"1","Boekjaar 2":"2",
                    "Boekjaar 3":"3"})
    df = df.iloc[1: , :] # Drop first row 
    df.insert(0,"Boekjaar",["Boekjaar 1","Boekjaar 2",
                    "Boekjaar 3"],True)
    df.columns = ["Boekjaar","REV"] # change column names
    
    
    return df

df_REV = get_REV_from_excel()
st.header('REV')
st.write(df_REV)

fig = px.line(df_REV, x="Boekjaar", y="REV", markers=True)
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)





# ---- READ EXCEL SOLVABILITEIT ----
@st.cache
def get_Solvabiliteit_from_excel():
    df = pd.read_excel(
        io="GIP_analyse van de jaarrekening_ford.xlsx",
        engine="openpyxl",
        sheet_name="Solvabiliteit",
        usecols="A:D",
        nrows=50
    )
     # change column names
    df.columns = ["Type","Boekjaar 1","Boekjaar 2","Boekjaar 3"]
    # filter row on column value
    sol = ["Solvabiliteit"]
    df = df[df["Type"].isin(sol)]

    df = df.T #Transponeren
    df = df.rename(index={"Boekjaar 1":"1","Boekjaar 2":"2",
                    "Boekjaar 3":"3"})
    df = df.iloc[1: , :] # Drop first row 
    df.insert(0,"Boekjaar",["Boekjaar 1","Boekjaar 2",
                    "Boekjaar 3"],True)
    df.columns = ["Boekjaar","Solvabiliteit"] # change column names
    
    
    return df

df_sol = get_Solvabiliteit_from_excel()

# ---- READ EXCEL Liquiditeit ----
@st.cache
def get_Liquiditeit_from_excel():
    df = pd.read_excel(
        io="GIP_analyse van de jaarrekening_ford.xlsx",
        engine="openpyxl",
        sheet_name="Liquiditeit",
        usecols="A:D",
        nrows=50,
        header=1
    )
     # change column names
    df.columns = ["type","boekjaar 1","boekjaar 2","boekjaar 3"]
    # filter row on column value
    liq = ["Liquiditeit in ruime zin"]
    df = df[df["type"].isin(liq)]

    df = df.T #Transponeren
    df = df.rename(index={"boekjaar 1":"1","boekjaar 2":"2","boekjaar 3":"3"})
    df = df.iloc[1: , :] # Drop first row 
    df.insert(0,"boekjaar",["boekjaar 1","boekjaar 2","boekjaar 3"],True)
    df.columns = ["boekjaar","Liquiditeit"] # change column names
    
    
    return df

df_liq = get_Liquiditeit_from_excel()
st.header('Liquiditeit')
st.write(df_liq)

fig = px.line(df_liq, x="boekjaar", y="Liquiditeit", markers=True)
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)



# ---- SIDEBAR ----
st.sidebar.header("Gelieve hier te filteren:")
boekjaar = st.sidebar.radio(
    "Selecteer boekjaar:",
    ("Boekjaar 1","Boekjaar 2","Boekjaar 3"),
    index=0
)


# Samenstelling activa boekjaar [TAART DIAGRAM]
fig_activa = px.pie(df_activa, 
            values=boekjaar, 
            names='ACTIVA',
            title=f'Samenstelling activa {boekjaar}'            
            )
fig_activa.update_traces(textfont_size=20, pull=[0, 0.2], marker=dict(line=dict(color='#000000', width=2)))
fig_activa.update_layout(legend = dict(font = dict(size = 20)), title = dict(font = dict(size = 30)))

# Samenstelling pasiva boekjaar [TAART DIAGRAM]
fig_passiva = px.pie(df_passiva, 
            values=boekjaar, 
            names='PASSIVA',
            title= f'Samenstelling passiva {boekjaar}'            
            )
fig_passiva.update_traces(textfont_size=20, pull=[0, 0.2], marker=dict(line=dict(color='#000000', width=2)))
fig_passiva.update_layout(legend = dict(font = dict(size = 20)), title = dict(font = dict(size = 30)))

# graph solvabiliteit
st.header('Solvabiliteit')
st.write(df_sol)
fig = px.line(df_sol, x="Boekjaar", y="Solvabiliteit", markers=True)
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)
##test
#
#
st.header('Verhouding activa - passiva')
col1, col2 = st.columns([1,1])
with col1:
    st.write(df_activa)
with col2:
    st.write(df_passiva)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_activa, use_container_width=True)
right_column.plotly_chart(fig_passiva, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)