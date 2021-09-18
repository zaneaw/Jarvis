    # Returns a wiki page and reads the first 2 sentences
    elif 'who is' in command or 'what is' in command:
        # Find the page adnd get the data from API
        info = wikipedia.summary(command, 2)
        # Replace words for speech response
        if 'who is' in command:
            command = command.replace('who is', '')
            engine_talk(f"Looking up {command} for you. {info}")
        elif 'what is' in command:
            command = command.replace('what is', '')
            engine_talk(f"Looking up {command} for you. {info}")

        # Let user know what is being looked up
        # Read back the queried info