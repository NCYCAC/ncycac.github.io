from __future__ import print_function
import httplib2
import os
from shutil import copyfile

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1ww_Rtz0B1timYpFa-xNo2gOLe_BrBKLZbABFiJdNCu0'
    rangeName = 'A2:F10'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Last Update, Author, Doc ID, Title:')
        for row in values:
            # Print columns A through D, which correspond to indices 0 to 3.
            print('%s, %s, %s, %s' % (row[0], row[1], row[2], row[3]))
        return values

def parse(content):
    structuredContent = {'title': content[3], 'md': content[4]}
    fileNameString = structuredContent['title'].replace(" ", "-")
    destFilePath = 'source/'+fileNameString+'.html.md'
    destinationFile = open(destFilePath, 'w')
    # Write front matter
    destinationFile.write('---\n')
    destinationFile.write('layout: "content_layout"\n')
    destinationFile.write('title: '+content[3]+'\n')
    destinationFile.write('---\n')
    destinationFile.write(structuredContent['md'].replace(u"\u2018", "'").replace(u"\u2019", "'"))
    destinationFile.close()

def parseOld(content):
	structuredContent = {'title': content[3], 'html': content[4]}
	destFilePath = '../gen/'+structuredContent['title']+'.html'
	# copyfile('../template.html', fileTitle)

	templateFile = open("../template_ncycac.html", 'r')
	destinationFile = open(destFilePath, 'w')

	for line in templateFile:
		line = line.replace("{doc-title}", structuredContent['title'])
		line = line.replace("{doc-body}", structuredContent['html'])
		destinationFile.write(line)

	templateFile.close()
	destinationFile.close()


if __name__ == '__main__':
    allContent = main()
    for content in allContent:
    	parse(content)
