#!/usr/bin/python
def questions(self, event):
    import random
    if event.arguments()[0].startswith(self.connection.get_nickname()):
        responses = [
            # Standard eight ball
            "Signs point to yes.",
            "Yes.",
            "Most likely.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see it, yes.",
            "You may rely on it.",
            "Outlook good.",
            "It is certain.",
            "It is decidedly so.",
            "Reply hazy, try again.",
            "Better not tell you now.",
            "Ask again later.",
            "Concentrate and ask again.",
            "Cannot predict now.", 
            "My sources say no.",
            "Very doubtful.",
            "My reply is no.",
            "Outlook not so good.",
            "Don't count on it.",
            # Affirmation ball
            "You look marvelous.",
            "Your breath is so minty.",
            # Sarcastic Ball
            "Do I Look Like I Care?",
            "Yeah, Right.",
            # Random
            "The sky might be octarine. I would go check."
            ]
        self.say(self.respond_to(event.source(), event.target()), random.choice(responses))
        
expression = ('.*\?\b*$', questions)
