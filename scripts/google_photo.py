import json
import os
import urllib.request
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow
from dotenv import load_dotenv
from googleapiclient.discovery import build

from line_notification import notify_line

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/photoslibrary"]
API_SERVICE_NAME = "photoslibrary"
API_VERSION = "v1"
CLIENT_SECRET_FILE = "../bin/client_secret.json"
CREDENTIAL_FILE = "../bin/credential.json"

BASE_FORM_URL = os.getenv("TEMPERATURE_FORM_URL")
NAME_ID = os.getenv("NAME_ID")
HAS_SYMPTOM_ID = os.getenv("HAS_SYMPTOM_ID")
BODY_TEMP_ID = os.getenv("BODY_TEMP_ID")


def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def getCredentials():
    if os.path.exists(CREDENTIAL_FILE):
        with open(CREDENTIAL_FILE) as f_credential_r:
            credentials_json = json.loads(f_credential_r.read())
            credentials = google.oauth2.credentials.Credentials(
                credentials_json["token"],
                refresh_token=credentials_json["_refresh_token"],
                token_uri=credentials_json["_token_uri"],
                client_id=credentials_json["_client_id"],
                client_secret=credentials_json["_client_secret"],
            )
    else:
        notify_line("Oauth認証が必要です")
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes=SCOPES
        )
        credentials = flow.run_console()
    with open(CREDENTIAL_FILE, mode="w") as f_credential_w:
        f_credential_w.write(
            json.dumps(
                vars(credentials), default=support_datetime_default, sort_keys=True
            )
        )

    return credentials


def download_file(item):
    photo_download_format = "{base}=w{width}-h{height}"
    base_url = item.get("baseUrl")
    metadata = item.get("mediaMetadata")
    filename = os.getenv("DOWNLOAD_DIR_ABS_PATH") + "/" + item.get("filename")
    download_url = photo_download_format.format(
        base=base_url, width=metadata["width"], height=metadata["height"]
    )
    urllib.request.urlretrieve(download_url, filename)
    return filename


def getGooglePhotoService():
    credentials = getCredentials()
    service = build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials, static_discovery=False
    )
    try:
        item = service.mediaItems().list(pageSize=1).execute()
    except:
        os.remove(CREDENTIAL_FILE)
        credentials = getCredentials()
        service = build(
            API_SERVICE_NAME,
            API_VERSION,
            credentials=credentials,
            static_discovery=False,
        )

    return service


def download_latest_image():
    service = getGooglePhotoService()
    remote_target_photo = (
        service.mediaItems().list(pageSize=1).execute()["mediaItems"][0]
    )
    file_path = download_file(remote_target_photo)
    return file_path
