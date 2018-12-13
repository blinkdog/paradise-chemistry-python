# chemistry.py
# Copyright 2018 Patrick Meade.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------------

from functools import cmp_to_key
from math import floor
import sys

# this is the basic equipment available at each chemistry station:
#   chem dispenser - able to dispense a variety of chemicals
#   chemical heater - able to heat a beaker to up 1000K
#   fuel tank - provides welding fuel used in some chemical preparations
BASIC_CHEMICALS = {
    "aluminum": "chem dispenser",
    "bromine": "chem dispenser",
    "carbon": "chem dispenser",
    "chlorine": "chem dispenser",
    "copper": "chem dispenser",
    "ethanol": "chem dispenser",
    "fluorine": "chem dispenser",
    "hydrogen": "chem dispenser",
    "iodine": "chem dispenser",
    "iron": "chem dispenser",
    "lithium": "chem dispenser",
    "mercury": "chem dispenser",
    "nitrogen": "chem dispenser",
    "oxygen": "chem dispenser",
    "phosphorus": "chem dispenser",
    "plasma": "chem dispenser",
    "potassium": "chem dispenser",
    "radium": "chem dispenser",
    "silicon": "chem dispenser",
    "silver": "chem dispenser",
    "sodium": "chem dispenser",
    "sugar": "chem dispenser",
    "sulfur": "chem dispenser",
    "temperature": "chemical heater",
    "water": "chem dispenser",
    "welding fuel": "fuel tank"
}

# this is a list of the chemical reactions that can be performed in a beaker
CHEM_RECIPES = {
    "acetone": {
        "desc": "Common ingredient in other recipes. Causes toxin damage when ingested.",
        "in": {
            "oil": 1,
            "oxygen": 1,
            "welding fuel": 1
        },
        "out": {
            "acetone": 3
        },
        "verified": True
    },

    "ammonia": {
        "desc": "An alternative fertilizer for botany and a key component for many common meds. Less effective than Diethylamine.",
        "in": {
            "hydrogen": 3,
            "nitrogen": 1
        },
        "out": {
            "ammonia": 3
        },
        "verified": True
    },

    "ash": {
        "desc": "Basic ingredient in a couple of recipes.",
        "in": {
            "oil": 2,
            "temperature": 480
        },
        "out": {
            "ash": 1
        },
        "verified": True
    },

    "diethylamine": {
        "desc": "A very potent fertilizer, and the base component of some medicines.",
        "in": {
            "ammonia": 1,
            "ethanol": 1,
            "temperature": 374
        },
        "out": {
            "diethylamine": 2
        },
        "verified": True
    },

    "oil": {
        "desc": "Burns in a small smoky fire, mostly used to get Ash.",
        "in": {
            "carbon": 1,
            "hydrogen": 1,
            "welding fuel": 1
        },
        "out": {
            "oil": 3
        },
        "verified": True
    },

    "phenol": {
        "desc": "Used for certain medical recipes.",
        "in": {
            "chlorine": 1,
            "oil": 1,
            "water": 1
        },
        "out": {
            "phenol": 3
        },
        "verified": True
    },

    "saltpetre": {
        "desc": "Ingredient for Bath Salts and Black Powder.",
        "in": {
            "nitrogen": 1,
            "oxygen": 3,
            "potassium": 1
        },
        "out": {
            "saltpetre": 3
        },
        "verified": True
    },

    "sulphuric acid": {
        "desc": "An acid that's utilized as a building block in a lot of medical chemicals. It's also useful for etching circuits....etching permanent scars in your coworker's face.",
        "in": {
            "hydrogen": 1,
            "oxygen": 1,
            "sulfur": 1
        },
        "out": {
            "sulphuric acid": 2
        },
        "verified": True
    },

    "space lube": {
        "desc": "Space Lube is a high performance lubricant intended for maintenance of extremely complex mechanical equipment.",
        "in": {
            "oxygen": 1,
            "silicon": 1,
            "water": 1
        },
        "out": {
            "space lube": 3
        },
        "verified": True
    },

}


