\# PhishGuard India: Scam SMS \& Link Detector



A Python tool that detects scam SMS messages and phishing links common in India

(fake KYC updates, UPI/bank fraud, prize scams, OTP theft) and \*\*explains why\*\* a

message looks suspicious. Built with cyber-crime investigation use cases in mind.



\## Features

\- Classifies input as \*\*Safe / Suspicious / Phishing\*\* with a risk score

\- Gives human-readable \*\*reasons\*\* (urgency language, fake bank domain, bad TLD, OTP request, no HTTPS)

\- Works on a full SMS or a single URL

\- Logs every check to a \*\*CSV report\*\* that can be downloaded for investigation records

\- Simple web interface built with Streamlit



\## Screenshots

!\[Phishing result](screenshots/phishing.png)

!\[Report](screenshots/report.png)



\## How it works

1\. \*\*SMS model:\*\* TF-IDF + Logistic Regression, trained on the SMS Spam Collection dataset

2\. \*\*URL model:\*\* Random Forest on URL features (length, hyphens, suspicious TLD, bank keywords, IP address, subdomains)

3\. \*\*Rule engine:\*\* flags urgency words, bank/KYC names near links, and OTP/PIN requests

4\. The final score combines the models and rules, and each triggered rule is shown as a reason



\## Results

| Model | Accuracy |

|---|---|

| SMS classifier | 98% |

| URL classifier | 85% |



\## Tech stack

Python, pandas, scikit-learn, Streamlit, joblib



\## Run locally

1\. Download from Kaggle: "SMS Spam Collection Dataset" (`spam.csv`) and

&#x20;  "Phishing Site URLs" (`phishing\_site\_urls.csv`). Put both in a `data/` folder.

2\. Install and run:



```

pip install -r requirements.txt

python train\_sms.py

python train\_url.py

streamlit run app.py

```



\## Limitations and future work

\- The SMS dataset is English (UK) spam, so Indian scam patterns are covered mainly by rules. Plan: build an Indian scam SMS dataset

\- No Marathi/Hindi (Devanagari) SMS support yet

\- URL model uses only lexical features. Plan: WHOIS domain age, page content analysis, known-phishing blocklists

\- Plan: replace TF-IDF with a fine-tuned DistilBERT model



\## Author

Lakhan Kale, B.Tech IT (Honours in Cyber Security), Vidyalankar Institute of Technology, Mumbai

