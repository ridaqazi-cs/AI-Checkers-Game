# ai.py
import random
import pickle

class QLearningAgent:
    def __init__(self, color,
                 alpha=0.1, gamma=0.9,
                 epsilon=1.0, epsilon_min=0.05,
                 epsilon_decay=0.995):
        self.color = color
        self.Q = {}  # state_str -> {action_str: Q-value}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def get_state(self, board):
        """Encode board to a state string."""
        return board.encode_state()

    def available_actions(self, board):
        """
        Return a list of action_str for this agent:
        each action_str is "sr,sc->dr,dc"
        """
        must_capture = board.has_capture(self.color)
        acts = []
        for piece in board.get_all_pieces(self.color):
            moves = board.get_valid_moves(piece)
            if must_capture:
                moves = {dst: caps for dst, caps in moves.items() if caps}
            for (dr, dc), caps in moves.items():
                key = f"{piece.row},{piece.col}->{dr},{dc}"
                acts.append(key)
        return acts

    def choose_action(self, board):
        """Epsilon-greedy selection over current Q."""
        state = self.get_state(board)
        actions = self.available_actions(board)
        # init Q[state] if unseen
        if state not in self.Q:
            self.Q[state] = {a: 0.0 for a in actions}
        # ensure new actions are in Q[state]
        for a in actions:
            if a not in self.Q[state]:
                self.Q[state][a] = 0.0

        # exploration vs exploitation
        if random.random() < self.epsilon:
            return random.choice(actions)
        # pick best-Q action (break ties randomly)
        qvals = self.Q[state]
        maxq = max(qvals[a] for a in actions)
        best = [a for a in actions if qvals[a] == maxq]
        return random.choice(best)

    def learn(self, old_state, action, reward, new_state, done):
        """
        Update Q-table using Bellman equation.
        - old_state, new_state: state strings
        - action: action_str taken from old_state
        - reward: numeric reward
        - done: True if new_state is terminal
        """
        # init entries if missing
        if old_state not in self.Q:
            self.Q[old_state] = {}
        if action not in self.Q[old_state]:
            self.Q[old_state][action] = 0.0

        old_q = self.Q[old_state][action]
        # estimate best future Q
        future_q = 0.0
        if not done and new_state in self.Q and self.Q[new_state]:
            future_q = max(self.Q[new_state].values())

        # Q-learning update
        self.Q[old_state][action] = old_q + self.alpha * (
            reward + self.gamma * future_q - old_q
        )

        # decay epsilon at end of episode
        if done and self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename):
        """Pickle your Q-table to disk."""
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)

    def load(self, filename):
        """Load a pickled Q-table."""
        with open(filename, 'rb') as f:
            self.Q = pickle.load(f)
            # after loading, you might set epsilon low for exploitation:
            self.epsilon = self.epsilon_min
    def choose_piece_action(self, board, piece):
        """
        Like choose_action, but restricts to moves *from* this one piece.
        Returns an action_str “sr,sc->dr,dc” for a capture jump.
        """
        state = self.get_state(board)
        # Get *all* capture actions (because multi-jump only occurs when captures exist)
        must_capture = True
        # Filter available actions to those that start at this piece
        all_actions = self.available_actions(board)  # this already enforces must_capture if True
        prefix = f"{piece.row},{piece.col}->"
        piece_actions = [a for a in all_actions if a.startswith(prefix)]
        if not piece_actions:
            return None

        # Epsilon-greedy over this subset
        # Initialize Q entries if missing
        if state not in self.Q:
            self.Q[state] = {}
        for a in piece_actions:
            self.Q[state].setdefault(a, 0.0)

        if random.random() < self.epsilon:
            return random.choice(piece_actions)
        # Exploit: pick max-Q action among piece_actions
        qvals = self.Q[state]
        best_q = max(qvals[a] for a in piece_actions)
        best = [a for a in piece_actions if qvals[a] == best_q]
        return random.choice(best)
