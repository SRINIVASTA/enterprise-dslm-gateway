import tempfile
import os

def upload_to_google_ai(api_key: str, display_name: str, text_content: str) -> dict:
    """
    Streams a plain text log dump payload directly to the Google File API ecosystem
    using the official, path-hardened Google GenAI client library.
    """
    if not api_key or not text_content.strip():
        return {"status": "error", "message": "Missing active credentials or payload assets."}
        
    try:
        # 🌐 Initialize the official, automated client session
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Write text buffer payload locally to a temporary secure transient file descriptor
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
            temp_file.write(text_content)
            temp_file_path = temp_file.name
            
        try:
            print(f"📡 Dispatching official file manager payload mapping stream...")
            # Route chunk arrays using Google's native hardened client protocol channel
            file_ref = client.files.upload(
                file=temp_file_path,
                config={"display_name": display_name}
            )
            
            # Clear up local memory space allocations immediately
            os.remove(temp_file_path)
            
            return {
                "status": "success",
                "uri": file_ref.uri
            }
        except Exception as upload_error:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise upload_error
            
    except Exception as e:
        return {"status": "error", "message": f"Google AI Library Upload Exception: {str(e)}"}
