import re
from urllib.parse import urlparse

BAD_TLDS = {"xyz", "top", "click", "tk", "ml", "ga", "cf", "gq", "buzz", "link"}
BRAND_WORDS = ["sbi", "hdfc", "icici", "axis", "paytm", "phonepe", "upi", "kyc", "bank", "aadhaar", "pan"]
URGENT_WORDS = ["urgent", "immediately", "today", "expire", "expires", "blocked", "suspend",
                "verify", "update", "claim", "winner", "reward", "last chance"]

FEATURE_NAMES = ["length", "num_dots", "num_hyphens", "num_digits", "has_at",
                 "has_ip", "bad_tld", "brand_word", "num_subdomains", "num_slashes"]

def _host(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        return urlparse(url).netloc.lower()
    except ValueError:
        return url.split("//", 1)[-1].split("/")[0].lower()

def url_features(url):
    u = url.lower()
    host = _host(u)
    tld = host.split(".")[-1] if "." in host else ""
    return {
        "length": len(u),
        "num_dots": u.count("."),
        "num_hyphens": u.count("-"),
        "num_digits": sum(c.isdigit() for c in u),
        "has_at": int("@" in u),
        "has_ip": int(bool(re.fullmatch(r"\d+\.\d+\.\d+\.\d+(:\d+)?", host))),
        "bad_tld": int(tld in BAD_TLDS),
        "brand_word": int(any(w in u for w in BRAND_WORDS)),
        "num_subdomains": max(host.count(".") - 1, 0),
        "num_slashes": u.count("/"),
    }

def url_reasons(url):
    f = url_features(url)
    r = []
    if f["has_ip"]: r.append("URL uses an IP address instead of a domain name")
    if f["bad_tld"]: r.append("Suspicious domain ending (.xyz, .top, .tk etc.)")
    if f["brand_word"] and (f["num_hyphens"] >= 1 or f["bad_tld"]):
        r.append("Bank/KYC keyword inside a fake-looking domain")
    if f["has_at"]: r.append("URL contains '@', often used to hide the real site")
    if f["length"] > 75: r.append("URL is unusually long")
    if f["num_subdomains"] >= 3: r.append("Too many subdomains")
    if url.lower().startswith("http://"): r.append("No HTTPS, only HTTP")
    return r

def sms_reasons(text):
    t = text.lower()
    r = []
    hits = [w for w in URGENT_WORDS if w in t]
    if hits: r.append("Creates urgency: " + ", ".join(hits[:3]))
    if any(w in t for w in BRAND_WORDS) and re.search(r"https?://|www\.", t):
        r.append("Bank/KYC name appears together with a link")
    if re.search(r"\b(otp|pin|cvv|password)\b", t):
        r.append("Asks for OTP/PIN/password")
    return r

def extract_urls(text):
    return re.findall(r"(?:https?://|www\.)\S+", text)