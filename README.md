# AI Checkers Game with Reinforcement Learning

This is a fully functional Checkers game implemented in **Python** using **Pygame**. It includes an **AI opponent powered by Q-learning**, a form of reinforcement learning. The AI can improve its gameplay via training and supports multiple difficulty levels, game modes, and a live stats dashboard.

---

## Game Features

- Human vs AI, Human vs Human, and AI vs AI modes  
- Multiple difficulty levels: Easy, Medium, Hard  
- Training for reinforcement learning  
- Live statistics dashboard: win/loss/tie count and average moves  
- Turn indicators and endgame messages  
- Graphical menu for mode and difficulty selection

---

## Getting Started

1. Clone or download this repository.
2. Ensure you have `q_black.pkl` and `q_red.pkl` in the same folder.
3. Run the game:

```bash
python main.py
```

---

## How to Play

### Main Menu
When the game launches:

- Press:
  - `1` → Human vs AI
  - `2` → Human vs Human
  - `3` → AI vs AI
  - `4` → Training Mode
- Then press:
  - `e` → Easy AI
  - `m` → Medium AI
  - `h` → Hard AI

The game begins once both are selected.

### Human Player Controls

- Click a piece of your color to select it.
- Valid destinations will be **highlighted in green**.
- Click a destination to move.
- Captures are forced if available.
- Multi-jumps are automatically handled.

### AI Behavior

- Uses **Q-learning** to learn optimal moves.
- Difficulty affects randomness:
  - **Easy**: very random
  - **Medium**: mostly smart
  - **Hard**: nearly optimal

---

## Statistics Dashboard

At the top-left of the screen:
- Games Played  
- 🔴 Red Wins  
- ⚫ Black Wins  
- Average Moves per Game

---

## Game Over

When a side wins:

- A message like **“Red Wins!”** or **“Black Wins!”** appears.
- Press:
  - `R` to restart
  - `Q` to quit

---

## File Structure

```
├── main.py                   # Main game loop & GUI
├── ai.py                     # Q-learning agent
├── board.py                  # Board logic
├── piece.py                  # Piece logic
├── q_black.pkl               # AI knowledge (black side)
├── q_red.pkl                 # AI knowledge (red side)
├── README.md                 # How to use
├── Project Report.pdf        # Workings and findings
├── Project Proposal.docx     # Initial proposal 
├── Demo Video Link.pdf       # Recorded voiceover 
```

---

## How Q-Learning Works

- The board is encoded as a string state.
- Actions like `2,3->3,4` represent piece moves.
- Rewards:
  - +10 for captures
  - +100 for winning
  - -100 for losing
- Values are updated with the **Bellman equation**.

---

## Possible Improvements

- Add save/load feature  
- Add sound effects  
- Visual animations  
- Online multiplayer  
- Upgrade to Deep Q-Networks (DQN)

---

## Team Members

- **Rida Qazi** – 22k-4409  
- **Mashal Jawed** – 22k-4552  
- **Abdul Wasey** – 22k-4172  
