# Welcome!

## This is BotFred, my Discord bot

## Contents

- [Summary](#summary)
- [BotFred's Purpose](#botfreds-purpose)
- [Response examples](#examples-of-botfred-responding)

### Summary

This is my first project creating a Discord bot using the discord library. I had a lot of fun learning how to read through the discord library documentation to get my bot to do as I envisioned. I also learned how to connect to a database (MongoDB) to store gamer tags and usernames to be assigned to their games of choice. Users that are assigned to a game can type a command and BotFred will alert other users who are also assigned to the same game.

### BotFred's purpose

BotFred listens for basic commands, attachments, and certain phrases in which he will respond with a Gif.

- The basic commands he listens for are:
  1. Adding games to the database - _admin command only_
  1. Alerting gamers that you are on and playing a certain game
  1. Listing the games you are subscribed to _- sends the user a DM to not clutter the chat_
  1. Listing all games in the channel _- sends the user a DM to not clutter the chat_
  1. Removing games from the db - _admin command only_
  1. Removing a user from a game
  1. Adding a user to a game
- BotFred listens for attachments.
  - Anytime a user posts an attachment, BotFred will post a comment which will stay in the chat for 5 minutes and then he deletes his own comment.
  - The comments come from a list that I filled with random phrases.
- BotFred listens for specific phrases from Star Wars and Deep Rock Galactic.
  - If want to know what phrases their are, use the command _!gif_ and BotFred will send you a DM with a list of phrases.
  - When a phrase is sent, BotFred will send a Gif in return.

### Examples of BotFred responding

##### BotFred's response to _!gif_

![Gif helper](/img/Gif.png)
<br/>

##### BotFred's response to _!help_

![helper command](/img/Help.png)
<br />

##### BotFred's response to a phrase: _So uncivilized_

![Obi Gif](/img/uncivilized.png)

- After 1 second BotFred deletes the users command.
- After 30 seconds BotFred will delete the Gif.
- This is done to not clutter the chat.
  <br />

##### BotFred's response to the command _!addtogame_

![add user to game](/img/far%20cry.png)

- After 1 second BotFred deletes the users command.
- After 60 seconds BotFred will delete the Gif.
- This is done to not clutter the chat.
  <br />

##### BotFred's response to _!listgames_

![list of games](/img/games.png)

- BotFred sends a DM of all the games in the DB in a nice format.
- The game card contains a list of gamers subscribed to the game, title, description, and an image of the game.
