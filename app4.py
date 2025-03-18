import streamlit as st
import requests
import json

# Base API URL
BASE_URL = "http://localhost:8000"

# Customizing UI
st.set_page_config(page_title="ML Concept Visualizer", page_icon="🤖", layout="wide")

# Sidebar Styling
st.sidebar.image("https://pbs.twimg.com/profile_images/1405548880389984262/9fIM-kvb_400x400.jpg", width=250)
st.sidebar.title("ML Concept Visualizer")
st.sidebar.markdown("Enter an ML concept and receive an **interactive** explanation with visuals.")

# Main Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>ML Concept Visualizer 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Learn ML with fun food-based analogies! 🍕🍪🥗</p>", unsafe_allow_html=True)

# Input Field
concept_name = st.text_input("🔍 Enter an ML Concept:", placeholder="e.g., Decision Trees, Neural Networks")

# Generate Explanation Button
if st.button("🚀 Generate Explanation", use_container_width=True):
    if not concept_name.strip():
        st.warning("⚠️ Please enter a valid ML concept!")
    else:
        with st.spinner("🤖 Generating response..."):
            try:
                response = requests.post(f"{BASE_URL}/ml_explanation/", json={"concept_name": concept_name})
                response.raise_for_status()
                response_data = response.json()

                # Extract Chat History
                if "output" in response_data and "chat_history" in response_data["output"]:
                    chat_history = response_data["output"]["chat_history"]
                    explanation = chat_history[5]["content"] if len(chat_history) > 2 else "Explanation not available."
                else:
                    explanation = "Invalid response format from API."

                # Display Output
                st.success("✅ Response generated successfully!")
                st.markdown("### 🤔 Explanation:")
                st.info(explanation)

                # Show Visualization if Available
                if "image_url" in response_data:
                    st.image(response_data["image_url"], caption="🔍 Visual Representation")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Created with ❤️ by <b>Thomas James</b></p>", unsafe_allow_html=True)
