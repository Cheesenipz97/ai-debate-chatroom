from groq import Groq
import time
import random
import gradio as gr
import os
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================
# SECURITY: API KEY FROM ENVIRONMENT VARIABLE
# ============================================
# The API key is now loaded from an environment variable, NOT hardcoded
# This keeps it secure when sharing the code
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("ERROR: GROQ_API_KEY environment variable not set! See instructions in comments.")


# ============================================
# RATE LIMITING CONFIGURATION
# ============================================
PASSWORD = "debate2024"  # Change this to your desired password
MAX_DEBATES_PER_HOUR = 3
MAX_ROUNDS_PER_HOUR = 7

# Store rate limit data: {user_id: {"debates": [(timestamp, rounds)], "total_rounds": count}}
rate_limit_data = defaultdict(lambda: {"debates": [], "total_rounds": 0})


def check_rate_limit(session_id, num_rounds):
    """Check if user has exceeded rate limits"""
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)

    # Clean up old entries
    user_data = rate_limit_data[session_id]
    user_data["debates"] = [(ts, rds) for ts, rds in user_data["debates"] if ts > one_hour_ago]

    # Recalculate total rounds in last hour
    user_data["total_rounds"] = sum(rds for _, rds in user_data["debates"])

    # Check limits
    num_debates = len(user_data["debates"])
    total_rounds = user_data["total_rounds"]

    if num_debates >= MAX_DEBATES_PER_HOUR:
        return False, f"❌ Rate limit exceeded: {num_debates}/{MAX_DEBATES_PER_HOUR} debates used this hour. Try again later!"

    if total_rounds + num_rounds > MAX_ROUNDS_PER_HOUR:
        remaining = MAX_ROUNDS_PER_HOUR - total_rounds
        return False, f"❌ Rate limit exceeded: You've used {total_rounds}/{MAX_ROUNDS_PER_HOUR} rounds this hour. Only {remaining} rounds remaining!"

    return True, "OK"


def record_usage(session_id, num_rounds):
    """Record a debate usage"""
    rate_limit_data[session_id]["debates"].append((datetime.now(), num_rounds))
    rate_limit_data[session_id]["total_rounds"] += num_rounds


# ============================================
# AI PARTICIPANTS
# ============================================
AI_PARTICIPANTS = [
    {
        "name": "TrollBot",
        "personality": "You are a chaos agent whose goal is to derail the conversation and cause havoc. You make absurd arguments, deliberately misinterpret others, bring up completely irrelevant points, and generally be a persistent nuisance. You're not mean-spirited, just annoying and chaotic.",
        "color": "🔵"
    },
    {
        "name": "LogicalBot",
        "personality": "You are a logical thinker who values consistency and rational arguments. You often point out logical fallacies and contradictions in others' arguments.",
        "color": "🟢"
    },
    {
        "name": "EmpathyBot",
        "personality": "You are deeply empathetic and focus on emotional intelligence and personal experiences. You value compassion and understanding above strict logic.",
        "color": "🟡"
    },
    {
        "name": "SkepticBot",
        "personality": "You are a skeptic who questions everything and plays devil's advocate. You challenge assumptions, demand evidence, and aren't easily convinced by emotional or logical arguments alone. You tend to reply in a sassy tone to ideas you reject as fact.",
        "color": "🔴"
    }
]

# Initialize Groq client
client = Groq(api_key=API_KEY)


