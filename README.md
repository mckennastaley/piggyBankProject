# How to run locally
1. Install Python v3.x.x
    1. You may want to use a virtual environment. [Here](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) are good instructions.
2. In piggyBankProject directory run `pip3 install -r requirements.txt` to install all necessary packages.
   1. If you are developing and install a new package run `pip3 freeze > requirements.txt` to update file. Should be in piggyBankProject directory
3. Create a file called .env file in piggyBankProject and ask me to send DB secrets. I am using the same DB for a personal project so I don't want to push the password to github, sorry :(
4. Run project with `python3 manage.py runserver` (also in piggyBankProject directory)
#### Let me know if you have questions!
