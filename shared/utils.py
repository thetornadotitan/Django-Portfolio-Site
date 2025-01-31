import re
from urllib.parse import urlparse

# Regular expression to match iframe tags and extract the src URLs
IFRAME_SRC_REGEX = r'<iframe[^>]*\s+src=["\'](https?://[^"\']+)["\'][^>]*>'

# List of allowed domains for iframe URLs
ALLOWED_DOMAINS = {
    'youtube.com',
    'google.com',
    'vimeo.com',
    'vine.co',
    'instagram.com',
    'dailymotion.com',
    'youku.com',
    'peertube.co',
}

def is_valid_url(url):
    """Check if the URL is a valid HTTP/HTTPS URL."""
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme in {'http', 'https'} and bool(parsed_url.netloc)
    except Exception:
        return False

def is_allowed_iframe(url):
    """Check if the URL is from one of the allowed domains."""
    if not is_valid_url(url):
        return False

    # Extract domain from URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')  # Remove 'www.' prefix if present

    return domain in ALLOWED_DOMAINS

def clean_iframes(content):
    """Filter out iframes that are not from allowed domains by removing the entire iframe tag."""
    def iframe_filter(match):
        iframe_url = match.group(1)
        return match.group(0) if is_allowed_iframe(iframe_url) else ''  # Keep allowed, remove disallowed

    return re.sub(IFRAME_SRC_REGEX, iframe_filter, content)

def replace_font_quotes(content):
    """Replace HTML-escaped double quotes with single quotes."""
    return content.replace('&quot;', "'")