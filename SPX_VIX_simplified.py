# -*- coding: utf-8 -*-
"""
@author: Hin C
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("SPXVIXInput90to18.csv", index_col='Date', )
df.index = pd.to_datetime(df.index)

SPXdata = df['SPX'].values
VIXdata = df['VIX'].values #####   delete this if you are testing other time-series ###############


plt.close('all')
plt.rcParams.update({'font.size': 10})   #### word size in plots
plt.figure(1)
plt.plot(df.index, SPXdata)
result_list = []
VIXfiltered = []
###################   Input Parameters     ###############################################
wind_size = 1000    # the size of rolling-window
bufferPeriod = 75   # restrict the recovery date should be at least 3 months later
err = 5             # A minor discrepancy between starting value of MDD and recovery value  
MDD = 20            # the smallest extent of MDD (in %) to be shown
##########################################################################################
k=0   # position of the rollilng window
m = 0 # the m-th MDD found

while k <= len(SPXdata) - wind_size :
    print("window position= %s " %k)
    
    xs_roll = SPXdata[k:k+wind_size]
    
    runningmax = np.maximum.accumulate(xs_roll)  
    diff = runningmax - xs_roll  
    
    if np.count_nonzero(diff) <2 :
        print("List is empty")
        pass
    else:
        i = np.argmax(diff) # locate the min point
        j = np.argmax(xs_roll[:i]) # locate the max point
        
        drawdown = (xs_roll[i] - xs_roll[j])/xs_roll[j] *100
        
        #print(drawdown)
        if abs(drawdown) < MDD: 
            pass
        else:
            print("*************************the %s-th MDD*************************" %(m+1))
                                
            MDDstart =  df.index[k+j]       
            MDDend   =  df.index[k+i]
            duration = (MDDend - MDDstart).days
              
            restofseries = SPXdata[k+j+bufferPeriod:-1]  # finding the recov. date 3 month later
            ### allows a minor discrepancy between starting value of MDD and recovery value 
            RecoverList = np.where((restofseries> xs_roll[j]- err) & (restofseries < xs_roll[j]+ err ))   
            temp = np.array(RecoverList)[0,:]   
            if temp.size == 0:   # checking if no recovery date is found? 
            ## most probably because it is the last window in the whole time-series
                resulttemp = [MDDstart, xs_roll[j], MDDend, xs_roll[i], duration, drawdown, 0 ,0, 0  ]
            else:       
                rec_index = temp.min() # locate the 1st recovery point              
                recoveredDate=  df.index[k+j+bufferPeriod+rec_index]
                recov_point = restofseries[rec_index]
                recov_days = (recoveredDate - MDDstart).days
                resulttemp = [MDDstart, xs_roll[j], MDDend, xs_roll[i], duration, drawdown,recoveredDate,recov_days, recov_point ]
                
            result_list.append(resulttemp)
            m += 1                 
    k += int(wind_size/4)  # distance to next window inspection
##########################################################################################

#####################  self-design algorithm to filter out many unwanted results #####################
unfiltered = [[1, 1 ] + result_list[0]]   # concatenate

# make 2 new parameters in the front of list 
for rowIndex in range(1,len(result_list)):
    StartdaysDifference = (result_list[rowIndex][0] - result_list[rowIndex-1][0]).days
    EnddaysDifference = (result_list[rowIndex][2] - result_list[rowIndex-1][2]).days
    temp_list= [StartdaysDifference,EnddaysDifference]+ result_list[rowIndex]
    unfiltered.append(temp_list)

####      filter all the unwanted MDDs     ####
firstfilter=[]
for row in range(0,len(unfiltered)):
    # eliminate the repeated results, 
    # DD with duration less than 10days, 
    # recovery period is less than 30 days, 
    # recov is earlier than the trough
    if (unfiltered[row][0] == 0 and unfiltered[row][1] == 0) or unfiltered[row][6] < 10 or unfiltered[row][9]<30 or unfiltered[row][4]> unfiltered[row][8]:
        pass
    else:
        firstfilter.append(unfiltered[row])
        
secondfilter = []
for row in range(0,len(firstfilter)-1):
    if (firstfilter[row][2] == firstfilter[row+1][2] and firstfilter[row][4]  < firstfilter[row+1][4]):
        pass
    else:
        secondfilter.append(firstfilter[row])       

secondfilter.append(firstfilter[row+1])  
####################################################################


for rowIndex in range(len(secondfilter)):
    [dayDiff,dayDiff2, MDDstart, high, MDDend,low, duration, DDPercent, recoveredDate, recov_days , recov_point] = secondfilter[rowIndex]
    plt.plot([MDDstart, MDDend], [high, low], 'ro--')
    
    MDDyear, MDDmonth, MDDdate = str(MDDstart.year),  str(MDDstart.month), str(MDDstart.day)
    DDendYear, DDendMonth, DDendDate = str(MDDend.year), str(MDDend.month), str(MDDend.day)
    
    height_MDD = (-1)**(rowIndex)*(200+ (rowIndex%3)*200 ) # a stupid way to avoid overlapping, need to revise later

    plt.annotate( '%s-%s-%s \n  %s-%s-%s \n %d DD days \n (%.2f %%)' % (MDDyear,MDDmonth,MDDdate, DDendYear,DDendMonth,DDendDate,duration, DDPercent), 
             xy=(MDDstart, high), xytext=(MDDstart, high+height_MDD),color='black', arrowprops=dict(facecolor='red', alpha=0.3),)
    
    if recoveredDate !=0:
        plt.plot([MDDstart, recoveredDate], [ high , recov_point], linestyle = '--',  label='%s-%s-%s (%d RecovDays)'% (str(recoveredDate.year), str(recoveredDate.month), str(recoveredDate.day),recov_days))           
                       
plt.title("All Maximum DrawDown of SPX larger than %s %% between 1990 and 2018" % MDD)
plt.legend(loc='best') 
  

###############   delete this if you are testing other time-series ###############
plt.figure(2)
plt.plot(df.index, VIXdata)
for row in range(len(secondfilter)):
    start = secondfilter[row][2]
    VIXstart = df.loc[start]['VIX']
    end = secondfilter[row][4]
    VIXend = df.loc[end]['VIX']
    delta = (VIXend-VIXstart)
    VIXfiltered.append([start, VIXstart,end, VIXend, delta])
    duration = (end - start).days
    plt.plot([start, end], [VIXstart, VIXend], 'ro--')
    MDDyear, MDDmonth, MDDdate = str(start.year),  str(start.month), str(start.day)
    DDendYear, DDendMonth, DDendDate = str(end.year), str(end.month), str(end.day)
    #height_MDD = (-1)**(row)*(20 + (row%3)*5)
    height_MDD = (20 + (row%3)*10)
    plt.annotate( '%s-%s-%s \n  %s-%s-%s \n %d DD days \n (%.2f %%)' % (MDDyear,MDDmonth,MDDdate, DDendYear,DDendMonth,DDendDate,duration, delta), 
             xy=(start, VIXstart), xytext=(start, VIXstart+height_MDD),color='black', arrowprops=dict(facecolor='red', alpha=0.3),)

plt.title('Change of VIX during SPX MDD > %s %% between 1990 and 2018' % MDD )

###############   delete this if you are testing other time-series ###############









                 

