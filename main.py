# main.py
import pygame
from board import Board
# from ai import AIPlayer
from ai import QLearningAgent

import random

# ─── Initialization ───────────────────────────────────────────
pygame.init()
WIDTH = HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Test")

board = Board()
ai = QLearningAgent("black")
ai.load("q_black.pkl")
ai.epsilon = 0.1    # small randomness if you like
     # black will be controlled by AI

tile_size = WIDTH // board.cols

turn = "red"            # red starts
selected_piece = None
valid_moves = {}

clock = pygame.time.Clock()
running = True

# ─── Main Game Loop ───────────────────────────────────────────
while running:
    clock.tick(60)  # 60 FPS

    # 1) Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            row, col = my // tile_size, mx // tile_size

            must_capture = board.has_capture(turn)

            if selected_piece:
                # (your existing move‐execution logic here…)
                if (row, col) in valid_moves:
                    captured = board.move_piece(selected_piece, row, col)
                    next_caps = {dst: caps
                                 for dst, caps in board.get_valid_moves(selected_piece).items()
                                 if caps}
                    if captured and next_caps:
                        valid_moves = next_caps
                    else:
                        selected_piece = None
                        valid_moves = {}
                        turn = "black" if turn == "red" else "red"
            else:
                piece = board.grid[row][col]
                if piece and piece.color == turn:
                    all_moves = board.get_valid_moves(piece)
                    if not all_moves:
                        continue
                    if must_capture:
                        cap_moves = {dst: caps
                                     for dst, caps in all_moves.items()
                                     if caps}
                        if not cap_moves:
                            continue
                        valid_moves = cap_moves
                    else:
                        valid_moves = all_moves
                    selected_piece = piece

    # 2) AI Move (Black)
    if turn == "black" and not selected_piece:
        pygame.time.delay(200)

        # pick & play a random forced-capture move
        action = ai.choose_action(board)
        sr, sc, dr, dc = map(int, action.replace('->', ',').split(','))
        piece = board.grid[sr][sc]
        captured = board.move_piece(piece, dr, dc)
        # chain any multi‐jumps
        # after the first move…
        while captured:
        # instead of random.choice, ask the Q-agent:
            action = ai.choose_piece_action(board, piece)
            if not action:
                break
            jr, jc, tr, tc = map(int, action.replace('->',',').split(','))
            captured = board.move_piece(piece, tr, tc)

        turn = "red"

    # 3) Drawing
    board.draw(screen)

    # Highlight valid moves
    if selected_piece:
        for (r, c) in valid_moves:
            cx = c * tile_size + tile_size // 2
            cy = r * tile_size + tile_size // 2
            pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 15)

    # 4) Flip display
    pygame.display.flip()

# ─── Cleanup ───────────────────────────────────────────────────
pygame.quit()
