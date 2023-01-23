# zelda

Little game create based on this [project](https://www.youtube.com/watch?v=QU1pPzEGrqw&t=23180s).

The idea will be to create a cleaner map on which the player and the ennemies will be able to move more "freely".

Then, using [Dijkstra algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm), the ennemies will be far more difficult to avoid and kill.
After that, based on a reinforcement learning policy, the longer you survive, the higher the difficulty.

# Installation (Need python 3.10)
Clone the repository.

Add src to path

`pip install pygame`

from root folder:

`python ./src/zelda/main.py` et voilà
