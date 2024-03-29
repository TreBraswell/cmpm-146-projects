import sys
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    """
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    """

    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    
    extra_planets = enemy_planets.copy()

    unused_planets = []

    sizeofunused =0
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            dist = state.distance(my_planet.ID, target_planet.ID)
            
            if my_planet.num_ships > required_ships+(dist/2):
                """if required_ships<10:
                    maxdist = dist
                    tempplanet = my_planet
                    for planet1 in state.my_planets():
                        if state.distance(planet1.ID, target_planet.ID) <maxdist:
                             maxdist = state.distance(planet1.ID, target_planet.ID)
                             tempplanet = planet1
                    return issue_order(state, tempplanet.ID, target_planet.ID, required_ships)
                    my_planet = next(my_planets)
                    target_planet = next(target_planets)
                    continue     """
                return issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                unused_planets.append(my_planet)
                my_planet = next(my_planets)
        if len(extra_planets)>0:
            logging.info('did we not attack')
            for planet in extra_planets:
                if planet.num_ships+1 <=len(unused_planets)*2:
                    logging.info('this was useful')
                    for used in unused_planets:
                        issue_order(state, planet.ID, used.ID, 2)
                    break

    except StopIteration:
        return


def spread_to_weakest_neutral_planet(state):
    """
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    """

    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    extra_planets = neutral_planets.copy()

    unused_planets = []

    sizeofunused =0
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1
            dist =state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            logging.info(my_planet.num_ships)
            if my_planet.num_ships-dist > required_ships:
                return issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                unused_planets.append(my_planet)
                my_planet = next(my_planets)
        if len(extra_planets)>0:
            logging.info('did we not attack')
            for planet in extra_planets:
                if planet.num_ships+1 <=len(unused_planets)*2:
                    logging.info('this was useful')
                    for used in unused_planets:
                        issue_order(state, planet.ID, used.ID, 2)
                    break
                        

    except StopIteration:
        return

def defensive(state):
    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return

    def strength(p):
        return p.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if (not weak_planets) or (not strong_planets):
        return

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        weak_planet = next(weak_planets)
        strong_planet = next(strong_planets)
        while True:
            need = int(avg - strength(weak_planet))
            have = int(strength(strong_planet) - avg)

            if have >= need > 0:
                return issue_order(state, strong_planet.ID, weak_planet.ID, need)
                weak_planet = next(weak_planets)
            elif have > 0:
                return issue_order(state, strong_planet.ID, weak_planet.ID, have)
                strong_planet = next(strong_planets)
            else:
                strong_planet = next(strong_planets)

    except StopIteration:
        return