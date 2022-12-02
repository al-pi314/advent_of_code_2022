from functools import reduce

values = {"A": 1, "B": 2, "C": 3}
score = {0: 3, 1:6, 2: 0} # 0 = draw, 1 = win, 2 = lose
a = {"X": -1, "Y":0, "Z":1} # value adjustment (-1 decrease to lose, 0 draw, 1 increase to win)
# ((values[rnd[0]] + a[rnd[1]] -1) % 3 +1) --> adjusted value based on desired result (-1 to operate on [0, 2] and +1 to move back to [1, 3])
print(
    reduce(lambda curr, rnd: curr + ((values[rnd[0]] + a[rnd[1]] -1) % 3 +1) + score[(((values[rnd[0]] + a[rnd[1]] -1) % 3 +1) - values[rnd[0]]) % 3],
        map(
            lambda line: line.strip().split(" "),
            open("input.txt", "r").readlines()
        ),
    0)
)