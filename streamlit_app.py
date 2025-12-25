import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

st.title("🍽️ Local Food Wastage Management System")
st.markdown("Connecting surplus food providers with people in need")

# ---------------- DATABASE CONNECTION ----------------
DB_PATH = "food_wastage.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

conn = get_connection()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Menu")
section = st.sidebar.selectbox(
    "Select Section",
    [
        "Dashboard",
        "SQL Queries Output",
        "Food Listings",
        "Claims Analysis"
    ]
)

if section == "SQL Queries Output":
    st.header("📊 SQL Query Results")

    st.subheader("1️⃣ Providers Count per City")

    query1 = """
    SELECT City, COUNT(*) AS provider_count
    FROM providers
    GROUP BY City
    """
    df1 = pd.read_sql(query1, conn)
    st.dataframe(df1)
    
    st.subheader("2️⃣ Providers & Receivers Count per City")

    query2 = """
    SELECT 
    p.City,
    COUNT(DISTINCT p.Provider_ID) AS providers,
    COUNT(DISTINCT r.Receiver_ID) AS receivers
    FROM providers p
    LEFT JOIN receivers r ON p.City = r.City
    GROUP BY p.City
    """

    df2 = pd.read_sql(query2, conn)
    st.dataframe(df2)

    st.subheader("3️⃣ Provider Type Contribution")

    query3 = """
    SELECT Provider_Type, COUNT(*) AS total_listings
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY total_listings DESC
    """

    df3 = pd.read_sql(query3, conn)
    st.dataframe(df3)

    st.subheader("4️⃣ Most Claimed Food Items")

    query4 = """
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY total_claims DESC
    """

    df4 = pd.read_sql(query4, conn)
    st.dataframe(df4)

    st.subheader("5️⃣ Total Quantity of Food Available")

    query5 = """
    SELECT SUM(Quantity) AS total_food_quantity
    FROM food_listings
    """

    df5 = pd.read_sql(query5, conn)
    st.dataframe(df5)

    st.subheader("6️⃣ City with Highest Food Listings")

    query6 = """
    SELECT Location AS City, COUNT(*) AS total_listings
    FROM food_listings
    GROUP BY Location
    ORDER BY total_listings DESC
    """

    df6 = pd.read_sql(query6, conn)
    st.dataframe(df6)

    st.subheader("7️⃣ Most Common Food Types")

    query7 = """
    SELECT Food_Type, COUNT(*) AS count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY count DESC
    """

    df7 = pd.read_sql(query7, conn)
    st.dataframe(df7)

    st.subheader("8️⃣ Number of Claims per Food Item")

    query8 = """
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS claim_count
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY claim_count DESC
    """

    df8 = pd.read_sql(query8, conn)
    st.dataframe(df8)

    st.subheader("9️⃣ Provider with Highest Successful Claims")

    query9 = """
    SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY successful_claims DESC
    """

    df9 = pd.read_sql(query9, conn)
    st.dataframe(df9)

    st.subheader("🔟 Claim Status Distribution")

    query10 = """
    SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS percentage
    FROM claims
    GROUP BY Status
    """

    df10 = pd.read_sql(query10, conn)
    st.dataframe(df10)

    st.subheader("1️⃣1️⃣ Average Quantity Claimed per Receiver")

    query11 = """
    SELECT r.Name, AVG(f.Quantity) AS avg_quantity
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY r.Name
    """

    df11 = pd.read_sql(query11, conn)
    st.dataframe(df11)

    st.subheader("1️⃣2️⃣ Most Claimed Meal Types")

    query12 = """
    SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY total_claims DESC
    """

    df12 = pd.read_sql(query12, conn)
    st.dataframe(df12)

    st.subheader("1️⃣3️⃣ Total Food Donated by Each Provider")

    query13 = """
    SELECT p.Name, SUM(f.Quantity) AS total_donated
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name
    ORDER BY total_donated DESC
    """

    df13 = pd.read_sql(query13, conn)
    st.dataframe(df13)
    
    st.subheader("1️⃣4️⃣ Total Food Available vs Total Claims")

    query14 = """
    SELECT 
    (SELECT SUM(Quantity) FROM food_listings) AS total_available,
    (SELECT COUNT(*) FROM claims) AS total_claims;
    """

    df14 = pd.read_sql(query14, conn)
    st.dataframe(df14)
    
    st.subheader("1️⃣5️⃣ City-wise Food Demand")

    query15 = """
    SELECT City, COUNT(*) AS total_claims
    FROM claims
    GROUP BY City
    ORDER BY total_claims DESC;
    """

    df15 = pd.read_sql(query15, conn)
    st.dataframe(df15)

