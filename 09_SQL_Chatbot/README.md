# 🦜 LangChain SQL Database Chat Interface

A Streamlit application that enables natural language interactions with SQL databases using LangChain and Groq LLM. Users can query both SQLite and MySQL databases using conversational language.

## ✨ Features
* Support for SQLite and MySQL databases
* Natural language to SQL query conversion
* Interactive chat interface
* Message history tracking
* Real-time streaming responses
* Secure credential handling

## 🛠️ Prerequisites
* Python 3.8+
* Groq API key
* MySQL database (optional)

## 📦 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/Duygu-Jones/LLM_Playground.git
cd LLM_Playground
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
```

## 🚀 Usage

1. **Start the Application**
```bash
streamlit run app.py
```

2. **Access the Interface**
- Open your browser and navigate to `http://localhost:8501`
- Select your database type (SQLite or MySQL)
- Enter your Groq API key
- Start querying your database using natural language!

## 💡 Example Queries
- "Show me all student names and their grades"
- "What is the average grade in the database?"
- "List the top 5 students by GPA"

## ⚙️ Configuration
* **SQLite**: Uses local `student.db` file
* **MySQL**: Requires host, user, password, and database name
* Cache duration: 2 hours (configurable)
* Model: Llama3-8b-8192

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🌱 About Me
I'm Duygu Jones, a Data Scientist passionate about Machine Learning and Generative AI.

### 🔗 Connect with Me
* [LinkedIn](https://linkedin.com/duygujones)
* [Website](https://duygujones.com)
* [Kaggle](https://kaggle.com/duygujones)
* [GitHub](https://github.com/Duygu-Jones)
* [Medium](https://medium.com/@duygujones)

Feel free to connect! 😊

## ✨ Acknowledgements
Thank you to the open-source community for making this project possible through your tools and support! 🙏

Happy coding! 👩‍💻✨

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.