import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import time


st.title("Airbnb Analysis")
# Creating a navigation bar using option_menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Explore data", "Overview", "About"],
        icons=["house", "search", "list", "info-circle"],
        default_index=0
)

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://ananthn:Ananth2000@cluster0.z0lxt6s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv("D:/machine learning/Airbnb_data.csv")


def show_cash_animation():

    animation_placeholder.empty()  # Clear previous animation

    for _ in range(10):  # Adjust range for animation duration
        animation_placeholder.markdown("💵💵💵 Cash Flow! 💵💵💵")
        time.sleep(0.1)
        animation_placeholder.empty()
        time.sleep(0.1)

# Display selected page
if selected == "Home":
    st.write("Welcome to the Home Page")

    col_1 , col_2 = st.columns(2)

    with col_1:
        st.write()
        st.subheader("About Airbnb:")
        
        # Key points about Airbnb with emojis/icons
        airbnb_points = [
            "🏠 **Founded in 2008**: Airbnb was started by Brian Chesky, Joe Gebbia, and Nathan Blecharczyk as a platform to rent out air mattresses during a conference in San Francisco.",
            "🌍 **Global Presence**: Airbnb operates in more than 220 countries and has millions of listings across various accommodation types, from apartments to unique stays like treehouses and castles.",
            "🔗 **Peer-to-Peer Model**: The platform connects hosts, who provide accommodations, with guests looking for short-term rentals, creating a sharing economy for travel.",
            "🏡 **Variety of Listings**: Airbnb offers a wide range of stay options, including homes, apartments, villas, boutique hotels, and even unique places like igloos and houseboats.",
            "🧑‍🍳 **Experiences**: Besides stays, Airbnb offers 'Experiences' where users can book activities hosted by locals, such as cooking classes, guided tours, and workshops.",
        ]
        # Displaying each point as a bullet point
        for point in airbnb_points:
            st.write(point)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.image("D:/machine learning/1_Bjxx73f5epqaaMYmR1EOqQ.png")


    with col_2:
        st.image("D:/machine learning/airbnb-logo.png",width=450)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        airbnb_points = [
            "🔐 **Trust and Safety**: Airbnb has a robust review system where guests and hosts leave feedback after each stay, promoting trust within the community.",
            "🛌 **Flexible Stays**: The platform introduced flexible cancellation policies and long-term stays, making it adaptable to different guest needs, especially during the pandemic.",
            "🌱 **Sustainability Efforts**: Airbnb encourages eco-friendly travel by promoting sustainable tourism and supporting initiatives that reduce the carbon footprint of its community.",
            "🏅 **Superhost Program**: Airbnb has a recognition system where top-rated hosts, called 'Superhosts,' are rewarded for maintaining a high level of hospitality.",
            "💰 **Revenue Model**: Airbnb charges a service fee from both guests and hosts, allowing them to provide services like customer support, insurance, and platform maintenance."
        ]
        
        for point in airbnb_points:
            st.write(point)
        st.write("")
        
        # Footer or additional notes
    st.markdown("*Learn more about Airbnb on their [official website](https://www.airbnb.com).*")


elif selected == "Explore data":
    st.write("Explore your data here")

    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

    # Trigger animation when the price slider value changes
    animation_placeholder = st.empty()
    show_cash_animation()

    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    col_1 , col_2 = st.columns(2)

    with col_1:

        pr_df = df.query(query).sort_values(['Room_type', 'Price'], ascending=[True, True])
        fig = px.bar(data_frame=pr_df,x='Room_type',y='Price',color='Price',title='Price in each Room type',color_continuous_scale='Plasma')
        st.plotly_chart(fig)

    with col_2:

        pr_df_2 = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df_2,x='Room_type',y='Price',color='Price',title='Avg Price in each Room type',color_continuous_scale="Plasma")
        st.plotly_chart(fig)

    # HEADING 2
    st.subheader("Availability Analysis")

    # room avaliablity boxplot analysis
    fig = px.box(data_frame=df.query(query),x='Room_type',y='Availability_365',color='Room_type',title='Availability by Room_type')
    st.plotly_chart(fig,use_container_width=True)

    col_1 , col_2 = st.columns(2,gap='medium')

    with col_1:
        # AvG AVAILABILITY IN PRICE SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,locations='Country',color= 'Price',hover_data=['Price'],locationmode='country names',size='Price',
                                title= 'Avg Price in each Country',color_continuous_scale='Viridis')
        st.plotly_chart(fig)

    with col_2:

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,locations='Country',color= 'Availability_365', hover_data=['Availability_365'],locationmode='country names',
                                    size='Availability_365',title= 'Avg Availability in each Country',color_continuous_scale='Viridis')
        st.plotly_chart(fig)


elif selected == "Overview":
    st.write("Over view the data here")
    st.subheader("Airbnb data")
    st.dataframe(df)
    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)
    st.download_button(label="Download data as CSV",data=csv_data,file_name="Airbnb.csv",mime="text/csv")

    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

    # Trigger animation when the price slider value changes
    animation_placeholder = st.empty()
    show_cash_animation()

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'


    df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
    # TOP 10 PROPERTY TYPES BAR CHART
    fig_1 = px.bar(df1, x='Listings', y='Property_type',hover_data=['Property_type', 'Listings'], color='Property_type',height=500,title="Top 10 Property type")
    st.plotly_chart(fig_1)

    # TOP 10 HOSTS BAR CHART
    df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
    fig_2 = px.bar(df2,title='Top 10 Hosts with Highest number of Listings',x='Listings',y='Host_name',color='Host_name',hover_data=["Host_name","Listings"])
    st.plotly_chart(fig_2)

    # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
    df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
    fig_3 = px.pie(df1,title='Total Listings in each Room_types',names='Room_type',values='counts',color='Room_type')
    fig_3.update_traces(textposition='outside', textinfo='value+label')
    st.plotly_chart(fig_3)

    # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
    country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
    fig_4 = px.choropleth(country_df,title='Total Listings in each Country',locations='Country',locationmode='country names',color='Country')
    st.plotly_chart(fig_4)

elif selected == "About":
    st.write("This is the About page")
    # Skills Takeaway
    st.header("Skills Takeaway From This Project")
    skills = """
    - **Python scripting** 
    - **Data Preprocessing** 
    - **Exploratory Data Analysis (EDA)** 
    - **Visualization** 
    - **Streamlit** 
    - **MongoDB** 
    - **PowerBI**
    """
    st.write(skills)

    # Domain
    st.header("Domain")
    st.write("**Travel Industry, Property Management, and Tourism**")

    # Problem Statement
    st.header("overview of the project:")
    problem_statement = """
    This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, 
    and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.
    """
    st.write(problem_statement)

    # Footer or additional information
    st.markdown("*This project provides key insights into the Airbnb dataset, helping stakeholders make data-driven decisions.*")


