from google.cloud import storage
import json
import os
import ee
import tempfile
import streamlit as st
from src.app_utils.session_states import SessionStateManager as ssm

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

class ConnectToGoogle:

    def connect_to_google(self):
        """
        Connects to Google Cloud Platform using the provided service account
        credentials stored in Streamlit secrets. It attempts to authenticate,
        set the credentials, and initialize the Earth Engine API for use.

        This method updates the session state variable `gee_initialized` to
        indicate whether the Earth Engine API has been successfully initialized.

        :raises Exception: If the Google Cloud Platform secrets cannot be loaded
            from Streamlit secrets.
        :raises Exception: If the connection to Google Cloud Platform or the
            Earth Engine API initialization fails.

        :return: None
        """

        try:
            gcp_credentials = dict(st.secrets["google_sa_secrets"])
            try:
                au = AuthenticateServiceAccount(gcp_credentials)
                au.set_credentials()
                st.info('Connecting to Google Cloud Platform...')
                au.initialize_ee()
                ssm.GEE_INITIALIZED.set(True)
            except Exception as e:
                st.error(f"❌ Failed to connect to Google Cloud: {str(e)}")
                ssm.GEE_INITIALIZED.set(False)
        except Exception as e:
            st.error(f"❌ Failed to open GCS Secrets: {str(e)}")

if __name__ == '__main__':
    import streamlit as st
    gcp_credentials = dict(st.secrets["google_sa_secrets"])

    gcp_auth = AuthenticateServiceAccount(gcp_credentials)
    gcp_auth.set_credentials()
    gcp_auth.initialize_ee()
    from src.variables.global_layers import GlobalLayer
    from src.utils.spatial import Spatial

    op_cost = GlobalLayer.SE_PLAN_OPPORTUNITY_COST
    bucket_name = "nbs-tool-public"
    gcs_path = f"gs://{bucket_name}/{op_cost.gcs_path}"
    lon = 16
    lat=0
    area_ha = 100
    value = Spatial.get_value_from_cog(gcs_path, lon, lat, area_ha)






