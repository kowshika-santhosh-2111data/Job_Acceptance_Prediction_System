import streamlit  as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")
st.title("Job Acceptance Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("job_acceptance_clean_Data.csv")
    return df
df = load_data()

with st.expander("Dataset Preview"):
    st.dataframe(df.head())

st.subheader("Dataset Overview")

total_candidates = len(df)
accepted_candidates = df[df['status'] == 'placed'].shape[0]
rejected_candidates = df[df['status'] == 'not placed'].shape[0]


col1, col2, col3 = st.columns(3)

col1.metric("Total", total_candidates) 
col2.metric("Accepted", accepted_candidates) 
col3.metric("Rejected", rejected_candidates) 

st.write("""This dataset contains information about job candidates, including their experience,
job title, and whether they were accepted or rejected for a position. 
The dataset can be used to analyze trends in job acceptance and rejection 
based on various factors such as experience and job title.""")

df['status'] = df['status'].astype(str).str.strip().str.lower()
st.write('status values:',df['status'].value_counts())
#total candiates
total_candidates = len(df['status'])
st.subheader("Total Candidates")
st.write(total_candidates)
#total candiates accepted
accepted_candidates = df[df['status'] == 'placed'].shape[0]
st.subheader("Total Candidates Accepted")
st.write(accepted_candidates)

#total candiates rejected
rejected_candidates = df[df['status'] == 'not placed'].shape[0]    
st.subheader("Total Candidates Rejected")
st.write(rejected_candidates)

#placement rate
placement_rate = (accepted_candidates / total_candidates) * 100
st.subheader("Placement Rate")
st.write(f"{placement_rate:.2f}%")

#job acceptance rate
job_acceptance_rate = df.groupby('job_role_match')['status'].apply(
lambda x: (x == 'placed').mean() * 100).reset_index(name='Acceptance_Rate').sort_values(by='Acceptance_Rate', ascending=False)
st.subheader("Job Acceptance Rate")
st.dataframe(job_acceptance_rate)

#average interview score
average_interview_score= df.groupby('degree_specialization')[
    'technical_score',
    'aptitude_score',
    'communication_score'
].mean().reset_index()
st.subheader("Average Interview Score by degree specalization")
st.dataframe(average_interview_score)

#average skills match %
average_skills_match = df.groupby('degree_specialization')['skills_match_percentage'].mean().reset_index(name='Average_Skills_Match').sort_values(by='Average_Skills_Match', ascending=False)
st.subheader("Average Skills Match Percentage by degree specialization")
st.dataframe(average_skills_match)

df['status'] = df['status'].str.lower().str.strip()

#offer dropout rate
offer_dropout_rate = df.groupby('degree_specialization')['status'].apply(
    lambda x: (x == 'not placed').mean() * 100
    ).reset_index(name='Offer_Dropout_Rate').sort_values(by='Offer_Dropout_Rate', ascending=False)
st.subheader("Offer Dropout Rate by degree specialization")
st.dataframe(offer_dropout_rate)

#high risk candidates percentage
high_risk_candidates_percentage = df.groupby('degree_specialization').apply(
    lambda x: (x[x['years_of_experience'] < 2]
               ['status'] == 'not placed').mean() * 100
).reset_index(name='High_Risk_Candidates_Percentage')
st.subheader("High risk candidates percentage")
st.dataframe(high_risk_candidates_percentage)
