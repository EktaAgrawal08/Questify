## 🚀 Questify: Transforming Documents into Interactive MCQs Powered by AI

**Questify** is an interactive web platform that automatically generates **multiple-choice questions (MCQs)** from **PDF**, **Word**, or **TXT** files using the powerful **Google Gemini API**. Designed for educators, students, and lifelong learners, Questify makes quiz creation effortless, fast, and accurate.

🌐 **Live Demo**: [Questify on Render](https://questify-kdkf.onrender.com)

---

## ✨ Features

- 📄 **Upload** your **PDF**, **Word**, or **TXT** documents  
- 🤖 **AI-Powered MCQ Generation** using **Google Gemini API**  
- 📥 **Download** questions in a clean, printable **PDF** format  
- 🧪 **Try Demo Files** from the `demo_docs/` folder  
- 🌙 **Dark Mode Toggle** for a better visual experience

---

## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap (for responsive, modern UI)  
- **Backend**: Python (Flask) — lightweight and flexible  
- **AI Integration**: Google Gemini API for document-based MCQ generation  
- **Environment**: `.env` for secure API key storage

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/EktaAgrawal08/Questify.git
cd Questify
```

### 2. (Optional) Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your API Key

- Copy `.env.example` to `.env`
- Add your **Google Gemini API key** to the `.env` file

### 5. Run the App Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your browser to use the app locally.

---

## 📂 How to Use

1. Upload a **PDF**, **Word**, or **TXT** file  
2. The system uses **Google Gemini API** to generate relevant MCQs  
3. Preview and **download** the questions as a **PDF**  
4. Experiment with demo files located in the `demo_docs/` folder

---

## 👩‍💻 Author

Made with 💙 by [**Ekta Agrawal**](https://github.com/EktaAgrawal08)

- 🔗 [LinkedIn](https://www.linkedin.com/in/ekta-agrawal-364b3a246/)  
- 🌐 [Live Site on Render](https://questify-kdkf.onrender.com)

