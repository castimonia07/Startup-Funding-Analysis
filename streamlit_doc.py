import streamlit as st

# Title of the app
st.title("Startup Dashboard")
# header
st.header("This is me")

# Header with emoji
st.header("Welcome to the Startup Dashboard! 🚀")

# Subheader
st.subheader("Your one-stop solution for startup management")

# Write
st.write('This is a normal text')

# Markdown
st.markdown("### Welcome to the Startup Dashboard")  # no. of # = heading level

# code block
st.code("""python
def hello_world():
    print("Hello, World!")
""", language='python')

# Latex
st.latex(r'''
    E = mc^2
''')

# DISPLAY MEDIA

# Image
st.image("https://via.placeholder.com/150", caption="Placeholder Image")

# Video
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Audio
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# DISPLAY ElEMENTS

# Dataframe
import pandas as pd
data=pd.DataFrame({
    'Column 1': [1, 2, 3],
    'Column 2': ['A', 'B', 'C'],
    'Column 3': [True, False, True]
})
st.dataframe(data)

# metric
st.metric(label="Revenue", value="$100,000", delta="$9,000")
# we can give percentage too
st.metric(label="Growth", value="1000",delta="2%")

# Json...used for making API calls
import json
data_json=({
    'name': 'Startup Inc.',
    'Column 1': [1, 2, 3],
    'Column 2': ['A', 'B', 'C'],
    'Column 3': [True, False, True]
})
st.json(data_json)

# Creating Layouts

#Sidebar
st.sidebar.header("Sidebar Header")

# what if we want to add the things in a single row i.e side by side
col1, col2 = st.columns(2)
with col1:
    st.image("https://via.placeholder.com/150", caption="Column 1 Image")
with col2: 
    st.image("https://via.placeholder.com/150", caption="Column 2 Image")


# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])    
with tab1:
    st.write("Content for Tab 1")   
with tab2:
    st.write("Content for Tab 2")

# Expander...in the a drop down menu is appeared
with st.expander("See more details"):
    st.write("Here are some more details about the startup.")

# Error message
st.error("This is an error message.")
# Warning message
st.warning("This is a warning message.")
# Info message
st.info("This is an info message.")
# Success message
st.success("This is a success message.")

# PROGRESS BAR
#used to show the progress of a task in a visual way similar to the download progress bar
import time
bar=st.progress(0)
for i in range(1,101):
    time.sleep(0.1)  # Simulating a long-running task
    bar.progress(i)  # Update the progress bar

# Spinner....used for showing a loading state
with st.spinner("Loading..."):
    time.sleep(2)  # Simulating a long-running task


# INPUTS FROM USER

# Text input
user_input = st.text_input("Enter some text")

# Number input
user_number = st.number_input("Enter a number", min_value=0, max_value=100)

# Date input
user_date = st.date_input("Select a date")

# Time input
user_time = st.time_input("Select a time")

# Button
import streamlit as st

email=st.text_input("Enter your email address")
password=st.text_input("Enter your password", type="password")

# Selectbox
gender=st.selectbox("Select your gender", ("Male", "Female", "Other"))

btn=st.button("Login")
if btn:
    if email=='rishabh@gmail.com' and password=='12345':
        # st.success("Login successful!")
        st.write(gender)
        st.balloons()  # Show balloons on successful login
        st.write("Welcome to the app!")
        st.write("You have successfully logged in.")
        # You can add more functionality here after login
        st.write("Feel free to explore the app.")   
    else:
        st.error("Login failed. Please check your credentials.")

# 




