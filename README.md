# 🎭 AI Debate Chatroom

Watch 4 unique AI personalities debate any topic in real-time! Available in both terminal and web GUI versions.

## 🤖 Meet the Debaters

- **🔵 TrollBot** - Chaos agent who derails conversations with absurd arguments
- **🟢 LogicalBot** - Rational thinker who points out logical fallacies
- **🟡 EmpathyBot** - Emotionally intelligent bot focused on compassion
- **🔴 SkepticBot** - Sassy skeptic who demands evidence for everything

## ✨ Features

- 🎲 **Randomized speaking order** - Different debate flow every time
- 🏆 **Automatic scoring** - Tracks engagement and determines winners
- 💬 **Custom topics** - Debate anything you want
- 🎨 **Two versions available:**
  - **Terminal version** - Fast, colorful console output
  - **Web GUI version** - Beautiful interface with real-time updates
- 🔒 **Secure** - API keys stored safely in environment variables
- 📊 **Rate limiting** - Prevents API abuse (GUI version)
- 🔐 **Password protection** - Control access to your debates (GUI version)

## 📸 Screenshots

*Coming soon! Feel free to add your own screenshots here.*

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Groq API key (get one free at [console.groq.com](https://console.groq.com/keys))

### Step 1: Clone the Repository

```bash
git clone https://github.com/Cheesenipz97/ai-debate-chatroom.git
cd ai-debate-chatroom
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# For terminal version only
pip install groq

# For GUI version (includes terminal dependencies)
pip install groq gradio
```

### Step 4: Set Up API Key

You need to set your Groq API key as an environment variable.

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="your_api_key_here"
```

**Note:** This sets the key temporarily. For permanent setup, add it to your system environment variables or create a `.env` file.

## 🎮 Usage

### Terminal Version

Quick and simple - runs directly in your console:

```bash
python "ai vs ai.py"
```

**Features:**
- Colored output for each bot
- Fast execution
- Saves transcript to `ai_debate_transcript.txt`
- Perfect for quick debates

**Customize the debate:**
Edit these variables in `ai vs ai.py`:
```python
DEBATE_TOPIC = "Your custom topic here"
NUM_ROUNDS = 3  # Change number of rounds
```

### GUI Version

Beautiful web interface with real-time updates:

```bash
python AI_Debate_GUI.py
```

Then open your browser to: `http://localhost:7860`

**Features:**
- Real-time debate display
- Adjustable rounds (1-5)
- Timer showing elapsed time
- Password protection (default: `debate2024`)
- Rate limiting (3 debates/hour, 7 rounds/hour)
- Live scoring display

**To share with friends (72-hour public link):**
Change line 371 in `AI_Debate_GUI.py`:
```python
share=True,  # Creates public shareable link
```

## 🔧 Configuration

### Change the Password (GUI Version)

Edit line 35 in `AI_Debate_GUI.py`:
```python
PASSWORD = "your_custom_password"
```

### Adjust Rate Limits (GUI Version)

Edit lines 36-37 in `AI_Debate_GUI.py`:
```python
MAX_DEBATES_PER_HOUR = 3
MAX_ROUNDS_PER_HOUR = 7
```

### Customize Bot Personalities

Both scripts have an `AI_PARTICIPANTS` list where you can modify personalities, names, and colors!

## 🛡️ Security Features

- ✅ API keys stored in environment variables (never hardcoded)
- ✅ Password protection on GUI version
- ✅ Rate limiting to prevent API abuse
- ✅ `.gitignore` protects sensitive files
- ✅ Safe to share publicly

## 📝 Example Topics

Try these fun debate topics:

- "Is a hot dog a sandwich?"
- "Should pineapple be allowed on pizza?"
- "Which came first: the chicken or the egg?"
- "Is AI going to take over the world?"
- "If all four of you were roommates, who gets kicked out first?"

## 🤝 Contributing

Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- ⭐ Star this repo if you like it!

## 📺 Support the Creator

If you enjoy this project and want to see more AI experiments and coding content:

**🎮 Follow me on Twitch: [Cheesenipz97](https://twitch.tv/Cheesenipz97)**

I stream coding projects, AI experiments, and more!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com/) for lightning-fast AI inference
- GUI powered by [Gradio](https://gradio.app/)
- Uses Llama 3.3 70B model for intelligent debates

## 🐛 Troubleshooting

### "ERROR: GROQ_API_KEY environment variable not set!"

Make sure you've set the environment variable before running the script. See the "Set Up API Key" section above.

### GUI won't start / Port already in use

Try changing the port in `AI_Debate_GUI.py` line 373:
```python
server_port=7861  # Change from 7860
```

### Gradio compatibility issues

Make sure you have the latest version:
```bash
pip install --upgrade gradio
```

## 📬 Contact

- GitHub: [@Cheesenipz97](https://github.com/Cheesenipz97)
- Twitch: [Cheesenipz97](https://twitch.tv/Cheesenipz97)

---

**Made with ❤️ and AI chaos by Cheesenipz97**