import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
import random

# Simulated similarity scores
genuine_scores = np.random.normal(loc=90, scale=5, size=50)  # Genuine signatures
forged_scores = np.random.normal(loc=50, scale=10, size=50)  # Forged signatures

genuine_scores = np.clip(genuine_scores, 60, 100)
forged_scores = np.clip(forged_scores, 0, 70)

# Combine data
all_scores = np.concatenate([genuine_scores, forged_scores])
labels = np.array([1] * 50 + [0] * 50)  # 1 = Genuine, 0 = Forged

# Plot histogram
plt.figure(figsize=(8, 6))
sns.histplot(genuine_scores, label='Genuine', kde=True, color='blue', bins=15)
sns.histplot(forged_scores, label='Forged', kde=True, color='red', bins=15)
plt.xlabel('Similarity Score')
plt.ylabel('Frequency')
plt.title('Distribution of Signature Similarity Scores')
plt.legend()
plt.show()

# Accuracy vs. Threshold
thresholds = np.linspace(40, 100, 20)
accuracies = [accuracy_score(labels, all_scores >= t) for t in thresholds]

plt.figure(figsize=(8, 6))
plt.plot(thresholds, accuracies, marker='o', linestyle='-')
plt.xlabel('Similarity Threshold')
plt.ylabel('Accuracy')
plt.title('Model Accuracy vs. Similarity Threshold')
plt.grid()
plt.show()

# Confusion Matrix (assuming threshold = 75)
predictions = all_scores >= 75
cm = confusion_matrix(labels, predictions)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Forged', 'Genuine'], yticklabels=['Forged', 'Genuine'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
