<div align="center">

# 🤖 AI Research Agent

**An intelligent research assistant powered by LangChain and LLaMA 3**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Latest-green?style=for-the-badge)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3-orange?style=for-the-badge)](https://groq.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) •
[Demo](#-demo) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Contributing](#-contributing)

---

</div>

## 📖 About

AI Research Agent is an autonomous research assistant that leverages the power of Large Language Models combined with external tools to perform comprehensive research tasks. Simply ask a question, and the agent will search the web, query Wikipedia, and compile a structured research response.

<div align="center">

```
┌─────────────────────────────────────────────────────────────────┐
│                    🔍 Ask Your Question                         │
│         "What are the latest developments in AI?"               │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│               🧠 AI Agent Thinks & Researches                   │
│    • Searches the web         • Queries Wikipedia               │
│    • Analyzes information     • Synthesizes findings            │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                   📊 Structured Response                        │
│    Topic | Summary | Sources | Tools Used                       │
└─────────────────────────────────────────────────────────────────┘
```

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🧠 Intelligent Agent
- **ReAct Pattern**: Reasons step-by-step before acting
- **Tool Selection**: Automatically chooses the best tool for each query
- **Structured Output**: Returns organized, parseable responses

</td>
<td width="50%">

### 🛠️ Powerful Tools
- **Web Search**: Real-time information via DuckDuckGo
- **Wikipedia**: Factual, encyclopedic knowledge
- **File Export**: Save research to text files

</td>
</tr>
<tr>
<td width="50%">

### ⚡ High Performance
- **Groq Integration**: Ultra-fast LLM inference
- **LLaMA 3 8B**: State-of-the-art open-source model
- **Optimized Prompts**: Efficient token usage

</td>
<td width="50%">

### 🎨 Modern Interface
- **Clean UI**: Intuitive, responsive design
- **Real-time Feedback**: Loading states and animations
- **Structured Display**: Topic, summary, sources, tools

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [Groq API Key](https://console.groq.com) (free tier available)

### Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Agent.git
cd AI-Agent
```

2️⃣ **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Configure environment**
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

5️⃣ **Run the application**
```bash
python app.py
```

6️⃣ **Open your browser**
```
http://localhost:5000
```

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t ai-research-agent .

# Run with environment variables
docker run -p 5000:5000 -e GROQ_API_KEY=your_api_key ai-research-agent

# Or use .env file
docker run -p 5000:5000 --env-file .env ai-research-agent
```

---

## 📁 Project Structure

```
AI-Agent/
├── 📄 app.py                 # Flask web server
├── 🧠 main.py                # AI agent core logic
├── 🛠️ tools.py               # Agent tools (search, wiki, save)
├── 📋 requirements.txt       # Python dependencies
├── 🐳 Dockerfile             # Container configuration
├── 📁 templates/
│   └── 📄 index.html         # Web interface
├── 📁 static/
│   └── 🎨 style.css          # Styling
└── 📄 .env                   # Environment variables (create this)
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for LLM access | ✅ Yes |

### Agent Settings

You can customize the agent behavior in `main.py`:

```python
# Change the model
llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# Adjust temperature (0 = deterministic, 1 = creative)
llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)
```

---

## 📚 Documentation

For detailed documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

### API Reference

#### `GET /`
Serves the main web interface.

#### `POST /ask`
Submit a research query.

**Request:**
```json
{
  "query": "What is quantum computing?"
}
```

**Response:**
```json
{
  "result": {
    "topic": "Quantum Computing",
    "summary": "Quantum computing is a type of computation that harnesses...",
    "sources": ["https://example.com", "Wikipedia"],
    "tools_used": ["search", "wikipedia"]
  }
}
```

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|:----------:|:-------:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core Language |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | Web Framework |
| ![LangChain](https://img.shields.io/badge/🦜_LangChain-green?style=flat-square) | Agent Framework |
| ![Groq](https://img.shields.io/badge/Groq-orange?style=flat-square) | LLM Inference |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Containerization |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) | Frontend |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | Styling |

</div>

---

## 🗺️ Roadmap

- [x] Basic research agent with web search
- [x] Wikipedia integration
- [x] File export functionality
- [x] Web interface
- [x] Docker support
- [ ] Conversation memory
- [ ] Streaming responses
- [ ] PDF document analysis
- [ ] User authentication
- [ ] Rate limiting
- [ ] Response caching

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) - For the amazing agent framework
- [Groq](https://groq.com) - For lightning-fast LLM inference
- [Meta AI](https://ai.meta.com) - For the LLaMA 3 model
- [DuckDuckGo](https://duckduckgo.com) - For privacy-respecting search

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
