import copy
import heapq
import metrics
import multiprocessing.pool as mpool
import os
import random
import shutil
import time
import math

width = 200
height = 16

options = [
    "-",  # an empty space
    "X",  # a solid wall
    "?",  # a question mark block with a coin
    "M",  # a question mark block with a mushroom
    "B",  # a breakable block
    "o",  # a coin
    "|",  # a pipe segment
    "T",  # a pipe top
    "E",  # an enemy
    #"f",  # a flag, do not generate
    #"v",  # a flagpole, do not generate
    #"m"  # mario's start position, do not generate
]

# The level as a grid of tiles

def pr(percent):
    return random.randint(0,100) <= percent



class Individual_Grid(object):
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None

    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.
    def calculate_fitness(self):
        measurements = metrics.metrics(self.to_level())
        # Print out the possible measurements or look at the implementation of metrics.py for other keys:
        # print(measurements.keys())
        # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
        # STUDENT Modify this, and possibly add more metrics.  You can replace this with whatever code you like.
        coefficients = dict(
            meaningfulJumpVariance=0.5,
            negativeSpace=0.6,
            pathPercentage=0.5,
            emptyPercentage=0.6,
            linearity=-0.5,
            solvability=2.0
        )
        self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                                coefficients))
        return self

    # Return the cached fitness value or calculate it as needed.
    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        return self._fitness

    # Mutate a genome into a new genome.  Note that this is a _genome_, not an individual!
    #This should be static
    def mutate(self, genome):
        # STUDENT implement a mutation operator, also consider not mutating this individual
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc

        left = 3
        right = width - 5
        items = {
            "-":0,
            "X":0,
            "B":0,
            "E":10,
            "?":0,
            "M":0,
            "o":10,
            "|":0,
            "T":0
        }
        
        for i in items.keys():
            for p in range(items[i]):
                x = random.randint(left,right)
                y = random.randint(0,height-1)
                genome[y][x] = i

        

        for x in range(left, right):
            for y in range(height):
                #x = random.randint(left,right)
                #y = random.randint(0,height-1)
                try:

                    if (genome[y][x] == '|' and not (genome[y+1][x] == 'X' or genome[y+1][x] == '|')):
                        genome[y][x] = '-'
                    if genome[y][x] == '|':
                        if pr(70) and genome[y-1][x] != "T":
                            genome[y-1][x] = "|"
                        else:
                            genome[y-1][x] = "T"
                            genome[y-2][x] = "-"
                        
                    if genome[y][x] == 'T' and genome[y+1][x] != '|':
                        genome[y][x] = '-'
                    

                    if genome[y][x] in ['B', 'E', '?', 'M']:
                        if genome[y+1][x] != "-" and genome[y+2][x] != "-":
                            genome[y-2][x] = genome[y][x]
                            genome[y-1][x] = "-"
                            genome[y][x] = "-"

                    
                    if genome[y][x] == "-":
                        if genome[y+1][x] not in ["-", "o"] and genome[y-1][x] not in ["-", "o"]:
                            genome[y+1][x] = "-"
                            genome[y-1][x] = "-"
                            

                    
                    if(genome[y+1][x] == "-" and genome[y+2][x] == "-"):
                        if(pr(5)):
                            genome[y][x] = random.choice(['?', 'M'])

                    if genome[y][x] in ['X','B']:
                        new_x = x
                        new_y = y
                        
                        while new_y > 2 and genome[new_y][new_x] in ["X",'B']:
                            new_y-=1
                        if abs(new_y - y) > 2:
                            genome[new_y+1][x] = "-"
                        new_y = y
                    
                    

                        if random.randint(0,100) < (100*(y/16)):
                            new_x = random.randint(2,4) - 1 + new_x
                            new_y = random.randint(-4,1) + 1 + new_y
                            if genome[new_y][new_x] not in ['o', '|', 'T']:
                                    genome[new_y][new_x] = genome[y][x]
                        elif random.randint(0,100) < 100 - 100*(y/16) and genome[new_y-1][new_x] not in ['?', 'M', '|', 'T']:
                            if genome[new_y][new_x] not in ['?', 'M', '|', 'T']:    
                                genome[new_y][new_x] = '-'
                
                    #if genome[y][x] == 'E' and genome[y+1][x] != 'X':
                    #    genome[y][x] = '-'

                    if genome[y][x] in ['?', 'M']:
                        keep = False
                        for off_x in range(-2,2):
                            for off_y in range(2, 4):
                                if genome[y+off_y][x+off_x] in  ["X", "B"]:
                                    keep = True
                        if not keep:
                            genome[y][x] = "-"
                            pass

                    #drop coins
                    if genome[y][x] in ['o', 'E']:
                        if y+1 > height:
                            genome[y][x] = "-"
                        if genome[y+1][x] == "-" and pr(10):
                            genome[y+1][x] = genome[y][x]
                            genome[y][x] = "-"
                    
                        

                    #if genome[y][x] == '?' or genome[y][x] == 'M' or genome[y][x] == 'B' or genome[y][x] == 'o':
                    #    genome[y][x] = '-'

                except:
                    pass
        

        for i in range(height-2):
            genome[i][0:5] = ["-"] * 5
        genome[14][1:5] = ["-"] * 4
        genome[13][1:5] = ["-"] * 4
        
        for i in range(height-1):
            genome[i][-5:-1] = ["-"] * 4
        
        for i in range(0,7):
            genome[i][-1] = "-"

        # genome[7][-3] = "v"
        # for col in range(8, 14):
        #     genome[col][-3] = "f"
        # for col in range(14, 16):
        #     genome[col][-3] = "X"

        return genome

    # Create zero or more children from self and other
    def generate_children(self, other):
        new_genomeS = copy.deepcopy(self.genome)
        new_genomeO = copy.deepcopy(other.genome)
        #genomeS = copy.deepcopy(self.genome)
        #genomeO = copy.deepcopy(other.genome)
        # Leaving first and last columns alone...
        # do crossover with other
        left = 1
        right = width - 1
        
        """for i in range(1000):
            x = random.randint(left,right - 5)
            y = random.randint(0,height-5)

            temp = new_genomeS[y][x]
            new_genomeO[y][x] = new_genomeS[y][x]
            new_genomeS[y][x] = temp 

            

            pass
        """
        
        
        """
        for x in range(left, right):
            s = 0
            o = 0
            for y in range(height):
                if new_genomeS[y][x] == "-":
                    s+=1
                    new_genomeO[y][x] = new_genomeS[y][x]

                if new_genomeO[y][x] == "-":
                    o+=1
                    new_genomeS[y][x] = new_genomeO[y][x]
        """
        
        
        
        for x in range(left, right):
            x += random.randint(0,20)  
            for offset in range(10):
                if(x+offset) >= right:
                    break
                for y in range(height):
                    #[y][x]
                    temp = new_genomeS[y][x+offset]
                    new_genomeS[y][x+offset] = new_genomeO[y][x+offset]
                    new_genomeO[y][x+offset] = temp
                    pass
                x+=10
        new_genomeO = self.mutate(new_genomeO)
        new_genomeS = self.mutate(new_genomeS)
        """        
        ngo = new_genomeO
        ngs = new_genomeS
        for y in range(0,height):
            for x in range(left, right):
                if ngs[y][x] == 'X':
                    count = 0
                    l = x
                    while ngs[y][l] == "X" and l < right:
                        count+=1
                        l+=1
                    r = x
                    while ngs[y][r] == "X" and r > left:
                        count+=1
                        r-=1
                    if  count < 1:
                        while r < l:
                            ngs[y][r] = "-"
                            r+=1
                if ngs[y][x] == 'E' and ngs[y-1][x] != 'X':
                    ngs[y][x] == "-"
                if ngs[y][x] == '|':
                    for a in range(y, 0, -1):
                        if ngs[a][x] == 'T':
                            break
                        if ngs[a][x] != '|':
                            ngs[a][x] = '-'
                            break
                if ngs[y][x] == '?' or 'M' or 'B' or 'o':
                    ngs[y][x] = '-' 

                pass
            """

        return (Individual_Grid(new_genomeS), Individual_Grid(new_genomeS))

    # Turn the genome into a level string (easy for this genome)
    def to_level(self):
        return self.genome

    # These both start with every floor tile filled with Xs
    # STUDENT Feel free to change these
    @classmethod
    def empty_individual(cls):
        g = [["-" for col in range(width)] for row in range(height)]
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        for col in range(8, 14):
            g[col][-1] = "f"
        for col in range(14, 16):
            g[col][-1] = "X"
        return cls(g)

    @classmethod
    def random_individual(cls):
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        g = [random.choices(options, k=width) for row in range(height)]
        
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        for col in range(8, 14):
            g[col][-1] = "f"
        for col in range(14, 16):
            g[col][-1] = "X"
        #g[8:14][-1] = ["f"] * 6
        #g[14:16][-1] = ["X", "X"]
        return cls(g)


