import sys
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
sys.path.insert(0, '../')
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

    
    extra_planets = enemy_planets.copy()

    unused_planets = []

    sizeofunused =0
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                extra_planets.remove(target_planet)
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
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                extra_planets.remove(target_planet)
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

