import io
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import uuid
from PIL import Image

class DriveUploader:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file('assets/unisysva-b828ca34cf61.json')
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    
    def upload_image_to_drive(self, image, folder_id):
        if isinstance(image, Image.Image):
            image_buffer = io.BytesIO()
            image.save(image_buffer, format='JPEG')
            mimetype = 'image/jpeg'
        else:
            try:
                mimetype = mimetypes.guess_type(image)[0]
                with open(image, 'rb') as f:
                    media = MediaIoBaseUpload(f, mimetype=mimetype)
            except TypeError:
                image_buffer = io.BytesIO()
                image_buffer.write(image)
                mimetype = 'image/jpeg'

        # Ensure media is assigned before attempting upload
        media = MediaIoBaseUpload(image_buffer, mimetype=mimetype)  # Moved outside try/except to ensure assignment

        file_name = str(uuid.uuid4()) + '.jpg'
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        try:
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('Image uploaded successfully. File ID:', file.get('id'))
        except Exception as e:
            print(f"Error uploading image: {e}")  # Handle any remaining errors during upload