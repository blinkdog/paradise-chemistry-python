# test_chemistry.py
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

from ss13.chemistry import BASIC_CHEMICALS
from ss13.chemistry import CHEM_RECIPES
from ss13.chemistry import createOrder
from ss13.chemistry import display
from ss13.chemistry import flatten
from ss13.chemistry import inCount
from ss13.chemistry import outCount
from ss13.chemistry import stepsFor
from ss13.chemistry import tabIt
from ss13.chemistry import usage


def test_basic_length():
    NUM_BASIC_CHEMICALS = 26
    assert len(BASIC_CHEMICALS) == NUM_BASIC_CHEMICALS, "There are %d basic chemicals (expected %d)." % (len(BASIC_CHEMICALS), NUM_BASIC_CHEMICALS)


def test_conservation_of_mass():
    for key in CHEM_RECIPES.keys():
        assert inCount(key) >= outCount(key)


def test_count_unknown_is_zero():
    assert inCount("blargh") == 0
    assert outCount("blargh") == 0


def test_count_ignores_temperature():
    assert inCount("ash") == 2


def test_create_order():
    # always do temperature first
    assert createOrder("temperature", "ash") == 1
    assert createOrder("temperature", "ethanol") == 1
    assert createOrder("temperature", "welding fuel") == 1
    assert createOrder("ash", "temperature") == -1
    assert createOrder("ethanol", "temperature") == -1
    assert createOrder("welding fuel", "temperature") == -1
    # always do recipes before basic chems
    assert createOrder("ash", "ethanol") == -1
    assert createOrder("ethanol", "ash") == 1
    # do similar things in alphabetical order
    assert createOrder("carbon", "ethanol") == -1
    assert createOrder("ethanol", "carbon") == 1
    # don't care what order we do the same thing
    assert createOrder("ash", "ash") == 0
    assert createOrder("carbon", "carbon") == 0
    assert createOrder("welding fuel", "welding fuel") == 0


def test_display():
    steps = [
        {
            "level": 0,
            "text": "Make 50u of unstable mutagen"
        },
        {
            "level": 1,
            "text": "Dispense 17u of chlorine from chem dispenser"
        },
        {
            "level": 1,
            "text": "Dispense 17u of plasma from chem dispenser"
        },
        {
            "level": 1,
            "text": "Dispense 17u of radium from chem dispenser"
        },
    ]
    result = "1. Make 50u of unstable mutagen\n  2. Dispense 17u of chlorine from chem dispenser\n  3. Dispense 17u of plasma from chem dispenser\n  4. Dispense 17u of radium from chem dispenser\n"
    assert display(steps) == result


def test_flatten():
    assert flatten([1, [2, [3, 4, 5], 6, 7]]) == [1, 2, 3, 4, 5, 6, 7]
    assert flatten(["alice", ["bob", ["carol", "dave", "eve"], "frank", "greg"]]) == ["alice", "bob", "carol", "dave", "eve", "frank", "greg"]
    assert flatten([{}, [{}, [{}, {}, {}], {}, {}]]) == [{}, {}, {}, {}, {}, {}, {}]


def test_recipe_length():
    NUM_CHEM_RECIPES = 9
    assert len(CHEM_RECIPES) == NUM_CHEM_RECIPES, "There are %d chem recipes (expected %d)." % (len(CHEM_RECIPES), NUM_CHEM_RECIPES)


def test_stepsFor_basic_chemical():
    assert stepsFor("ethanol", 100, 0) == [
        {
            "level": 0,
            "action": "dispense",
            "reagent": "ethanol",
            "volume": 100,
            "text": "Dispense 100u of ethanol from chem dispenser"
        }
    ]


def test_stepsFor_basic_temperature():
    assert stepsFor("temperature", 480, 0) == [
        {
            "level": 0,
            "action": "heat",
            "reagent": "temperature",
            "volume": 480,
            "text": "Heat contents of beaker to 480K"
        }
    ]


