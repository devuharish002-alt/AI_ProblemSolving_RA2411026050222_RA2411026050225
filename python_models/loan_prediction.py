"""
Loan Approval Prediction System
Problem Statement 19 Implementation
Algorithm: K-Nearest Neighbors (KNN)
Implementation: Pure Python (No external libraries)
"""

import math
import random

class LoanDataGenerator:
    """Class responsible for generating synthetic financial data."""
    
    def __init__(self, num_samples: int = 200, seed: int = 42):
        self.num_samples = num_samples
        random.seed(seed)
        self.dataset = []

    def generate(self) -> list:
        """Generates synthetic loan applications based on defined logic."""
        for _ in range(self.num_samples):
            income = random.randint(20000, 120000)
            credit = random.randint(300, 850)
            emp = random.choice([0, 1, 2]) # 0=Unemployed, 1=Self, 2=Employed
            loan = random.randint(5000, 50000)
            
            # Logical target generation
            score = (income / 120000) * 0.4 + (credit / 850) * 0.4 + (emp / 2) * 0.2
            approved = 1 if score > 0.55 else 0 
            
            self.dataset.append(([income, credit, emp, loan], approved))
        return self.dataset

class KNNClassifier:
    """Custom implementation of the K-Nearest Neighbors Algorithm."""
    
    def __init__(self, k: int = 5):
        self.k = k
        self.train_data = []
        self.max_vals = [120000, 850, 2, 50000] # For feature normalization

    def fit(self, train_data: list):
        """Loads training data into the model."""
        self.train_data = train_data

    def _euclidean_distance(self, row1: list, row2: list) -> float:
        """Calculates normalized Euclidean distance between two data points."""
        distance = 0.0
        for i in range(len(row1)):
            norm1 = row1[i] / self.max_vals[i]
            norm2 = row2[i] / self.max_vals[i]
            distance += (norm1 - norm2) ** 2
        return math.sqrt(distance)

    def predict(self, test_row: list) -> int:
        """Predicts the class label for a given test row."""
        distances = []
        for train_row, label in self.train_data:
            dist = self._euclidean_distance(test_row, train_row)
            distances.append((dist, label))
        
        # Sort by closest distance
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:self.k]
        
        # Calculate majority vote
        votes = [label for _, label in neighbors]
        return max(set(votes), key=votes.count)

    def evaluate(self, test_data: list) -> float:
        """Evaluates model accuracy against a test dataset."""
        correct = 0
        for test_row, actual_label in test_data:
            prediction = self.predict(test_row)
            if prediction == actual_label:
                correct += 1
        return correct / float(len(test_data))

def main():
    print("="*50)
    print(" AI LOAN APPROVAL PREDICTOR (KNN) ".center(50, "="))
    print("="*50)

    # 1. Generate Data
    print("\n[System] Generating synthetic financial dataset...")
    generator = LoanDataGenerator(num_samples=200)
    data = generator.generate()

    # 2. Split Data
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]
    print(f"[System] Data split: {len(train_data)} Train | {len(test_data)} Test")

    # 3. Train & Evaluate Model
    model = KNNClassifier(k=5)
    model.fit(train_data)
    
    accuracy = model.evaluate(test_data)
    print(f"[System] Model trained successfully.")
    print(f"[Result] Validation Accuracy: {accuracy * 100:.2f}%\n")

    # 4. Interactive Testing
    print("-" * 50)
    print("Test a New Applicant:")
    test_income = int(input("Enter Annual Income ($): ") or 75000)
    test_credit = int(input("Enter Credit Score (300-850): ") or 720)
    print("Employment Status: [0] Unemployed  [1] Self-Employed  [2] Employed")
    test_emp = int(input("Enter Status Code: ") or 2)
    test_loan = int(input("Enter Loan Amount ($): ") or 20000)

    features = [test_income, test_credit, test_emp, test_loan]
    prediction = model.predict(features)

    print("\n" + "="*50)
    if prediction == 1:
        print(" FINAL DECISION: LOAN APPROVED ".center(50, " "))
    else:
        print(" FINAL DECISION: LOAN REJECTED ".center(50, " "))
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
