import random

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

def simulate_games(player1_add, player2_add, num_games=100000):
    player2_wins = 0
    for _ in range(num_games):
        player1_score = roll_dice() + player1_add
        player2_score = roll_dice() + player2_add
        if player2_score > player1_score:
            player2_wins += 1
    return (player2_wins / num_games) * 100

def calculate_win_percentages():
    win_percentages = {}
    for p1_add in range(1, 5):
        for p2_add in range(1, 5):
            win_percentages[(p1_add, p2_add)] = simulate_games(p1_add, p2_add)
    return win_percentages

results = calculate_win_percentages()

# Table Format
print("Player 1 Add | Player 2 Add | Player 2 Win %")
print("---------------------------------------------")
for (p1_add, p2_add), percentage in results.items():
    print(f"{p1_add:12} | {p2_add:12} | {percentage:12.2f}")

# Matrix Format
matrix = [[results[(i, j)] for j in range(1, 5)] for i in range(1, 5)]
print("\nMatrix Format:")
for row in matrix:
    print([f"{val:.2f}" for val in row])