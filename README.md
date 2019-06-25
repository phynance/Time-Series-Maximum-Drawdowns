## Time-Series-Maximum-Drawdowns
Find and plot the multiple maximum drawdown in a time-series. The duration and extent of a drawdown is shown. Also, the recovery period is calculated and shown.
The program can be applied to different time-series and the stock index S&P500 is just used as an example here. The data of SPX and VIX are downloaded from [CBOE](http://www.cboe.com/products/vix-index-volatility/vix-options-and-futures/vix-index/vix-historical-data) .

## Installation
### Pre-requisite
The python scripts are written for Python 3 only and requires the following modules:
1. numpy
2. pandas
3. matplotlib


### Clone this repo
`$ git clone https://github.com/phynance/maximum-drawdown/`

## How to use?
1. The file `SPXVIXInput90to18.csv` contains the daily data of SPX and its volatility index VIX from 1990 to 2018. Open the CSV file `SPXVIXInput90to18.csv` and change the time-series to that you want to study. Or you can just keep using this SPX and VIX data given. If you are testing other time-series, the line 

``` VIXdata = df['VIX'].values #####   delete this if you are testing other time-series ############# ```

and the block of code
```
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
```
should be commented or deleted. 

2. The python script `SPX_VIX_simplified.py` contains the algorithm to find the MMDs happened all over these 28 years. In the script, the user may need to change the values of parameters in the section "Input Parameters".
```
###################   Input Parameters     ###############################################
wind_size = 1000  # the size of rolling-window 
bufferPeriod = 75 
err = 5   # A minor discrepancy between starting value of MDD and recovery value 
MDD = 20  # the smallest % of MDD to be shown
##########################################################################################
```
(i) ```wind_size = 1000``` sets the size of rolling-window. It is chosen to be 1000 days as the drawdown usually finish within 4 years. 

(ii)```bufferPeriod``` restrict the recovery date should be at least 3 months later to avoid minor drops are mistakenly shown.

(iii) ```err = 5``` allows a small discrepancy between starting value of MDD and recovery value as the time-series is not continuous.

(iv) ```MDD = 20``` implies the minimum extent of drawdown is 20%. 

3. Run the script `SPX_VIX_simplified`. After finding all the drawdowns which are larger than 20% through rolling-window, the program will further filter the results through two steps.

Step 1: It eliminates all the repeated results, very short drawdowns and recovery period, and those results of recovery date earlier than the troughs. All of these are considered as wrong results.

Step 2: For multiple drawdowns with the same start-date, only choose the drawdown with the latest end-date. 


## Result
The program output 2 graphs 

Graph 1 shows all the MDDs found in the SPX. The starting and ending-dates of MDDS, included the duration, are annotated. The recovery dates are shown in the upper left corner. 
<img src="https://github.com/phynance/maximum-drawdown/blob/master/Figure_1.png">

Graph 2 further indicates the corresponding MDD start and end dates on the plot of VIX time-series.
<img src="https://github.com/phynance/maximum-drawdown/blob/master/Figure_2.png">

The details of the result are stored in the list 
```
secondfilter
```
