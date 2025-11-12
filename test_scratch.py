import streamlit as st
import rioxarray as rxr
from st_files_connection import FilesConnection
import json
from google.cloud import storage
import ee

import json



gcp_credentials = st.secrets["google_sa_secrets"]
credentials_json_string = json.dumps(dict(gcp_credentials))
credentials_dict = json.loads(credentials_json_string)
client = storage.Client.from_service_account_info(credentials_dict)

service_account_email = credentials_dict['client_email']
private_key = credentials_dict['private_key']
credentials = ee.ServiceAccountCredentials(service_account_email, key_data=credentials_json_string)
project_id = 'nbs-value'
ee.Initialize(credentials, project=project_id)


a = st.secrets.google_sa_secrets.type
gcs_path = 'gs://nbs-tool-public/data/global_data/cost/se_plan/opportunity_cost.tif'
bounds = (11.0, 0.0, 12.0, 1.0)  # (minx, miny, maxx, maxy)
da = rxr.open_rasterio(gcs_path)