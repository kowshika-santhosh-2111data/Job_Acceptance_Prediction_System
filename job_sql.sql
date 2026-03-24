create database job_acceptance;
use job_acceptance;
create table job_data (
    age_years INT,
    gender VARCHAR(10),
    ssc_percentage FLOAT,
    hsc_percentage FLOAT,
    degree_percentage FLOAT,
    degree_specialization VARCHAR(50),
    technical_score FLOAT,
    aptitude_score FLOAT,
    communication_score FLOAT,
    skills_match_percentage FLOAT,
    certifications_count INT,
    internship_experience VARCHAR(10),
    years_of_experience INT,
    career_switch_willingness VARCHAR(10),
    relevant_experience VARCHAR(10),
    previous_ctc_lpa FLOAT,
    expected_ctc_lpa FLOAT,
    company_tier VARCHAR(20),
    job_role_match VARCHAR(20),
    competition_level VARCHAR(20),
    bond_requirement VARCHAR(20),
    notice_period_days INT,
    layoff_history VARCHAR(10),
    employment_gap_months INT,
    relocation_willingness VARCHAR(10),
    status VARCHAR(20)
);

show tables;
describe job_data;
select * from job_data;

#acceptance rate by compay tier
select  company_tier,
		count(*) as total_candidates,
        sum(case when status = 'placed' then 1 else 0 end) as accepted,
        round(
			sum(case when status = 'placed' then 1 else 0 end) *100.0/2) as acceptance_rate
from job_data
group by company_tier;


select  status,
		count(*) as total_candidates,
        sum(case when status = 'placed' then 1 else 0 end) as accepted
from job_data
group by status;

#academic scores vs placement
select status, 
avg(degree_percentage) as avg_degree_score
from job_data
group by status;

#skills match vs placement
select status,
 avg(skills_match_percentage) as avg_skills_match
 from job_data
 group by status;
 
 #Certifications Impact
 Select status,
avg(certifications_count) as avg_certifications
from job_data
group by status;

#experience vs placement
select status,
avg(years_of_experience) as avg_experience
from job_data
group by status;

#Interview Score vs Placement
select status,
avg(
	(technical_score + aptitude_score + communication_score)/3
    ) as avg_interview_score
from job_data
group by status;

#Competition Level vs Acceptance
select competition_level,
count(*) as total,
sum(case when status = 'placed' THEN 1 ELSE 0 END) AS accepted
from job_data
group by competition_level;

#Experience Category Analysis
select 
    case 
        when years_of_experience = 0 then 'Fresher'
        when years_of_experience <= 3 then 'Junior'
        else 'Senior'
    end as experience_level,
    count(*) as total,
    sum(case when status = 'placed' then 1 else 0 end) as accepted
from job_data
group by experience_level;