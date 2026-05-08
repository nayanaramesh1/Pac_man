# 🎮 Pac-Man AI Game
A Python-based Pac-Man style game built using Pygame, featuring dynamic maze generation and intelligent ghost movement powered by the A* pathfinding algorithm.

---

## 🚀 Features
- 🧱 Dynamic maze generation (every level is unique)
- 👻 Intelligent ghost AI using A* pathfinding
- 🎮 Smooth player movement with collision detection
- 🪙 Coin collection system with score tracking
- ✨ Special coins with higher rewards and visual effects
- 📈 Level progression with increasing difficulty
- ⚡ Adaptive game speed based on level
- 🧠 Smart ghost behavior (mix of A* + randomness)
- 🏆 High score tracking within session

---

## 🧠 How It Works
- A random maze is generated at each level
- Player (Pac-Man) navigates through the maze using arrow keys
- Coins and special coins are placed randomly on valid paths
- A ghost spawns and attempts to chase the player

### Game Logic:
- Ghost uses A* algorithm to find shortest path
- When close → actively chases player
- When far → moves semi-randomly
- Coins increase score
- Special coins give bonus points
### End Condition:
- Game ends when ghost catches Pac-Man

---

## ⚙️ Game Mechanics
- 🎮 Player movement restricted to paths
- 👻 Ghost adapts behavior based on distance
- 🪙 Coins disappear when collected
- 📊 Score increases with level multiplier
- 📈 Level increases when most coins are collected
- ⚡ Speed increases as level increases

---

## 🎨 Visual Elements
- Blue blocks → Walls
- Yellow circle → Pac-Man
- Red circle → Ghost
- Yellow dots → Coins
- Blinking white dots → Special coins
- Top bar → Score, Level, High Score

---

## 🛠️ Tech Stack
- Python
- Pygame
- Heapq (for A* priority queue)
- Random module

---

## 📁 Project Structure
pacman-ai-game/

│── pacman.py

│── README.md

---

## ▶️ How to Run
### 1. Clone the repository
git clone https://github.com/nayanaramesh1/Pac_man.git
### 2. Navigate to project folder
cd pacman-ai-game
### 3. Install dependencies
pip install pygame
### 4. Run the game
python pacman.py

---

## 🎮 Controls
- ⬆️ Up Arrow → Move Up
- ⬇️ Down Arrow → Move Down
- ⬅️ Left Arrow → Move Left
- ➡️ Right Arrow → Move Right
- 🔄 R → Restart after Game Over

---

## 🎯 Game Modes
- Endless progression with increasing levels
- Difficulty scales with:
- Maze size
- Ghost intelligence
- Game speed

## ⚠️ Limitations
- Single ghost only
- No sound effects
- High score not stored permanently
- Basic graphics

## 🚀 Future Enhancements
- 👻 Multiple ghosts with different AI behaviors
- 🔊 Sound effects and background music
- ⚡ Power-ups (invincibility, ghost-eating mode)
- 💾 Persistent high score storage
- 🎨 Enhanced UI and animations
