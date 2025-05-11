import pygame
from board import Board
from ai import QLearningAgent
import random

# Initialize Pygame and screen
pygame.init()
pygame.event.clear()
font = pygame.font.SysFont(None, 24)
WIDTH = HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Checkers")

def show_menu():
    menu_font = pygame.font.SysFont(None, 36)
    mode = None
    difficulty = None
    waiting = True

    while waiting:
        screen.fill((30, 30, 60))
        title = menu_font.render("AI Checkers", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        options = [
            "1. Human vs AI",
            "2. Human vs Human",
            "3. AI vs AI",
            "Select difficulty: E(easy), M(medium),",
            "H(Hard)"
        ]

        for i, text in enumerate(options):
            line = menu_font.render(text, True, (200, 200, 255))
            screen.blit(line, (100, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "Human_vs_AI"
                elif event.key == pygame.K_2:
                    mode = "Human_vs_Human"
                elif event.key == pygame.K_3:
                    mode = "AI_vs_AI"
                elif event.key == pygame.K_e:
                    difficulty = "Easy"
                elif event.key == pygame.K_m:
                    difficulty = "Medium"
                elif event.key == pygame.K_h:
                    difficulty = "Hard"
            if mode and (mode == "Training" or difficulty):
                print(f"Selected mode: {mode}, difficulty: {difficulty}")
                return mode, difficulty

# Game statistics
stats = {
    "games_played": 0,
    "red_wins": 0,
    "black_wins": 0,
    "ties": 0,
    "total_moves": 0
}

difficulty_settings = {
    "Easy": 0.5,
    "Medium": 0.2,
    "Hard": 0.05
}

# Show menu and configure agents
mode, difficulty = show_menu()
pygame.event.clear()

red_is_ai = mode != "Human_vs_Human"
black_is_ai = mode == "AI_vs_AI"

board = Board()
tile_size = WIDTH // board.cols
turn = "red"
selected_piece = None
valid_moves = {}
moves_count = 0
clock = pygame.time.Clock()
running = True

ai_red = QLearningAgent("red") if red_is_ai else None
ai_black = QLearningAgent("black") if black_is_ai else None

if ai_red:
    ai_red.load("q_red.pkl")
    ai_red.epsilon = difficulty_settings[difficulty]

if ai_black:
    ai_black.load("q_black.pkl")
    ai_black.epsilon = difficulty_settings[difficulty]

# Function to show win message and handle restart/quit
def handle_game_end(winner):
    stats["games_played"] += 1
    stats["total_moves"] += moves_count
    if winner == "red":
        stats["red_wins"] += 1
    elif winner == "black":
        stats["black_wins"] += 1
    else:
        stats["ties"] += 1

    win_msg = f"{winner.capitalize()} wins!"
    text1 = font.render(win_msg, True, (255, 215, 0))
    text2 = font.render("Press R to restart or Q to quit", True, (0, 0, 0))
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # restart
                elif event.key == pygame.K_q:
                    pygame.quit(); exit()

# Main game loop
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (turn == "red" and not red_is_ai) or (turn == "black" and not black_is_ai):
                mx, my = pygame.mouse.get_pos()
                row, col = my // tile_size, mx // tile_size
                must_capture = board.has_capture(turn)

                if selected_piece:
                    if (row, col) in valid_moves:
                        captured = board.move_piece(selected_piece, row, col)
                        moves_count += 1
                        winner = board.check_winner()
                        if winner:
                            if handle_game_end(winner):
                                board = Board(); turn = "red"; selected_piece = None
                                valid_moves = {}; moves_count = 0
                                continue

                        next_caps = {
                            dst: caps for dst, caps in board.get_valid_moves(selected_piece).items() if caps
                        }
                        if captured and next_caps:
                            valid_moves = next_caps
                        else:
                            selected_piece = None; valid_moves = {}
                            turn = "black" if turn == "red" else "red"
                else:
                    piece = board.grid[row][col]
                    if piece and piece.color == turn:
                        all_moves = board.get_valid_moves(piece)
                        if not all_moves:
                            continue
                        if must_capture:
                            cap_moves = {dst: caps for dst, caps in all_moves.items() if caps}
                            if not cap_moves:
                                continue
                            valid_moves = cap_moves
                        else:
                            valid_moves = all_moves
                        selected_piece = piece

    for ai, color in [(ai_red, "red"), (ai_black, "black")]:
        if turn == color and ai and not selected_piece:
            pygame.time.delay(800)
            action = ai.choose_action(board)
            sr, sc, dr, dc = map(int, action.replace('->', ',').split(','))
            piece = board.grid[sr][sc]
            captured = board.move_piece(piece, dr, dc)
            moves_count += 1
            winner = board.check_winner()
            if winner:
                if handle_game_end(winner):
                    board = Board(); turn = "red"; selected_piece = None
                    valid_moves = {}; moves_count = 0
                    break

            while captured:
                action = ai.choose_piece_action(board, piece)
                if not action:
                    break
                sr, sc, dr, dc = map(int, action.replace('->', ',').split(','))
                captured = board.move_piece(piece, dr, dc)
                moves_count += 1
            winner = board.check_winner()
            if winner:
                if handle_game_end(winner):
                    board = Board(); turn = "red"; selected_piece = None
                    valid_moves = {}; moves_count = 0
                    break

            turn = "black" if turn == "red" else "red"

    # Draw board
    board.draw(screen)
    turn_color = (255, 0, 0) if turn == "red" else (0, 0, 0)
    turn_text = font.render(f"Turn: {turn.capitalize()}", True, turn_color)
    screen.blit(turn_text, (WIDTH - 150, 10))

    stats_text = f"Games: {stats['games_played']}  Red Wins: {stats['red_wins']}  Black Wins: {stats['black_wins']}"
    if stats['games_played'] > 0:
        avg_moves = stats['total_moves'] / stats['games_played']
        stats_text += f"  Avg Moves/Game: {avg_moves:.1f}"
    text_surface = font.render(stats_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    if selected_piece:
        for (r, c) in valid_moves:
            cx = c * tile_size + tile_size // 2
            cy = r * tile_size + tile_size // 2
            pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 15)

    pygame.display.flip()

pygame.quit()