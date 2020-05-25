import random
import math
from parameters import params, experimentation
from sklearn.neighbors import KDTree
from fireFly import FireFly
import numpy as np
import turtle


#############################################
#
#   DIFFERENT WAYS TO GENERATE POPULATION
#
#############################################
def generate_population_randomly():
    population = []
    x_max = params['X_MAX']
    y_max = params['Y_MAX']
    period_domain = [params['PERIOD_MIN'], params['PERIOD_MAX']]
    latency = params['LATENCY'] # we can change so latency will also between some min and max value
    subtraction_time = params['SUBTRACTION_TIME'] # time we substract from counter if we get signal from other firefly
    period_threshold = 0.0
    coords = []
    for id in range(params['POP_SIZE']):
        t = turtle.Turtle(shape="circle")
        t.shapesize(0.5,0.5)
        x_coord = random.randint(0, x_max)
        y_coord = random.randint(0,y_max)
        t.hideturtle()
        t.up()
        t.goto((x_coord, y_coord))
        t.showturtle()
        coords.append([x_coord, y_coord])
        latency = 0#random.randint(0,10)
        period = random.uniform(period_domain[0], period_domain[1])
        waiting_time = 1
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.01), expFunct(0.01,-1), latency, t))

    find_n_nearest_neighbours(population, coords)

    return population

def generate_population_randomly_grid():
    x_max = params['X_MAX']
    y_max = params['Y_MAX']
    empty_cells = [(x, y) for y in range(y_max) for x in range(x_max)]

    if x_max * y_max <= params["POP_SIZE"]:
        print("Not enough size on the grid for the chosen number of fireflies")

    population = []
    period_domain = [params['PERIOD_MIN'], params['PERIOD_MAX']]
    latency = params['LATENCY'] # we can change so latency will also between some min and max value
    subtraction_time = params['SUBTRACTION_TIME'] # time we substract from counter if we get signal from other firefly
    period_threshold = 0.0
    coords = []
    for id in range(params['POP_SIZE']):
        # t = turtle.Turtle(shape="circle")
        # t.shapesize(0.5,0.5)
        t = None
        x_coord, y_coord = empty_cells.pop(random.randint(0,len(empty_cells)-1))

        # t.hideturtle()
        # t.up()
        # t.goto((x_coord, y_coord))
        # t.showturtle()
        coords.append([x_coord, y_coord])
        latency = 0 #random.randint(0,10)
        period = random.uniform(period_domain[0], period_domain[1])
        waiting_time = 1
        population.append(FireFly(id,x_coord, y_coord, period, period_threshold,waiting_time, linearFunct(0.01), expFunct(0.01,-1), latency, turtle=t))

    for ff in population:
        ff.setNeighbours(get_neighbours(ff, population))
    # find_n_nearest_neighbours(population, coords)

    return population

def generate_population_manualy():
    fireflyes = []

    fireflyes.append(FireFly(1, 0, 0, 4, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 5))
    fireflyes.append(FireFly(2, 1, 2, 3, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 1))
    fireflyes.append(FireFly(3, 4, 5, 2.5, 1.5, 0.5, linearFunct(0.05), expFunct(0.1,-1), start_delay = 3))
    fireflyes.append(FireFly(4, 9, 9, 7, 1.5, 0.5, linearFunct(0.05), expFunct(5,-1), start_delay = 7))

    fireflyes[0].setNeighbours([fireflyes[1], fireflyes[2], fireflyes[3]])
    fireflyes[1].setNeighbours([fireflyes[0], fireflyes[2], fireflyes[3]])
    fireflyes[2].setNeighbours([fireflyes[3], fireflyes[0], fireflyes[1]])
    fireflyes[3].setNeighbours([fireflyes[0], fireflyes[1], fireflyes[2]])

    return fireflyes


################################################
#
#   DIFFERENT FUNCTIONS FOR ADDING TO PERIOD WHEN FIREFLY
#   DIDN'T GET ANY SIGNAL FROM OTHER FIREFLIES
#
################################################

def expFunct(A=0.1, b=1):
    def fun(x):
        return A * math.exp(b*x)
    return fun

def linearFunct(m = 0.1, b = 0):
    def fun(x):
        return m * x + b
    return fun

def contFunction(A=0.05):
    def fun(x):
        return A
    return fun


################################################
#
#   OTHER AUXILIARY FUNCTIONS
#
################################################


def find_n_nearest_neighbours(fireflyes, X):
    neighbours = []
    X = np.array(X)
    tree = KDTree(X, leaf_size=2)
    for i in range(len(fireflyes)):
        _ , ind = tree.query([X[i]], k=params['N_NEIGHBOURS'] + 1)
        for j in ind[0]:
            if j != i:
                neighbours.append(fireflyes[j])
        fireflyes[i].setNeighbours(neighbours)

def get_neighbours(firefly, fireflies):
    neighbors = []
    for f in fireflies:
        if f.id != firefly.id:
            dx = abs(firefly.x_coord - f.x_coord)
            dy = abs(firefly.y_coord - f.y_coord)
            if dx <= params["NEIGHBOURS_DIST"] * math.sqrt(2) and dy <= params["NEIGHBOURS_DIST"] * math.sqrt(2):
                neighbors.append(f)
    return neighbors