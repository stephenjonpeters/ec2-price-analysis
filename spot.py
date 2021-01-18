import boto3
import json
import pprint as pp
import pandas as pd
import sys
from datetime import datetime, timedelta

dateTimeEnd = datetime.now()
timeDeltaWeek = timedelta(weeks=1)
timeDeltaDay = timedelta(days=1)
dateTimeStart = dateTimeEnd - timeDeltaDay 
print(dateTimeStart)
listOS= [ 'Linux/UNIX']
listAZ= ['us-west-2a']
listInstType = [ 'm4.4xlarge']

pd.set_option('display.max_rows', None)
def devExit():
    sys.exit("developer exit")

def trimAllColumns(df):
    trimStrings = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trimStrings)

def avgList(lst): 
    return sum(lst) / len(lst) 

maxResults = 100 # 1 to 100

client=boto3.client('ec2',region_name='us-west-2')

listFilters = [ 
        { 'Name': 'availability-zone', 'Values': listAZ } ,
        { 'Name': 'instance-type', 'Values': listInstType } ,
        { 'Name': 'product-description', 'Values': listOS} 
        ]

response=client.describe_spot_price_history(Filters= listFilters,  MaxResults= maxResults, StartTime=dateTimeStart)
strNextToken = ''
listSpotPrices =[]

listSpotPriceHistory= response['SpotPriceHistory']
if len(listSpotPriceHistory) > 0:
    for dictSpotPrice in listSpotPriceHistory:
        fltSpotPrice=float(dictSpotPrice['SpotPrice'])
        print(str(fltSpotPrice))
        listSpotPrices.append(fltSpotPrice)

strNextToken = response['NextToken']

while not strNextToken == '':
    response=client.describe_spot_price_history(NextToken=strNextToken, Filters= listFilters,  MaxResults= maxResults, StartTime=dateTimeStart)
    if 'NextToken' in response.keys(): strNextToken = response['NextToken']
    else: strNextToken = ''
    listSpotPriceHistory= response['SpotPriceHistory']
    if len(listSpotPriceHistory) > 0:
        for dictSpotPrice in listSpotPriceHistory:
            fltSpotPrice=float(dictSpotPrice['SpotPrice'])
            print(str(fltSpotPrice))
            listSpotPrices.append(fltSpotPrice)


print("avg spot")
if len(listSpotPrices) > 0:
    fltAvgSpot = avgList(listSpotPrices)
    print(fltAvgSpot)


