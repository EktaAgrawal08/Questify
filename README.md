### 🚀 Questify

**Questify** is an interactive platform that allows users to upload PDF, Word, or TXT files and instantly generate MCQs from the content using the powerful Google Gemini API. Whether you're a student, teacher, or lifelong learner, Questify makes quiz creation seamless and efficient.

## ✨ Features

- 📄 Upload **PDF, Word, or TXT** documents
- 🤖 **AI-Powered MCQ Generation** using Google Gemini API
- 🎯 Accurate and contextually relevant questions
- 📥 **Download generated MCQs** in PDF format
- 📂 Includes **demo documents** to explore functionality
- 🌙 Dark mode toggle for comfortable viewing


## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python
- **AI Integration**: Google Gemini API 
- **Environment Management**: `.env` with a provided `.env.example`


## 🚀 Getting Started

To get Questify up and running on your local machine, follow the steps below:

1. **Clone the repository**First, clone the repository to your local machine and navigate into the project folder:

```shellscript
git clone https://github.com/EktaAgrawal08/Questify.git
cd Questify
```


2. **Create and activate a virtual environment (optional but recommended)**It is highly recommended to set up a virtual environment to manage dependencies. You can do this by running:

```shellscript
python -m venv venv
# For Linux/macOS
source venv/bin/activate
# For Windows
venv\Scripts\activate
```


3. **Install dependencies**Install all the required dependencies listed in `requirements.txt`:

```shellscript
pip install -r requirements.txt
```


4. **Set up environment variables**

1. Create a `.env` file in the root directory based on the `.env.example` file provided.
2. Add your **Google Gemini API key** to the `.env` file.



5. **Run the application**Finally, start the application by running:

```shellscript
python app.py
```

The application should now be running locally. Open your browser and start using Questify!




## 📂 Usage

1. Upload a **PDF**, **Word**, or **TXT** file.
2. The Google Gemini API processes the content and generates MCQs from it.
3. View and download the generated MCQs in PDF format.
4. You can explore the `demo_docs/` folder for sample documents to test the platform.


## 🙋‍♀️ Author

Made with 💙 by [Ekta Agrawal](https://github.com/EktaAgrawal08)

- 🔗 [Linkedin Profile](https://www.linkedin.com/in/ekta-agrawal-364b3a246/)