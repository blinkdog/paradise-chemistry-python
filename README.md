# paradise-chemistry-python
Helper program in Python for Chemistry on Paradise Station (SS13)

## Usage
First, make sure that you've created and are running in a virtual environment:

    python3.7 -m venv ./env
    source env/bin/activate

Now you can invoke the chemistry helper from the command line:

    python ss13/chemistry.py oil 50

And it will return a pretty-printed list of chemistry steps:

    1. Make 50u of oil
      2. Dispense 16u of carbon from chem dispenser
      3. Dispense 16u of hydrogen from chem dispenser
      4. Dispense 16u of welding fuel from fuel tank

Enjoy!

## Development
If you want to hack on the code, here are some instructions to
get you started on creating a development environment:

    cd ~/projects
    git clone git@github.com:blinkdog/paradise-chemistry-python.git
    cd paradise-chemistry-python
    python3.7 -m venv ./env
    source env/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

## License
paradise-chemistry-python  
Copyright 2018 Patrick Meade

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
