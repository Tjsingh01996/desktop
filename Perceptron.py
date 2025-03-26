import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score

class PerceptronNoLearningRate:
    def __init__(self, n_iterations=1000):
        self.n_iterations = n_iterations  # Number of iterations
        self.w = None  # Weights
        self.b = None  # Bias
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)  # Initialize weights to 0
        self.b = 0  # Initialize bias to 0
        
        for _ in range(self.n_iterations):
            for i, Xi in enumerate(X):
                # Perceptron Update Rule: w = w + y_i * X_i, b = b + y_i
                if y[i] * (np.dot(Xi, self.w) + self.b) <= 0:  # Misclassified point
                    self.w += y[i] * Xi  # Update weights
                    self.b += y[i]  # Update bias
        
        return self.w, self.b
    
    def predict(self, X):
        # Predict using the sign of the decision function
        pred = np.dot(X, self.w) + self.b
        return [1 if val > 0 else -1 for val in pred]  # Return 1 or -1 based on the sign

# Plotting function to visualize the result
def plot_perceptron(X, y, w, b, title="Perceptron Classification (No Learning Rate)"):
    plt.scatter(X[:, 0], X[:, 1], marker='o', c=y)
    
    # Plot the decision boundary
    x0_1 = np.amin(X[:, 0])
    x0_2 = np.amax(X[:, 0])
    x1_1 = (-w[0] * x0_1 - b) / w[1]
    x1_2 = (-w[0] * x0_2 - b) / w[1]
    
    plt.plot([x0_1, x0_2], [x1_1, x1_2], 'k--')  # Decision boundary
    plt.title(title)
    plt.show()

# Example usage
perceptron = PerceptronNoLearningRate(n_iterations=1000)

# Generate a simple dataset
X, y = make_blobs(n_samples=200, centers=2, random_state=0, cluster_std=0.60)
y = np.where(y <= 0, -1, 1)  # Convert labels to -1 and 1

# Train the Perceptron model
w, b = perceptron.fit(X, y)

# Evaluate accuracy
y_pred = perceptron.predict(X)
print("Accuracy:", accuracy_score(y, y_pred))

# Plot the result
plot_perceptron(X, y, w, b, title='Perceptron Without Learning Rate')
