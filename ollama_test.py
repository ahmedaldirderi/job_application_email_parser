import ollama
import time 
from tqdm import tqdm 
from gmail_app import GmailClient


def extractCompanyName(txt):
  txt = txt.replace("\n","")
  txt += ". Company"
  response = ollama.chat(model='zeffmuks/universal-ner', messages=[
    {
      'role': 'user',
      'content': txt,
    },
  ])
  return response['message']['content']
  


gc = GmailClient()
apps_df = gc.getAllJobApps('job-applications')


start_time = time.time()
for x in tqdm(apps_df.body): 
  r = extractCompanyName(x)
  print(r)
print(time.time() - start_time)