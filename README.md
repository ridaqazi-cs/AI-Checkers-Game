# 🧠 AI Checkers Game with Reinforcement Learning

This is a fully functional Checkers game implemented in **Python** using **Pygame**. It includes an **AI opponent powered by Q-learning**, a form of reinforcement learning. The AI can improve its gameplay via self-play and supports multiple difficulty levels, game modes, and a live stats dashboard.

---

## 🎮 Game Features

- ✅ Human vs AI, Human vs Human, and AI vs AI modes  
- ✅ Multiple difficulty levels: Easy, Medium, Hard  
- ✅ Self-play training mode for reinforcement learning  
- ✅ Live statistics dashboard: win/loss/tie count and average moves  
- ✅ Turn indicators and endgame messages  
- ✅ Graphical menu for mode and difficulty selection

---

## 🖥️ Requirements

- Python 3.9+
- Pygame  
- Numpy

Install dependencies:

```bash
pip install pygame numpy
```

---

## 🚀 Getting Started

1. Clone or download this repository.
2. Ensure you have `q_black.pkl` and `q_red.pkl` in the same folder.
3. Run the game:

```bash
python main.py
```

---

## 🕹️ How to Play

### 🎛️ Main Menu
When the game launches:

- Press:
  - `1` → Human vs AI
  - `2` → Human vs Human
  - `3` → AI vs AI
  - `4` → Training Mode
- Then press:
  - `E` → Easy AI
  - `M` → Medium AI
  - `H` → Hard AI

The game begins once both are selected.

### 👤 Human Player Controls

- Click a piece of your color to select it.
- Valid destinations will be **highlighted in green**.
- Click a destination to move.
- Captures are forced if available.
- Multi-jumps are automatically handled.

### 🤖 AI Behavior

- Uses **Q-learning** to learn optimal moves.
- Difficulty affects randomness:
  - **Easy**: very random
  - **Medium**: mostly smart
  - **Hard**: nearly optimal

---

## 📊 Statistics Dashboard

At the top-left of the screen:
- 🕹️ Games Played  
- 🔴 Red Wins  
- ⚫ Black Wins  
- 📉 Average Moves per Game

---

## 🏁 Game Over

When a side wins:

- A message like **“Red Wins!”** or **“Black Wins!”** appears.
- Press:
  - `R` to restart
  - `Q` to quit

---

## 🧪 Self-Play Training Mode

To let AI play against itself:

1. From the menu, press `4` for **Training Mode**.
2. AI will learn by playing multiple episodes.
3. Use `.save()` methods in `ai.py` to save new Q-tables for stronger play.

> You can tweak the number of episodes and reward logic in the training loop for better performance.

---

## 📁 File Structure

```
├── main.py             # Main game loop & GUI
├── ai.py               # Q-learning agent
├── board.py            # Board logic
├── piece.py            # Piece logic
├── q_black.pkl         # AI knowledge (black side)
├── q_red.pkl           # AI knowledge (red side)
```

---

## 🧠 How Q-Learning Works

- The board is encoded as a string state.
- Actions like `2,3->3,4` represent piece moves.
- Rewards:
  - +0.2 for captures
  - +1.0 for winning
  - -1.0 for losing
- Values are updated with the **Bellman equation**.

---

## 💡 Possible Improvements

- Add save/load feature  
- Add sound effects  
- Visual animations  
- Online multiplayer  
- Upgrade to Deep Q-Networks (DQN)

---

## 👥 Team Members

- **Rida Qazi** – 22k-4409  
- **Mashal Jawed** – 22k-4552  
- **Abdul Wasey** – 22k-4172  

---

## 📄 License

This project is licensed under the **MIT License**.
