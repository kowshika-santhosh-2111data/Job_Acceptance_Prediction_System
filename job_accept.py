import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import joblib
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv("HR_Job_Placement_Dataset.csv")
data.head()
data.columns
data.shape
data.info()
data.isnull().sum()
data.describe()
(data.isnull().sum()/len(data))*100
data.duplicated().sum()
data[data.duplicated()]
data = data.drop_duplicates()
#duplicated checks
print(data.duplicated().sum())
print("-----------------------")
#identify dupilcated rows
data[data.duplicated()].head()

data.dtypes
cat_col = data.select_dtypes(include=['object','category']).columns
cat_col
num_col = data.select_dtypes(include=['float64','int64']).columns
num_col
#check invalid categories logical inconsistency
#numerical invalid
#age
data[(data['age_years'] < 18) | (data['age_years']> 60)]

#percentage
data[(data['ssc_percentage'] < 0) |(data['ssc_percentage']> 100)]
data[(data['hsc_percentage'] < 0)|(data['hsc_percentage'] > 100)]
data[(data['degree_percentage'] < 0)|(data['degree_percentage']> 100)]

#scores
data[(data['technical_score'] < 0)|(data['technical_score'] > 100)]
data[(data['aptitude_score'] < 0)|(data['aptitude_score'] > 100)]
data[(data['communication_score'] < 0)|(data['communication_score'] > 100)]
data[(data['skills_match_percentage'] < 0)|(data['skills_match_percentage'] > 100)]

#counts
data[(data['certifications_count'] < 0)]

#experience
data[(data['years_of_experience'] < 0)|(data['years_of_experience']>40)]

#salary details & discuss
data[(data['previous_ctc_lpa'] < 0)]
data[(data['expected_ctc_lpa'] < 0)]

#notice period
data[(data['notice_period_days'] < 0)|(data['notice_period_days']>365)]

#employment gap details
data[(data['employment_gap_months'] < 0)|(data['employment_gap_months']>120)]

cat_col = ['gender', 'degree_specialization', 'internship_experience',
       'career_switch_willingness', 'relevant_experience', 'company_tier',
       'job_role_match', 'competition_level', 'bond_requirement',
       'layoff_history', 'relocation_willingness', 'status']
#clean spaces & convert into lower case
for col in cat_col:
    print(f"\n{col}")
    print(data[col].astype(str).str.strip().value_counts(dropna=False))
    #categorical invalid - predefined
valid_values = {
    'gender' : ['male','female','nan'],
    'degree_specialization' : ['computer science', 'electronics', 'information technology','mechanical', 'others','nan'],
    'internship_experience' : ['yes','no','nan'],
    'career_switch_willingness' : ['yes','no','nan'],
    'relevant_experience' : ['relevant','not relevant','nan'],
    'company_tier' : ['tier 1', 'tier 2', 'tier 3','nan'],
    'job_role_match' : ['not matched', 'matched','nan'],
    'competition_level' : ['low','medium', 'high'],
    'bond_requirement' : ['not required', 'required'],
    'layoff_history' : ['yes', 'no','nan'],
    'relocation_willingness' : ['willing', 'not willing','nan'],
    'status': ['not placed', 'placed']
            }
#clean +lowercase
for col in cat_col:
    data[col] = data[col].astype(str).str.strip().str.lower()
    
#standardize the categorical
for col, valid in valid_values.items():
    data[col] = data[col].replace({v.lower(): v for v in valid})

#check invalid categories
for col, valid in valid_values.items():
    print(f"\nInvalid values in {col}:")
    print(data[~data[col].isin(valid) & data[col].notna()][col].value_counts())
data.describe()
#handling missing values
#numnerical
data['ssc_percentage'].fillna(data['ssc_percentage'].median(),inplace = True)
data['hsc_percentage'].fillna(data['hsc_percentage'].median(),inplace = True)
data['notice_period_days'].fillna(0, inplace=True)
data['employment_gap_months'].fillna(0, inplace=True)
#categorical
for col in cat_col:
    data[col].fillna(data[col].mode()[0], inplace=True)
data[num_col].skew()
#OUTLIER HANDLING
outlier_cols = [
    'employment_gap_months',
    'notice_period_days',
    'certifications_count',
    'years_of_experience'
]
for col in outlier_cols:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    data[col] = np.where(data[col] > upper, upper, data[col])
    data[col] = np.where(data[col] < lower, lower, data[col])

    print(f"{col} → {len(outlier_cols)} outliers ({len(outlier_cols)/len(data)*100:.2f}%)")
    
