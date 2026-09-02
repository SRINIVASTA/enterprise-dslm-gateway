import json
import requests

def upload_to_google_ai(api_key: str, display_name: str, text_content: str) -> dict:
    """Streams a plain text log dump payload directly to the Google File API ecosystem."""
    if not api_key or not text_content.strip():
        return {"status": "error", "message": "Missing active credentials or payload assets."}
        
    try:
        # 🌐 FIXED: Rebuilt uploading path targeting Google's native multi-part storage endpoint
        upload_url = "https://googleapis.com"
        
        # Inject key through the headers block to protect the upload stream domain
        headers = {
            "x-goog-api-key": api_key
        }
        
        file_metadata = {"file": {"displayName": display_name}}
        multipart_payload = {
            'metadata': ('metadata.json', json.dumps(file_metadata), 'application/json'),
            'file': (display_name, text_content.encode('utf-8'), 'text/plain')
        }
        
        # Pass headers alongside multi-part form parameters
        response = requests.post(upload_url, files=multipart_payload, headers=headers, timeout=30)
        
        if response.status_code in (200, 201):
            upload_data = response.json()
            return {
                "status": "success",
                "uri": upload_data.get('file', {}).get('uri', 'No URI returned')
            }
        else:
            return {"status": "error", "message": f"Google Cloud Core Rejection ({response.status_code}): {response.text}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Network bridge transport layer exception: {str(e)}"}
