#dependancies 
import json
import pprint
import pandas as pd
import sqlite3
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#oauth2.0 google drive api
SCOPES = ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive.readonly","https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/drive.appdata","https://www.googleapis.com/auth/drive.metadata"]
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

#credentials and permission screen 
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
credentials = flow.run_local_server(host='localhost',
    port=8080,
    authorization_prompt_message='Please visit this URL: {url}',
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)

#google drive api query and json output

service = build('drive', 'v3', credentials=credentials)
lists = service.revisions().list(fileId = "1i8yoMxDYCpXYNBt-6zb_UePwDJlchorKVaYAe3xxYo0", fields = 'revisions(id,modifiedTime,lastModifyingUser/emailAddress,lastModifyingUser/displayName)', pageSize = 1000).execute()

#formatting json to remove unwanted data

lists = json.dumps(lists)
lists = lists[13:-1]
print(lists)
lists = json.loads(lists)


#json to sql 

#flattening of data
norm = pd.json_normalize(lists)
df = pd.DataFrame(norm)

#connecting to the database
conn = sqlite3.connect("audittrail.db")
c = conn.cursor()

#saving to new table
df.to_sql("GDocs_Data",conn,if_exists='replace',index = False)



#### github
username = 'tinobless'
token = "{replace with string}"
owner = 'issajojo'
repo = 'Assignment3'

info = requests.get(f'https://api.github.com/repos/{owner}/{repo}/commits', auth=(username,token),params='*')

info = json.loads(info.text)

norm = pd.json_normalize(info)

df = pd.DataFrame(norm)

df = df.iloc[:, 6:9]
df.astype(str) 

print(df)

conn = sqlite3.connect("audittrail.db")
c = conn.cursor()

df.to_sql("Github_Data",conn,if_exists='replace',index = False)

