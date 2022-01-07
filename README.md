# MyChatbotChum

![Intro](https://media.giphy.com/media/OmmsDoFCDwgJjE1lSS/giphy.gif)

DEPENDENCIES NEEDED:

Type the following into your console (in the MyChatbotChum folder):

    pip install -r requirements.txt --user

INSTRUCTIONS FOR USE: (Windows)

Type the following 2 commands into powershell/terminal (in the folder this project is in):

    $env:FLASK_APP = "userInterface" 

    flask run

The bot will be active on http://127.0.0.1:5000

Press CTRL+C to stop the web app running

IMAGES USED:

-background: 
https://www.istockphoto.com/vector/chat-bot-and-bubble-seamless-pattern-gm838406396-136520391
used with iStock standard licence (no attribution required)

-send icon:
https://www.svgrepo.com/svg/258678/send
used with CC licence (no attribution required)

-robot avatar:
https://pixabay.com/vectors/robot-icon-flat-flat-design-2192617/
used with Pixabay license (no attribution required)

-mic icon
https://www.seekpng.com/ipng/u2w7w7o0o0q8y3y3_recording-symbol-vector-iphone-microphone-icon/
used with SeekPNG licence (no attribution required)

-recording gif, volume icons
created by Nathan Burrows

CONVERSATION FLOW:

-----'I can either help you make a booking, or find delays'

-"book me a train ticket"
-"a booking"
-"I'd like to book a single ticket"
-"book me a return ticket"
-"I want a single ticket from northampton to london"
-"I want a ticket from northampton to london"

-"I want to find delays"
-"predict delay"
-"is my train delayed?"

NOTE: If you do not specify single/return here when you ask to book a train, a follow-up question is asked

-----'Where would you like to depart from/travel to?'

-"London"
-"London Euston"
-"EUS"

-----'What date will you be leaving on?'

-"28th February 2022"
-"28th of February"
-"28th February"
-"28th of Feb"
-"28th Feb"
-"28/02/2022"
-"28/02/22"
-"28/02"
-"today"
-"tomorrow"
-"monday/tuesday/wednesday.....etc"

-----'Please specify a time for this journey.'

-"13:45"
-"1:45 pm"
-"1:45 p.m."
-"12 pm"
-"morning"
-"afternoon"
-"evening"
-"noon"
-"midnight"
-"whenever"
-"I want to arrive before 4pm"
-"I want to leave before 12:45"