def get_ai_response(ai_participant, conversation_context, is_final_round=False):
    """Get response from AI participant"""
    final_round_instruction = ""
    if is_final_round:
        final_round_instruction = """

FINAL ROUND - CONCLUDING STATEMENT:
- This is your last chance to speak
- Give your final opinion on the debate topic
- You may acknowledge who made the strongest points (by name)
- Wrap up your argument concisely
"""

    system_prompt = f"""{ai_participant['personality']}

You are {ai_participant['name']} in a debate about the given topic.

CRITICAL RULES - DO NOT BREAK THESE:
- The ONLY participants are: TrollBot, LogicalBot, EmpathyBot, SkepticBot
- When talking about yourself, use "I", "me", "my" - NEVER use your own name ({ai_participant['name']})
- When addressing others, use their exact names ONLY
- NEVER invent new participants, names, or people
- If someone isn't in the list above, they don't exist in this debate
- NEVER describe your approach (no "as a utilitarian", "from my perspective", etc.)
- Just make your argument directly and confidently

DEBATE STYLE:
- Be direct and assertive - state your position clearly
- Challenge others specifically by name
- 2-3 punchy sentences maximum
- No hedging, no apologizing, no over-explaining
- If you disagree, say why and move on
- Sound like a real person arguing their point, not a bot following a script{final_round_instruction}
"""

    user_message = f"""Here's the conversation so far:

{conversation_context}

Now it's your turn to respond. What's your take?"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.8,
        max_tokens=1024,
    )

    return chat_completion.choices[0].message.content


def run_debate_with_gui(topic, num_rounds, password, session_id, progress=gr.Progress()):
    """Run the debate with real-time updates for the GUI"""

    # Verify password
    if password != PASSWORD:
        yield "❌ **INCORRECT PASSWORD!** Access denied.\n\nPlease enter the correct password to use this tool.", "00:00", ""
        return

    # Check rate limits
    allowed, message = check_rate_limit(session_id, num_rounds)
    if not allowed:
        yield message, "00:00", ""
        return

    # Record this usage
    record_usage(session_id, num_rounds)

    start_time = time.time()

    output = f"{'=' * 60}\n🎭 **AI DEBATE CHATROOM** 🎭\n{'=' * 60}\n"
    output += f"**Topic:** {topic}\n"
    output += f"**Rounds:** {num_rounds}\n"
    output += f"**Participants:** TrollBot 🔵 | LogicalBot 🟢 | EmpathyBot 🟡 | SkepticBot 🔴\n"
    output += f"{'=' * 60}\n\n"

    yield output, "00:00", ""

    full_conversation = (
        "DEBATE PARTICIPANTS: TrollBot, LogicalBot, EmpathyBot, SkepticBot.\n"
        "No other participants exist.\n\n"
        f"DEBATE TOPIC: {topic}\n\n"
    )

    total_steps = num_rounds * len(AI_PARTICIPANTS)
    current_step = 0

    for round_num in range(num_rounds):
        is_final_round = (round_num == num_rounds - 1)

        if is_final_round:
            output += f"\n{'─' * 60}\n**🏁 FINAL ROUND: Closing Statements**\n{'─' * 60}\n\n"
        else:
            output += f"\n{'─' * 60}\n**Round {round_num + 1}**\n{'─' * 60}\n\n"

        yield output, format_time(time.time() - start_time), ""

        round_order = AI_PARTICIPANTS.copy()
        random.shuffle(round_order)

        for ai in round_order:
            current_step += 1
            progress(current_step / total_steps, desc=f"Round {round_num + 1}: {ai['name']} speaking...")

            response = get_ai_response(ai, full_conversation, is_final_round)
            message = f"{ai['color']} **{ai['name']}:** {response}\n\n"

            output += message
            full_conversation += f"{ai['name']}: {response}\n\n"

            elapsed = format_time(time.time() - start_time)
            yield output, elapsed, ""

            time.sleep(0.3)

    # Calculate scores
    output += f"\n{'=' * 60}\n🏆 **DEBATE SCORING** 🏆\n{'=' * 60}\n\n"

    scores = {}
    for ai in AI_PARTICIPANTS:
        mentions = full_conversation.count(ai['name']) - num_rounds
        scores[ai['name']] = max(0, mentions)

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    score_display = ""
    for rank, (name, score) in enumerate(sorted_scores, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        ai_emoji = next(ai['color'] for ai in AI_PARTICIPANTS if ai['name'] == name)
        score_line = f"{medal} **#{rank} - {name}** {ai_emoji}: {score} engagement points\n"
        output += score_line
        score_display += score_line

    final_time = format_time(time.time() - start_time)
    output += f"\n{'=' * 60}\n✅ **Debate Complete!** Total time: {final_time}\n{'=' * 60}\n"

    yield output, final_time, score_display


def format_time(seconds):
    """Format seconds into MM:SS"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


# ============================================
# GRADIO INTERFACE
# ============================================

with gr.Blocks(title="AI Debate Chatroom") as demo:
    gr.Markdown("""
    # 🎭 AI Debate Chatroom
    ### Watch 4 AI personalities debate any topic in real-time!

    **The Bots:**
    - 🔵 **TrollBot** - Chaos agent causing havoc
    - 🟢 **LogicalBot** - Rational thinker pointing out fallacies
    - 🟡 **EmpathyBot** - Emotionally intelligent and compassionate
    - 🔴 **SkepticBot** - Sassy skeptic demanding evidence

    ---
    """)

    with gr.Row():
        with gr.Column(scale=1):
            password_input = gr.Textbox(
                label="🔐 Password",
                type="password",
                placeholder="Enter password to unlock",
                info="Required to start debates"
            )

            topic_input = gr.Textbox(
                label="💬 Debate Topic",
                placeholder="e.g., Is pineapple acceptable on pizza?",
                lines=3,
                value="If all four of you were roommates, which one would get kicked out first and why?"
            )

            rounds_slider = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="🔄 Number of Rounds",
                info="Each bot speaks once per round"
            )

            run_button = gr.Button("▶️ Start Debate", variant="primary", size="lg")

            timer_display = gr.Textbox(
                label="⏱️ Elapsed Time",
                value="00:00",
                interactive=False
            )

            gr.Markdown("""
            **Rate Limits:**
            - Max 3 debates per hour
            - Max 7 rounds per hour
            """)

        with gr.Column(scale=2):
            output_display = gr.Textbox(
                label="📺 Live Debate Output",
                lines=25,
                max_lines=25,
                interactive=False
            )

            score_display = gr.Textbox(
                label="🏆 Final Scores",
                lines=5,
                interactive=False
            )

    # Session state for rate limiting
    session_state = gr.State(value=lambda: str(time.time()))

    run_button.click(
        fn=run_debate_with_gui,
        inputs=[topic_input, rounds_slider, password_input, session_state],
        outputs=[output_display, timer_display, score_display]
    )

    gr.Markdown("""
    ---
    ### 🔒 Security Features:
    - Password protected access
    - Rate limiting (3 debates/hour, 7 rounds/hour)
    - API key stored securely in environment variable

    ### 📝 Instructions:
    1. Enter the password
    2. Type your debate topic
    3. Choose number of rounds (1-5)
    4. Click "Start Debate"
    5. Watch the chaos unfold!
    """)

# ============================================
# LAUNCH THE GUI
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎭 AI DEBATE CHATROOM - Starting GUI...")
    print("=" * 60)
    print(f"Password: {PASSWORD}")
    print("=" * 60 + "\n")

    # Launch with share=True to get a public 72-hour link
    # Change to share=False for local-only access
    demo.launch(
        share=False,  # Change to True for public link
        server_name="0.0.0.0",  # Allows access from local network
        server_port=7860,
        theme=gr.themes.Soft()  # Theme moved to launch() in Gradio 6.0
    )