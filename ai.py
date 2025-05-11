import random
import pickle

class QLearningAgent:
    def __init__(self, color,
                 alpha=0.1, gamma=0.9,
                 epsilon=1.0, epsilon_min=0.05,
                 epsilon_decay=0.995):
        self.color = color
        self.Q = {}  
        self.alpha = alpha  
        self.gamma = gamma  
        self.epsilon = epsilon  
        self.epsilon_min = epsilon_min  
        self.epsilon_decay = epsilon_decay  

    def get_state(self, board):
        return board.encode_state()

    def available_actions(self, board):
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
        state = self.get_state(board)
        actions = self.available_actions(board)
        if state not in self.Q:
            self.Q[state] = {a: 0.0 for a in actions}
        for a in actions:
            if a not in self.Q[state]:
                self.Q[state][a] = 0.0
        if random.random() < self.epsilon:
            return random.choice(actions)
        qvals = self.Q[state]
        maxq = max(qvals[a] for a in actions)
        best = [a for a in actions if qvals[a] == maxq]
        return random.choice(best)

    def learn(self, old_state, action, reward, new_state, done):
        if old_state not in self.Q:
            self.Q[old_state] = {}
        if action not in self.Q[old_state]:
            self.Q[old_state][action] = 0.0
        old_q = self.Q[old_state][action]
        future_q = 0.0
        if not done and new_state in self.Q and self.Q[new_state]:
            future_q = max(self.Q[new_state].values())
        # Bellman equation to update Q-value
        self.Q[old_state][action] = old_q + self.alpha * (
            reward + self.gamma * future_q - old_q
        )
        if done and self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.Q = pickle.load(f)
            self.epsilon = self.epsilon_min  

    def choose_piece_action(self, board, piece):
        state = self.get_state(board)
        must_capture = True
        all_actions = self.available_actions(board)
        prefix = f"{piece.row},{piece.col}->"
        piece_actions = [a for a in all_actions if a.startswith(prefix)]
        if not piece_actions:
            return None
        if state not in self.Q:
            self.Q[state] = {}
        for a in piece_actions:
            self.Q[state].setdefault(a, 0.0)
        if random.random() < self.epsilon:
            return random.choice(piece_actions) 
        qvals = self.Q[state]
        best_q = max(qvals[a] for a in piece_actions)
        best = [a for a in piece_actions if qvals[a] == best_q]
        return random.choice(best)