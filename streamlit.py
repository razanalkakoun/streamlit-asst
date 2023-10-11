import pandas as pd
import numpy as np 
import streamlit as st
import plotly.express as px


st.title("Titanic Visualization using Streamlit")

#description of the dataset
st.write("The dataset selected pertains to the passengers aboard the RMS titanic during its ill-fated voyage in 1912" 
         "This dataset encompasses comprehensive information about the passengers, including their ticket class, gender, age, familial connections, ticket number, cabin details, passenger fare, and the port of embarkation"
         " Moreover, it includes a binary indicator of survival, where 0 signifies 'did not survive' and 1 signifies 'survived.'"
         "I am really interested in investigating the influence of these gathered inputs on passenger survival.") 


def load_data(nrows): 
    data = pd.read_csv("train.csv", nrows=nrows)  #we read the specifed number of rows from this CSV file 
    lowercase = lambda x: str(x).lower() #then we convert names to lowercase; it takes x as an input and converts it to str(x), and the applies ;lower()
    data.rename(lowercase, axis='columns', inplace=True) #this means that the lambda function "lwecasr" will be applied to each column of the dataframe 
    return data


# Set the app title and description
st.title("Titanic Data Visualization")
st.write("Explore the Titanic dataset and visualize passenger information.")



st.write("By clicking on the checkbox, you can view the raw data")

show_data = st.checkbox("Show Row Data")

#load the data
data = load_data(10000)

data_load_state = st.text('Loading data...')

#display data if checkbox is clicked
if show_data:
    st.subheader("Data")
    st.write(data)



#interactive feature to filter the data by ticket class: 
ticket_class_options = data['pclass'].unique()
selected_class = st.selectbox("Filter by Ticket Class", ticket_class_options)
st.subheader(f"Passengers in Ticket Class {selected_class}")
filtered_data = data[data['pclass'] == selected_class]
st.write(filtered_data)

st.write("You can see the passenger in ticket class that you choose.")
st.write("Now, I am interested in investigating whether there is any direct relation between the people who survived and their ticket class.")

st.subheader("Survival Rate by Ticket Class- visualization ")
# Group data by ticket class and calculate the survival rate
survival_rate_data = data.groupby('pclass')['survived'].mean().reset_index()

# Create a bar chart to visualize the survival rate by ticket class
fig = px.bar(survival_rate_data, x='pclass', y='survived', title="Survival Rate by Ticket Class - visualization # 2")
fig.update_traces(marker_color='teal')
st.plotly_chart(fig)


# Calculate the survival rates for each ticket class
survival_rate_data = data.groupby('pclass')['survived'].mean().reset_index()

# Create a pie chart to visualize the survival rate by ticket class
fig = px.pie(survival_rate_data, names='pclass', values='survived', title="Survival Rate by Ticket Class - visualization # 2")
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig)

st.write("We can observe from both visualizations, the bar chart and the pie chart, that the largest proportion of survivors, constituting 46.8%, belongs to Ticket Class 1.")
st.write("Ticket Class 1 represents the most expensive tickets, suggesting a possible correlation between higher socioeconomic status and priority during the rescue process." 
         "As an analyst, we can probably infer that individuals with premium tickets might have received preferential treatment during the rescue process of the Titanic.")


# # Create a bar chart to investigate the correlation between age, ticket class, and survival
# st.subheader("Correlation between Age, Ticket Class, and Survival")

# # Add age slider
# selected_age = st.slider("Select Maximum Age", min_value=data['age'].min(), max_value=data['age'].max())

# # Create a bar chart with age, survival status, and ticket class
# filtered_data = data[data['age'] <= selected_age]

# fig_bar = px.bar(filtered_data, x='survived', y='pclass', title="Correlation between Age, Ticket Class, and Survival")
# fig_bar.update_xaxes(title_text="Survival (0 = No, 1 = Yes)")
# fig_bar.update_yaxes(title_text="Ticket Class")
# st.plotly_chart(fig_bar)


