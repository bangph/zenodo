# Upload deposition with file to zenodo.org (current only upload 1 zipped file).
# Author: Bang Pham Huu - email: b.phamhuu@jacobs-university.de
# License: Apache License 2.0
# API examples: http://developers.zenodo.org/?python#quickstart-upload
import os

class Config:
    # Create user token from https://zenodo.org/account/settings/applications/
    # New token for Personal access tokens with scopes (deposit:actions and deposite:write)
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
    SANDBOX_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

    # Sandbox is used for testing upload and publish.
    # NOTE: CANNOT REMOVE THE PUBLISHED DEPOSITION, TEST FIRST WITH SANDBOX.
    URL = "https://zenodo.org"
    SANDBOX_URL = "https://sandbox.zenodo.org"

    ########## NOTE: Change here from test server to real server to publish
    url = SANDBOX_URL
    access_token = SANDBOX_ACCESS_TOKEN

    # the source code folder is used to compress as a zipped file to upload.
    file_name_to_upload = 'rasdaman.tar.gz'
    folder_path_to_upload = self.get_script_directory() + '/rasdaman'

    def get_script_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def get_deposition_file(self):
        # if run create_new_deposition.py successful, it will create a new deposition in zenodo with an id,
        # and this id is stored in a file to be used to update new version.    
        return self.get_script_directory() + "/deposition_id"
