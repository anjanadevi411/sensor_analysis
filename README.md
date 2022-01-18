# sensor_analysis
Introduction
This task is about visualizing sensor timeseries data from a cultivation tank in the active pharmaceutical ingredient (API) production.  When a cell cultivation starts it is given a unique BatchID, and a cultivation batch will be active for about 24 hours. Keep in mind that the sensors will gather data even when no batch is active.
Description of data
The data you have received consists of timeseries data from four sensors and some batch meta information. The data is stored in tab separated csv files.
The four different sensors are: 
·	400E_Temp1
·	400E_Temp2
·	400E_PH1
·	400E_PH2
and the data is sampled at a one-minute rate. 
The batch information contains the StartDate and EndDate for each BatchID. The BatchID column contains two types of BatchID:
·	Production batches that follow the naming convention XP400EYYYY where X is a letter from A-Z and YYYY is the trailing batch-number that resets when X changes (BP400E0101, BP400E0102, CP400E0101, etc.). 
·	Test-batches that follow the naming convention TEST_YYYY
In between each batch a small time period is reserved for preparing the next batch and is denoted by a NULL/NaN value in the BatchID column. 


Task

•	Listing all the batches in the data including the duration of each batch
•	Visualizing data from all the sensor values for each batch
    o	Given the view link for production batches only
•	Computed and visualized the difference between the temperature (400E_Temp2 – 400E_temp1) and PH (400E_PH2 – 400E_PH2) sensors for the period of each batch
• storing the data in a database.

![image](https://user-images.githubusercontent.com/10669618/149989837-8e29ceab-b830-40a0-ab12-7d068655c001.png)

