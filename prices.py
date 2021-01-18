import boto3
import json
import pprint as pp
import pandas as pd


pd.set_option('display.max_rows', None)

def trimAllColumns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trimStrings = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trimStrings)

url = 'https://api.pricing.us-east-1.amazonaws.com'
serviceCode = 'AmazonEC2'
formatVersion= 'aws_v1'
maxResults = 100 # 1 to 100

client = boto3.client('pricing')
listFilters = [
          { 'Field': 'ServiceCode', 'Type': 'TERM_MATCH', 'Value': 'AmazonEC2' },
          { 'Field': 'currentGeneration', 'Type': 'TERM_MATCH', 'Value': 'Yes' },
          { 'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'US West (Oregon)' },
          { 'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared' },
          { 'Field': 'processorArchitecture', 'Type': 'TERM_MATCH', 'Value': '64-bit' },
          { 'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux' },
          { 'Field': 'preInstalledSw', 'Type': 'TERM_MATCH', 'Value': 'NA' }
        ]
strNextToken =''

response = client.get_products( ServiceCode=serviceCode, FormatVersion=formatVersion,  MaxResults=maxResults, Filters=listFilters)
strNextToken = response['NextToken']
listPriceList = response['PriceList']
listDict = []
for strPrice in listPriceList:
    dictPrice = json.loads(strPrice)
    dictAtt = dictPrice['product']['attributes']
    listDict.append(dictAtt)

while not strNextToken == '':
    print("paginating...", end ='')
    response = client.get_products( ServiceCode=serviceCode,NextToken=strNextToken, FormatVersion=formatVersion,  MaxResults=maxResults, Filters=listFilters)
    if 'NextToken' in response.keys(): strNextToken = response['NextToken']
    else: strNextToken = ''
    listPriceList = response['PriceList']
    for strPrice in listPriceList:
        dictPrice = json.loads(strPrice)
        dictAtt = dictPrice['product']['attributes']
        listDict.append(dictAtt)

print("done") 
df1 = pd.DataFrame(listDict)
df1 = df1.drop('operation',axis=1)
df1 = df1.drop('processorFeatures',axis=1)
df1 = df1.drop('location',axis=1)
df1 = df1.drop('currentGeneration',axis=1)
df1 = df1.drop('dedicatedEbsThroughput',axis=1)
df1 = df1.drop('servicecode',axis=1)
df1 = df1.drop('licenseModel',axis=1)
df1 = df1.drop('preInstalledSw',axis=1)
df1 = df1.drop('usagetype',axis=1)
df1 = df1.drop('intelTurboAvailable',axis=1)
df1 = df1.drop('enhancedNetworkingSupported',axis=1)
df1 = df1.drop('tenancy',axis=1)
df1 = df1.drop('normalizationSizeFactor',axis=1)
df1 = df1.drop('intelAvxAvailable',axis=1)
df1 = df1.drop('processorArchitecture',axis=1)
df1 = df1.drop('capacitystatus',axis=1)
df1 = df1.drop('locationType',axis=1)
df1 = df1.drop('storage',axis=1)
df1 = df1.drop('intelAvx2Available',axis=1)
df1 = df1.drop('servicename',axis=1)
df1 = df1.drop('physicalProcessor',axis=1)
df1 = df1.drop('instancesku',axis=1)
df1 = df1.drop('operatingSystem',axis=1)
df1 = df1.drop('ecu',axis=1)

df1['MemGb'] = df1['memory'].str.replace('GiB','')
df1['MemGb'] = df1['MemGb'].astype(float)
df1['CpuGhz'] = df1['clockSpeed'].str.replace('GHz','')
df1['CpuGhz'] = df1['CpuGhz'].str.replace('Up to ','')
df1['CpuGhz'] = df1['CpuGhz'].astype(float)
df1['instanceFamily'] = df1['instanceFamily'].str.replace('optimized','')
df1['instanceFamily'] = df1['instanceFamily'].str.replace('purpose','')
df1['instanceFamily'] = df1['instanceFamily'].str.replace('Machine Learning ASIC Instances','ML')
df1['instanceFamily'] = df1['instanceFamily'].str.replace('instance','')
df1['instanceFamily'] = df1['instanceFamily'].str.replace('Instances','')
df1['Family'] = df1['instanceFamily']
df1 = df1.drop('memory',axis=1)
df1 = df1.drop('clockSpeed',axis=1)
df1 = df1.drop('instanceFamily',axis=1)
df1['NetGbps'] = df1['networkPerformance'].str.replace('Gigabit','')
df1['NetGbps'] = df1['NetGbps'].str.replace('Up to ','')
df1['NetGbps'] = df1['NetGbps'].str.replace('High','0')
df1['NetGbps'] = df1['NetGbps'].str.replace('Low to Moderate','0')
df1['NetGbps'] = df1['NetGbps'].str.replace('Moderate','0')
df1['NetGbps'] = df1['NetGbps'].astype(float)
df1['gpu'] = df1['gpu'].fillna(0)
df1['gpu'] = df1['gpu'].astype(float)
df1 = df1.drop('networkPerformance',axis=1)
df1 =trimAllColumns(df1)
print(df1)

