import urllib.request
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

df=pd.read_csv('vehicles_us.csv')

# Function for replacing implicit duplicates
# Passing a list of wrong model names and a string with the correct model name on the function's input
def replace_wrong_models(wrong_models, correct_model): 
    for wrong_model in wrong_models: # looping over misspelled names
        df['model'] = df['model'].replace(wrong_models, correct_model) # calling replace() for each wrong name
# Removing implicit duplicates
wrong_models = 'ford f-150' # misspelled name
correct_model = 'ford f150' # correct model name
replace_wrong_models(wrong_models, correct_model) 

wrong_models = 'ford f-250' # misspelled name
correct_model = 'ford f250' # correct model name
replace_wrong_models(wrong_models, correct_model) 

wrong_models = ['ford f-250 sd', 'ford f-250 super duty'] # list of misspelled names
correct_model = 'ford f250 super duty' # correct model name
replace_wrong_models(wrong_models, correct_model) 

wrong_models = 'ford f-350 sd' # misspelled name
correct_model = 'ford f350 super duty' # correct model name
replace_wrong_models(wrong_models, correct_model) 

# Filling NaN values 
df['model_year'] = df['model_year'].fillna(df.groupby(['model'])
['model_year'].transform('median'))
#transforming model_year column to integer type 
df['model_year'] = df['model_year'].apply( lambda x: int(x)) 

# Filling NaN values
df['cylinders'] = pd.to_numeric(df['cylinders'], errors='ignore')
df['cylinders'] = df['cylinders'].fillna(df.groupby(['model'])
['cylinders'].transform('mean')).round()
# Filling NaN values
df['odometer'] = df['odometer'].fillna(df.groupby(['model_year'])['odometer'].transform('median'))
df['odometer'] = df['odometer'].round()

# Transforming "is_4wd" column to object type
df['is_4wd'] = df['is_4wd'].astype(str)

# Replacing NaN values by "unknown"
df['paint_color']=df['paint_color'].fillna('unknown')
df['is_4wd']=df['is_4wd'].replace('nan', 'unknown')
   
# Creating the header and subheader of app
st.header('Web App :red[**VEHICLES MARKETPLACE**]')
st.subheader(':violet[Use this app to explore the vehicles market in US]')

urllib.request.urlretrieve(
'https://pictures.dealer.com/b/butlermilledgevillefordfd/1702/e257e74b3dd14d4c5a88a596374e6036x.jpg?impolicy=downsize&w=568', "cars.png")
  
img = Image.open("cars.png")

st.image(img)

# Creating a new column "manufacturer"
df['manufacturer'] = df['model'].apply(lambda x:x.split()[0])

st.write('**Below you can see:**  \n- :green[**Histogram**] showing the information about :red[**Distribution of price range**]  \n - :red[**Bar Chart**] showing :green[**manufacturers**] split by :violet[**condition**] of the vehicles.  \n- :blue[**Scatter plot**] showing information about :green[**models**] split by :violet[**model year**] and :violet[**price**]')
st.write('*Use sliders, dropdown or visualizations for filtering data.*')
# Creating filter for price
price_range = st.slider(
     "Set the price range", 
     min_value=200, max_value=70000, value=(200,70000))

actual_range=list(range(price_range[0],price_range[1]+1))

filtered_data=df[df.price.isin(actual_range)]

# Creating filter for model_year
model_year_range = st.slider(
     "Set the year range", 
     min_value=1960, max_value=2020,value=(1960, 2020))

actual_range=list(range(model_year_range[0],model_year_range[1]+1))
filtered_data=filtered_data[filtered_data.model_year.isin(actual_range)]

# Creating multiselect dropdown for type of transmission
transmission_select_changed = False
transmission_options = df['transmission'].unique()
transmission_select = st.multiselect(
    "Choose the type of transmission", transmission_options, key="transmission")
