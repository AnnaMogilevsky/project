**Note for reviewer**: I removed versions from requirements because these old versions don’t work with colors.

# Project

## Links
Link to GitHub repository: https://github.com/AnnaMogilevsky/project  

URL of app on Render: https://cars-marketplace-n7os.onrender.com

# Project Description

This project was made to develop web app as a tool to explore the vehicles market, by using different visualizations and filters.
For this project were used pandas, streamlit, plotly.express, urllib.request libraries and urllib.request.urlretrieve, st.image, st.write, st.header, st.subheader, st.slider, st.multiselect, st.plotly_chart, st.checkbox, px.scatter ,px.histogram methods used to implement it.

# How to use application
Use filters to see only information you are interested in. First three filters, such as price range, year range and multiselect dropdown with the types of transmission,  change data in visualizations. 
First visualization displays the total number of sales advertisements split by manufacturers. Each manufacturer bar is split by condition of vehicles. Press the “condition” from the right side of the visualization to remove the condition to have only information you are interested in.
Second visualization displays  the total number of sales advertisements split by price. The color shows the type of fuel. Press the “fuel” from the right side of the visualization to remove the fuel type to have only information you are interested in.
Third visualization displays the sales advertisements for models of vehicles by their year and price. Press the “model name” from the right side of the visualization to remove it to have only information you are interested in.
Below the visualizations you will find the data overview. Use multiselect dropdowns and checkbox to filter data. Also you can press the column header to sort each column.

You can launch the application also on your local machine. 
To do this you need to have all packages installed on your local machine, such as: pandas, streamlit, plotly.express, urllib.request, altair.
Use this link: https://github.com/AnnaMogilevsky/project
Find file ‘app.py’, download it to your local machine and run it with command “streamlit run app.py” from the terminal. 
