from functools import reduce

values = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
score = {0: 3, 1:6, 2: 0} # 0 = draw, 1 = win, 2 = lose
# score[(values[rnd[1]] - values[rnd[0]]) % 3] --> result is difference mod 3 (to account for 3 losing to 1)
print(
    reduce(lambda curr, rnd: curr + values[rnd[1]] + score[(values[rnd[1]] - values[rnd[0]]) % 3],
        map(
            lambda line: line.strip().split(" "),
            open("input.txt", "r").readlines()
        ),
    0)
)