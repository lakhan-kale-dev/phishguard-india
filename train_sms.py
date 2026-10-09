import pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("data/spam.csv", encoding="latin-1")[["v1", "v2"]]
df.columns = ["label", "text"]
df["label"] = (df["label"] == "spam").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df.text, df.label, test_size=0.2, random_state=42, stratify=df.label)

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), stop_words="english"),
    LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))
joblib.dump(model, "sms_model.joblib")