# ---------------- DASHBOARD ----------------
if section == "Dashboard":
    st.subheader("📊 Overall Statistics")

    q1 = "SELECT SUM(Quantity) AS total_food FROM food_listings"
    total_food = pd.read_sql(q1, conn)

    q2 = "SELECT COUNT(*) AS total_providers FROM providers"
    total_providers = pd.read_sql(q2, conn)

    q3 = "SELECT COUNT(*) AS total_receivers FROM receivers"
    total_receivers = pd.read_sql(q3, conn)

    col1, col2, col3 = st.columns(3)
    col1.metric("🥘 Total Food Quantity", int(total_food.iloc[0, 0]))
    col2.metric("🏢 Total Providers", int(total_providers.iloc[0, 0]))
    col3.metric("🤝 Total Receivers", int(total_receivers.iloc[0, 0]))
    
    st.subheader("📈 Food Distribution by Food Type")

    query = """
    SELECT Food_Type, SUM(Quantity) AS total_quantity
    FROM food_listings
    GROUP BY Food_Type
    """

    df = pd.read_sql(query, conn)
    st.bar_chart(df.set_index("Food_Type"))
    
# ---------------- PROVIDERS & RECEIVERS ----------------
elif section == "Providers & Receivers":
    st.subheader("🏙️ Providers per City")

    q = """
    SELECT City, COUNT(*) AS provider_count
    FROM providers
    GROUP BY City
    """
    df = pd.read_sql(q, conn)

    st.dataframe(df)

    fig = px.bar(df, x="City", y="provider_count", title="Providers by City")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOD LISTINGS ----------------
elif section == "Food Listings":
    st.subheader("🥗 Food Listings")

    city_filter = st.selectbox(
        "Filter by City",
        ["All"] + pd.read_sql("SELECT DISTINCT Location FROM food_listings", conn)["Location"].tolist()
    )

    query = "SELECT * FROM food_listings"
    if city_filter != "All":
        query += f" WHERE Location = '{city_filter}'"

    df = pd.read_sql(query, conn)
    st.dataframe(df)

    food_type_count = df["Food_Type"].value_counts().reset_index()
    food_type_count.columns = ["Food_Type", "Count"]

    fig = px.pie(
        food_type_count,
        names="Food_Type",
        values="Count",
        title="Food Type Distribution"
    )
    st.plotly_chart(fig)
    
    st.divider()

    st.subheader("🗑️ Delete Food Listing")

    food_id = st.number_input(
        "Enter Food ID to delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Food"):
        conn.execute(
            "DELETE FROM food_listings WHERE Food_ID = ?",
            (food_id,)
        )
        conn.commit()
        st.success(f"Food listing with ID {food_id} deleted successfully!")


# ---------------- CLAIMS ANALYSIS ----------------
elif section == "Claims Analysis":
    st.subheader("📦 Claims Status Analysis")

    q = """
    SELECT Status, COUNT(*) AS count
    FROM claims
    GROUP BY Status
    """
    df = pd.read_sql(q, conn)

    st.dataframe(df)

    fig = px.pie(
        df,
        names="Status",
        values="count",
        title="Claims Status Breakdown"
    )
    st.plotly_chart(fig)

# ---------------- CLOSE CONNECTION ----------------
conn.close()