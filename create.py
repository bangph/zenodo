# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
from config import Config

# Create a new deposition with file and upload to zenodo.org (current only upload 1 zipped file).
# Author: Bang Pham Huu - email: b.phamhuu@jacobs-university.de
# License: Apache License 2.0
# API examples: http://developers.zenodo.org/?python#quickstart-upload

# Description:
# This script is used to create a new deposition in zenodo (or sandbox.zenodo) with a zipped file from your input folder.
# Also, this deposition will contain the metadata which you defined below.

# NOTE: ******DON'T RUN THIS SCRIPT MORE THANE ONE TIME******* as it will upload another deposition with same contents (no error, but you will have duplicate depositions.)
config = Config()

################### Configuration #####################
# the metadata of this deposition
metadata = {
     'metadata': {
         'title': "rasdaman - raster data manager",
         'upload_type': 'software',
         'creators': [{'name': 'Peter Baumann',
                       'affiliation': 'rasdaman.org'}, {'name': 'email: p.baumann@jacobs-university.de'}, {'name': 'website: rasdaman.org'}],
         'description': '<p><strong>Welcome to rasdaman -- the world&#39;s most flexible and scalable Array Engine</strong></p><p>rasdaman (&quot;raster&nbsp;data&nbsp;manager&quot;) allows storing and querying massive multi-dimensional&nbsp;​arrays, such as&nbsp;<strong>sensor, image, simulation, and statistics data</strong>&nbsp;appearing in&nbsp;domains&nbsp;like&nbsp;<strong>earth, space, and life science</strong>. This worldwide leading array analytics engine distinguishes itself by its flexibility, performance, and scalability. Rasdaman can process arrays residing in file system directories as well as in databases with key features:.</p> <p><ul><li><b>Fast</b>: parallel access to Exascale archives and Terabyte objects in fractions of a second.</li><li><b>Scalable</b>: seamlessly from laptop to high-parallel, high-availability clouds and server farms.</li><li><b>Flexible</b>: &quot;Array SQL&quot; for navigation, extraction, processing, and ad-hoc analysis. Array data can reside in a conventional database, in files optimized by rasdaman, or in some pre-existing archive.</li><li><b>Open standards as issued by OGC</b>: WMS, WCS, WCS-T, WCPS; rasdaman is WCS Core Reference Implementation and listed in the GEOSS Component and Service Registry.</li><li><b>Free</b>: available as open source in a lively, mature, and professionally managed open-source project supervised by Jacobs University, in incubation by the OSGeo foundation.</li><li><b>Cost-efficient: </b>through intelligent, economic resource utilization and free source code.</li></ul> </p> <p>In fact, rasdaman has pioneered&nbsp;​Array Databases&nbsp;being the first fully implemented, operationally used system with an array query language and optimized processing engine with unprecedented scalability. Known rasdaman databases exceed dozens of TB;&nbsp;​EarthServer, is establishing intercontinental fusion of Petabyte datacubes.</p><p>​http://standards.rasdaman.com&nbsp;is a demonstration site showcasing rasdaman-enabled the Big Earth Data standards OGC WCS and WCPS in a variety of 1-D to 5-D geo use cases. Next, you can&nbsp;download&nbsp;readily configured VMs, RPMs, or - of course - compile rasdaman from source. For each step, there is&nbsp;​ample documentation&nbsp;available, as well as&nbsp;​professional support, including dedicated&nbsp;​mailing lists.</p><p><strong>Next-Generation Geo Raster Server</strong>. From simple geo imagery services up to complex analytics, rasdaman provides the whole spectrum of functionality on spatio-temporal raster data - both regular and irregular grids. And it does so with an unprecedented performance and scalability, as recent scientific benchmarks show. To leverage this enabling technology, users do not necessarily have to learn new interfaces: rasdaman&nbsp;integrates&nbsp;smoothly with R, OpenLayers, Leaflet, NASA WorldWind, GDAL, MapServer, ESRI ArcGIS, and many more.</p><p><strong>Makers of Big Data Standards</strong>. Rasdaman is brought to you by the guys writing the Big Datacube standards. The forthcoming ISO SQL/MDA (Multi-Dimensional Arrays) standard, integrating n-D arrays seamlessly into table world, has been crafted by the rasdaman team. This standard will be domain-independent and can serve all of Earth, Space, Life sciences, and beyond. Further, rasdaman is the blueprint for&nbsp;​OGC WCS&nbsp;and&nbsp;​WCPS, the OGC raster query language. No surprise, rasdaman supports&nbsp;​OGC&nbsp;​WMS,&nbsp;​WCS&nbsp;core and all extensions including&nbsp;​WCS-T,&nbsp;​WCPS, and&nbsp;​WPS. Further, rasdaman is&nbsp;INSPIRE WCS&nbsp;reference implementation.</p><p><strong>Worldwide Recognition and Success</strong>. In 2016, US CIO Review&nbsp;​picks rasdaman&nbsp;into their&nbsp;​100 Most Promising Big Data Technologies. rasdaman is official OGC and&nbsp;INSPIRE&nbsp;WCS Reference Implementation. Further, rasdaman is&nbsp;​listed in the GEOSS Component and Service Registry. Finally, rasdaman is included in the&nbsp;OSGeo Live DVD) of particularly recommended open-source geo tools.</p><p><strong>Game changing, disruptive technology</strong>. During a thorough review in Fall 2014, independent experts unanimously attested that, based on &quot;proven evidence&quot;, rasdaman will&nbsp;<strong>significantly transform the way scientists access and use data in a way that hitherto was not possible</strong>. In 2014, rasdaman was selected sole&nbsp;​winner of Big Data Challenge&nbsp;in the worldwide&nbsp;​Copernicus Masters&nbsp;competition, underlining its maturity and scalability. This is along a&nbsp;​chain of innovation awards&nbsp;rasdaman continues to receive. See also the&nbsp;​listing on OpenHub&nbsp;for the business value of the rasdaman open source code. In 2017, The European Space Agency (ESA) recognizes rasdaman as &quot;the world-leading technology in this field&quot;.</p><p>&nbsp;</p>',
         'version': '9.5.0',
         'language': 'eng',
         'keywords': ['Big Data', 'arrays', 'raster data', 'OGC', 'WMS', 'WCS', 'WCS-T', 'WCPS', 'fast', 'scalable', 'flexible', 'open standards', 'free', 'cost-efficient', 'sensor', 'image', 'simulation', 'statistics data'],
         'notes': ''
     }
}

