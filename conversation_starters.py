
import random

def get_random_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the coffee file a police report? It got mugged.",
        "How does a computer get drunk? It takes screenshots.",
        "What do you call fake spaghetti? An impasta.",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What do you call a parade of rabbits hopping backwards? A receding hare-line.",
        "Why did the programmer quit his job? Because he didn't get arrays."
    ]
    return random.choice(jokes)

def get_random_question():
    questions = [
        "If you could have dinner with any historical figure, who would it be and why?",
        "What's the most interesting project you've worked on recently?",
        "If you could instantly become an expert in something, what would it be?",
        "What's something you've learned in the last week?",
        "If you could live in any fictional universe, which one would you choose?",
        "What's a book that changed your perspective on something?",
        "If you could travel anywhere in the world, where would you go first?",
        "What's a hobby you've always wanted to try but haven't yet?",
        "What's the best piece of advice you've ever received?",
        "If you could have any superpower, what would it be and why?"
    ]
    return random.choice(questions)

def get_random_debate():
    debates = [
        "Is artificial intelligence ultimately beneficial or harmful to society?",
        "Should coding be a mandatory subject in schools?",
        "Is remote work better than working in an office?",
        "Are digital books better than physical books?",
        "Is social media improving or damaging human connection?",
        "Should everyone learn to code?",
        "Is automation going to create more jobs than it eliminates?",
        "Should internet access be considered a basic human right?",
        "Is the concept of privacy becoming obsolete in the digital age?",
        "Do open source projects lead to better software?"
    ]
    return random.choice(debates)

def get_random_conversation_starter(starter_type=None):
    if starter_type is None:
        starter_type = random.choice(["joke", "question", "debate"])
    
    if starter_type.lower() == "joke":
        return f"Joke: {get_random_joke()}"
    elif starter_type.lower() == "question":
        return f"Question: {get_random_question()}"
    elif starter_type.lower() == "debate":
        return f"Discussion topic: {get_random_debate()}"
    else:
        return get_random_conversation_starter()
