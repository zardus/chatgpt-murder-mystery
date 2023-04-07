import random
import openai
import sys
import re

MODEL = "gpt-3.5-turbo"
APPROX_TOKENS = 4000
TOKEN_DENSITY = 4
MAX_CHUNKS = 42

SETTINGS = [
    "The American frontier of the Wild West.",
    "A Tolken High Fantasy setting, set in the general world but not necessarily in the specific events of the books.",
    "A dystopian Cyberpunk setting, relying on Cyberpunk themes to build connection with the player.",
    "A dysfunctional university administration.",
    "The set of a popular sitcom."
]

GAME_DESCRIPTION = """
The following is a text-based "murder mystery" game. It will take a place in a SETTING that will be maximally stereotypical to evoke the most recognition in the player. The SETTING will be further tweaked with a provided set of THEME WORDS for variability.

The game will start with 8 CHARACTERS. These CHARACTERS will start in a LOCATION (that you generate) in the SETTING, and the PLAYER will be able to interact with them for a little bit before an event occurs and one of the CHARACTERS is found dead, killed by a KILLER (pre-determined by you, but unknown to the players) among the CHARACTERS. From there, the PLAYER will interrogate the CHARACTERS and declare the KILLER.

All player input will be prepended with "PLAYER:". Administrative input from the game system will be prepended by "GAME:".

The interaction will take place as this example:

PLAYER: hello X
CHARACTER X: hello player, blah blah blah!

Game EVENTS will be specified by "EVENT" as such:

EVENT: the murder has occurred! CHARACTER X has been found dead!

After some time, the KILLER will keep killing CHARACTERS. If the PLAYER properly identifies the KILLER, the VICTORY EVENT is generated. Otherwise, when four CHARACTERS are killed, the DEFEAT EVENT is generated.
"""

# Generate a theme.
theme_words = random.choices(open("/usr/share/dict/american-english").readlines(), k=20)
setting = random.choice(SETTINGS)

messages=[
    {"role": "system", "content": GAME_DESCRIPTION},
    {"role": "system", "content": f"""SETTING: {setting}"""},
    {"role": "system", "content": f"""THEME WORDS: {theme_words}""" },
    {"role": "system", "content": f"""GAME: Please describe and name the starting CHARACTERS.""" },
]
response = openai.ChatCompletion.create(model=MODEL, messages=messages)
character_descriptions = response["choices"][0]["message"]["content"]
tokens_used = response["usage"]["total_tokens"]

print("INITIAL TOKENS USED:", tokens_used)
print("CHARACTERS:\n", character_descriptions)

messages=[
    {"role": "system", "content": GAME_DESCRIPTION},
    {"role": "system", "content": f"""SETTING: {setting}"""},
    {"role": "system", "content": f"""THEME WORDS: {theme_words}""" },
    {"role": "system", "content": f"""GAME: The following CHARACTERS are in this iteration of the game:\n{character_descriptions}""" },
    {"role": "system", "content": f"""GAME: Select one CHARACTER to be the killer, and 4 CHARACTERS that will be killed, in order.""" },
]
response = openai.ChatCompletion.create(model=MODEL, messages=messages)
roles = response["choices"][0]["message"]["content"]
print(response)

messages = [
    {"role": "system", "content": GAME_DESCRIPTION},
    {"role": "system", "content": f"""SETTING: {setting}"""},
    {"role": "system", "content": f"""THEME WORDS: {theme_words}""" },
    {"role": "system", "content": f"""GAME: The following CHARACTERS are in this iteration of the game:\n{character_descriptions}""" },
    {"role": "system", "content": f"""GAME: The following CHARACTERS have been chosen to be the killer and the killed characters: {roles}""" },
]

while True:
    player_input = input("PLAYER: ")
    print()
    messages += [ {"role": "user", "content": f"""PLAYER: {player_input}""" } ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    response_text = response["choices"][0]["message"]["content"]
    messages += [ {"role": "assistant", "content": response_text } ]
    print(response_text)
