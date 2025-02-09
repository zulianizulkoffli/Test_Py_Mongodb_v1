# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 12:40:57 2025

@author: zzulk
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://admin:admin@cluster0.qa6yj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# Select Database and Collection
db = client["university"]
collection = db["students"]

# Streamlit App
st.title("📚 Student Database Viewer")

# Fetch Data
students = list(collection.find({}, {"_id": 0}))  # Exclude ObjectId

if students:
    df = pd.DataFrame(students)
    st.dataframe(df)

    # 📊 Bar Chart: Age Distribution
    st.subheader("📊 Age Distribution")
    fig, ax = plt.subplots()
    df["age"].value_counts().sort_index().plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

    # 🏫 Pie Chart: Course Distribution
    st.subheader("🏫 Course Distribution")
    fig, ax = plt.subplots()
    df["course"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90, colors=["lightcoral", "lightblue", "lightgreen"])
    st.pyplot(fig)

else:
    st.warning("No student records found!")

# Insert Data Form
st.subheader("➕ Add a New Student")
with st.form("student_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        new_student = {"name": name, "age": age, "course": course}
        collection.insert_one(new_student)
        st.success(f"🎉 {name} has been added!")
        st.rerun()  # Refresh after adding data

