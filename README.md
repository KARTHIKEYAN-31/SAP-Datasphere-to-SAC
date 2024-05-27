# SAP Datasphere with SAC

## Data Preparation, Transformation and Model creation in SAP Datasphere

### Table Creation:

Creating Tables in SAP Datasphere Data Builder: A Guide to Structured Data Management

In the world of data management, the creation of tables is a fundamental task that allows for the organization and analysis of vast amounts of information. SAP Datasphere Data Builder offers a robust platform for managing and manipulating data within a structured environment. This blog post will guide you through the process of creating five specific tables within the SAP Datasphere Data Builder: PdM_maintenance, PdM_machine, PdM_errors, PdM_failures, and PdM_telemetry.

**Step 1: Preparing Your CSV File**
Before creating the tables, ensure that your CSV file is formatted correctly. The data types should be clearly defined, with decimals set as DecimalFloat, IDs as strings, and date-time values as datetime data types. This preparation will ensure that the data is imported correctly and that the tables function as intended.

**Step 2: Creating the Tables**
Once your CSV file is prepared, you can begin creating the tables in the SAP Datasphere Data Builder. The process involves defining the structure of each table by specifying the columns and their respective data types. For instance, a maintenance table (PdM_maintenance) might include columns for maintenance ID, date, type, and status, each with the appropriate data type.

![Creating Columns of Table](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/Table%20columns.png)

**Step 3: Importing Data**
With the tables created, the next step is to import the data from your CSV file. SAP Datasphere Data Builder provides tools for mapping the CSV columns to the corresponding table columns, ensuring that the data is transferred accurately.

**Step 4: Validating and Managing Data**
After the import, it's crucial to validate the data to ensure there are no errors. This step might involve checking for correct data types, verifying that the date-time values are consistent, and ensuring that the DecimalFloat values are precise.

**Step 5: Creating View**
From Data Builder create a view. Drag and drop each table created in above steps. Join all the table based on datetime and machineID. Use Projection to avoid duplication of columns.

![View](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/MS_view1.png)

### Creating Data Flow to calculate STD and Mean for Telemetry Data:

**Step 1: Creating Data Flow**
From Data Builder create a Data Flow and drop the view created in the last step. Add a python script to it.

![Data Flow 1](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/data_flow_1.png)

**Step 2: Target Table**
Create new table and add the columns which are in the output of the python scrip of the dataframe.

![Target table](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/cleaned_data.png)

**Step 3: Python scrip**
Write a python script to calcualte and aggregate standard deviation and mean for pressure, vibration, volt and rotate for 1 hour, 3 hour and 24 hour. 

![Python Script](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/data_flow_1_script.png)

**Step 4: Target Table**
Drop the Target table created in step 2 in the data flow and make it as target. Map all the columns between script and target table.

![Target Table Mapping](https://github.com/KARTHIKEYAN-31/SAP-Datasphere-to-SAC/blob/main/Screenshot/data_flow_1_target_table.png)


### Creating SAC Model

From Data Builder create a view and drop the Cleaned Data table (target table in last step). Set the sematic of the view as fact.

Create a Model from data Builder and drop the view created in last step and deploy it.

### Create and Deploy other Data Flow and Model

**Statistical Model: ** 
In the similar way of obove create a Data flow from the cleaned data table to calculate statistical values like quantile ranges for each Telemetry data. Use the calcualted quantile to Analyse the data like "is the recent value is different from previous data(Outlier)".

**Days Between Fault: **
Create a Data Flow and SAC model to calculate the average days and days since last fault between two error or maintanence or failure for each component.










