import matplotlib.pyplot as plt
import numpy as np

strategy = [[0 for x in range(2)] for y in range(12)]
beliefs = [[0 for x in range(2)] for y in range(12)]
utilities = [[0 for x in range(2)] for y in range(12)]

strategy[0][0] = 2/3
strategy[1][0] = 1/2
strategy[2][0] = 1/3
strategy[3][0] = 1
strategy[4][0] = 1
strategy[5][0] = 1/2
strategy[6][0] = 2/3
strategy[7][0] = 0
strategy[8][0] = 1/3
strategy[9][0] = 1
strategy[10][0] = 1/2
strategy[11][0] = 0

for i in range(12):
    strategy[i][1] = 1 - strategy[i][0]


CARDS = ["K", "Q", "J"]
MOVE = ["", "b", "p", "pb"]
temp = ["K", "Q", "J", "Kb", "Kp", "Qb", "Qp", "Jb", "Jp", "Kpb", "Qpb", "Jpb"]


class InfoSet:

    def __init__(self, info):
        self.infoSet = info
        self.bet = strategy[temp.index(info)][0]
        self.fold = strategy[temp.index(info)][1]
        self.gains = [0, 0]

    def findBelief(self):
        cur_card = self.infoSet[0]
        cards = [card for card in CARDS if card != cur_card]
        belief = {}
        if len(self.infoSet)== 1:
            belief[0] = 1/2
            belief[1] = 1/2
            return belief

        action = self.infoSet[1]
        if len(self.infoSet)== 3:
            a = infoSets.get(cards[0]+action).bet
            b = infoSets.get(cards[1]+action).bet
        else:
            if action == "b":
                a = infoSets.get(cards[0]).bet
                b = infoSets.get(cards[1]).bet
            else:
                a = infoSets.get(cards[0]).fold
                b = infoSets.get(cards[1]).fold

        if a > 0:
            belief[0] = a/(a+b)
        else:
            belief[0] = 0
        belief[1] = 1 - belief[0]
        return belief

    def findUtility(self):
        cost = 1
        c = 2
        c2 = c
        utility = {}
        cur_card = self.infoSet[0]
        cards = [card for card in CARDS if card != cur_card]
        if  CARDS.index(cur_card) > CARDS.index(cards[0]):
            c *= -1
        if  CARDS.index(cur_card) > CARDS.index(cards[1]):
            c2 *= -1
        cost *= -1

        a = beliefs[temp.index(self.infoSet)][0]
        b = beliefs[temp.index(self.infoSet)][1]
        d = infoSets.get(cards[0] + "pb").bet
        e = infoSets.get(cards[0] + "pb").fold
        d2 = infoSets.get(cards[1] + "pb").bet
        e2 = infoSets.get(cards[1] + "pb").fold

        if len(self.infoSet) == 3 or len(self.infoSet) == 2 and self.infoSet[1] == "b":
            utility[0] = a*c + b*c2
            utility[1] = a*cost + b*cost

        elif len(self.infoSet) == 2:
            utility[0] = a*(d*c + e*(cost*-1)) + b*(d2*c2 + e2*(cost*-1))
            if  CARDS.index(cur_card) > CARDS.index(cards[0]):
                cost = -1
            else: cost = 1
            if  CARDS.index(cur_card) > CARDS.index(cards[1]):
                cost2 = -1
            else: cost2 = 1
            utility[1] = a*cost + b*cost2

        else:
            d = infoSets.get(cards[0] + "b").bet
            e = infoSets.get(cards[0] + "b").fold
            d2 = infoSets.get(cards[1] + "b").bet
            e2 = infoSets.get(cards[1] + "b").fold

            utility[0] = a*(d*c + e*(cost*-1)) + b*(d2*c + e2*(cost*-1))

            d = infoSets.get(cards[0] + "p").bet
            e = infoSets.get(cards[0] + "p").fold
            d2 = infoSets.get(cards[1] + "p").bet
            e2 = infoSets.get(cards[1] + "p").fold

            f = utilities[temp.index(self.infoSet + "pb")][0]
            h = utilities[temp.index(self.infoSet + "pb")][1]
            c = f*infoSets.get(cur_card + "pb").bet + h*infoSets.get(cur_card + "pb").fold

            if  CARDS.index(cur_card) > CARDS.index(cards[0]):
                cost = -1
            else: cost = 1
            if  CARDS.index(cur_card) > CARDS.index(cards[1]):
                cost2 = -1
            else: cost2 = 1

            utility[1] = a*(d*c + e*cost) + b*(d2*c + e2*cost2)

        if abs(utility[0]) < 1e-9:  # Set an appropriate threshold for "close to zero"
            utility[0] = 0
        if abs(utility[1]) < 1e-9:  # Set an appropriate threshold for "close to zero"
            utility[1] = 0
        return utility

    def calculateGains(self):
        cur_card = self.infoSet[0]
        cards = [card for card in CARDS if card != cur_card]
        c = utilities[temp.index(self.infoSet)][0]*self.bet + utilities[temp.index(self.infoSet)][1]*self.fold
        if len(self.infoSet) == 1:
            self.gains[0] += max(1/3*(utilities[temp.index(self.infoSet)][0]-c), 0)
            self.gains[1] += max(1/3*(utilities[temp.index(self.infoSet)][1]-c), 0)
        else:
            if self.infoSet[len(self.infoSet)-1] == "b":
                self.gains[0] += max(1/6*(strategy[temp.index(cards[0])][0]+strategy[temp.index(cards[1])][0])*(utilities[temp.index(self.infoSet)][0]-c), 0)
                self.gains[1] += max(1/6*(strategy[temp.index(cards[0])][0]+strategy[temp.index(cards[1])][0])*(utilities[temp.index(self.infoSet)][1]-c), 0)
            else:
                self.gains[0] += max(1/6*(strategy[temp.index(cards[0])][1]+strategy[temp.index(cards[1])][1])*(utilities[temp.index(self.infoSet)][0]-c), 0)
                self.gains[1] += max(1/6*(strategy[temp.index(cards[0])][1]+strategy[temp.index(cards[1])][1])*(utilities[temp.index(self.infoSet)][1]-c), 0)


