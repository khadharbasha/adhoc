import pandas as pd
import re

df = pd.read_csv('Translate.csv')
df = df.drop(['Modified Main Service','Modified Service Name'], axis=1)

def con_k(x,y):
    x = clean_text(x)
    y = clean_text(y)
    if x=='agency charges':
        if y=='agency fee' or 'other agency expenses' or 'agents transport' or 'processing fee':
            return x+';'+y
    elif x=='agency fee':
        if y=='agency fee' or 'other agency expenses' or 'agents transport' or 'processing fee':
            return x+';'+y
    elif x=='charter expenses':
        if y=='agency fee':
            x = 'agency charges'
            return x+';'+y
        else: 
            x = 'port charges'
            return x+';'+y
 
def clean_text(text):
    text = text.lower()
    text = re.sub(r'processing/hub fee', 'processing fee', text)
    text = re.sub(r'canal dues - recoverable', 'canal dues', text)
    text = re.sub(r'agency fee - recoverable', 'agency fee', text)
    text = re.sub(r'custom dues - recoverable', 'customer dues', text)
    text = re.sub(r'harbour dues - recoverable', 'harbour dues / port dues', text)
    text = re.sub(r'launch hire for agent - recoverable', 'launch', text)
    text = re.sub(r'miscellaneous (charterers expenses)', 'other port expenses', text)
    text = re.sub(r'mooring - recoverable', 'mooring / unmooring', text)
    text = re.sub(r'other port charges - recoverable', 'other port expenses', text)
    text = re.sub(r'pilotage - recoverable', 'pilotage', text)
    text = re.sub(r'towage - recoverable', 'towage', text)
    text = re.sub(r'wharfage - recoverable', 'wharfage', text)
    return text
    
   
df['new1'] = df.apply(lambda x: con_k(x['Main Service'],x['Service Name']), axis=1)
    
split_data = df["new1"].str.split(";")
data = split_data.to_list()
names = ['Modified Main Service','Modified Service Name']
new_df = pd.DataFrame(data, columns=names)
result = pd.concat([df, new_df], axis=1, sort=False)


## Below procedure create a dict key value pair lookup table
df=pd.read_excel('POC Service Code Mappings.xlsx')

                    # Creating Key
df['Main Service Names'] = df['Main Service Names'].str.strip()
df['Service Names'] = df['Service Names'].str.strip()
df['Key'] = df[['Main Service Names', 'Service Names']].agg('-'.join, axis=1)

                    # Creating Value
df['Standard Main Service Name'] = df['Standard Main Service Name'].str.strip()
df['Standard Service Name'] = df['Standard Service Name'].str.strip()
df['Value'] = df[['Standard Main Service Name', 'Standard Service Name', 'Use / Ignore']].agg('-'.join, axis=1)

                    # Creating dict
mydict = dict(zip(df.Key, df.Value))
mydict

# Using dict in Input
input_data = pd.read_excel('Input.xlsx')
input_data['key'] = input_data['Main Service Name'].str.strip() + '-' + input_data['Service Name'].str.strip()

def mapping(df2):
    #for key,value in mydict.items():
       # if key in df2['Main Service Name'] & key in df2['Service Name']:
    #key = df2['Main Service Name'].str.strip() + '-' + df2['Service Name']
    return mydict.get(df2, 'Invalid')

input_data['Value'] = input_data.key.apply(mapping)

input_data[['Main Service','Sub Service','Use/Ignore']]=input_data.Value.str.split('-',expand=True)


model_data = input_data[['Main Service Name', 'Sub Service']]
