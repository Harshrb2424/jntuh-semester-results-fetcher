import pandas as pd
from sqlalchemy import create_engine

# Read the CSV file
df = pd.read_csv('D:/Github/jntuh-semester-results-fetcher/results/subject_details.csv')

# Create a SQLAlchemy engine
engine = create_engine('mysql+pymysql://username:password@localhost/db')

# Write the DataFrame to MySQL
df.to_sql('subjects', con=engine, if_exists='replace', index=False)

# Read the CSV file
df = pd.read_csv('D:/Github/jntuh-semester-results-fetcher/results/personal_info.csv')

# Create a SQLAlchemy engine
engine = create_engine('mysql+pymysql://username:password@localhost/db')

# Write the DataFrame to MySQL
df.to_sql('students', con=engine, if_exists='replace', index=False)
