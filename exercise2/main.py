import requests
import xlsxwriter
from datetime import date, datetime

# Create the workbook and sheet
workbook = xlsxwriter.Workbook('Report.xlsx')
worksheet = workbook.add_worksheet()

# Download the latest files json
latest_file_downloads = requests.get('https://download.appdynamics.com/download/downloadfilelatest/')
agents = latest_file_downloads.json()

# Add the headers row
row = ['Title','Description','Version','File Type','Operating System','Bits','Creation Time','Major Version','Minor Version','Hotfix Version','Build Number','Download Path']
for columnIndex, title in enumerate(row):
    worksheet.write(0, columnIndex, title)

# Get today's date and initialize the row index
today = datetime.today()
rowIndex = 1

#Sort the agents by creation_time and then filetype
for agent in sorted(agents, key = lambda x: (x['creation_time'], x['filetype'])):

    # Parse the creation_time into a datetime
    date = datetime.strptime(agent['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    # Calculate how many months ago the creation_time is
    monthsAgo = (today - date).days / 31
    # Skip processing if more than 3 months old
    if monthsAgo > 3:
        continue

    # Create the row array and write it to the XLSX
    row = [agent['title'], agent['description'], agent['version'], agent['filetype'], agent['os'], agent['bit'], agent['creation_time'], agent['major_version'], agent['minor_version'], agent['hotfix_version'], agent['build_number'], agent['download_path']]
    for columnIndex, data in enumerate(row):
        worksheet.write(rowIndex, columnIndex, data)
    rowIndex += 1

# Close and write the XLSX
workbook.close()