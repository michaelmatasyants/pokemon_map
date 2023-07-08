# Pokemon map

![screenshot](https://dvmn.org/filer/canonical/1563275070/172/)

### Subject area

This site was created to help with the game [Pokemon GO](https://www.pokemongo.com/en-us/). It's a game about catching [Pokemons](https://en.wikipedia.org/wiki/Pok%C3%A9mon).

The essence of the game is that pokemon periodically appear on the map, for a certain period of time. Each player can catch a pokemon to add to his personal collection.

There can be several individuals of the same pokemon on the map at once: for example, 3 Bulbasaurus. Each individual can be caught by several players at once. If a player catches a pokemon specimen, it disappears for him, but remains for others.

Pokemon of one species can "evolve" into another. For example, Bullbasaurus transforms into Ivesaurus, and the latter transforms into Venusaurus.

![bulba evolution](https://dvmn.org/filer/canonical/1562265973/167/)

### How to run

1. Firstly, you have to install python and pip (package-management system) if they haven't been already installed.

2. Create a virtual environment with its own independent set of packages using [virtualenv/venv](https://docs.python.org/3/library/venv.html). It'll help you to isolate the project from the packages located in the base environment.

3. Install all the packages used in this project, in your virtual environment which you've created on the step 2. Use the `requirements.txt` file to install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the server for development:
    ```sh
    python3 manage.py runserver
    ```

### Environment variables

Some of the project settings come from environment variables. To define them, create a file `.env` next to `manage.py` and write data in this format: `VARIABLE=value`.

Two variables are available:
- `DEBUG` — debug mode. Set it to True to see debugging information in case of an error.
- `SECRET_KEY` — project secret key

## Project Objectives

The code is written for educational purposes
