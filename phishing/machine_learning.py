import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Load data
import os

# Get the directory where this script (machine_learning.py) is located
base_path = os.path.dirname(__file__)

# Build full paths to the CSV files
legitimate_csv = os.path.join(base_path, "structured_data_legitimate.csv")
phishing_csv = os.path.join(base_path, "structured_data_phishing.csv")

# Read the CSVs safely
legitimate_df = pd.read_csv(legitimate_csv)
phishing_df = pd.read_csv(phishing_csv)


# Combine and shuffle
df = pd.concat([legitimate_df, phishing_df], axis=0).sample(frac=1, random_state=42)
df = df.drop('URL', axis=1).drop_duplicates()
X = df.drop('label', axis=1)
Y = df['label']

# Show class distribution
print("Original class counts:\n", Y.value_counts())

# Stratified train/test split
x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=10, stratify=Y
)
print("Train class counts:\n", y_train.value_counts())
print("Test class counts:\n", y_test.value_counts())

# List of (name, model) tuples for all classifiers
models = [
    ("Random Forest", RandomForestClassifier(n_estimators=60, class_weight='balanced')),
    ("Decision Tree", tree.DecisionTreeClassifier(class_weight='balanced')),
    ("AdaBoost", AdaBoostClassifier()),
    ("Support Vector Machine", svm.LinearSVC()),
    ("Gaussian Naive Bayes", GaussianNB()),
    ("Neural Network", MLPClassifier(alpha=1, max_iter=1000)),
    ("K-Neighbors", KNeighborsClassifier()),
    ("Gaussian Process", GaussianProcessClassifier(1.0 * RBF(1.0)))
]

# Evaluate each model and collect results
results = []
for name, model in models:
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0.0
    print(f"{name} accuracy --> {accuracy}")
    print(f"{name} precision --> {precision}")
    print(f"{name} recall --> {recall}\n")
    results.append([name, accuracy, precision, recall])

# Display results as a table
df_results = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall"])
print(df_results)

# Plot comparison
ax = df_results.set_index('Model')[["Accuracy", "Precision", "Recall"]].plot.bar(rot=15)
plt.ylabel("Score")
plt.ylim(0, 1)
plt.title("Classifier Performance Metrics")
plt.show()