# Check if deposition_id file is not empty, then allow to run this script
with open(config.get_deposition_file()) as f: 
    deposition_id = f.read()
    if deposition_id != "":
    	print "Already published a deposition with id '" + deposition_id + "' in deposition_id file."
    	print "Script will not run, clear the content of deposition_id file and rerun the script if you want to create a new deposition to publish."
    	sys.exit(1)

################## ACTIONS ####################
# 1. create a new empty upload, not publish yet
headers = {"Content-Type": "application/json"}
r = requests.post(config.url + '/api/deposit/depositions',
                  params = {'access_token': config.access_token}, json = {},
                  headers = headers)
                
if r.status_code != 201:          
	print "Error occured when creating an empty depositon to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Created an empty deposition to server."

# Get the deposition id from the previous response (the empty upload)
deposition_id = str(r.json()['id'])
print "Current unpublished deposition URL is '" + config.url + "/deposit/" + deposition_id + "'."

# 2. upload a new file to this empty deposition
# Create a zipped file from this folder
file_path_to_upload = os.path.dirname(config.folder_path_to_upload) + "/" + config.file_name_to_upload
os.system("tar --exclude='" + config.folder_path_to_upload + "/.git' -czf " + file_path_to_upload  + " " + config.folder_path_to_upload)

data = {'filename': config.file_name_to_upload}
files = {'file': open(file_path_to_upload, 'rb')}
r = requests.post(config.url + '/api/deposit/depositions/%s/files' % deposition_id,
                  params = {'access_token': config.access_token}, data = data,
                  files = files)
if r.status_code != 201:          
	print "Error occured when uploading file to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Uploaded file to server."

# 3. add some metadata to the uploaded deposition
r = requests.put(config.url + '/api/deposit/depositions/%s' % deposition_id,
                 params = {'access_token': config.access_token}, data = json.dumps(metadata),
                 headers = headers)
if r.status_code != 200:          
	print "Error occured when adding some metadata to current deposition to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Updated current depositon's metadata."                 

                 
# 4. publish it
r = requests.post(config.url + '/api/deposit/depositions/%s/actions/publish' % deposition_id,
                  params = {'access_token': config.access_token} )
if r.status_code != 202:          
	print "Error occured when publising current deposition to server: ", r.status_code, r.json()
	sys.exit(1)
else:
	print "Published current depositon to server."  
	
print "Current published deposition URL is '" + config.url + "/record/" + deposition_id + "'."

# 5. New deposition is published, save this deposition_id to a file then could be used later for updating new version
with open(config.get_deposition_file(), "w") as f: 
    f.write(deposition_id)
