import re

def mask_sensitive_data(text: str) -> str:
    """Finds IPv4 addresses and strips them out for enterprise privacy."""
    if not text:
        return ""
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.sub(ip_pattern, "[MASKED_IP_ADDRESS]", text)
