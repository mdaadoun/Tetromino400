# Tetromino400

![screenshot](screenshot.png "Tetromino400")


## A free and open source 80's remake of a famous copyrighted falling brick gameplay.

* Made with Python and Pygame on and for the Raspberry Pi 400.


### Features :

* Incredible Gamplay : Two types of points, the score which grow depending of the level and the speed points which grow until 100 to switch to next level. (Ingame help & instructions.)
* In full color (Up to 8 color displaying simulatenously on the screen !!)
* With modern sounds ("Borrowed", so probably copyrighted, see contribute.)
* Technological innovation : Choose your gaming style : play with the keyboard or the gamepad. (You are the AI.)
* Multiplayer : The scores are saved in a separate file (save.xml) that you can mail on a disk to your friend to compete with (Mutual trust required.).


### Contribute :

I like the idea to have a library of open source games with a eigties feel for the RPI400 like if it was an computer this long forgotten time where amiga, atari or amstrad was magical names.

To be a bit more serious, it was more of a learning project where the goal was to complete a full game with Python before to tackle my bigger project PIKO-12, but if you want to add features or improve it, don't hesitate to fork and propose pull requests. 

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
