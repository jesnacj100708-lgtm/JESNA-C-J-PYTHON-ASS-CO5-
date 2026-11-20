POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()

    total = 0
    previous = None

    for word in words:
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0

        if previous in NEGATORS:
            value *= -1

        total += value
        previous = word

    return total


def label(text):
    value = score(text)
    return "positive" if value > 0 else "negative" if value < 0 else "neutral"


complaints = [
    "Roads are clean and the bus was fast.",
    "Smoke from the factory, air is bad.",
    "The staff were not helpful.",
    "Not bad, service improved.",
    "The road is dirty and the bus is slow.",
    "The air is good today."
]

for item in complaints:
    print(f"{label(item):8} | {item}")
