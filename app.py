import pandas as pd
import plotly.express as px

# Load the CSV file
# file_path = '/Users/simon/Desktop/Builds/Dashboard/race_20240103_042233.csv'
file_path = '/Users/simon/Desktop/Builds/Dashboard/final.csv'

data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
print(data.head())

# Convert the 'Time' column to a datetime format if it's not already
# Assuming 'Time' is the name of your time column and it's in a recognizable time format
data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S.%f', errors='ignore')
print(data.head())
# Selecting a parameter to plot against time. Replace 'Parameter1' with the actual column name.
# For demonstration, I'll choose the second column ('0.93' from the first row) as it's numeric.

parameter_to_plot = data.columns[3]

# Creating the plot
fig = px.line(data, x='Time', y=parameter_to_plot, title=f'Time vs. {parameter_to_plot}')
# fig = px.line(data, x='Time', y=parameter_to_plot, title=f'Time vs. {parameter_to_plot}')


# Showing the plot
fig.show()
