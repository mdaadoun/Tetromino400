# Tetromino400

![screenshot](screenshot.png "Tetromino400")


## A free and open source 80's remake of a famous copyrighted falling brick gameplay.

* Made with Python and Pygame on and for the Raspberry Pi 400.


### Features :

* Incredible Gameplay : Two point types, the score which grow depending of the level and the speed points which grow until 100 to switch to next level. (Ingame help & instructions.)
* In full color (Up to 8 colors displaying simulatenously on the screen !!... But most of the time, it will be 2.)
* With modern sounds ("Borrowed", so probably copyrighted, see contribute.)
* Technological innovative design : Choose your favorite gaming style : play with the keyboard or with the gamepad. (You are the AI.)
* Multiplayer : The scores are saved in a separate file (save.csv) that you can send on a disk by mail to your friend to compete with. Display the 8 best scores on the HIGHSCORES Board.
* The game is over when 100 speed point at last level are reached. Max time before game over is 1 hour, 1 minute & 1 seconde. (+ 1 point)
* Use "F" to swith into fullscreen mode. (I didn't set fullscreen by default, there is some trouble right now around fullscreen mode on Ubuntu based linux distribution, maybe you will need to compile pygame on those platform to get it working.)


### Contribute :

I like the idea to have a library of open source games with a eigties feel for the RPI400 machine like if it was a computer coming from this long forgotten time where amiga, atari or amstrad was magical names.

To be a bit more serious, it was more of a motivation project where the goal was to complete a full game with Python before to tackle my bigger projects, but if you want to add features or improve it, don't hesitate. 

Also I need help to make it safely FLOSS compatible as possible, I used sounds and a font that I found but I don't believe it has a clear licence, that would help it for a clean distribution and avoid trouble from the big falling brick company. 

* The font source url :
* The sound source url :


### Releases :

* On github as code, on Pypi as package or on itchio as a build for the Raspberry Pi 400.


### Install the game :

```
pip install Tetromino400
```
* **pip3** if pip is used by python 2


### Dependency :

It should work fine with a python 3.7+ version, but be careful as it requires the recent pygame 2 release (will crash with 1.9 versions).


### Start the game :


In the root directory :

```
python game.py
```
* **python3** on linux, if python is the version 2
