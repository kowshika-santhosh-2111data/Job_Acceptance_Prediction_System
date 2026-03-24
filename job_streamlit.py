import streamlit  as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
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

st.write("This dataset contains information about job candidates, including their experience, job title, and whether they were accepted or rejected for a position. The dataset can be used to analyze trends in job acceptance and rejection based on various factors such as experience and job title.")

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
job_acceptance_rate = df.groupby('job_role_match')['status'].apply(lambda x: (x == 'placed').mean() * 100).reset_index(name='Acceptance_Rate').sort_values(by='Acceptance_Rate', ascending=False)
st.subheader("Job Acceptance Rate")
st.dataframe(job_acceptance_rate)

#average interview score
average_interview_score= df.groupby('degree_specialization')[[
    'technical_score',
    'aptitude_score',
    'communication_score'
]].mean().reset_index()
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

scaler = joblib.load('scaler.pkl')
model = joblib.load('model.pkl')

st.subheader('enter candidate details')

age = st.number_input('age', 18,60)
experience = st.number_input('Years of Experience', 0, 40)
technical = st.slider('Technical Score', 0, 100)
aptitude = st.slider('Aptitude Score', 0, 100)
communication = st.slider('Communication Score', 0, 100)
certifications_count = st.number_input('certifications',0,10)
hsc_pct = st.slider('HSC %',0,100)
ssc_pct = st.slider('SSC %',0,100)
degree_pct = st.slider('degree %',0,100)
expected_ctc = st.number_input('expected ctc',1.0,30.0)
gap = st.number_input('employment gap months',0)

degree = st.selectbox('degree_specialization',['computer science','electronics','information technology','mechanical','others'])
job_match = st.selectbox('job_role_match',['matched','not matched'])
company = st.selectbox('company_tier',['tier 1','tier 2','tier 3'])


columns = joblib.load('columns.pkl')
num_cols= joblib.load('num_columns.pkl')

# Create empty dataframe with ALL 41 columns
input_df = pd.DataFrame(0,index= [0],columns=columns)


input_df[num_cols] = scaler.transform(input_df[num_cols])


# Fill only known values
input_df.loc[0, 'age_years'] = age
input_df.loc[0, 'years_of_experience'] = experience
input_df.loc[0, 'technical_score'] = technical
input_df.loc[0, 'aptitude_score'] = aptitude
input_df.loc[0, 'communication_score'] = communication
input_df.loc[0,'certifications_count'] = certifications_count
input_df.loc[0,'degree_percentage'] = degree_pct
input_df.loc[0,'hsc_percentage'] = hsc_pct

input_df.loc[0,'ssc_percentage'] = ssc_pct
input_df.loc[0,'expected_ctc_lpa'] = expected_ctc
input_df.loc[0,'employment_gap_months'] = gap


col1 = f"degree_specialization_{degree}"
if col1 in input_df.columns:
    input_df.loc[0,col1] = 1

col2 = f"job_role_match_{job_match}"
if col2 in input_df.columns:
    input_df.loc[0,col2] = 1

col3= f"company_tier_{company}"
if col3 in input_df.columns:
    input_df.loc[0,col3] = 1


# Fill remaining columns with 0
input_df = input_df.fillna(0)


prediction = model.predict(input_df)


if st.button('Predict'):
    if input_df is not None:
        prediction = model.predict(input_df)
        prob = model.predict_proba(input_df)[0][1]

        st.write(f'Placement Probability:  {prob * 100:.2f}%')


        if prob > 0.5:
            st.success('candidate will  placed')       
        else:
            st.error('candidate will not placed')
