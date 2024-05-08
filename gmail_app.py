import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd 
from tqdm import tqdm
import base64
from bs4 import BeautifulSoup
from jsonpath_ng import jsonpath, parse

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def getCreds():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

class GmailClient():
  def __init__(self):
    creds = getCreds()
    self.service = build("gmail", "v1", credentials=creds)
    self.messages = []

  def testLabels(self):
    try:
      # Call the Gmail API
      results = self.service.users().labels().list(userId="me").execute()
      labels = results.get("labels", [])

      if not labels:
        print("No labels found.")
        return
      print("Labels:")
      for label in labels:
        print(label["name"])

    except HttpError as error:
      print(f"An error occurred: {error}")

  def list_messages(self, request_id, response, exception): 
    if exception is not None:
      print(exception)
    else:
      self.messages.append(response)
    
  def processEmailTxt(self, txt):
    with open('test.txt', 'w') as file:
      file.write(str(txt))
    payload = txt['payload']
    headers = payload['headers']
    for d in headers: 
      if d['name'] == 'Subject': 
          subject = d['value'] 
      if d['name'] == 'From': 
          sender = d['value']
      if d['name'] == 'Date':
        date = d['value']

    data_path = parse('$..data')
    matches = [match.value for match in data_path.find(payload)]
    data = "\n".join(matches)
    body = base64.urlsafe_b64decode(data)
    body = BeautifulSoup(body, 'lxml').body.get_text()
    return {"Sender" : sender, "Subject": subject, "Date" : date, "body": body}
  
  def getAllJobApps(self, label):
    msg_ids = self.service.users().messages().list(userId='me', q=f'label:{label}').execute()['messages']
    batches = []
    for i, msg_id in enumerate(msg_ids):
      if i % 30 == 0 or i == 0: # batch size 
        batch = self.service.new_batch_http_request()
        batches.append(batch)
      
      batch.add(
        self.service.users().messages().get(userId='me', id=msg_id['id']),
        callback=self.list_messages
      )
    
    for batch in tqdm(batches):
      batch.execute()
    data = []
    for txt in self.messages:
      data.append(self.processEmailTxt(txt))
    self.messages = []
    return pd.DataFrame(data)