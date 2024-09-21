import streamlit as st
import joblib;
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.graph_objects as go
with st.sidebar:
    selected = option_menu(
        menu_title="ECI",  # Required
        options=["Home", "Section 1", "Section 2", "Section 3"],  # Required
        icons=["house", "file-earmark-text", "gear", "envelope"],  # Optional
        menu_icon="cast",  # Optional
        default_index=0,  # Optional
    )

# Define the content for each page
if selected == "Home":
    # Define the CSS for the header with a colored border
    header_css = """
    <style>
        .header {
            border: 3px solid #000000; /* Green border color */
            padding: 10px;
            text-align: center;
            margin-bottom: 5px;
            background-color: #af2b3c;
            color: white;
             }
        
        .header1{
            padding: 0px;
            text-align: center;
            margin-bottom: 10px;
            background-color: #f5e2af;
            color: black;
        }
          .header2{
            padding: 0px;
            text-align: center;
            margin-bottom: 10px;
            background-color:#d4d8db;
            color: black;}
    </style>
    """     

    # Render the header with the custom CSS
    st.markdown(header_css, unsafe_allow_html=True)     

    # Define the header with the class 'header' for styling
    st.markdown('<div ><h1 class="header">Election Commission of India</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="header1"><b>Disclaimer</b>:ECI is displaying the information as being filled in the system by the Returning Officers from their respective Counting Centres.The final data for each AC/PC will be shared in Form-20.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    # Define actions for each button
    with col1:
        if st.button("Parliamentary Constituency General"):
          st.write("Hello, Streamlit user!")
    
    with col2:
        if st.button("Assembly Constituency General"):
           st.write("Hello, Streamlit user!")
    with col3:
        if st.button("Assembly Constituency bye 2024"):
          st.write("Hello, Streamlit user!")

    st.markdown('<p class="header2"><b>General Election to Parliamentary Constituencies: Trends & Results June-2024</b></p>', unsafe_allow_html=True)
    df=pd .read_csv("election/election.csv")
     # Extract the list of unique states
    df = pd.DataFrame(df)
     
     # Extract the list of unique states
    unique_states = df['state'].unique()
     
     # Create a Streamlit app to display the filters and update options dynamically
     
     # Select box widget for state selection
    selected_state = st.selectbox("Select:", unique_states)
   



    # # Calculate sizes and labels for the pie chart
    states1=pd.read_csv("seatcount.csv")
   
    labels = states1['Party Name']
    sizes = states1['count']
    
    total_count = sum(sizes)

    # Calculate percentages
    percentages = [(count / total_count) * 100 for count in sizes]
    
    # Combine counts <= 7 into "Others"
    others_count = sum(count for count in sizes if count <= 7)
    Party_Name_names_combined = [Party_Name for Party_Name, count in zip(labels, sizes) if count > 4] + ["Others"]
    sizes_combined = [count for count in sizes if count > 4] + [others_count]
    
    # Recalculate percentages for combined data
    percentages_combined = [(count / total_count) * 100 for count in sizes_combined]
    
    # Create labels with Party_Name names and number of seats, showing sum for "Others"
    labels_combined = [
        f"{Party_Name} ({count} seats)" if Party_Name != "Others" else f"{Party_Name} ({others_count} seats)"
        for Party_Name, count in zip(Party_Name_names_combined, sizes_combined)]
    plt.figure(figsize=(300,30))
    
    # Create the half pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=labels_combined, values=sizes_combined, hole=0.5, direction='clockwise', sort=True)])

    # Update layout for half pie chart appearance
    fig.update_layout(
        title_text='Half Pie Chart Example',
        showlegend=False,
        annotations=[dict(text='543/543', x=0.5, y=0.5, font_size=20,showarrow=False)],
        margin=dict(t=0, b=0, l=0, r=0),
    )
    
    # Modify the angles to make it look like a half pie chart
    fig.update_traces(rotation=-85, pull=[0.0]*len(sizes), 
                      hoverinfo='label+value', 
                      marker=dict(line=dict(color='#000000', width=0.5)))
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)
    col1, col2 = st.columns(2)
    with col2:
         if st.markdown("Party Wise Results Status"):
             st.dataframe(states1)
    with col1:
        if st.write("Party Wise Vote Share"):
            st.write("not found")
elif selected == "Section 1":
 

         # Data filtering according to the states,constituency and Party_Name
     
     
    df=pd .read_csv("election/election.csv")
     # Extract the list of unique states
    df = pd.DataFrame(df)
     
     # Extract the list of unique states
    unique_states = df['state'].unique()
     
     # Create a Streamlit app to display the filters and update options dynamically
    st.title('Filter Winning Parties by State, Constituency, and Party')
     
     # Select box widget for state selection
    selected_state = st.selectbox("Select a state to filter the data:", unique_states)
     
     # Filter the DataFrame based on selected state to update constituency and party options
    if selected_state:
         filtered_df = df[df['state'] == selected_state]
         unique_constituencies = filtered_df['constituency'].unique()
         unique_parties = filtered_df['Party Name'].unique()
    else:
         unique_constituencies = df['constituency'].unique()
         unique_parties = df['Party Name'].unique()
     
     # Select box widget for constituency selection
    selected_constituency = st.selectbox("Select a constituency to filter the data:", unique_constituencies)
     
     # Select box widget for party selection
    selected_party = st.selectbox("Select a party to filter the data:", unique_parties)
     
     # Filter the DataFrame based on selected filters and show only winning parties
    filtered_df = df[
         (df['state'] == selected_state) & 
         (df['constituency'] == selected_constituency) & 
         (df['Party Name'] == selected_party) & 
         (df['won status'] == 'won')
     ]
     
     # Display the filtered DataFrame
    if not filtered_df.empty:
         st.write("Filtered Data (Winning Parties):")
         st.dataframe(filtered_df)
    else:
         st.write("No winning data found for the selected filters.")




elif selected == "Section 2":
    st.title("Section 2")
    st.write("Welcome to Section 2 of the app.")
elif selected == "Section 3":
    st.title("Section 3")
    st.write("Welcome to Section 3 of the app.")
    st.title("Streamlit Button Example")


import numpy as np
# Define actions for buttons


