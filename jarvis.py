# Base Imports
import speech_recognition as sr
import winsound
import pyttsx3
import pywhatkit
import random
import wikipedia
import webbrowser as wb
import sys
import os
import requests

# From Imports
from time import sleep
from datetime import datetime, timedelta
from dadjokes import Dadjoke
from newsapi import NewsApiClient

# File Imports
from weather import weather
from dotenv import load_dotenv
load_dotenv()

# Variables
number_game_instructions = "I'm thinking of a number between 1 and 10. You have 3 chances to guess the correct number. Good luck!"

# For number game, changes to singular 'guess' if 1 guess left
def guess_guesses(guesses):
    if guesses == 1:
        return 'guess'
    else:
        return 'guesses'

# Computer speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")

def engine_talk(text):
<<<<<<< HEAD
    print(text, flush=True)
=======
    print(text)
>>>>>>> 59ae6a195db5cf30218bea816cf3ef90eed228e8
    engine.say(text)
    engine.runAndWait()

# List of commands
def jarvis(command):

    # Stops execution if user says 'stop listening'
    if 'stop listening' in command:
        print('Yes sir!')
        winsound.Beep(200, 500)
        sys.exit()

    # If 'jarvis' isn't heard, program will not respond
    if 'jarvis' in command:
        command = command.replace('jarvis', '')
    else:
        print("Didn't hear Jarvis, try again")
        user_commands()

    # If 'for me' is heard, replace with 'for you'
    # If Jarvis speaks, it will say 'for you'
    if 'for me' in command:
        command = command.replace('for me', 'for you')

    # Starts number game
    elif 'number game' in command or 'play a game' in command:
        guesses = 3
        number = random.randint(1, 10)
        engine_talk(number_game_instructions)
        num_game(guesses, number)

    # Plays a video on YT that matches the query
    elif 'play' in command:
        song = command.replace('play', '')
        engine_talk('Playing' + song)
        pywhatkit.playonyt(song)

    # Returns the current time
    elif 'time' in command:
        time = datetime.now().strftime('%I:%M %p')
        time = time.replace(':', ' ')
        if time == '12 00 AM':
            engine_talk("It's currently midnight")
        elif time == '12 00 PM':
            engine_talk("It's currently noon")
        elif time.startswith('0'):
            time = time.replace('0', '')
        engine_talk('The current time is ' + time)

    # Returns a wiki page and reads the first 2 sentences
    elif 'who is' in command or 'what is' in command:
        engine_talk(f"{command}? Just a moment")
        info = wikipedia.summary(command, 2)
        engine_talk(info)

    # Speaks a dadjoke
    elif 'joke' in command:
        dadjoke = Dadjoke()
        joke = dadjoke.joke
        engine_talk(joke)

    # Opens Reddit mainpage or Subreddit if specified
    elif 'reddit' in command:
        url = 'https://www.reddit.com/'
        x = command.split('reddit ')
        if x[1]:
            url += 'r/' + x[1]
            print(f'Opening r/{sub}')
        else:
            print('Got it boss, opening Reddit...')
        winsound.Beep(200, 500)
        wb.open(url)

    # Opens a webpage in users default browser
    elif 'open' in command:
        url = 'https://www.'
        x = command.split('open ')
        url += x[1]
        if not '.com' in url:
            url += '.com'
        print(f"Opening... {url}")
        winsound.Beep(200, 500)
        wb.open(url)

    # Returns weather in specified city or asks for
    # user to specify city
    elif 'weather' in command:
        if ' in ' in command:
            x = command.split(' in ')
            city = x[1]
            print(city)
            engine_talk(weather(city))
        else:
            engine_talk("Please specify your city")
            return weather_command()

    # Returns 10 news headlines, descriptions, and urls
    # Reads the first 5, prints the last 5 w/5 sec delay
    elif 'news' in command:
        # init
        key = os.getenv('NEWS_API_KEY')
        newsapi = NewsApiClient(key)
        headline_num = 1

        top_headlines = newsapi.get_top_headlines(language='en',
                                                page_size=10,
                                                sources='the-wall-street-journal,'
                                                        'business-insider, buzzfeed,'
                                                        'crypto-coins-news, engadget,' 
                                                        'hacker-news, ign, mashable,' 
                                                        'national-geographic, new-scientist,' 
                                                        'new-york-magazine, next-big-future,' 
                                                        'recode, reddit-r-all, techcrunch,' 
                                                        'techradar, the-huffington-post,' 
                                                        'the-next-web, the-verge,' 
                                                        'the-wall-street-journal, time,' 
                                                        'vice-news, wired')

        headlines = top_headlines['articles']
        for x in headlines:
            title = x['title']
            if headline_num <= 5:
                print(f"=========================")
                engine_talk(f"Headline number {headline_num}.")
                print(f"=========================")
                engine_talk(title)
                engine_talk(x['description'])                
                print(f"URL:\n {x['url']}\n\n")
                headline_num += 1
                continue
            else:
                print(f"=========================")
                print(f" ===Headline Number {headline_num}===")
                print(f"=========================")
                print(f"TITLE:\n {title}")
                print(f"DESCRIPTION:\n {x['description']}")
                print(f"URL:\n {x['url']}\n\n")
                sleep(5)
            headline_num += 1

    # If command isn't recognized, prints unkown
    # and repeats the loop
    else:
        print("Unkown command, please try again")
        user_commands()
    user_commands()