infoSets: dict[str, InfoSet] = {}



for i in range(3):
    for j in range(4):
        infoSets[CARDS[i] + MOVE[j]] = InfoSet(CARDS[i] + MOVE[j])


iterations = 30000
lastGains = 0
regret = []

for k in range(iterations):
    for key, infoSet in infoSets.items():
        beliefs[temp.index(infoSet.infoSet)] = list(infoSet.findBelief().values())

    for i in range(12):
        utilities[11-i] = list(infoSets.get(temp[11-i]).findUtility().values())

    totalGains = 0
    for key, infoSet in infoSets.items():
        infoSet.calculateGains()
        idx = temp.index(infoSet.infoSet)
        normalization_factor = infoSet.gains[0] + infoSet.gains[1]
        totalGains += normalization_factor

        if normalization_factor > 0:
            strategy[idx][0] = infoSet.gains[0]
            strategy[idx][1] = infoSet.gains[1]


            strategy[idx][0] /= normalization_factor
            strategy[idx][1] /= normalization_factor

    for key, infoSet in infoSets.items():
        infoSet.bet = strategy[temp.index(key)][0]
        infoSet.fold = strategy[temp.index(key)][1]

    if k%100 == 0:
        regret.append(totalGains - lastGains)
        print(totalGains-lastGains)
        lastGains = totalGains

print("Information Set Strategies:")
print("-----------------------------------------")
print("Info Set  | Bet/Call (%) | Fold (%)")
print("-----------------------------------------")
for key in temp:
    idx = temp.index(key)
    bet_percentage = round(strategy[idx][0] * 100, 2)
    fold_percentage = round(strategy[idx][1] * 100, 2)
    print(f"{key:8} | {bet_percentage:12.2f} | {fold_percentage:9.2f}")
print("-----------------------------------------")

plt.figure(figsize=(10, 6))
plt.plot(np.arange(0, iterations, 100), regret, marker='o', linestyle='-')
plt.title('Regret Over Iterations')
plt.xlabel('Iterations (x100)')
plt.ylabel('Regret')
plt.grid(True)
plt.show()




