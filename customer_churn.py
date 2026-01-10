import pandas as pd
import numpy as np
import tensorflow as tf
import streamlit as st
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# ------------------- Load and preprocess once -------------------
if "model" not in st.session_state:
    df = pd.read_csv(r"C:\Users\Admin\AVSCODE\TENSOFLOW KERAS\Churn_Modelling.csv")

    # Data preprocessing
    x = df.iloc[:, 3:-1].values
    y = df.iloc[:, -1].values

    le = LabelEncoder()
    x[:, 2] = le.fit_transform(x[:, 2])

    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
    x = np.array(ct.fit_transform(x))

    sc = StandardScaler()
    x = sc.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0)

    # Build ANN
    ann = tf.keras.models.Sequential([
        tf.keras.layers.Dense(units=6, activation='relu'),
        tf.keras.layers.Dense(units=6, activation='relu'),
        tf.keras.layers.Dense(units=5, activation='relu'),
        tf.keras.layers.Dense(units=4, activation='relu'),
        tf.keras.layers.Dense(units=1, activation='sigmoid')
    ])
    ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    st.session_state["data"] = (x_train, x_test, y_train, y_test)
    st.session_state["encoders"] = (le, ct, sc)
    st.session_state["model"] = ann

# ------------------- UI Section -------------------
st.title("Customer Churn Prediction App")

# Train model only on button click
if st.button("🧠 Train Model"):
    with st.spinner("Training ANN..."):
        x_train, x_test, y_train, y_test = st.session_state["data"]
        ann = st.session_state["model"]
        ann.fit(x_train, y_train, batch_size=32, epochs=5, validation_data=(x_test, y_test))
        st.session_state["trained"] = True
    st.success("✅ Model training complete!")

# Sidebar Inputs (user interaction won’t retrigger training)
st.sidebar.header("Input Features")
credit_score = st.sidebar.number_input("Credit Score", min_value=0)
geography = st.sidebar.selectbox("Geography", ("Delhi", "Mumbai", "Hyd"))
gender = st.sidebar.selectbox("Gender", ("Female", "Male"))
age = st.sidebar.number_input("Age", min_value=0)
tenure = st.sidebar.number_input("Tenure", min_value=0)
balance = st.sidebar.number_input("Balance", min_value=0.0, format="%.2f")
num_of_products = st.sidebar.number_input("Number of products", min_value=1, max_value=4)
has_cr_card = st.sidebar.selectbox("Has Credit Card", (0, 1))
is_active_member = st.sidebar.selectbox("Is Active Member", (0, 1))
estimated_salary = st.sidebar.number_input("Estimated Salary", min_value=0.0, format="%.2f")

# Predict only when button clicked
if st.button("🔮 Predict"):
    if "trained" not in st.session_state:
        st.warning("Please train the model first.")
    else:
        le, ct, sc = st.session_state["encoders"]
        model = st.session_state["model"]

        user_data = np.array([[credit_score, geography, gender, age, tenure,
                               balance, num_of_products, has_cr_card, is_active_member, estimated_salary]])

        user_data[:, 2] = le.transform(user_data[:, 2])
        user_data = ct.transform(user_data)
        user_data = sc.transform(user_data)

        prediction = (model.predict(user_data) > 0.5)[0][0]
        result = "🚨 Churn" if prediction == 1 else "✅ No Churn"
        st.subheader(f"Prediction: {result}")