print('Final_Missing_Values:\n',data.isnull().sum())
print('\n Final_shape:',data.shape)
clean_data = data.to_csv('job_acceptance_clean_Data.csv',index = False)
dataa = pd.read_csv("job_acceptance_clean_Data.csv")
dataa.head()
#Data visualization
#Interview score vs job acceptance
sns.boxplot(x='status', y='communication_score', data=dataa)
plt.title("Interview Score vs Job Acceptance")
plt.show()

#Skills match percentage impact on placement
sns.boxplot(x='status', y='skills_match_percentage', data=dataa)
plt.title("Skills Match vs Job Acceptance")
plt.show()

#Company tier vs acceptance rate
sns.countplot(x='company_tier', hue='status', data=dataa)
plt.title("Company Tier vs Job Acceptance")
plt.show()

#Competition level vs job acceptance
sns.countplot(x='competition_level', hue='status', data=dataa)
plt.title("Competition Level vs Job Acceptance")
plt.show()

#HEATMAP CORRELATION
plt.figure(figsize=(10,12))
sns.heatmap(dataa[num_col].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

#FEATURE ENGINEERING
dataa['experience_level'] = dataa['years_of_experience'].apply(lambda x:'fresher' if x== 0 else('junior' if x<=3 else 'senior'))
dataa['academic_performance'] = dataa['degree_percentage'].apply(lambda x:'low' if x<60 else('medium' if x<75 else 'high'))
dataa['skills_level'] = dataa['skills_match_percentage'].apply(lambda x:'low' if x < 40 else ('medium' if x<70 else'high'))
dataa['interview_score'] = (dataa['technical_score'] +dataa['aptitude_score']+ dataa['communication_score'])/3
dataa['interview_category'] = dataa['interview_score'].apply(lambda x:'poor' if x < 50 else ('average' if x< 70 else 'good'))
dataa['placement_score'] = (0.25 *dataa['skills_match_percentage'] +
                            0.25 * dataa['technical_score'] +
                            0.25 * dataa['aptitude_score'] +
                            0.25 * dataa['communication_score'])
dataa['avg_score'] = ((dataa['technical_score'] + dataa['aptitude_score'] + dataa['communication_score']) / 3)
dataa['gap_category'] = dataa['employment_gap_months'].apply(lambda x: 'no gap' if x == 0 else 'has gap')

#ENCODING
dataa = pd.get_dummies(dataa, columns=['gender', 'degree_specialization', 'internship_experience',
       'career_switch_willingness', 'relevant_experience', 'company_tier',
       'job_role_match', 'competition_level', 'bond_requirement',
       'layoff_history', 'relocation_willingness','experience_level', 'academic_performance', 'skills_level',
       'interview_category', 'gap_category'], drop_first=True)

dataa['status'].isnull().sum()
#Supervised Machine Learning (Classification)
y = dataa['status']
x = dataa.drop('status', axis=1)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000,class_weight='balanced'))
])

scaler = StandardScaler()
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42)

x_train[num_col] = scaler.fit_transform(x_train[num_col])
x_test[num_col] = scaler.transform(x_test[num_col])



pipeline.fit(x_train,y_train)

y_prob = pipeline.predict_proba(x_test)[:,1]
y_pred = (y_prob > 0.45).astype(int)

#prediction
y_pred = pipeline.predict(x_test)

#evaluation
print("Logistic Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(x_train, y_train)

y_pred_rf = rf.predict(x_test)

print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=42)
dt.fit(x_train, y_train)

y_pred_dt = dt.predict(x_test)

print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred_dt))

#Academic scores vs placement outcome
sns.boxplot(x = 'status',y = 'degree_percentage',data = dataa)
plt.title('Academic score vs job acceptance')
plt.show()

#skills maatch vs interview performance
sns.scatterplot(x='skills_match_percentage', y='technical_score', hue='status', data=dataa)
plt.title("Skills Match vs Technical Score")
plt.show()

#Certification Impact on Job Acceptance
sns.boxplot(x='status', y='certifications_count', data=dataa)
plt.title("Certifications vs Job Acceptance")
plt.show()

#Interview Score vs Placement Probability
sns.boxplot(x='status', y='avg_score', data=dataa)
plt.title("Interview Score vs Job Acceptance")
plt.show()

#Employability Test vs Technical Score
sns.scatterplot(x='aptitude_score', y='technical_score', hue='status', data=dataa)
plt.title("Aptitude vs Technical Score")
plt.show()

#save model
model_col = x.columns
joblib.dump(num_col,'num_columns.pkl')
joblib.dump(scaler,'scaler.pkl')
joblib.dump(pipeline,'model.pkl')
joblib.dump(x_train.columns, 'columns.pkl')
