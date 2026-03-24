import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus

password = quote_plus("Kowshika*1999")

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:{password}@localhost/job_acceptance",
    echo = True)

def main():
    #Load csv file
    df = pd.read_csv(r"C:\Users\Kowsh\OneDrive\Desktop\vscode_project\Job_acceptance\job_acceptance_clean_Data.csv") 
    print(df.head())
    print(df.info())
    print(df.shape)
    #insert into sql
    df.to_sql(
        name = "job_data",
        con = engine,
        if_exists = "replace",
        index = False
    )
    
    print("Data inserted into Mysql successfully")

if __name__ == "__main__":
    main()