# Using filtered_data for visualizations not to be empty before using multiselect
filtered_data=filtered_data[filtered_data.model_year.isin(actual_range)]
# Changing data according to user's selection
if transmission_select:
    transmission_select_changed= True
    filtered_data=filtered_data[filtered_data.transmission.isin(transmission_select)]
    
# Creating a bar graph to show quantity of advertisements split by condition
st.subheader(':green[**Manufacturers split by condition of vehicles**]')
fig = px.histogram(filtered_data, x="manufacturer", color="condition").update_xaxes(categoryorder='total descending')
st.plotly_chart(fig)
fig.update_xaxes(tickangle=-90)

# Creating histogram to show the price range distribution
st.subheader(':red[**Distribution of price range**]')
fig2 = px.histogram(filtered_data, x="price", color="fuel")
st.plotly_chart(fig2)


# Creating a scatter plot to show the models price and year range 
st.subheader(':violet[**Models by model year and price**]')
fig3 = px.scatter(filtered_data, x="price", y="model_year", color="model")
st.plotly_chart(fig3)
fig.update_xaxes(range=[200, 90000])


st.subheader(':blue[**Data overview**]')
st.write('*Use selection and checkbox to filter the data*')

# Sorting data in the table by price and hiding outliers
df=df.sort_values(by='price')
df=df[df.price>=200]

# Creating an empty DataFrame to store filtered data    
df_filtered = pd.DataFrame()

# Initializing the model_select variable
model_select = None

# Getting a list of unique manufacturer options from the original DataFrame
manufacturer_options = df['manufacturer'].unique()

# Creating a multi-select widget to select manufacturers
manufacturer_select = st.multiselect("Select manufacturer", manufacturer_options, key="manufacturer")


# Creating a flag to track if the manufacturer select has been changed
manufacturer_select_changed = False

# If the user selects one or more manufacturers:
if manufacturer_select:
    # Set the flag to indicate the manufacturer select has been changed
    manufacturer_select_changed = True
    
    # Filter the original DataFrame to only include rows with the selected manufacturers
    df_filtered = df[df['manufacturer'].isin(manufacturer_select)]
    
    # Get a list of unique model options from the filtered DataFrame
    model_options = df_filtered['model'].unique()
    
    # Create a multi-select widget to select models
    model_select = st.multiselect("Select model", model_options, key="model")
# If user selects manufacturer and model    
if model_select and manufacturer_select:
    df_filtered = df_filtered[df_filtered['model'].isin(model_select)]

# If the user selects one or more models, but the manufacturer select has not been changed:
if model_select and not manufacturer_select_changed:
    # Filter the original DataFrame to only include rows with the selected models
    df_filtered = df_filtered[df_filtered['model'].isin(model_select)]
    
    # Get a list of unique manufacturer options from the filtered DataFrame
    manufacturer_options = df_filtered['manufacturer'].unique()
    
    # Create a multi-select widget to select manufacturers
    manufacturer_select = st.multiselect("Select manufacturer", manufacturer_options, key="manufacturer")

# Creating checkbox to filter only new vehicles
condition_new = st.checkbox('Only new vehicles')
# Adding conditions to make it work in any direction and on any stage of multiselect
if condition_new and not df_filtered.empty:
        
    df_filtered=df_filtered[df_filtered.condition=='new']
    
elif condition_new and df_filtered.empty:
    df_filtered=df[df.condition=='new']
    
elif condition_new and df[df['manufacturer'].isin(manufacturer_select)]:
    df_filtered=df[df.condition=='new']
    
elif condition_new and df[df['manufacturer'].isin(manufacturer_select)] and df[df['model'].isin(model_select)]:
    df_filtered=df[df.condition=='new']
      
# If the filtered DataFrame is not empty, display it
if not df_filtered.empty:
    st.write(df_filtered) 
# If no filters were applied displaying DataFrame   
if df_filtered.empty:
    st.write(df)
