# 🔬 Multi-Agent Research & Report Generator

An AI-powered system that automatically researches topics, analyzes information, and generates comprehensive reports using multiple specialized agents.

---

## 🎯 What It Does

This tool uses 4 AI agents working together to create research reports:

- **Research Agent** - Searches the web and gathers information
- **Analysis Agent** - Extracts insights and identifies patterns
- **Writer Agent** - Creates structured, professional reports
- **Fact-Checker Agent** - Verifies quality and accuracy

---

## 🚀 How to Use

### 1. Get a Free Groq API Key
- Go to [console.groq.com](https://console.groq.com)
- Sign up (it's free, no credit card needed)
- Create an API key
- Copy it (starts with `gsk_`)

### 2. Open the App
Visit the live app: **https://multi-agent-research-9xwblu4yg4x2vhch8u4z2t.streamlit.app/**

### 3. Enter Your API Key
- Look at the **sidebar** (left side of the app)
- Find the "Groq API Key" input field
- Paste your API key there

### 4. Generate a Report
- Type your research topic (e.g., "Benefits of solar energy")
- Choose research depth: Quick, Standard, or Deep
- Click "Generate Report"
- Watch the agents work!
- Download your report when done

---

## 💻 Run Locally

Want to run on your computer?

```bash
# Clone the repository
git clone https://github.com/SnehaPradhan04/multi-agent-research.git
cd multi-agent-research

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` and enter your Groq API key in the sidebar.


## 📁 Project Structure

```
multi-agent-research/
├── app.py              # Main application
├── agents/             # AI agents
│   ├── coordinator.py
│   ├── researcher.py
│   ├── analyzer.py
│   ├── writer.py
│   └── fact_checker.py
├── utils/              # Helper functions
│   ├── llm_client.py
│   ├── logger.py
│   └── state_manager.py
└── requirements.txt    # Dependencies
```

---

## 🛠️ Tech Stack

- **Framework:** Streamlit
- **AI Model:** Groq (Llama 3.3 70B)
- **Search:** DuckDuckGo
- **Language:** Python 3.10+

---

## 📝 Example Topics

Try researching:
- "Impact of AI on healthcare"
- "Future of renewable energy"
- "Benefits of remote work"
- "Cryptocurrency trends in 2024"

---

## 🔒 Privacy

- Your API key is only stored in your browser session
- No data is saved permanently
- All research is done in real-time

---

## 📄 License

MIT License - feel free to use and modify!

---

## 🙏 Credits

Built with:
- [Groq](https://groq.com) - Fast LLM inference
- [Streamlit](https://streamlit.io) - Web framework
- [DuckDuckGo](https://duckduckgo.com) - Search API

---

**Made with ❤️ and AI**
