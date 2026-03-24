import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pprint import pprint
from sqlalchemy import select,func,and_,desc,case,text
from streamlit.elements.widgets.time_widgets import _DATETIME_UI_FORMAT

password = quote_plus("Kowshika*1999")

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:{password}@localhost/job_acceptance_clean_Data",echo = True)
Connection = engine.connect()
metadata = sqlalchemy.MetaData()
job_data = sqlalchemy.Table(
    'job_data',
    metadata,
    autoload_with=engine)  

#total candiates
q1 = (
    select(job_data.c.status).label('Total_Candidates')
    .group_by(job_data.c.status)
    .order_by(desc('total_Candidates'))
)  
df_total_candidates = pd.read_sql(q1, engine)
print("Total Candidates:")
print(df_total_candidates)

#total candiates accepted
q2 = (
    select(
        case(
            [(job_data.c.status == 1, 'placed')],
            else_='not placed'
        ).label('status')
    )
    .group_by(job_data.c.status)
    .order_by(desc('status'))
)
df_accepted_candidates = pd.read_sql(q2, engine)    
print("Total Candidates Accepted:")
print(df_accepted_candidates)

#total candiates rejected
q3 = (
    select( 
        case(
            [(job_data.c.status == 0, 'not placed')],
            else_='placed'
        ).label(job_data.c.status)
    )
    .group_by(job_data.c.status)
    .order_by(desc('status'))
)
df_rejected_candidates = pd.read_sql(q3, engine)    
print("Total Candidates Rejected:")
print(df_rejected_candidates)

#placement rate
q4 = (
    select(
        func.count().label('Total_Candidates'),
        func.sum(case([(job_data.c.status == 1, 1)], else_=0)).label('Accepted_Candidates'),
        (func.sum(case([(job_data.c.status == 1, 1)], else_=0)) / func.count() * 100).label('Placement_Rate')
    )
)
df_placement_rate = pd.read_sql(q4, engine)
print("Placement Rate:")
print(df_placement_rate)

#job acceptance rate
q5 = (
    select(
        job_data.c.degree_specialization,
        func.count().label('Total_Candidates'),
        func.sum(case([(job_data.c.status == 1, 1)], else_=0)).label('Accepted_Candidates'),
        (func.sum(case([(job_data.c.status == 1, 1)], else_=0)) / func.count() * 100).label('Acceptance_Rate')
    )
    .group_by(job_data.c.degree_specialization)
    .order_by(desc('Acceptance_Rate'))
)      
df_acceptance_rate = pd.read_sql(q5, engine)
print("Job Acceptance Rate:")
print(df_acceptance_rate)

#average interview score
q6 = (
    select(
        job_data.c.degree_specialization,
        func.avg(job_data.c.technical_score).label('avg_technical_score'),
        func.avg(job_data.c.aptitude_score).label('avg_aptitude_score'),
        func.avg(job_data.c.communication_score).label('avg_communication_score')
    )
    .group_by(job_data.c.degree_specialization)
)
average_interview_score = pd.read_sql(q6, engine)
print("Average Interview Score by Job Title:")
print(average_interview_score)

#average skills match %
q7 = (
    select(
        job_data.c.degree_specialization,
        func.avg(job_data.c.skills_match_percentage).label('Average_Skills_Match_Percentage')
    )
    .group_by(job_data.c.degree_specialization)
    .order_by(desc('Average_Skills_Match_Percentage'))
)
df_average_skills_match = pd.read_sql(q7, engine)
print("Average Skills Match Percentage by Job Title:")
print(df_average_skills_match)

#offer dropout rate
q8 = (
    select(
        job_data.c.degree_specialization,
        func.count().label('Total_Candidates'),
        func.sum(case([(job_data.c.status == 1, 1)], else_=0)).label('Accepted_Candidates'),
        (func.sum(case([(job_data.c.status == 1, 1)], else_=0)) / func.count() * 100).label('Offer_Dropout_Rate')
    )
    .group_by(job_data.c.degree_specialization)
    .order_by(desc('Offer_Dropout_Rate'))
)
df_offer_dropout_rate = pd.read_sql(q8, engine)
print("Offer Dropout Rate by Job Title:")
print(df_offer_dropout_rate)

#high risk candidates percentage
q9 = (
    select(
        job_data.c.degree_specialization,
        func.count().label('Total_Candidates'),
        func.sum(case([(job_data.c.status == 1, 1)], else_=0)).label('Accepted_Candidates'),
        (func.sum(case([(job_data.c.status == 1, 1)], else_=0)) / func.count() * 100).label('High_Risk_Candidates_Percentage')
    )
    .group_by(job_data.c.degree_specialization)
    .order_by(desc('High_Risk_Candidates_Percentage'))
)
df_high_risk_candidates = pd.read_sql(q9, engine)
print("High Risk Candidates Percentage by Job Title:")
print(df_high_risk_candidates)