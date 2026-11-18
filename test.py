from user_agents import parse


def enrich_data(data):
    user_agent = parse(data["user_agent"])
    data["browser"] = user_agent.browser.family
    data["os"] = user_agent.os.family
    data["device"] = user_agent.device.family
    data["is_mobile"] = user_agent.is_mobile
    data["is_tablet"] = user_agent.is_tablet
    data["is_pc"] = user_agent.is_pc
    return data


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Android) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]


# for agent in user_agents:
#     d = enrich_data({"user_agent": agent})
#
#     for k, v in d.items():
#         print(k, v)
#
#     print("=" * 30)


def parse_user_agent(user_agent):
    try:
        ua = parse(user_agent)
    except Exception:
        return {
            "browser": "unknown",
            "os": "unknown",
            "device": "unknown",
            "is_mobile": "unknown",
            "is_tablet": "unknown",
            "is_pc": "unknown"
        }
    else:
        return {
            "browser": ua.browser.family,
            "os": ua.os.family,
            "device": ua.device.family,
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc
        }


from urllib.parse import urlparse


def extract_domain(url):
    if not url:
        return "http://127.0.0.1:5000"
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"  # Extracts http/https + domain


# Test cases
print(extract_domain("http://127.0.0.1:5000/page3"))  # ✅ Expected: "http://127.0.0.1:5000"
print(extract_domain("https://secure.bankofamerica.com/login"))  # ✅ Expected: "https://secure.bankofamerica.com"
print(extract_domain("https://www.google.com/search?q=test"))  # ✅ Expected: "https://www.google.com"
print(extract_domain("ftp://example.com/files"))
