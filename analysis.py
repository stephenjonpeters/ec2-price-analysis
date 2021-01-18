import pandas as pd
pd.set_option('display.max_rows', None)

pfile = '~/ec2-parameters.csv'
df1 = pd.read_csv(pfile)

print("Price = EC2 OnDemand Price")
print("Spot  = EC2 Spot Price")
print("CompCost = CpuCost + NetCost + MemCost")
df1["CpuCost"] = df1["Price"] / df1["Cpu"]
df1["NetCost"] = df1["Price"] / df1["NetGbps"]
df1["MemCost"] = df1["Price"] / df1["MemGb"]
df1["CompCost"] = df1["CpuCost"] + df1["NetCost"] + df1["MemCost"] 
df1['CompCostRank'] = df1['CompCost'].rank()
df1.sort_values("CompCostRank",inplace=True)
df1 = df1.reset_index(drop=True)

print("top 10")
df2 = df1[df1["CompCostRank"] <=10]
print(df2)
