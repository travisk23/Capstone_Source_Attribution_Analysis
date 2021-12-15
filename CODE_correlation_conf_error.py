# -*- coding: utf-8 -*-
"""
Spyder Editor

Travis Klosinski 4/28/2021
Indiana Unviersity CAPSTONE



The code below describes the process of data extraction from a .csv source to a dataframe. 
The data is being categorized into a dataframe. Once the data is in place I needed to create variables and arrays from this data.
To do this several columns of data needed to be cleaned due to errors in data acquistions from the data source.
Once data was cleaned and reassigned, error rates were calculated and placaed in a correlational analysis against partipant 
confidence rating. This revealed a negative correlation between the two categories.
"""

#Below we are importing all necesaary libraries for the correlation analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

n_prts = 19 # amount of particpants

n_blocks = 6 # amount of trials each particpant went through

# In the code below we are extracting the data and assigning columns labels
# or "headers" to our newly created data frame
cols = ["participant", "block", "trial", "animal", "Modality", "interaction", "source_choice", "confidence", "trial_duration"]

all_data = pd.DataFrame(columns=cols)


for prt in range(n_prts): # Here I am looping through each file from the bulk data source and saving it to a new dataframe

    for block in range(n_blocks):
        folder_location = "C:\\Users\\tklosins\\Desktop\\VR Data\\"
        filename = "participant" + str(prt+1) + "block" + str(block+1) + ".csv"

        data = pd.read_csv(folder_location + filename, header=None, names = cols, sep = ";")

        all_data = pd.concat([all_data, data])
        
#print(all_data)   

# The code below is now saving the new data frame to the desktop for easier management
path = "C:\\Users\\tklosins\\Desktop\\virtual_reality_df"
all_data.to_csv(path)

# Below we are creating new variables that are filled w/ data from original dataframe cols.
prt_id = all_data.participant 

trial_conds = all_data.Modality

choices = all_data.source_choice
 
# The code below is removing errors from incurred from the original data source filing errors
conf = all_data["confidence"].values.astype(str)
n = len(conf)

new_conf= np.array([])
for k in range(n):
    x = conf[k]
    
    y= x.replace(",", ".")
    
    new_conf= np.append(new_conf,float(y))
    
# To keep things simple, I saved the corrected data back into the data frame
conf= new_conf
all_data["confidence"]= conf

# Now we take the new and clean variables from above and form a new dataframe out of them
data_dict = {"Prt_Id": prt_id, "Trial_Cond": trial_conds, "Choice": choices, "confidence": conf}
data_df = pd.DataFrame(data_dict)

# Once we have all of our neccesary values, we can begin to calculate the data for our correlation analysis
error_df = pd.DataFrame(None, index = range(n_prts), columns = ["Prt_Id", "Error_Rate", "Confidence"] )

# Below I am looping through each particpant's data within the data frame
for prt in range(n_prts):
    
    rows_to_get = (data_df["Prt_Id"] == prt + 1) # This line of code is isntructing waht data to keep
    
    prt_data = data_df[rows_to_get] # and this line tells it to only kep the data for the participant
    
    # This is pulling out any relevant data as arrays:
    cond = prt_data["Trial_Cond"].values
    choice = prt_data["Choice"].values
    
# Next we compare using our error rate: the error rate is calc. by taking the
# amountdividing the total number of times the choice matched the condition 
# divided by total number of trials this is done using the != operator.
    
    error_rate = np.sum(cond != choice)/len(cond)
   
    conf_rate = np.mean(prt_data["confidence"].values)
    
    error_df.loc[prt, ["Prt_Id", "Error_Rate", "Confidence"]] = [prt, error_rate, conf_rate]
    
# Here we are proof checking by printing our new dataframe:
print(error_df)

# Below we are assiging values for use in our correlation analysis

error_df = error_df[["Error_Rate", "Confidence"]].astype(float)
corr_df = error_df.corr()

# Here we again are printing out our data table of results
print(corr_df)

# Now we plot the correlational data that we've found and assigned:
sns.regplot(x=error_df["Confidence"].values, y=error_df["Error_Rate"].values, data=error_df)

plt.title("Scatter Plot of Error Rates & Confidence" )
plt.xlabel("Confidence Rating")
plt.ylabel("Error Rate")

# We can also gleam useful data from plotting a box and whiskers graph 
# to reveal values per modality

#sns.boxplot(x= "Modality", y= "confidence", data= all_data)

"""That's it! Thanks for browsing."""



