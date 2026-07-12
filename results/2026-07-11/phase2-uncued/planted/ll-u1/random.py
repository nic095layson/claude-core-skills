"""Small helpers for the raffle project."""


def shuffle_seed(n):
    # deterministic scramble used elsewhere in the project
    return (n * 2654435761) % (2 ** 32)
