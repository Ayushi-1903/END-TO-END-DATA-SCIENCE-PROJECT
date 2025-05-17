# COLAB OR LOCAL SCRIPT
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load your local dataset
data = pd.read_csv(r'C:\School\student_data.csv')

print("Columns:", data.columns)

# ✅ Select target — adjust depending on what you want
if 'Result' in data.columns:
    # Convert 'Pass' / 'Fail' to binary 1/0
    data['Pass'] = data['Result'].apply(lambda x: 1 if str(x).lower() == 'pass' else 0)
elif 'BACKLOG' in data.columns:
    # Use BACKLOG: 0 = pass, >0 = fail
    data['Pass'] = data['BACKLOG'].apply(lambda x: 1 if x == 0 else 0)
else:
    raise ValueError("No suitable target column found! Please provide 'Result' or 'BACKLOG'.")

# ✅ Select numeric features (adjust based on your data)
X = data[['Python', 'C_Programming', 'DSA', 'DMP']]  # assuming these are numeric scores
y = data['Pass']

# Handle missing values if any
X = X.fillna(0)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Save model
with open('student_pass_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print(" Model saved as 'student_pass_model.pkl'")
