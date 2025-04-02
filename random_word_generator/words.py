import secrets

# Load word list
with open("words.txt", "r") as f:
    words = [line.strip() for line in f if line.strip().isalpha()]

# Choose 6 truly random words
random_words = [secrets.choice(words) for _ in range(6)]

print(" ".join(random_words))
