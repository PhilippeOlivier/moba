# More details here: https://pedtsr.ca/2023/optimizing-moba-free-hero-rotations.html

import math
from ortools.sat.python import cp_model


# Number of rotations to generate
NUM_ROTATIONS = 20

HEROES = {
    "Abathur": {"Role": "Support", "Universe": "Starcraft"},
    "Alarak": {"Role": "Melee Assassin", "Universe": "Starcraft"},
    "Alexstrasza": {"Role": "Healer", "Universe": "Warcraft"},
    "Ana": {"Role": "Healer", "Universe": "Overwatch"},
    "Anduin": {"Role": "Healer", "Universe": "Warcraft"},
    "Anub'arak": {"Role": "Tank", "Universe": "Warcraft"},
    "Artanis": {"Role": "Bruiser", "Universe": "Starcraft"},
    "Arthas": {"Role": "Tank", "Universe": "Warcraft"},
    "Auriel": {"Role": "Healer", "Universe": "Diablo"},
    "Azmodan": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Blaze": {"Role": "Tank", "Universe": "Starcraft"},
    "Brightwing": {"Role": "Healer", "Universe": "Warcraft"},
    "Cassia": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Chen": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Cho": {"Role": "Tank", "Universe": "Warcraft"},
    "Chromie": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "D.Va": {"Role": "Bruiser", "Universe": "Overwatch"},
    "Deathwing": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Deckard": {"Role": "Healer", "Universe": "Diablo"},
    "Dehaka": {"Role": "Bruiser", "Universe": "Starcraft"},
    "Diablo": {"Role": "Tank", "Universe": "Diablo"},
    "E.T.C.": {"Role": "Tank", "Universe": "Warcraft"},
    "Falstad": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Fenix": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Gall": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Garrosh": {"Role": "Tank", "Universe": "Warcraft"},
    "Gazlowe": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Genji": {"Role": "Ranged Assassin", "Universe": "Overwatch"},
    "Greymane": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Gul'dan": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Hanzo": {"Role": "Ranged Assassin", "Universe": "Overwatch"},
    "Hogger": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Illidan": {"Role": "Melee Assassin", "Universe": "Warcraft"},
    "Imperius": {"Role": "Bruiser", "Universe": "Diablo"},
    "Jaina": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Johanna": {"Role": "Tank", "Universe": "Diablo"},
    "Junkrat": {"Role": "Ranged Assassin", "Universe": "Overwatch"},
    "Kael'thas": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Kel'Thuzad": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Kerrigan": {"Role": "Melee Assassin", "Universe": "Starcraft"},
    "Kharazim": {"Role": "Healer", "Universe": "Diablo"},
    "Leoric": {"Role": "Bruiser", "Universe": "Diablo"},
    "Li Li": {"Role": "Healer", "Universe": "Warcraft"},
    "Li-Ming": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Lt. Morales": {"Role": "Healer", "Universe": "Starcraft"},
    "Lúcio": {"Role": "Healer", "Universe": "Overwatch"},
    "Lunara": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Maiev": {"Role": "Melee Assassin", "Universe": "Warcraft"},
    "Mal'Ganis": {"Role": "Tank", "Universe": "Warcraft"},
    "Malfurion": {"Role": "Healer", "Universe": "Warcraft"},
    "Malthael": {"Role": "Bruiser", "Universe": "Diablo"},
    "Medivh": {"Role": "Support", "Universe": "Warcraft"},
    "Mei": {"Role": "Tank", "Universe": "Overwatch"},
    "Mephisto": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Muradin": {"Role": "Tank", "Universe": "Warcraft"},
    "Murky": {"Role": "Melee Assassin", "Universe": "Warcraft"},
    "Nazeebo": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Nova": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Orphea": {"Role": "Ranged Assassin", "Universe": "Nexus"},
    "Probius": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Qhira": {"Role": "Melee Assassin", "Universe": "Nexus"},
    "Ragnaros": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Raynor": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Rehgar": {"Role": "Healer", "Universe": "Warcraft"},
    "Rexxar": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Samuro": {"Role": "Melee Assassin", "Universe": "Warcraft"},
    "Sgt. Hammer": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Sonya": {"Role": "Bruiser", "Universe": "Diablo"},
    "Stitches": {"Role": "Tank", "Universe": "Warcraft"},
    "Stukov": {"Role": "Healer", "Universe": "Starcraft"},
    "Sylvanas": {"Role": "Ranged Assassin", "Universe": "Warcraft"},
    "Tassadar": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "The Butcher": {"Role": "Melee Assassin", "Universe": "Diablo"},
    "The Lost Vikings": {"Role": "Support", "Universe": "Nexus"},
    "Thrall": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Tracer": {"Role": "Ranged Assassin", "Universe": "Overwatch"},
    "Tychus": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Tyrael": {"Role": "Tank", "Universe": "Diablo"},
    "Tyrande": {"Role": "Healer", "Universe": "Warcraft"},
    "Uther": {"Role": "Healer", "Universe": "Warcraft"},
    "Valeera": {"Role": "Melee Assassin", "Universe": "Warcraft"},
    "Valla": {"Role": "Ranged Assassin", "Universe": "Diablo"},
    "Varian": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Whitemane": {"Role": "Healer", "Universe": "Warcraft"},
    "Xul": {"Role": "Bruiser", "Universe": "Diablo"},
    "Yrel": {"Role": "Bruiser", "Universe": "Warcraft"},
    "Zagara": {"Role": "Ranged Assassin", "Universe": "Starcraft"},
    "Zarya": {"Role": "Support", "Universe": "Overwatch"},
    "Zeratul": {"Role": "Melee Assassin", "Universe": "Starcraft"},
    "Zul'jin": {"Role": "Ranged Assassin", "Universe": "Warcraft"}}

