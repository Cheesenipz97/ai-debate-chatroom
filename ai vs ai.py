from groq import Groq
import time
import random
import os

# ============================================
# CONFIGURATION - Edit these settings
# ============================================

# Your Groq API key (get from: https://console.groq.com/keys)
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("ERROR: GROQ_API_KEY environment variable not set!")
# The debate topic/question
DEBATE_TOPIC = "If all four of you were roommates, which one would get kicked out first and why?"

# Number of back-and-forth exchanges
NUM_ROUNDS = 3

# AI participants and their assigned viewpoints
AI_PARTICIPANTS = [
    {
        "name": "TrollBot",
        "personality": "You are a chaos agent whose goal is to derail the conversation and cause havoc. You make absurd arguments, deliberately misinterpret others, bring up completely irrelevant points, and generally be a persistent nuisance. You're not mean-spirited, just annoying and chaotic.",
        "color": "\033[94m"  # Blue
    },
    {
        "name": "LogicalBot",
        "personality": "You are a logical thinker who values consistency and rational arguments. You often point out logical fallacies and contradictions in others' arguments.",
        "color": "\033[92m"  # Green
    },
    {
        "name": "EmpathyBot",
        "personality": "You are deeply empathetic and focus on emotional intelligence and personal experiences. You value compassion and understanding above strict logic.",
        "color": "\033[93m"  # Yellow
    },
    {
        "name": "SkepticBot",
        "personality": "You are a skeptic who questions everything and plays devil's advocate. You challenge assumptions, demand evidence, and aren't easily convinced by emotional or logical arguments alone. You tend to reply in a sassy tone to ideas you reject as fact.",
        "color": "\033[91m"  # Red
    }
]

# ============================================
# MAIN SCRIPT
# ============================================

# Initialize the Groq client with your API key
client = Groq(api_key=API_KEY)

# Reset color code (for terminal output)
RESET_COLOR = "\033[0m"

# Store the conversation history for each AI
# This helps each AI remember what has been said
conversation_histories = {ai["name"]: [] for ai in AI_PARTICIPANTS}


def get_ai_response(ai_participant, conversation_context, is_final_round=False):
    """
    This function sends a prompt to Groq and gets a response.

    Parameters:
    - ai_participant: Dictionary with AI's name and personality
    - conversation_context: String containing the full conversation so far

    Returns:
    - The AI's response as a string
    """

    # Build the system prompt that defines this AI's personality and role
    system_prompt = f"""{ai_participant['personality']}

You are {ai_participant['name']} in a debate about: "{DEBATE_TOPIC}"

CRITICAL RULES:
- When talking about yourself, use "I", "me", "my" - NEVER use your own name ({ai_participant['name']})
- When addressing others, use their exact names: TrollBot, LogicalBot, EmpathyBot, SkepticBot
- NEVER describe your approach (no "as a utilitarian", "from my perspective", etc.)
- Just make your argument directly and confidently
- No other participants exist

DEBATE STYLE:
- Be direct and assertive - state your position clearly
- Challenge others specifically by name
- 2-3 punchy sentences maximum
- No hedging, no apologizing, no over-explaining
- If you disagree, say why and move on
- Sound like a real person arguing their point, not a bot following a script
"""

    # Build the user message with full conversation context
    user_message = f"""Here's the conversation so far:

{conversation_context}

Now it's your turn to respond. What's your take?"""

    # Call the Groq API to get a response
    # Using llama-3.3-70b-versatile - one of Groq's best models for reasoning
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama-3.3-70b-versatile",  # Fast and intelligent model
        temperature=0.8,  # Makes responses more creative and varied
        max_tokens=1024,
    )

    # Extract the text from the response
    return chat_completion.choices[0].message.content


def print_colored(text, color):
    """Helper function to print colored text in the terminal"""
    print(f"{color}{text}{RESET_COLOR}")


def run_debate():
    """Main function that runs the AI debate"""

    print("\n" + "=" * 60)
    print_colored(f"🎭 AI DEBATE CHATROOM 🎭", "\033[95m")
    print(f"Topic: {DEBATE_TOPIC}")
    print("=" * 60 + "\n")

    # Store the full conversation as a string
    # Initialize with the participants list and topic
    full_conversation = (
        "DEBATE PARTICIPANTS: TrollBot, LogicalBot, EmpathyBot, SkepticBot.\n"
        "No other participants exist.\n\n"
        f"DEBATE TOPIC: {DEBATE_TOPIC}\n\n"
    )

    # Run the debate for the specified number of rounds
    for round_num in range(NUM_ROUNDS):
        is_final_round = (round_num == NUM_ROUNDS - 1)

        if is_final_round:
            print(f"\n--- FINAL ROUND: Closing Statements ---\n")
        else:
            print(f"\n--- Round {round_num + 1} ---\n")

        # Randomize the order of speakers for this round
        round_order = AI_PARTICIPANTS.copy()
        random.shuffle(round_order)

        # Each AI gets a turn to speak in random order
        for ai in round_order:
            # Get this AI's response
            response = get_ai_response(ai, full_conversation, is_final_round)

            # Format the message
            message = f"{ai['name']}: {response}"

            # Print it with color
            print_colored(message, ai['color'])
            print()  # Empty line for readability

            # Add to the full conversation history (APPEND, don't replace!)
            full_conversation += message + "\n\n"

            # Small delay so you can read along (optional since Groq is so fast!)
            time.sleep(0.5)

    # Calculate debate scores based on mentions and engagement
    print("\n" + "=" * 60)
    print_colored("🏆 DEBATE SCORING 🏆", "\033[95m")
    print("=" * 60 + "\n")

    scores = {}
    for ai in AI_PARTICIPANTS:
        # Count how many times other bots mentioned this bot's name
        mentions = full_conversation.count(ai['name']) - NUM_ROUNDS  # Subtract their own messages

        # Simple scoring: mentions indicate engagement/relevance
        scores[ai['name']] = max(0, mentions)

    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for rank, (name, score) in enumerate(sorted_scores, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        ai_color = next(ai['color'] for ai in AI_PARTICIPANTS if ai['name'] == name)
        print_colored(f"{medal} #{rank} - {name}: {score} engagement points", ai_color)

    print()

    # Save the conversation to a text file
    with open("ai_debate_transcript.txt", "w", encoding="utf-8") as f:
        f.write(full_conversation)
        f.write("\n" + "=" * 60 + "\n")
        f.write("DEBATE SCORING\n")
        f.write("=" * 60 + "\n")
        for rank, (name, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
            f.write(f"{medal} #{rank} - {name}: {score} engagement points\n")

    print("\n" + "=" * 60)
    print_colored("💾 Debate saved to 'ai_debate_transcript.txt'", "\033[95m")
    print("=" * 60 + "\n")


# ============================================
# RUN THE PROGRAM
# ============================================

if __name__ == "__main__":
    # This block only runs if you execute this file directly
    run_debate()