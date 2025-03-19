import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.title("🚀 Growth Mindset Challenge")

# User Input
st.markdown("### 📚 Daily Learning")
learning = st.text_area("", placeholder="What did you learn today?")
st.markdown("### ⚡ Challenges")
challenges = st.text_area("", placeholder="What challenges did you face?")
st.markdown("### 💭 Reflections")
reflections = st.text_area("", placeholder="What key insights did you gain today?")
st.markdown("### 🌟 Self-Assessment")
rating = st.slider("Rate your daily growth (1-5)", 1, 5, 3)

# Session state to store data in memory
if "entries" not in st.session_state:
    st.session_state.entries = pd.DataFrame(columns=["Date", "Daily Learning", "Challenges", "Reflections", "Rating"])

# Function to Generate Download Link
def get_download_link(df, file_format="csv"):
    buffer = BytesIO()
    
    if file_format == "csv":
        df.to_csv(buffer, index=False)
        mime_type = "text/csv"
        file_ext = "csv"
    else:
        df.to_excel(buffer, index=False, engine="openpyxl")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_ext = "xlsx"
    
    buffer.seek(0)
    return st.download_button(f"📥 Download as {file_ext.upper()}", buffer, f"growth_mindset_data.{file_ext}", mime=mime_type)

# Save Data in Memory
if st.button("Submit"):
    if not learning or not challenges or not reflections:
        st.warning("⚠️ Please fill all fields before submitting.")
    else:
        new_data = {"Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "Daily Learning": learning, 
                    "Challenges": challenges, 
                    "Reflections": reflections,
                    "Rating": rating}
        new_df = pd.DataFrame([new_data])
        
        # Append new data to session state (memory only, no file saving)
        st.session_state.entries = pd.concat([st.session_state.entries, new_df], ignore_index=True)
        
        st.success("✅ Your entry has been saved successfully!")

# Display Data
if not st.session_state.entries.empty:
    st.write("### Your Previous Entries:")
    st.dataframe(st.session_state.entries)
    
    # Calculate Average Rating
    avg_rating = st.session_state.entries["Rating"].mean()
    st.write(f"### 📊 Average Growth Rating: {avg_rating:.2f} ⭐")
    
    # Progress Bar for Average Rating
    st.progress(avg_rating / 5)
    
    # Feedback Message
    if avg_rating >= 4:
        st.success("🚀 Great job! You're consistently improving. Keep it up! 💪")
    elif avg_rating >= 3:
        st.info("😊 Good progress! A little more effort can make a big difference.")
    else:
        st.warning("📉 Don't worry! Keep learning and reflecting, and you'll improve in no time. 💡")
    
    # Show Download Buttons
    st.write("### 📂 Download Your Data:")
    get_download_link(st.session_state.entries, "csv")
    get_download_link(st.session_state.entries, "xlsx")
    
    # Data Visualization
    st.write("### 📈 Progress Over Time")
    
    # Convert Date column to datetime
    st.session_state.entries["Date"] = pd.to_datetime(st.session_state.entries["Date"])
    
    # Line Chart for Ratings Over Time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(st.session_state.entries["Date"], st.session_state.entries["Rating"], marker='o', linestyle='-', color='b', label="Daily Rating")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Rating", fontsize=12)
    ax.set_title("Daily Growth Rating Over Time", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
