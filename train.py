import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

# read the data
df = pd.read_csv(r"C:\Users\raghotham\Downloads\cleaned_data - cleaned_data.csv (4).csv")

# convert the glucose column to numerical values
glucose_map = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8
}
df['Glucose'] = df['Glucose'].map(glucose_map)

# engineer new features
df['BMI_Insulin'] = df['BMI'] * df['Insulin']
df['Age_BMI'] = df['Age'] * df['BMI']
df['Age_BloodPressure'] = df['Age'] * df['BloodPressure']
df['Age_SkinThickness'] = df['Age'] * df['SkinThickness']
df['Insulin_BloodPressure'] = df['Insulin'] * df['BloodPressure']
df['Insulin_SkinThickness'] = df['Insulin'] * df['SkinThickness']
df['SkinThickness_BloodPressure'] = df['SkinThickness'] * df['BloodPressure']

# remove outliers using IQR method
Q1 = df.drop('Glucose', axis=1).quantile(0.25)
Q3 = df.drop('Glucose', axis=1).quantile(0.75)
IQR = Q3 - Q1
df = df[~((df.drop('Glucose', axis=1) < (Q1 - 1.5 * IQR)) |(df.drop('Glucose', axis=1) > (Q3 + 1.5 * IQR))).any(axis=1)]

# split the data into training and testing sets
X = df.drop('Glucose', axis=1)
y = df['Glucose']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# scale the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# define the base models
rf = RandomForestClassifier(n_estimators=100, random_state=42)
dt = DecisionTreeClassifier(random_state=42)
knn = KNeighborsClassifier()
svm = SVC(probability=True, random_state=42)
mlp = MLPClassifier(random_state=42)

# define the ensemble model
ensemble = VotingClassifier(
    estimators=[
        ('rf', rf),
        ('dt', dt),
        ('knn', knn),
        ('svm', svm),
        ('mlp', mlp)
    ],
    voting='soft'
)

# train the ensemble model
ensemble.fit(X_train, y_train)

# evaluate the model
y_pred = ensemble.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)
