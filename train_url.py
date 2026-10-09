import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from features import url_features, FEATURE_NAMES

df = pd.read_csv("data/phishing_site_urls.csv")
df = df.sample(100000, random_state=42)
df["y"] = (df["Label"] == "bad").astype(int)

X = pd.DataFrame([url_features(u) for u in df["URL"]])[FEATURE_NAMES]
X_train, X_test, y_train, y_test = train_test_split(
    X, df["y"], test_size=0.2, random_state=42, stratify=df["y"])

clf = RandomForestClassifier(n_estimators=150, n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)

print(classification_report(y_test, clf.predict(X_test)))
joblib.dump(clf, "url_model.joblib")