# Function for end of num_game
# if yes, plays again with new number
# else, returns to user_commands
def play_again(func):

    engine_talk(
        "Would you like to play again? Reply yes if you'd like to lose, or no if you're finished playing.")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for response...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        # waiting for play again response
        try:
            response = r.recognize_google(audio).lower()
            if response:
                print(f"You said: {response}")
            # play again
            if 'yes' in response:
                engine_talk("Great, good luck")
                if func == 'num_game':
                    engine_talk(number_game_instructions)
                    func = num_game(3, random.randint(1, 10))

                return func
            else:
                engine_talk("Later loser.")
                return user_commands()
        except Exception:
            sr.UnknownValueError()
            print("Didn't catch that, try again.")
            return play_again(func)

# Number game
# 3 chances to guess a number between 1 and 10
def num_game(guesses_remaining, number_to_guess):

    print(f"guesses_remaining = {guesses_remaining}")
    r = sr.Recognizer()

    # loop until guesses_remaining == -1
    while guesses_remaining != -1:

        with sr.Microphone() as source:

            # Computer won
            if guesses_remaining == 0:
                engine_talk(
                    f"I won. Ha ha ha. Better luck next time, loser! The number was {number_to_guess}")
                play_again('num_game')

            # still playing, not out of guesses yet
            else:
                print(f"Number to guess: {number_to_guess}")
                print("Listening for guess...")
                audio = r.listen(source)

                # waiting for resposne
                try:
                    guess = r.recognize_google(audio).lower()

                    # exit if 'stop'
                    if 'stop' in guess:
                        return user_commands()
                        # convert guess to int for comparison
                    try:
                        guess = int(guess)
                    except ValueError:
                        engine_talk("Couldn't understand, please try again")
                        return num_game(guesses_remaining, number_to_guess)

                    # print users guess
                    print(f"You guessed: {guess}")

                    # if guess was too high or too low
                    # mostly if you say the same number twice or try
                    # to say another number before comp response
                    if guess > 10:
                        engine_talk(f"Whoops, I heard {guess}, that's too high of a number. Try again.")
                        return num_game(guesses_remaining, number_to_guess)

                    # if guess was correct, you win!
                    if guess == number_to_guess:
                        engine_talk(
                            "Great job, you're a mind reader! You won!")
                        play_again('num_game')
                    # guess incorrect, -1 guesses, continue back around
                    else:
                        guesses_remaining -= 1
                        engine_talk(
                            f"Nope, you've got {guesses_remaining} {guess_guesses(guesses_remaining)} left")
                        return num_game(guesses_remaining, number_to_guess)
                # error in audio, try again
                except Exception:
                    sr.UnknownValueError()
                    engine_talk("Couldn't understand, please try again")
                    return num_game(guesses_remaining, number_to_guess)

# Determines if user specified city,
# if no city, program asks for city,
# else, calls weather from external file,
# runs API
def weather_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for city...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            city = r.recognize_google(audio).lower()
            if 'stop' in city:
                return user_commands()
            engine_talk(weather(city))
            return user_commands()
        except Exception:
            sr.UnknownValueError()
            engine_talk("Please try again.")
            city = weather_command()

# Listens for command from user
# if it recognizes user input
# goes to Jarvis to determine
# what happens next
def user_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            return jarvis(command)
        except Exception:
            sr.UnknownValueError()
            command = user_commands()

# run 
try:
    user_commands()
except KeyboardInterrupt:
    print("Shutting down via keyboard command.")