# # Create a bar chart to show the count of survivors for each age group
# st.subheader("Count of Survivors by Age Group")

# # Define the age group boundaries
# age_groups = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

# # Create age group labels for the X-axis
# age_group_labels = [f"{age}-{age+9}" for age in age_groups[:-1]]

# # Count survivors in each age group
# survivors_count = []
# for i in range(len(age_groups) - 1):
#     lower_bound = age_groups[i]
#     upper_bound = age_groups[i + 1]
#     count = len(data[(data['age'] >= lower_bound) & (data['age'] <= upper_bound) & (data['survived'] == 1)])
#     survivors_count.append(count)

# # Create a bar chart to display the count of survivors for each age group
# fig_bar = px.bar(x=age_group_labels, y=survivors_count, title="Count of Survivors by Age Group")
# fig_bar.update_xaxes(title_text="Age Group")
# fig_bar.update_yaxes(title_text="Survivor Count")
# st.plotly_chart(fig_bar)


# Create a bar chart to show the count of survivors for each age group
st.subheader("Count of Survivors by Age Group and Port of Embarkation")

# Define the age group boundaries
age_groups = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

# Create age group labels for the X-axis
age_group_labels = [f"{age}-{age+9}" for age in age_groups[:-1]]

# Define the port of embarkation options
embarked_options = ["C", "Q", "S", "All"]

# Create checkboxes to allow users to select ports
selected_ports = st.multiselect("Select Ports of Embarkation", embarked_options, ["C", "Q", "S"])

# Count survivors in each age group and for selected ports
survivors_count = []
for i in range(len(age_groups) - 1):
    lower_bound = age_groups[i]
    upper_bound = age_groups[i + 1]
    count = len(data[(data['age'] >= lower_bound) & (data['age'] <= upper_bound) & (data['survived'] == 1) &
                     (data['embarked'].isin(selected_ports))])
    survivors_count.append(count)

# Create a bar chart to display the count of survivors for each age group and selected ports
fig_bar = px.bar(x=age_group_labels, y=survivors_count, title="Count of Survivors by Age Group and Port of Embarkation")
fig_bar.update_xaxes(title_text="Age Group")
fig_bar.update_yaxes(title_text="Survivor Count")
st.plotly_chart(fig_bar)

st.write("In this visualization, we've introduced a filter that allows you to select the port of embarkation: C (Cherbourg), Q (Queenstown), and S (Southampton). You can add or remove these ports to explore the age groups of people who survived. Upon examining the data for all three ports, a notable observation emerges. The majority of survivors fall within the age group of 20 to 39, accounting for almost 150 individuals who survived. We can also notice that the elderly was coming from Southampton port. ")



# Create a stacked bar chart to show survival by gender and ticket class
st.subheader("Survival by Gender and Ticket Class")

fig_stacked_bar = px.bar(data, x='pclass', y='survived', color='sex', labels={'pclass': 'Ticket Class'},
                        title="Survival by Gender and Ticket Class",
                        category_orders={'pclass': [1, 2, 3]},
                        color_discrete_map={'Male': 'darkblue', 'Female': 'pink'})

fig_stacked_bar.update_xaxes(title_text="Ticket Class")
fig_stacked_bar.update_yaxes(title_text="Count")
st.plotly_chart(fig_stacked_bar)

st.write("In this representation, the ticket classes (1st, 2nd, and 3rd) are visualized on the X-axis, and the count of survivors is depicted on the Y-axis. Moreover, the color-coded filter distinguishes passengers by gender (Male and Female). Notably, the majority of survivors are male. This observation raises intriguing questions about the role of physical strength and its potential impact on passenger survival.")


# import seaborn as sns
# import matplotlib.pyplot as plt

# # Create a correlation matrix
# st.subheader("Correlation Matrix")

# # Select numerical features for the correlation matrix
# numerical_features = data[['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']]

# # Compute the correlation matrix
# correlation_matrix = numerical_features.corr()

# # Create a heatmap to visualize the correlations
# plt.figure(figsize=(10, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5)
# st.pyplot()
