# Tetromino400

![screenshot](screenshot.png "Tetromino400")


## A free and open source 80's remake of a famous copyrighted falling brick gameplay.

* Made with Python and Pygame on and for the Raspberry Pi 400.


### Features :

* Two types of points, the score which grow depending of the speed level and the speed points which grow until 100 to switch level.
* In full color (up to 8 color displaying simulatenously on the screen !!)
* With modern sounds (borrowed so probably copyrighted, see contribute.)
* Technological innovation : Choose your gaming style : play with the keyboard or the gamepad.
* Multiplayer : The 10 best scores are saved in a separate file (save.xml) that you can mail on a disk to your friend to compete with.


### Contribute :

I like the idea to have a library of open source games with a eigties feel for the RPI400 like it was an old amiga or atari.

To be a bit more serious, it was more of a learning project where the goal was to complete a full game with Python before to tackle my bigger project PIKO-12, but if you want to add features or improve it, don't hesitate to fork and propose pull requests. 

Also I need help to make it safely FLOSS compatible as possible, I used sounds and a font that I found but I don't believe it has a clear licence, that would help it to distribute without more trouble from the big falling brick company. 

* The font source url :
* The sound source url :


### Releases for the RPI400 :

* here and on itchio, as .deb package 


### Install the game :

```
pip install PiTetromino400
```
* **pip3** if pip is used by python 2


### Start the game :

It should work fine with any python 3 installation, but careful it requires the recent pygame 2 release (will crash with 1.9 versions).

In the root directory :

```
python game.py
```
* **python3** if pip is used by python 2


# TODO :

* Build package with the setup tool to add it to pypi 
* A launch method to get it in the raspberry menu game
