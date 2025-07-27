# tools/detect_fraud.py

def classify_fraud_in_input(query: str) -> str | None:
    suspicious_keywords = [
        "bypass", "hack", "override", "access someone else's account",
        "steal", "unauthorized", "malicious", "transfer without consent"
    ]

    for keyword in suspicious_keywords:
        if keyword in query.lower():
            return "Suspicious activity detected. This session has been flagged for review."

    return None
