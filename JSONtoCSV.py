import pandas as pd
import json

def load_csv_to_dataframe(filename):
    """Load a CSV file into a DataFrame."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        # If file doesn't exist, return an empty DataFrame with expected columns
        return pd.DataFrame(columns=[
            'HTNO', 'subject_code', 'subject_name', 'internal', 'external', 'total', 'grade', 'credits'
        ]) if 'subject' in filename else pd.DataFrame(columns=[
            'HTNO', 'NAME', 'FATHER NAME', 'COLLEGE CODE', 'sem'
        ])

def load_json_to_dataframe(filename):
    """Load JSON data into DataFrames."""
    with open(filename, 'r') as file:
        data = json.load(file)

    personal_info_list = []
    subject_details_list = []

    for entry in data:
        personal_info = entry['personal_info']
        subjects = entry['subject_details']

        personal_info_list.append({
            'HTNO': personal_info['HTNO'],
            'NAME': personal_info['NAME'],
            'FATHER NAME': personal_info['FATHER NAME'],
            'COLLEGE CODE': personal_info['COLLEGE CODE'],
            'sem': personal_info['sem']
        })

        for subject in subjects:
            subject_details_list.append({
                'HTNO': personal_info['HTNO'],
                'subject_code': subject['subject_code'],
                'subject_name': subject['subject_name'],
                'internal': subject['internal'],
                'external': subject['external'],
                'total': subject['total'],
                'grade': subject['grade'],
                'credits': subject['credits']
            })

    df_personal_info = pd.DataFrame(personal_info_list)
    df_subject_details = pd.DataFrame(subject_details_list)

    return df_personal_info, df_subject_details

def append_new_data(existing_df, new_df, key_columns):
    """Append only new unique rows from new_df to existing_df."""
    existing_keys = existing_df[key_columns].drop_duplicates()
    new_keys = new_df[key_columns].drop_duplicates()
    
    # Merge to find only new unique rows
    new_data = pd.merge(new_keys, existing_keys, on=key_columns, how='left', indicator=True)
    new_data = new_data[new_data['_merge'] == 'left_only'].drop('_merge', axis=1)
    
    # Merge new_data with new_df to get full details of new rows
    result_df = pd.merge(new_df, new_data, on=key_columns, how='inner')
    updated_df = pd.concat([existing_df, result_df]).drop_duplicates().reset_index(drop=True)
    
    return updated_df

# File paths
personal_info_file = 'results/personal_info.csv'
subject_details_file = 'results/subject_details.csv'
new_json_file = 'results/Q9_66_1-1_data.json'

# Load existing CSV data
existing_personal_info_df = load_csv_to_dataframe(personal_info_file)
existing_subject_details_df = load_csv_to_dataframe(subject_details_file)

# Load new JSON data
new_personal_info_df, new_subject_details_df = load_json_to_dataframe(new_json_file)

# Append only new data
updated_personal_info_df = append_new_data(existing_personal_info_df, new_personal_info_df, ['HTNO'])
updated_subject_details_df = append_new_data(existing_subject_details_df, new_subject_details_df, ['HTNO', 'subject_code'])

# Save updated data back to CSV
updated_personal_info_df.to_csv(personal_info_file, index=False)
updated_subject_details_df.to_csv(subject_details_file, index=False)

print('CSV files have been updated with new distinct data.')
