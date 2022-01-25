#!/usr/bin/env python
# coding: utf-8

# Importing libraries
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import sqlalchemy
import os



#SQL Connection

import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-VBRKFH1\SQLEXPRESS;'
                      'Database=Bar;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
engine = sqlalchemy.create_engine("mssql+pyodbc://<username>:<password>@<dsnname>",pool_pre_ping=True)


#Folder to extract the data
analyze_folder = "D://Documentos//Data Science//Personal Projects//Jobcity Challenge//Data"


#Defining diferente functions to act over diferents dataframes

def df_transform(df): #Changin formats and adding new columns to the original dataframe.
    df["Origin_x"] = df.origin_coord.str.split(expand=True)[1].str.replace("(","").astype(float).round(0)
    df["Origin_y"] = df.origin_coord.str.split(expand=True)[2].str.replace(")","").astype(float).round(0)

    df["Destination_x"] = df.destination_coord.str.split(expand=True)[1].str.replace("(","").astype(float).round(0)
    df["Destination_y"] = df.destination_coord.str.split(expand=True)[2].str.replace(")","").astype(float).round(0)


    df['datetime'] = pd.to_datetime(df['datetime'])

    time_window = "30min"

    df["Time"] = df['datetime'].dt.round(time_window).dt.strftime('%H:%M')
    df["Week"] = df['datetime'].dt.isocalendar().week
    
    return df

def creating_tables (df): #Creating two new dataframes 

    df_grouped = df.groupby(["Origin_x","Origin_y","Destination_x","Destination_y","Time"]).agg({"region": "min","origin_coord": "min","destination_coord" : "min","datetime":"min"}).reset_index()
    df_grouped_2 = df.groupby(["Week","region"]).agg({"origin_coord":"count"}).sort_index().reset_index()
    
    return df_grouped, df_grouped_2

def  inserting_sql(df,df2,df3): #Saving the dataframes in the SQL server.
    
    df.to_sql('trips', con = engine,if_exists = 'append', index = False)
    df2.to_sql('trips_per_origin', con = engine ,if_exists = 'replace', index = False)
    df3.to_sql('avg_trips_week', con = engine ,if_exists = 'replace', index = False)
        


#Creating a loop to load everyfile in the folder to SQL. 

for file in os.listdir(analyze_folder):
    if file.split(".")[1] == "csv":    
        analytics_df = pd.read_csv(analyze_folder + "//" + file)
        analytics_df = df_transform(analytics_df)
        df_grouped, df_grouped_2 = creating_tables(analytics_df)
        inserting_sql(analytics_df,df_grouped,df_grouped_2)
        
        print ("File " + str(file) + " finished")
        
    elif file.split(".")[1] == "xlsx":    
        analytics_df = pd.read_excel(analyze_folder + "//" + file)
        analytics_df = df_transform(analytics_df)
        df_grouped, df_grouped_2 = creating_tables(analytics_df)
        inserting_sql(analytics_df,df_grouped,df_grouped_2)
        
        print ("file" + str(file) + "finished")

print ("Process Finished!")
    
        

        
        
        


# In[ ]:




