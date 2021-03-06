from app.core import api
import numpy as np
import pickle

with open('../recording/data/master/sig1.pickle', 'rb') as f:
    sig1 = pickle.load(f)

angles = np.array([
    -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5,
    0,
    +5, +10, +15, +20, +25, +30, +35, +40, +45, +50, +55, +60, +65, +70, +75
])
offsets = np.array([
    [-164, -82, 82, 164],
    [-160, -80, 80, 160],
    [-154, -77, 77, 154],
    [-146, -73, 73, 146],
    [-138, -69, 69, 138],
    [-130, -65, 65, 130],
    [-120, -60, 60, 120],
    [-108, -54, 54, 108],
    [-98, -49, 49, 98],
    [-84, -42, 42, 84],
    [-72, -36, 36, 72],
    [-58, -29, 29, 58],
    [-44, -22, 22, 44],
    [-30, -15, 15, 30],
    [-14, -7, 7, 14],
    [0, 0, 0, 0],
    [14, 7, -7, -14],
    [30, 15, -15, -30],
    [44, 22, -22, -44],
    [58, 29, -29, -58],
    [72, 36, -36, -72],
    [84, 42, -42, -84],
    [98, 49, -49, -98],
    [108, 54, -54, -108],
    [120, 60, -60, -120],
    [130, 65, -65, -130],
    [138, 69, -69, -138],
    [146, 73, -73, -146],
    [154, 77, -77, -154],
    [160, 80, -80, -160],
    [164, 82, -82, -164]
], dtype='double')

api.calculate_signals(offsets, sig1.T)