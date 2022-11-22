import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os


def len_line(text): # return the number of lines in a file
    line_count = 0
    for line in text:
        line_count += 1
    return line_count

# convert list to string
def listToString(list):

    str = " "

    return (str.join(list))

# plot I-V degredation graphs
def plot_IV(sorted_experiment_values_wrt_voltage,channel1U_settings,channel1B_settings,measurement_name,i):

    fig,axes = plt.subplots(1,2,constrained_layout = True)
    fig.suptitle(listToString(channel1U_settings[i-1]) + '\n' + listToString(channel1B_settings[i-1]))
    axes[0].plot(sorted_experiment_values_wrt_voltage[6*(i-1)],sorted_experiment_values_wrt_voltage[6*(i-1) + 1],label = 'Current1 Sweep Channel')
    axes[0].plot(sorted_experiment_values_wrt_voltage[6*(i-1)],sorted_experiment_values_wrt_voltage[6*(i-1) + 2],label = 'Current2 Sweep Channel')
    axes[0].set_xlabel('Voltage(V)')
    axes[0].set_ylabel('Current(A)')
    axes[0].legend()
    axes[0].set_title('I-V Graph for Voltage Sweep ' + listToString(measurement_name[i-1]))

    axes[1].plot(sorted_experiment_values_wrt_voltage[6*(i-1) + 3],sorted_experiment_values_wrt_voltage[6*(i-1) + 4],label = 'Current1 Sweep Channel')
    axes[1].plot(sorted_experiment_values_wrt_voltage[6*(i-1) + 3],sorted_experiment_values_wrt_voltage[6*(i-1) + 5],label = 'Current2 Sweep Channel')
    axes[1].set_xlabel('Voltage(V)')
    axes[1].set_ylabel('Current(A)')
    axes[1].legend()
    axes[1].set_title('I-V Graph for Reverse Voltage Sweep ' + listToString(measurement_name[i-1]))
    plt.show()



FILE_PATH = Path(os.path.dirname(os.path.realpath(__file__))) # you can specify your dataset path
text1 = open(str(FILE_PATH/'AI_Dataset1_edited.txt')) # I created a new dataset txt file by deleting the last four line of the original file (AI_Dataset1_edited.txt)

line_count_1 = len_line(text1) # number of lines in text1, I deleted the last four line before
channel1U_settings = np.zeros(int(line_count_1/18),dtype=object) # U2722 Channel settings:
channel1B_settings = np.zeros(int(line_count_1/18),dtype=object) # B2900 Channel settings:
measurement_name = np.zeros(int(line_count_1/18),dtype=object) # Measurement and Channel Number
text1.close()
text1 = open(str(FILE_PATH/'AI_Dataset1_edited.txt'))

count1 = 0
count2 = 0
count3 = 0

# assign edited dataset values to our variables
for i,line in enumerate(text1):
    if i % 18 != 0 and i % 18 != 2 and i % 18 != 4:
        continue
    elif i % 18 == 0:
        measurement_name[count1] = line.split()
        count1 += 1
    elif i % 18 == 2:
        channel1U_settings[count2] = line.split()
        count2 += 1
    else:
        channel1B_settings[count3] = line.split()
        count3 += 1

df = pd.read_table(str(FILE_PATH/'AI_Dataset1_edited.txt'))
df = df.dropna() # drop NA values in the dataset

df.to_csv(str(FILE_PATH/'AI_Dataset1_cleaned.txt'),header=None,index=None,sep=' ',mode='w') # create a cleaned txt file, can be commented after saving the file 

# Structure of cleaned data:
# Voltage Sweep Channel 1
# Current1 Sweep Channel 1
# Current2 Sweep Channel 1
# Voltage Sweep Reversed Channel 1
# Current1 Sweep Channel 1
# Current2 Sweep Channel 1 ...

text2 = open(str(FILE_PATH/'AI_Dataset1_cleaned.txt'))

line_count_2 = len_line(text2) # number of lines in text1, I deleted the last four line before
experiment_values = np.zeros(line_count_2,dtype=object) # Channel values like Voltage Sweep Channel values
experiment_names = np.zeros(line_count_2,dtype=object) # Channel names like "Voltage Sweep Channel"
text2.close()
text2 = open(str(FILE_PATH/'AI_Dataset1_cleaned.txt'))

# assign cleaned dataset values to our variables
for i,line in enumerate(text2):
    if i % 6 != 3:
        experiment_values[i] = line.split()[4:] # all values except the first four elements
        experiment_names[i] = line.split()[:4] # first four elements
    else:
        experiment_values[i] = line.split()[5:] # all values except the first five elements
        experiment_names[i] = line.split()[:5] # first five elements

sorted_experiment_values_wrt_voltage = np.zeros(line_count_2,dtype=object) # sorted experiment values with respect to voltage values

# sorting with respect to voltage values
for i in range(line_count_2):
    if i % 3 == 0:
        sorted_experiment_values_wrt_voltage[i] = sorted(experiment_values[i])
    elif i % 3 == 1:
        sorted_experiment_values_wrt_voltage[i] = [x for _,x in sorted(zip(experiment_values[i-1],experiment_values[i]))]
    else:
        sorted_experiment_values_wrt_voltage[i] = [x for _,x in sorted(zip(experiment_values[i-2],experiment_values[i]))]

# create sorted and cleaned txt file based on our experiment values
with open(str(FILE_PATH/'AI_Dataset1_sorted.txt'),'w') as file:

    for i,line in enumerate(sorted_experiment_values_wrt_voltage):

        file.write(listToString(experiment_names[i]) + ' ')
        for item in line:
            file.write(item)
            file.write(' ')

        file.write('\n') # can be commented after saving the file  

for i in range(line_count_2):
    sorted_experiment_values_wrt_voltage[i] = [float(x) for x in sorted_experiment_values_wrt_voltage[i]] # convert experiment values to float 

number = int(input('Please enter the number which you want to see the I-V graph of... \nFor example, if you want to see the graphs of experiment "Measurement number: 1_2 Channel number: 2"(Second in the dataset) you should enter 2... '))

plot_IV(sorted_experiment_values_wrt_voltage,channel1U_settings,channel1B_settings,measurement_name,number)