def offset_by_upto(val, variance, min=None, max=None):
    val += random.normalvariate(0, variance**0.5)
    if min is not None and val < min:
        val = min
    if max is not None and val > max:
        val = max
    return int(val)


def clip(lo, val, hi):
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val

# Inspired by https://www.researchgate.net/profile/Philippe_Pasquier/publication/220867545_Towards_a_Generic_Framework_for_Automated_Video_Game_Level_Creation/links/0912f510ac2bed57d1000000.pdf


class Individual_DE(object):
    # Calculating the level isn't cheap either so we cache it too.
    __slots__ = ["genome", "_fitness", "_level"]

    # Genome is a heapq of design elements sorted by X, then type, then other parameters
    def __init__(self, genome):
        self.genome = list(genome)
        heapq.heapify(self.genome)
        self._fitness = None
        self._level = None

    # Calculate and cache fitness
    def calculate_fitness(self):
        measurements = metrics.metrics(self.to_level())
        # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
        # STUDENT Add more metrics?
        # STUDENT Improve this with any code you like
        coefficients = dict(
            meaningfulJumpVariance=0.5,
            negativeSpace=0.6,
            pathPercentage=0.5,
            emptyPercentage=0.6,
            linearity=-0.5,
            solvability=2.0
        )
        penalties = 0
        # STUDENT For example, too many stairs are unaesthetic.  Let's penalize that
        if len(list(filter(lambda de: de[1] == "6_stairs", self.genome))) > 5:
            penalties -= 2
        if len(list(filter(lambda de: de[1] == "3_coin", self.genome))) < 2: # too few coins
            penalties -= 2
        if len(list(filter(lambda de: de[1] == "0_hole", self.genome))) < 1: # no gaps/holes
            penalties -= 2
        if len(list(filter(lambda de: de[1] == "5_qblock", self.genome))) > 6: # too many qblocks 
            penalties -= 2
        if len(list(filter(lambda de: de[1] == "2_enemy", self.genome))) > 6: # too many enemies
            penalties -= 2
        if len(list(filter(lambda de: de[1] == "2_enemy", self.genome))) < 2: # not enough enemies
            penalties -= 2

        for item in list(filter(lambda de: de[1] == "0_hole", self.genome)): # connected holes
            try:
                if self.to_level()[15][item[0] + item[2]] == "-":
                    penalties -= 6
            except:
                    pass

        for x in range(0,2): # check for cluttering around mario
            for item in list(filter(lambda de: de[0] == x, self.genome)):
                if item[1] != "4_block" or item[2] != 15:
                    penalties -= 4
                
        # STUDENT If you go for the FI-2POP extra credit, you can put constraint calculation in here too and cache it in a new entry in __slots__.
        self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                                coefficients)) + penalties
        return self

    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        return self._fitness

    def mutate(self, new_genome):
        # STUDENT How does this work?  Explain it in your writeup.
        # STUDENT consider putting more constraints on this, to prevent generating weird things
        if random.random() < 0.1 and len(new_genome) > 0:
            to_change = random.randint(0, len(new_genome) - 1)
            de = new_genome[to_change]
            new_de = de
            x = de[0]
            de_type = de[1]
            choice = random.random()
            if de_type == "4_block":
                y = de[2]
                breakable = de[3]
                if choice < 0.33:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.66:
                    y = offset_by_upto(y, height / 2, min=0, max=height - 1)
                else:
                    breakable = not de[3]
                new_de = (x, de_type, y, breakable)
            elif de_type == "5_qblock":
                y = de[2]
                has_powerup = de[3]  # boolean
                if choice < 0.33:
                    try:
                        count = 0
                        while self.to_level()[y + 1][x] != "-" and x > 14 and count < 16:
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                            count += 1
                    except:
                        pass
                elif choice < 0.66:
                    try:
                        count = 0
                        while self.to_level()[y + 1][x] != "-" and count < 200:
                            y = offset_by_upto(y, height / 2, min=0, max=height - 1)
                            count += 1
                    except:
                        pass
                else:
                    has_powerup = not de[3]
                new_de = (x, de_type, y, has_powerup)
            elif de_type == "3_coin":
                y = de[2]
                if choice < 0.5:
                    while x > 14:
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                else:
                    y = offset_by_upto(y, height / 2, min=0, max=height - 1)
                new_de = (x, de_type, y)
            elif de_type == "7_pipe":
                h = de[2]
                if choice < 0.5:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                else:
                    h = offset_by_upto(h, 2, min=2, max=height - 4)
                new_de = (x, de_type, h)
            elif de_type == "0_hole":
                w = de[2]
                if choice < 0.5:
                    try:
                        count = 0
                        while self.to_level()[y][x + w] == "-" and count < 200:
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                            count += 1
                    except:
                        pass
                else:
                    try:
                        count = 0
                        while self.to_level()[y][x + w] == "-" and count < 8:
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                            count += 1
                        else:
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                    except:
                        pass
                    w = offset_by_upto(w, 4, min=1, max=width - 2)
                new_de = (x, de_type, w)
            elif de_type == "6_stairs":
                h = de[2]
                dx = de[3]  # -1 or 1
                if choice < 0.33:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.66:
                    h = offset_by_upto(h, 8, min=1, max=height - 4)
                else:
                    dx = -dx
                new_de = (x, de_type, h, dx)
            elif de_type == "1_platform":
                w = de[2]
                y = de[3]
                madeof = de[4]  # from "?", "X", "B"
                if choice < 0.25:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.5:
                    w = offset_by_upto(w, 8, min=1, max=width - 2)
                elif choice < 0.75:
                    y = offset_by_upto(y, height, min=0, max=height - 1)
                else:
                    madeof = random.choice(["?", "X", "B"])
                new_de = (x, de_type, w, y, madeof)
            elif de_type == "2_enemy":
                x = de[0]
                y = de[0]
                if self.to_level()[15][x] == "X":
                    try:
                        count = 0
                        while self.to_level()[y][x] != "X" and count < 200: 
                            x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                            count += 1
                    except:
                        pass
            new_genome.pop(to_change)
            heapq.heappush(new_genome, new_de)
        return new_genome

    def generate_children(self, other):
        # STUDENT How does this work?  Explain it in your writeup.
        pa = random.randint(0, len(self.genome) - 1)
        pb = random.randint(0, len(other.genome) - 1)
        a_part = self.genome[:pa] if len(self.genome) > 0 else []
        b_part = other.genome[pb:] if len(other.genome) > 0 else []
        ga = a_part + b_part
        b_part = other.genome[:pb] if len(other.genome) > 0 else []
        a_part = self.genome[pa:] if len(self.genome) > 0 else []
        gb = b_part + a_part
        # do mutation
        return Individual_DE(self.mutate(ga)), Individual_DE(self.mutate(gb))

    # Apply the DEs to a base level.
    def to_level(self):
        if self._level is None:
            base = Individual_Grid.empty_individual().to_level()
            for de in sorted(self.genome, key=lambda de: (de[1], de[0], de)):
                # de: x, type, ...
                x = de[0]
                de_type = de[1]
                if de_type == "4_block":
                    y = de[2]
                    breakable = de[3]
                    base[y][x] = "B" if breakable else "X"
                elif de_type == "5_qblock":
                    y = de[2]
                    has_powerup = de[3]  # boolean
                    base[y][x] = "M" if has_powerup else "?"
                elif de_type == "3_coin":
                    y = de[2]
                    base[y][x] = "o"
                elif de_type == "7_pipe":
                    h = de[2]
                    base[height - h - 1][x] = "T"
                    for y in range(height - h, height):
                        base[y][x] = "|"
                elif de_type == "0_hole":
                    w = de[2]
                    for x2 in range(w):
                        base[height - 1][clip(1, x + x2, width - 2)] = "-"
                elif de_type == "6_stairs":
                    h = de[2]
                    dx = de[3]  # -1 or 1
                    for x2 in range(1, h + 1):
                        for y in range(x2 if dx == 1 else h - x2):
                            base[clip(0, height - y - 1, height - 1)][clip(1, x + x2, width - 2)] = "X"
                elif de_type == "1_platform":
                    w = de[2]
                    h = de[3]
                    madeof = de[4]  # from "?", "X", "B"
                    for x2 in range(w):
                        base[clip(0, height - h - 1, height - 1)][clip(1, x + x2, width - 2)] = madeof
                elif de_type == "2_enemy":
                    base[height - 2][x] = "E"
            self._level = base
        return self._level

    @classmethod
    def empty_individual(_cls):
        # STUDENT Maybe enhance this
        g = []
        return Individual_DE(g)

    @classmethod
    def random_individual(_cls):
        # STUDENT Maybe enhance this
        elt_count = random.randint(8, 128)
        g = [random.choice([
            (random.randint(1, width - 2), "0_hole", random.randint(1, 8)),
            (random.randint(1, width - 2), "1_platform", random.randint(1, 8), random.randint(0, height - 1), random.choice(["?", "X", "B"])),
            (random.randint(1, width - 2), "2_enemy"),
            (random.randint(1, width - 2), "3_coin", random.randint(0, height - 1)),
            (random.randint(1, width - 2), "4_block", random.randint(0, height - 1), random.choice([True, False])),
            (random.randint(1, width - 2), "5_qblock", random.randint(0, height - 1), random.choice([True, False])),
            (random.randint(1, width - 2), "6_stairs", random.randint(1, height - 4), random.choice([-1, 1])),
            (random.randint(1, width - 2), "7_pipe", random.randint(2, height - 4))
        ]) for i in range(elt_count)]
        return Individual_DE(g)


Individual = Individual_Grid


def generate_successors(population):
    # STUDENT Design and implement this
    # Hint: Call generate_children() on some individuals and fill up results.
    results = []
    popTuple = []
    selectIndiv = []
    for i in range(0, len(population)):
        popTuple.append((population[i],population[i].fitness()))
    popTuple.sort(key = lambda x: x[1], reverse = True)
    #popTuple.pop()
    #for i in range(math.floor((len(popTuple)+1)/3)):
    
    #remove the weakest
    
    #selectIndiv = popTuple

    #roulette
    for i in range(0, len(popTuple)):
        if(random.randrange(0,len(popTuple) - 1) < i):
            selectIndiv.append(popTuple[i])

    #elitism
    b = int(len(popTuple)/2)
    while b<len(popTuple):
        temp= popTuple[b]
        results.append(temp[0])
        b = b +1
    
    for i in range(0, int(len(selectIndiv) / 2)): # pair selected individuals randomly and repopulate
        if len(selectIndiv[i][0].genome) == 0:
            results.append(selectIndiv[i + int(len(selectIndiv) / 2)][0])
        elif len(selectIndiv[i + int(len(selectIndiv) / 2)][0].genome) == 0:
            results.append(selectIndiv[i][0])
        else:
            for child in selectIndiv[i][0].generate_children(selectIndiv[i + int(len(selectIndiv) / 2)][0]):
                results.append(child)
        # for child in selectIndiv[i + int(len(selectIndiv) / 2)][0].generate_children(selectIndiv[i][0]):
        #     results.append(child)
    # # print("Original population: ", population)
    # # print("Result population: ", results)
    for item in selectIndiv:
        if len(results) < 200:
            results.append(item[0])
    print("Original num: ", len(population))
    print("Result num: ", len(results))
    # print("genome: ", results[0].genome)
    # print("fitness: ", results[0].fitness())
    return results


