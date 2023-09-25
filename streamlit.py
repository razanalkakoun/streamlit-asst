import pandas as pd
import numpy as np 
import streamlit as st
import plotly.express as px


st.title("Titanic Visualization using Streamlit")



def load_data(nrows): 
    data = pd.read_csv("train.csv", nrows=nrows)  #we read the specifed number of rows from this CSV file 
    lowercase = lambda x: str(x).lower() #then we convert names to lowercase; it takes x as an input and converts it to str(x), and the applies ;lower()
    data.rename(lowercase, axis='columns', inplace=True) #this means that the lambda function "lwecasr" will be applied to each column of the dataframe 
    return data


data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!')

# Set the app title and description
st.title("Titanic Data Visualization")
st.write("Explore the Titanic dataset and visualize passenger information.")

# Interactive Feature 1: Select Feature to Display
feature_to_display = st.selectbox("Select a Feature to Display", data.columns)

# Visualization 1: Bar Chart
st.subheader(f"Bar Chart of {feature_to_display}")
bar_chart = px.bar(data, x=feature_to_display)
st.plotly_chart(bar_chart)

# Interactive Feature 2: Select X and Y Features for Scatter Plot
x_feature = st.selectbox("Select X-axis Feature", data.columns)
y_feature = st.selectbox("Select Y-axis Feature", data.columns)

# Visualization 2: Scatter Plot
st.subheader(f"Scatter Plot of {x_feature} vs. {y_feature}")
scatter_plot = px.scatter(data, x=x_feature, y=y_feature, color='survived', title=f'{x_feature} vs. {y_feature}')
st.plotly_chart(scatter_plot)

# Example for age distribution
st.subheader("Age Distribution")
hist_age = px.histogram(data, x="age", nbins=30, title="Age Distribution")
st.plotly_chart(hist_age)

# Example for count plot of passenger class
st.subheader("Passenger Class Count")
count_pclass = px.histogram(data, x="pclass", color="pclass", title="Passenger Class Count")
st.plotly_chart(count_pclass)

# Example for box plot of age by passenger class
st.subheader("Age Distribution by Passenger Class")
box_age_class = px.box(data, x="pclass", y="age", title="Age Distribution by Passenger Class")
st.plotly_chart(box_age_class)

# Example for pie chart of gender distribution
st.subheader("Gender Distribution")
gender_distribution = data["sex"].value_counts()
st.write(gender_distribution)

# Example for pie chart of survival distribution
st.subheader("Survival Distribution")
survival_distribution = data["survived"].value_counts()
st.write(survival_distribution)

# Interactive Feature 3: Filter Data by Age
min_age = int(data['age'].min())
max_age = int(data['age'].max())
selected_age = st.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Filter the data based on the selected age range
filtered_data_by_age = data[(data['age'] >= selected_age[0]) & (data['age'] <= selected_age[1])]

# Display the filtered data
st.subheader(f"Passengers Aged {selected_age[0]} to {selected_age[1]}")
st.write(filtered_data_by_age)

# Interactive Feature 4: Filter Data by Passenger Class
min_pclass = int(data['pclass'].min())
max_pclass = int(data['pclass'].max())
selected_pclass = st.slider("Select Passenger Class", min_pclass, max_pclass, (min_pclass, max_pclass))

# Filter the data based on the selected passenger class range
filtered_data_by_pclass = data[(data['pclass'] >= selected_pclass[0]) & (data['pclass'] <= selected_pclass[1])]

# Display the filtered data
st.subheader(f"Passengers in Class {selected_pclass[0]} to {selected_pclass[1]}")
st.write(filtered_data_by_pclass)



# Example for bar chart of average fare by passenger class
st.subheader("Average Fare by Passenger Class")
avg_fare_by_class = data.groupby("pclass")["fare"].mean().reset_index()
bar_avg_fare = px.bar(avg_fare_by_class, x="pclass", y="fare", title="Average Fare by Passenger Class")
st.plotly_chart(bar_avg_fare)
