# Python Clash of Code discord bot
An early version of my clash of code bot in Python.  
Creates a private Clash of Code lobby by using a Discord command, responds to the command with a link, deletes the command instantly and response after 10 minutes to not clutter up the channel.  
!clash mode language

# Setup
Insert Codingame rememberMe cookie and Discord token in .env

### Cookie
Log into https://www.codingame.com/ with an account you'll use for the bot and open dev tools (F12 in Chrome), find "rememberMe" cookie and copy paste the value from value tab  
![image](https://user-images.githubusercontent.com/106081841/192303232-49f774ba-dc12-486a-a643-ef05a516b9a7.png)  
:exclamation:Don't log out of the bot account, if you want to use another account on Codingame after you've set up the bot delete rememberMe cookie from your browser or use incognito mode while setting up the bot.  
:exclamation:Cookie will expire after 1 year and will have to be updated.

### Discord token  
Your Discord token can be found at https://discord.com/developers/applications/ in the bot tab.

---

Keep in mind I made this with 0 prior knowledge of Python so there could be some eyesores.
