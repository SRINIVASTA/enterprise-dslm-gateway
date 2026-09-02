import re

def mask_sensitive_data(text: str) -> str:
    """Finds valid IPv4 addresses and strips them out for enterprise privacy."""
    if not text:
        return ""
    
    # Strict 0-255 decimal grouping validation regex pattern
    strict_ip_pattern = r'\b(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.sub(strict_ip_pattern, "[MASKED_IP_ADDRESS]", text)