def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 50
    # Code to parallelize some computations
    batches = os.cpu_count()
    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))
    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()
        # STUDENT (Optional) change population initialization
        population = [Individual.random_individual() if random.random() < 0.9
                      else Individual.empty_individual()
                      for _g in range(pop_limit)]
        # But leave this line alone; we have to reassign to population because we get a new population that has more cached stuff in it.
        population = pool.map(Individual.calculate_fitness,
                              population,
                              batch_size)
        init_done = time.time()
        print("Created and calculated initial population statistics in:", init_done - init_time, "seconds")
        generation = 0
        start = time.time()
        now = start
        print("Use ctrl-c to terminate this loop manually.")
        try:
            while True:
                now = time.time()
                # Print out statistics
                best = max(population, key=Individual.fitness)
                if generation > 0:
                    print("Generation:", str(generation))
                    print("Max fitness:", str(best.fitness()))
                    print("Average generation time:", (now - start) / generation)
                    print("Net time:", now - start)
                    with open("level.txt", 'w') as f:
                        for row in best.to_level():
                            f.write("".join(row) + "\n")
                generation += 1
                # STUDENT Determine stopping condition
                stop_condition = False
                if Individual == Individual_DE:
                    if best.fitness() > 2.9 and metrics.metrics(best.to_level())['solvability'] == 1:
                        stop_condition = True
                elif Individual == Individual_Grid:
                    if best.fitness() > 4 and metrics.metrics(best.to_level())['solvability'] == 1:
                        stop_condition = True
                if stop_condition:
                    break
                # STUDENT Also consider using FI-2POP as in the Sorenson & Pasquier paper
                gentime = time.time()
                next_population = generate_successors(population)
                gendone = time.time()
                print("Generated successors in:", gendone - gentime, "seconds")
                # Calculate fitness in batches in parallel
                next_population = pool.map(Individual.calculate_fitness,
                                           next_population,
                                           batch_size)
                popdone = time.time()
                print("Calculated fitnesses in:", popdone - gendone, "seconds")
                population = next_population
        except KeyboardInterrupt:
            pass
    return population


if __name__ == "__main__":
    final_gen = sorted(ga(), key=Individual.fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness: " + str(best.fitness()))
    now = time.strftime("%m_%d_%H_%M_%S")
    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...
    for k in range(0, 10):
        with open( now + "_" + str(k) + ".txt", 'w') as f:
            for row in final_gen[k].to_level():
                f.write("".join(row) + "\n")
