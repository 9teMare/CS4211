import numpy as np
from gen_prob import *

def gen_softmax_home_prob(home_prob, away_prob):
    probs = np.array([home_prob, away_prob])
    softmax_probs = np.exp(probs) / np.sum(np.exp(probs))
    return softmax_probs[0]

# Example usage
home_prob = gen_prob("20152016_12115_AFC_Bournemouth_Aston_Villa_home")
print("home_prob: {0}".format(home_prob))
away_prob = gen_prob("20152016_12115_AFC Bournemouth_Aston Villa_away")
print("away_prob: {0}".format(away_prob))
softmax_home_prob = gen_softmax_home_prob(home_prob, away_prob)
print("softmax_home_prob: {0}".format(softmax_home_prob))