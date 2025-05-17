# main.py

import datetime
import os
from generate_wade_draft import run_gpt_fill_pipeline_minimal
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def format_to_html(title, sections):
    html = f"<html><head><title>{title}</title></head><body>"
    html += f"<h1>{title}</h1>"
    for header, content in sections.items():
        html += f"<h2>{header}</h2><p>{content}</p>"
    html += "</body></html>"
    return html

def upload_html_to_drive(filename, html_content):
    # Save HTML to local temp file
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Load credentials
    service_json = os.getenv("GOOGLE_SERVICE_JSON")
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    creds = Credentials.from_service_account_info(eval(service_json))
    service = build("drive", "v3", credentials=creds)

    # Upload as Google Doc
    file_metadata = {
        "name": filename,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id]
    }
    media = MediaFileUpload("temp.html", mimetype="text/html")
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"✅ Uploaded to Google Drive with file ID: {file.get('id')}")

if __name__ == "__main__":
    result = run_gpt_fill_pipeline_minimal()
    html = format_to_html(result["title"], result["sections"])
    today = datetime.date.today().isoformat()
    filename = f"Expected Torture — {today}"
    upload_html_to_drive(filename, html)
