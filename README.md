# 🚀 Autogen's Agentic Tutor

An interactive Autogen web application that explains Machine Learning (ML) concepts in a fun and engaging way, using food-based analogies. The app generates easy-to-understand explanations along with visualizations.

## 🌟 Features
✅ **Simple ML Explanations** - Uses relatable analogies for better understanding  
✅ **Interactive UI** - A visually appealing interface with icons, colors, and structured output  
✅ **Auto-Generated Visuals** - Displays relevant images or diagrams for ML concepts  
✅ **API-Powered** - Connects to a FastAPI backend for dynamic responses  

---

## 📌 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/ml-concept-visualizer.git
cd ml-concept-visualizer
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv env
source env/bin/activate   # On macOS/Linux
env\Scripts\activate      # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the FastAPI Backend**
Make sure you have an API running locally at `http://localhost:8000`. Start your FastAPI server:
```bash
uvicorn api3:app --reload
```

### **5️⃣ Run the Streamlit App**
```bash
streamlit run app.py
```

---

## 🚀 Usage

1️⃣ Open **Streamlit** in your browser at `http://localhost:8501`  
2️⃣ Enter an ML concept (e.g., `Decision Trees`, `Neural Networks`)  
3️⃣ Click **"Generate Explanation"**  
4️⃣ Read the simple explanation & view the generated visualization  

---

## 🎨 UI Preview

![image](https://github.com/user-attachments/assets/1bae6fb6-59a4-4868-8111-23913a956d45)


---

## 🔧 Future Improvements

🔹 **Enhanced Visualizations** using Matplotlib, Graphviz, or D3.js  
🔹 **Voice Input Support** for accessibility  
🔹 **More ML Concepts** with real-world examples  
🔹 **Multi-Language Support** for better accessibility  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch (`feature-new-idea`)  
3. Commit changes (`git commit -m "Added a new feature"`)  
4. Push to the branch (`git push origin feature-new-idea`)  
5. Open a **Pull Request**  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 📬 NOTE

💡 This is just a proof of concept and with adequate time and effort I truly believe we could change it to be in a much better and interactive manner.