def test_stepsFor_recipe_ammonia():
    assert stepsFor("ammonia", 100, 0) == [
        {
            "level": 0,
            "action": "make",
            "reagent": "ammonia",
            "volume": 100,
            "ratio": 0.75,
            "text": "Make 100u of ammonia"
        },
        {
            "level": 1,
            "action": "dispense",
            "reagent": "hydrogen",
            "volume": 100,
            "text": "Dispense 100u of hydrogen from chem dispenser"
        },
        {
            "level": 1,
            "action": "dispense",
            "reagent": "nitrogen",
            "volume": 33,
            "text": "Dispense 33u of nitrogen from chem dispenser"
        }
    ]


def test_stepsFor_recipe_ash():
    assert stepsFor("ash", 100, 0) == [
        {
            "level": 0,
            "action": "make",
            "reagent": "ash",
            "volume": 100,
            "ratio": 0.50,
            "text": "Make 100u of ash"
        },
        {
            "level": 1,
            "action": "make",
            "reagent": "oil",
            "volume": 200,
            "ratio": 1,
            "text": "Make 200u of oil"
        },
        {
            "level": 2,
            "action": "dispense",
            "reagent": "carbon",
            "volume": 66,
            "text": "Dispense 66u of carbon from chem dispenser"
        },
        {
            "level": 2,
            "action": "dispense",
            "reagent": "hydrogen",
            "volume": 66,
            "text": "Dispense 66u of hydrogen from chem dispenser"
        },
        {
            "level": 2,
            "action": "dispense",
            "reagent": "welding fuel",
            "volume": 66,
            "text": "Dispense 66u of welding fuel from fuel tank"
        },
        {
            "level": 1,
            "action": "heat",
            "reagent": "temperature",
            "volume": 480,
            "text": "Heat contents of beaker to 480K"
        }
    ]


def test_stepsFor_recipe_oil():
    assert stepsFor("oil", 100, 0) == [
        {
            "level": 0,
            "action": "make",
            "reagent": "oil",
            "volume": 100,
            "ratio": 1,
            "text": "Make 100u of oil"
        },
        {
            "level": 1,
            "action": "dispense",
            "reagent": "carbon",
            "volume": 33,
            "text": "Dispense 33u of carbon from chem dispenser"
        },
        {
            "level": 1,
            "action": "dispense",
            "reagent": "hydrogen",
            "volume": 33,
            "text": "Dispense 33u of hydrogen from chem dispenser"
        },
        {
            "level": 1,
            "action": "dispense",
            "reagent": "welding fuel",
            "volume": 33,
            "text": "Dispense 33u of welding fuel from fuel tank"
        }
    ]


def test_stepsFor_welding_fuel():
    assert stepsFor("welding fuel", 25, 0) == [
        {
            "level": 0,
            "action": "dispense",
            "reagent": "welding fuel",
            "volume": 25,
            "text": "Dispense 25u of welding fuel from fuel tank"
        }
    ]


def test_stepsFor_unknown():
    assert stepsFor("blood", 30, 0) == [
        {
            "level": 0,
            "action": "obtain",
            "reagent": "blood",
            "volume": 30,
            "text": "Look up in the Wiki how to obtain 30u of blood"
        }
    ]


def test_stoichiometry_unusual():
    assert inCount("ammonia") != outCount("ammonia")
    assert inCount("ash") != outCount("ash")
    assert inCount("saltpetre") != outCount("saltpetre")
    assert inCount("sulphuric acid") != outCount("sulphuric acid")


def test_stoichiometry_usual():
    assert inCount("acetone") == outCount("acetone")
    assert inCount("diethylamine") == outCount("diethylamine")
    assert inCount("oil") == outCount("oil")
    assert inCount("phenol") == outCount("phenol")
    assert inCount("space lube") == outCount("space lube")


def test_tabIt():
    assert tabIt(0) == ""
    assert tabIt(1) == "  "
    assert tabIt(2) == "    "
    assert tabIt(3) == "      "


def test_usage():
    assert usage("ss13/chemistry.py") == "Usage: python ss13/chemistry.py <chemical> <volume>"


def test_verified():
    for key, value in CHEM_RECIPES.items():
        assert value["verified"], "%s is not verified" % key

# ---------------------------------------------------------------------------
# end of test_chemistry.py
