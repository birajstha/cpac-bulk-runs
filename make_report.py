import os
import pandas as pd
import re

def list_subjects_sessions(root_dir):
    subjects_sessions = []
    for subject_name in sorted(os.listdir(root_dir)):  # Sort subject names
        subject_path = os.path.join(root_dir, subject_name)
        if os.path.isdir(subject_path):
            sessions = sorted([session_name for session_name in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, session_name))])
            subjects_sessions.append({'Subject': subject_name, 'Sessions': sessions, 'Completed': []})
    return subjects_sessions

def mark_completed(df, subject, session):
    for index, row in df.iterrows():
        if row['Subject'] == subject:
            sessions = row['Sessions']
            if session in sessions:
                #print(subject, session)
                if session not in df.at[index, 'Completed']:
                    df.at[index, 'Completed'].append(session)
                break
    return df

def search_and_mark(root_dir, df):
    for filename in os.listdir(root_dir):
        if filename.startswith("slurm") and filename.endswith(".out"):
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if "CPAC run complete:" in line:
                        line = lines[i+3]
                        temp = line.split("_")
                        subject = temp[-2]
                        session = temp[-1].strip()
                        print(f"Subject: {subject}, Session: {session}")
                        df = mark_completed(df, subject, session)
                        continue
    return df


# Define the directories
raw_data_directory = "/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw"  
output_directory = "/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/ANTS_FSL_noBBR_strict"

# Name your output csv file
output_csv = "remaining.csv"


data = list_subjects_sessions(raw_data_directory)
df = pd.DataFrame(data)

# Sort DataFrame by subjects in ascending order
df = df.sort_values(by='Subject')

import multiprocessing as mp
with mp.Pool() as pool:
    # Use pool.starmap to pass multiple arguments to the function
    # This will run search_and_mark in parallel for each item in the iterable
    results = pool.starmap(search_and_mark, [(output_directory, df)])

# The result will be a list of modified DataFrames
modified_df = results[0]  # Assuming only one result is returned

print(type(modified_df))

# add another column to the dataframe as remaining and it will be the sessions- completed
# Define a function to subtract lists element-wise
def subtract_lists(sessions, completed):
    return [item for item in sessions if item not in completed]

# Apply the function to each row
modified_df['Remaining'] = modified_df.apply(lambda row: subtract_lists(row['Sessions'], row['Completed']), axis=1)


# Save DataFrame to CSV file preserving the ascending order
modified_df.to_csv(output_csv, index=False)  # Index set to False to exclude index column
print(f"DataFrame saved to {output_csv}")

