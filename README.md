# 🐍 SnakeBoy
<img src="assets/Images/logo.png" alt="drawing" width="800"/>

**SnakeBoy** is a modern twist on the classic Snake game with a clean visual design inspired by the aesthetic of the GameBoy and the old Nokia phones, enhanced sound effects, and support for both singleplayer and competitive 2-player modes.

## 🎮 Features

- Classic snake gameplay with modern polish
- 1-player level-based progression (up to 5 levels)
- 2-player competitive mode with real-time collision and scoring
- Custom high score tracking (singleplayer & multiplayer)
- Adjustable music and sound effects volume

## 🛠 Requirements

- Python 3.8+

## 📦 Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/hlbobo/snakeboy.git
   cd snakeboy
    ````

2. **Install dependencies:**

   ```bash
   pip install pygame
   ```

3. **Run the game:**

   ```bash
   python SnakeBoy.py
   ```


## 🎮 Controls

### 1 Player Mode:

* `W` – Up
* `A` – Left
* `S` – Down
* `D` – Right

### 2 Player Mode:

#### Player 1:

* `W` – Up
* `A` – Left
* `S` – Down
* `D` – Right

#### Player 2:

* `↑` – Up Arrow
* `←` – Left Arrow
* `↓` – Down Arrow
* `→` – Right Arrow


## 🧠 Objective

* Eat the fruit to grow and earn points.
* In singleplayer, complete 5 increasingly difficult levels.
* In 2-player mode, survive longer than your opponent or outscore them.
* Avoid hitting walls, yourself, or your opponent.


## 🏆 High Scores

* Singleplayer highscores are saved in `highscore.txt`
* Multiplayer highscores are saved in `mp_highscore.txt`


## 📁 Assets

The following folder structure is required for the game to function:

```
assets/
├── Audio/
│   ├── bgm.mp3
│   ├── eat.mp3
│   └── button_select.mp3
├── Font/
│   └── Gamer.ttf
├── Images/
│   ├── bg.png
│   ├── logo.png
│   ├── button.png
│   ├── button1.png
│   ├── fruit.png
│   └── icon.png
```


## ⚙️ Options Menu

* Adjust BGM and SFX volume
* Toggle fullscreen
* View game controls

## 🙌 Credits

Music by: Filippo Game Audio: https://youtu.be/J65VhFxSSRk?si=7PqPIkZyBmb6VM35

