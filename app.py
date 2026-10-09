import streamlit as st, pandas as pd, joblib, os
from datetime import datetime
from features import (url_features, FEATURE_NAMES, url_reasons,
                      sms_reasons, extract_urls)

sms_model = joblib.load("sms_model.joblib")
url_model = joblib.load("url_model.joblib")

st.title("PhishGuard India: Scam SMS & Link Detector")
text = st.text_area("Paste an SMS or URL here", height=150)

if st.button("Check") and text.strip():
    stripped = text.strip()
    only_url = (" " not in stripped) and ("." in stripped)

    urls = extract_urls(text)
    if only_url and not urls:
        urls = [stripped]

    reasons = sms_reasons(text)
    sms_p = 0.0 if only_url else sms_model.predict_proba([text])[0][1]

    url_p = 0.0
    for u in urls:
        feats = pd.DataFrame([url_features(u)])[FEATURE_NAMES]
        url_p = max(url_p, url_model.predict_proba(feats)[0][1])
        reasons += url_reasons(u)

    score = max(sms_p, url_p)
    score = min(1.0, score + 0.1 * len(reasons))
    if any("OTP" in r for r in reasons):
        score = max(score, 0.75)

    if score >= 0.7:
        verdict = "Phishing"
    elif score >= 0.4:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    {"Phishing": st.error, "Suspicious": st.warning, "Safe": st.success}[verdict](
        f"{verdict} (score: {score:.2f})")

    st.subheader("Reasons")
    for r in (reasons or ["No suspicious signs found"]):
        st.write("- " + r)

    row = pd.DataFrame([{"time": datetime.now().isoformat(timespec="seconds"),
                         "input": text[:200], "verdict": verdict,
                         "score": round(score, 2)}])
    row.to_csv("reports.csv", mode="a", header=not os.path.exists("reports.csv"),
               index=False)

if os.path.exists("reports.csv"):
    st.subheader("Detected cases report")
    df = pd.read_csv("reports.csv")
    st.dataframe(df.tail(10))
    st.download_button("Download report (CSV)", df.to_csv(index=False),
                       "report.csv")