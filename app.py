
import streamlit as st
import numpy as np
import pandas as pd
import os

# Initialize grid
grid_size = 10
terrain = np.zeros((grid_size, grid_size))

# Options for x and y coordinates
options_x = ['Soil', 'Community', 'Wolves', 'Capital', 'Ritual', 'Safety', 'Transformation']
options_y = [
    'Environmental and Economic Impact of Coal Mining',
    'Community Engagement and Cultural Traditions',
    'Safety and Human Interaction Concerning Contamination',
    'Influence of Nature on Well-being',
    'Impact of Human Activities on Wildlife Regeneration',
    'Balancing Economic Decisions and Environmental Sustainability',
    'Cultural Reflection and Future Sustainability'
]

# Define a function for quadratic cost
def quadratic_cost(votes):
    return sum(v ** 2 for v in votes.values())

st.title('Terril Robotic Forming Voting System')

# User information
name = st.text_input('Name')
age = st.number_input('Age', min_value=0, max_value=120, step=1)

st.header('Voting in x-coordinate')
votes_x = {option: st.slider(f'Votes for {option}', 0, 7, 0, key=f"x_{option}") for option in options_x}
total_cost_x = quadratic_cost(votes_x)
st.write(f"Total cost for x-coordinate distribution: {total_cost_x} points")

st.header('Voting in y-coordinate')
votes_y = {option: st.slider(f'Votes for {option}', 0, 7, 0, key=f"y_{option}") for option in options_y}
total_cost_y = quadratic_cost(votes_y)
st.write(f"Total cost for y-coordinate distribution: {total_cost_y} points")

budget = 70
if total_cost_x > budget:
    st.write("The distribution for the x-coordinate exceeds the budget. Please adjust your votes.")
if total_cost_y > budget:
    st.write("The distribution for the y-coordinate exceeds the budget. Please adjust your votes.")

# Function to get the next available file number
def get_next_file_number(directory, base_filename):
    file_number = 1
    while os.path.exists(f"{directory}/{base_filename}{file_number}.csv"):
        file_number += 1
    return file_number

# Create directory for voting results if it doesn't exist
results_directory = 'voting_results'
os.makedirs(results_directory, exist_ok=True)

# Save the results if within budget
if st.button('Save') and total_cost_x <= budget and total_cost_y <= budget:
    x_votes = [votes_x[option] for option in options_x]
    y_votes = [votes_y[option] for option in options_y]

    # Normalize to grid
    max_height = 10
    for i in range(len(x_votes)):
        for j in range(len(y_votes)):
            terrain[i, j] = min(x_votes[i] + y_votes[j], max_height)

    # Prepare results for saving
    num_votes = len(options_x)
    results = {
        'Name': [name] * num_votes,
        'Age': [age] * num_votes,
        'x_option': options_x,
        'x_votes': x_votes,
        'y_option': options_y,
        'y_votes': y_votes
    }
    df = pd.DataFrame(results)

    # Determine the next file number
    base_filename = 'terrain'
    file_number = get_next_file_number(results_directory, base_filename)
    path = f"{results_directory}/{base_filename}{file_number}.csv"
    
    try:
        df.to_csv(path, index=False)
        st.write(f'The voting results have been saved at: {path}')
    except Exception as e:
        st.write(f'Error saving the file: {e}')
        st.write(f'Please check the path and permissions: {path}')

    # Verify that the file was saved
    if os.path.exists(path):
        st.write('File was saved successfully.')
    else:
        st.write('Error: File was not saved.')

# Function to calculate statistics from all voting result files
def calculate_statistics(directory):
    all_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    all_votes = pd.DataFrame()
    for file in all_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        all_votes = pd.concat([all_votes, df], ignore_index=True)

    if not all_votes.empty:
        statistics = all_votes.describe()
        st.write("Statistics of voting results:")
        st.write(statistics)
    else:
        st.write("No voting results found.")

# Add a button to calculate statistics
if st.button('Calculate Statistics'):
    calculate_statistics(results_directory)
