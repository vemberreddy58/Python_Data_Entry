import streamlit as st
import pyodbc

# ---------- Database Connection ----------
def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=QHYDL2603;"   # or . , or localhost\SQLEXPRESS
            "DATABASE=TestDB;"    # change to your DB name
            "UID=JobOwnerUser;"
            "PWD=SQL123@;"
            "Trusted_Connection=yes;"  # Windows Auth
            #need to remove windows auth 
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# ---------- Insert Data ----------
def insert_data(name, age, email):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO PersonData (Name, Age, Email) VALUES (?, ?, ?)",
                (name, age, email)
            )
            conn.commit()
            st.success("✅ Data inserted successfully!")
        except Exception as e:
            st.error(f"Error inserting data: {e}")
        finally:
            cursor.close()
            conn.close()

# ---------- Streamlit UI ----------
st.title("📌 Streamlit to SQL Server App")  

with st.form("data_form"):
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=1, max_value=120, step=1)
    email = st.text_input("Enter Email")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and email:
            insert_data(name, age, email)
        else:
            st.warning("⚠️ Please fill in all required fields.")
