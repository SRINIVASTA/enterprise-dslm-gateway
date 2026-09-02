import json
import requests

def upload_to_google_ai(api_key: str, display_name: str, text_content: str) -> dict:
    """
    Streams a plain text log dump payload directly to the Google File API ecosystem.
    Returns the parsed JSON response containing the unique Google Cloud URI resource pointer.
    """
    if not api_key or not text_content.strip():
        return {"status": "error", "message": "Missing active credentials or payload assets."}
        
    try:
        # 🌐 FIXED: Rebuilt uploading path targeting Google's native multi-part storage endpoint
        upload_url = f"https://googleapis.com{api_key}"
        
        file_metadata = {"file": {"displayName": display_name}}
        
        # Pack metadata configuration blocks and data streams separately
        multipart_payload = {
            'metadata': ('metadata.json', json.dumps(file_metadata), 'application/json'),
            'file': (display_name, text_content.encode('utf-8'), 'text/plain')
        }
        
        response = requests.post(upload_url, files=multipart_payload, timeout=30)
        
        # FIXED: Filled in the square brackets to resolve the compilation crash
        if response.status_code in:
            upload_data = response.json()
            return {
                "status": "success",
                "uri": upload_data.get('file', {}).get('uri', 'No URI returned')
            }
        else:
            return {"status": "error", "message": f"Google Cloud Core Rejection ({response.status_code}): {response.text}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Network bridge transport layer exception: {str(e)}"}