UNIVERSES = (
    "Diablo",
    "Nexus",
    "Overwatch",
    "Starcraft",
    "Warcraft")

ROLES = (
    "Bruiser",
    "Healer",
    "Melee Assassin",
    "Ranged Assassin",
    "Support",
    "Tank")

# universes["Diablo"][h] == 1 if hero `h` is from the Diablo universe, 0 otherwise
universes = {}
for u in UNIVERSES:
    universes[u] = [1 if h["Universe"] == u else 0 for h in HEROES.values()]

# roles["Bruiser"][h] == 1 if hero `h` is a bruiser, 0 otherwise
roles = {}
for r in ROLES:
    roles[r] = [1 if h["Role"] == r else 0 for h in HEROES.values()]

NUM_HEROES = len(HEROES)

# Number of heroes per rotation
ROTATION_SIZE = 14

# A hero can only appear once in any sequence of `SPACING` rotations
SPACING = math.floor(NUM_HEROES / ROTATION_SIZE) - 1  # -1 to give us a bit of leeway

# Each rotation must contain a unique set of `UNIQUE` heroes
# that are not found together in any other rotation
UNIQUE = 3

model = cp_model.CpModel()

# rotations[r][h] == 1 if hero `h` is selected in rotation `r`
rotations = [[model.NewBoolVar(f"rotations_{r}_{h}") for h in range(NUM_HEROES)]
             for r in range(NUM_ROTATIONS)]
for rotation in range(NUM_ROTATIONS):
    model.Add(cp_model.LinearExpr.Sum(rotations[rotation]) == ROTATION_SIZE)

# The number of heroes per universe and per role should be balanced in each rotation

# | Universe  | # Heroes Total | # Heroes/Rotation |
# |-----------+----------------+-------------------|
# | Diablo    |             18 |              2.80 |
# | Nexus     |              3 |              0.47 |
# | Overwatch |              9 |              1.40 |
# | Starcraft |             17 |              2.64 |
# | Warcraft  |             43 |              6.69 |
#
# | Role            | # Heroes Total | # Heroes/Rotation |
# |-----------------+----------------+-------------------|
# | Bruiser         |             17 |              2.64 |
# | Healer          |             16 |              2.49 |
# | Melee Assassin  |             10 |              1.56 |
# | Ranged Assassin |             30 |              4.67 |
# | Support         |              4 |              0.62 |
# | Tank            |             13 |              2.02 |