def count(name, side):
    if name not in CHEM_RECIPES:
        return 0
    chemicals = CHEM_RECIPES[name][side]
    count = 0
    for key, value in chemicals.items():
        if key is not "temperature":
            count += value
    return count


def createOrder(a, b):
    # always do temperature last
    if a is "temperature":
        return 1
    if b is "temperature":
        return -1
    # always do complex recipes before simple chemicals
    if (a in CHEM_RECIPES) and (b in BASIC_CHEMICALS):
        return -1
    if (a in BASIC_CHEMICALS) and (b in CHEM_RECIPES):
        return 1
    # otherwise just sort by name
    if a < b:
        return -1
    if a > b:
        return 1
    # if they are the same, then order doesn't matter
    return 0


def display(steps):
    stepCount = 0
    result = ""
    for step in steps:
        stepCount += 1
        result += tabIt(step["level"])
        result += str(stepCount)
        result += ". "
        result += step["text"]
        result += "\n"
    return result


def flatten(A):
    rt = []
    for i in A:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i)
    return rt


def inCount(name):
    return count(name, "in")


def outCount(name):
    return count(name, "out")


def stepsFor(chem, volume, level):
    # print(f"DEBUG: stepsFor {volume}u of {chem}")
    steps = []
    # if it's just a basic chemical, then dispense it
    if chem in BASIC_CHEMICALS:
        if chem is "temperature":
            steps.append({
                "level": level,
                "action": "heat",
                "reagent": chem,
                "volume": volume,
                "text": f"Heat contents of beaker to {volume}K"
            })
        else:
            steps.append({
                "level": level,
                "action": "dispense",
                "reagent": chem,
                "volume": volume,
                "text": f"Dispense {volume}u of {chem} from {BASIC_CHEMICALS[chem]}"
            })
        return flatten(steps)
    # otherwise, it's a more complicated recipe
    if chem in CHEM_RECIPES:
        # check stoichiometry
        outParts = outCount(chem)
        inParts = inCount(chem)
        # adjust volume for unusual stoichiometry
        volumeRatio = 1
        if inParts != outParts:
            volumeRatio = (outParts / inParts)
        # sort the reagents by preferred work order
        reagents = CHEM_RECIPES[chem]["in"].keys()
        reagents = sorted(reagents, key=cmp_to_key(createOrder))
        # add the top level step for this recipe
        steps.append({
            "level": level,
            "action": "make",
            "reagent": chem,
            "volume": volume,
            "ratio": volumeRatio,
            "text": f"Make {volume}u of {chem}"
        })
        # now add the substeps, in the appropriate order
        for reagent in reagents:
            if reagent is "temperature":
                subSteps = stepsFor(reagent, CHEM_RECIPES[chem]["in"][reagent], level + 1)
            else:
                reagentIn = CHEM_RECIPES[chem]["in"][reagent]
                chemOut = CHEM_RECIPES[chem]["out"][chem]
                reagentRatio = float(reagentIn) / float(chemOut)
                reagentNeeded = floor(float(volume) * reagentRatio)
                subSteps = stepsFor(reagent, reagentNeeded, level + 1)
            steps.append(subSteps)
        return flatten(steps)
    # otherwise, we have no idea how to make this
    steps.append({
        "level": level,
        "action": "obtain",
        "reagent": chem,
        "volume": volume,
        "text": f"Look up in the Wiki how to obtain {volume}u of {chem}"
    })
    return flatten(steps)


def tabIt(count):
    result = ""
    while count > 0:
        result += "  "
        count -= 1
    return result


def usage(script):
    return f"Usage: python {script} <chemical> <volume>"


# if this python script is called from the command line
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(usage(sys.argv[0]))
        sys.exit(1)
    [script, chem, volume] = sys.argv
    print(display(stepsFor(chem, volume, 0)))

# ---------------------------------------------------------------------------
# end of chemistry.py
