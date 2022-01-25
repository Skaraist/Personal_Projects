Jobcity Project

Requests:

- Trips with similar origin, destination, and time of day should be grouped together. (df_grouped)
- Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region. (df_grouped_2)
 - Develop a way to inform the user about the status of the data ingestion without using a polling solution.
- The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable.
- Use a SQL database.

Assumptions:

- A csv file or a xlsx file will be inserted into a "analyze_folder" and then be extracted to be load in a SQL server
- The files will have the same format and column names that the example in the "data" folder
- In case the file is inserted in the server generating duplicates. It would be solve in a different solution
- The used path for the "analyze_folder" and the direction fro the SQL Server are using local references just for the purpouse of this exercise.
- The way used to schedule this process is through crontab. Include in this github you will find the code to use in crontab.
- The SQL connection access is granted for the users.

Instructions:
- Deposit the file in a folder.
- Change the "analyze path" for the path where you deposited the folder.
- Change the SERVER and DATABASE in the conn variable.
- Be sure to have access to a SQL server.
- Run the code (Install libraries if necesary)