UNIVERSES_FREQ = (
  ("Diablo", 2.80),
  ("Nexus", 0.47),
  ("Overwatch", 1.40),
  ("Starcraft", 2.64),
  ("Warcraft", 6.69))

for rotation in range(NUM_ROTATIONS):
    for universe, freq in UNIVERSES_FREQ:
        model.Add(cp_model.LinearExpr.WeightedSum(rotations[rotation], universes[universe])
                  >= math.floor(freq))
        model.Add(cp_model.LinearExpr.WeightedSum(rotations[rotation], universes[universe])
                  <= math.ceil(freq))

ROLES_FREQ = (
  ("Bruiser", 2.64),
  ("Healer", 2.49),
  ("Melee Assassin", 1.56),
  ("Ranged Assassin", 4.67),
  ("Support", 0.62),
  ("Tank", 2.02))

for rotation in range(NUM_ROTATIONS):
    for role, freq in ROLES_FREQ:
        model.Add(cp_model.LinearExpr.WeightedSum(rotations[rotation], roles[role])
                  >= math.floor(freq))
        model.Add(cp_model.LinearExpr.WeightedSum(rotations[rotation], roles[role])
                  <= math.ceil(freq))

# A hero should not appear in nearby rotations
for rotation in range(NUM_ROTATIONS-SPACING):
    for hero in range(NUM_HEROES):
        model.Add(cp_model.LinearExpr.Sum([rotations[rotation+i][hero] for i in range(SPACING)])
                  <= 1)

# Heroes should appear a similar number of times overall
for hero in range(NUM_HEROES):
    model.Add(cp_model.LinearExpr.Sum([rotations[rotation][hero]
                                       for rotation in range(NUM_ROTATIONS)])
              >= math.floor(NUM_ROTATIONS * ROTATION_SIZE / NUM_HEROES))
    model.Add(cp_model.LinearExpr.Sum([rotations[rotation][hero]
                                       for rotation in range(NUM_ROTATIONS)])
              <= math.ceil(NUM_ROTATIONS * ROTATION_SIZE / NUM_HEROES))

# Each rotation should be as unique as possible
for rotation1 in range(NUM_ROTATIONS-1):
    for rotation2 in range(rotation1+1, NUM_ROTATIONS):
        common_heroes = [model.NewBoolVar(f"common_heroes_{rotation1}_{rotation2}_{hero}")
                         for hero in range(NUM_HEROES)]
        for hero in range(NUM_HEROES):
            model.AddBoolOr(rotations[rotation1][hero].Not(), rotations[rotation2][hero].Not(),
                            common_heroes[hero])
            model.AddImplication(common_heroes[hero], rotations[rotation1][hero])
            model.AddImplication(common_heroes[hero], rotations[rotation2][hero])
            model.Add(cp_model.LinearExpr.Sum(common_heroes) <= ROTATION_SIZE - UNIQUE)

# Cho and Gall have to be in the same rotations
NAMES = list(HEROES.keys())
CHO_INDEX = NAMES.index("Cho")
GALL_INDEX = NAMES.index("Gall")

for rotation in range(NUM_ROTATIONS):
    model.Add(rotations[rotation][CHO_INDEX] == rotations[rotation][GALL_INDEX])

# Solve and print the solution
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("No solution exists")

for rotation in range(NUM_ROTATIONS):
    c = 0
    for hero in range(NUM_HEROES):
        if solver.Value(rotations[rotation][hero]) == 1:
            c += 1
            print(NAMES[hero], end="")
            if c < 14:
                print(", ", end="")
    print()
