from __future__ import print_function
from __future__ import annotations

import pickle
import os.path
from pathlib import Path
from typing import List, Dict
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive"]


def creds_provider(
    filename: Path, creds_filename: Path = "credentials.json"
) -> "Credentials":
    if os.path.exists(filename):
        with open(filename, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_filename,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        with open(filename, "wb") as token:
            pickle.dump(creds, token)


def service_builder(
    creds: "Credentials",
    service: str = "drive",
    version: str = "v3",
) -> "Resource":
    return build(service, version, credentials=creds)


def folder_lister(
    service: "Resource",
    parent_id: str = None,
    fields: str = "files(id, name, md5Checksum, version)",
) -> List[Dict[str, str]]:
    files = (
        service.files()
        .list(
            q=f"parents={parent_id}" if parent_id else "",
            fields=fields,
        )
        .execute()
        .get("files", [])
    )
    return files
