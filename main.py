# importing libraries
import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Setting Page Layout
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Application setup
st.write("<h1 class='title'>🔄 FILE CONVERSION & 🧹 DATA CLEANING </h1>", unsafe_allow_html=True)

def styling_css():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

styling_css()

st.write("<p class='subtitle1'>Transform your files between CSV and Excel with built-in data and visualization </p>", unsafe_allow_html=True)

# File Uploading
upload_files = st.file_uploader("Upload your file (CSV or Excel) in below section : 👇", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file, encoding='ISO-8859-1')
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"{file_ext} : File type is not supported")
            continue

        # Displaying the information about the uploaded file
        st.write(f"<p class='file_name'>** File Name :** {file.name} </p>", unsafe_allow_html=True)
        st.write(f"<p class='file_size'>** File Size :** {file.size/1024} </p>", unsafe_allow_html=True)

        # Show 5 rows of our data frame(df)
        st.subheader("🔎 Preview the Head of the Data Frame")
        st.dataframe(df.head())

        # Options for Data Cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)

            with col1:
                if st.button(f"Removes Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed !")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled !")

        # Choose specific column to keep or convert

        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose column for {file.name}" , df.columns, default=df.columns)
        df = df[columns]

        # Create some Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.line_chart(df.select_dtypes(include='number').iloc[:,:2])

        # File Conversion -> CSV to Excel
        st.subheader("🔄 File Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to :", ["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.malformations-office document.spreadsheet.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed!")
