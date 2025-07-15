import matplotlib
matplotlib.use('Agg')  # ✅ Use non-GUI backend for server-side rendering

import pandas as pd
import numpy as np
import io, base64
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    r2_score,
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# ✅ Utility: Save fig to base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# ✅ 1️⃣ Generalized preprocessing
def preprocess_data(df, target_column):
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in data.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    encoders = {}
    if y.dtype == 'object':
        le_y = LabelEncoder()
        y = le_y.fit_transform(y)
        encoders[target_column] = le_y

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

    X_processed = preprocessor.fit_transform(X)

    return X_processed, y, encoders, preprocessor

# ✅ 2️⃣ Train Classification
def train_classification(df, X, y, target_column):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)

    # Confusion matrix plot
    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title("Confusion Matrix")
    cm_image = fig_to_base64(fig)

    # Class balance plot
    unique, counts = np.unique(y, return_counts=True)
    fig2, ax2 = plt.subplots()
    ax2.bar(unique, counts)
    ax2.set_title("Class Distribution")
    ax2.set_xlabel("Class")
    ax2.set_ylabel("Count")
    balance_image = fig_to_base64(fig2)

    # Group label stats
    group_counts = pd.Series(y).value_counts()
    most_common = group_counts.idxmax()
    least_common = group_counts.idxmin()

    group_summary = (
        f"Most frequent class: {most_common} ({group_counts.max()} samples)\n"
        f"Least frequent class: {least_common} ({group_counts.min()} samples)"
    )

    # Prediction sample
    preds_df = pd.DataFrame({'Actual': y_test, 'Predicted': preds})

    return acc, report, preds_df.head(10), cm_image, balance_image, group_summary

# ✅ 3️⃣ Train Regression
def train_regression(df, X, y, date_col=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # Scatter: Actual vs Predicted
    fig, ax = plt.subplots()
    ax.scatter(y_test, preds)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.set_title("Actual vs Predicted")
    scatter_image = fig_to_base64(fig)

    # Date plot if date_col present
    date_image = None
    if date_col and date_col in df.columns:
        df_copy = df[[date_col, y.name]].dropna()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
        df_copy = df_copy.dropna()

        df_copy = df_copy.sort_values(date_col)
        fig2, ax2 = plt.subplots()
        ax2.plot(df_copy[date_col], df_copy[y.name])
        ax2.set_title(f"{y.name} over Time")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Value")
        date_image = fig_to_base64(fig2)

    preds_df = pd.DataFrame({'Actual': y_test, 'Predicted': np.round(preds, 2)})

    return mse, r2, preds_df.head(10), scatter_image, date_image

# ✅ 4️⃣ Train KNN
def train_knn(df, X, y, target_column):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)

    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', ax=ax)
    ax.set_title("KNN Confusion Matrix")
    cm_image = fig_to_base64(fig)

    # Class balance plot
    unique, counts = np.unique(y, return_counts=True)
    fig2, ax2 = plt.subplots()
    ax2.bar(unique, counts)
    ax2.set_title("KNN Class Distribution")
    ax2.set_xlabel("Class")
    ax2.set_ylabel("Count")
    balance_image = fig_to_base64(fig2)

    group_counts = pd.Series(y).value_counts()
    most_common = group_counts.idxmax()
    least_common = group_counts.idxmin()
    group_summary = (
        f"Most frequent class: {most_common} ({group_counts.max()} samples)\n"
        f"Least frequent class: {least_common} ({group_counts.min()} samples)"
    )

    preds_df = pd.DataFrame({'Actual': y_test, 'Predicted': preds})

    return acc, report, preds_df.head(10), cm_image, balance_image, group_summary
