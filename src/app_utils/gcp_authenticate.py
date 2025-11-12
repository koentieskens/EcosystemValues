from google.cloud import storage
import json
import os
import ee
import tempfile


class AuthenticateServiceAccount:

    def __init__(self, cred: dict = None):
        """
		Authenticate with Google cloud to access data stored on cloud storage.
		:param credentials_json:
			local json file with authentication details. See readme for details on the necesarry content of this
			JSON file
		"""
        self.credentials_json_string = json.dumps(cred)
        self.cred = json.loads(self.credentials_json_string)
        self.client_email = self.cred['client_email']
        self.project = self.cred['project_id']
        self.service_account_email = self.cred['client_email']
        self.private_key = self.cred['private_key']
        self.client = storage.Client.from_service_account_info(self.cred)
        self.bucket = self.client.get_bucket('nbs-tool-public')

    def initialize_ee(self):
        """
        Start an ee session with the account specified in the credentials.json
        :return: -
        """
        credentials = ee.ServiceAccountCredentials(self.service_account_email, key_data=self.credentials_json_string)
        ee.Initialize(credentials, project=self.project)

    def set_credentials(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(self.cred, temp_file)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file.name



if __name__ == '__main__':
    import streamlit as st
    gcp_credentials = dict(st.secrets["google_sa_secrets"])

    gcp_auth = AuthenticateServiceAccount(gcp_credentials)
    gcp_auth.set_credentials()
    from src.variables.global_layers import GCSLayer
    from src.utils.spatial import Spatial

    op_cost = GCSLayer.SE_PLAN_OPPORTUNITY_COST
    bucket_name = "nbs-tool-public"
    gcs_path = f"gs://{bucket_name}/{op_cost.gcs_path}"
    lon = 16
    lat=0
    area_ha = 100
    value = Spatial.get_value_from_cog(gcs_path, lon, lat, area_ha)






