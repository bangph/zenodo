# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
from config import Config

# Update an existing deposition with file to zenodo.org (current only upload 1 zipped file).
# Author: Bang Pham Huu - email: b.phamhuu@jacobs-university.de
# License: Apache License 2.0
# API examples: http://developers.zenodo.org/?python#quickstart-upload

# Description:
# This script is used to update an existing deposititon in zenodo (or sandbox.zenodo) with a zipped file from your input folder. 

# NOTE: It will read the deposition's id from ****deposition_id file**** in script folder to know which record should be updated in server.

config = Config()

################### Configuration #####################

# read the description from file to update to new version
version = ""
description = ""
with open(config.get_script_directory() + "/change_log") as content:
    jsonObj = json.load(content)
    version = jsonObj["version"]
    description = jsonObj["description"]

print version, description
sys.exit(1)

# the metadata of this deposition
metadata = {
     'metadata': {
         'title': "rasdaman - raster data manager new version",
         'upload_type': 'software',
         'creators': [{'name': 'Peter Baumann',
                       'affiliation': 'rasdaman.org'}, {'name': 'email: p.baumann@jacobs-university.de'}, {'name': 'website: rasdaman.org'}],
         'description': description,
         'version': version,
         'language': 'eng',
         'keywords': ['Big Data', 'arrays', 'raster data', 'OGC', 'WMS', 'WCS', 'WCS-T', 'WCPS', 'fast', 'scalable', 'flexible', 'open standards', 'free', 'cost-efficient', 'sensor', 'image', 'simulation', 'statistics data'],
         'notes': ''
     }
}

deposition_id = ""
# Check if deposition_id file is not empty, then allow to run this script
with open(config.get_deposition_file()) as f: 
    deposition_id = f.read()
    if deposition_id == "":
    	print "Script will not run, it needs the deposition's id to update new version, run the creating script to create and publish a new deposition first."
    	sys.exit(1)

################## ACTIONS ####################
# 0. create a new deposition version with different deposition_id from the existing deposition
r = requests.post(config.url + '/api/deposit/depositions/' + deposition_id + '/actions/newversion',
                  params={'access_token': config.access_token})
if r.status_code != 201:          
	print "Error occured when creating a newly draft version for published deposition: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Created a newly draft version for published deposition."

# You have to use the new version's deposit link
newversion_draft_url = r.json()['links']['latest_draft']

# There is a new "deposition_id" now:
# Extract deposition_id from url
deposition_id = newversion_draft_url.split('/')[-1]  

# 1. Remove the old tar file of last version in this new version
response = requests.get(config.url + '/api/deposit/depositions/'+ deposition_id + '/files',
                 params={'access_token': config.access_token})
# e.g: https://sandbox.zenodo.org/api/deposit/depositions/142622/files/a5690b72-0df6-4125-b248-221699988032
old_tar_file_url = response.json()[0]['links']['self']
r = requests.delete(old_tar_file_url,
                    params={'access_token': config.access_token})

# 2. upload a new file to this existing deposition
# Create a zipped file from this folder
file_path_to_upload = os.path.dirname(config.folder_path_to_upload) + "/" + config.file_name_to_upload
os.system("tar --exclude='" + config.folder_path_to_upload + "/.git' -czf " + file_path_to_upload  + " " + config.folder_path_to_upload)

headers = {"Content-Type": "application/json"}
data = {'filename': config.file_name_to_upload}
files = {'file': open(file_path_to_upload, 'rb')}
r = requests.post(newversion_draft_url + '/files',
                  params = {'access_token': config.access_token}, data = data,
                  files = files)
if r.status_code != 201:          
	print "Error occured when uploading file to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Uploaded file to server."


# 3. add some metadata to the uploaded deposition
r = requests.put(newversion_draft_url,
                 params = {'access_token': config.access_token}, data = json.dumps(metadata),
                 headers = headers)
if r.status_code != 200:          
	print "Error occured when adding some metadata to current deposition to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Updated current depositon's metadata."                 
              
# 4. publish it
r = requests.post(newversion_draft_url + '/actions/publish',
                  params = {'access_token': config.access_token} )
if r.status_code != 202:          
	print "Error occured when publising current deposition to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Published current depositon to server."  
