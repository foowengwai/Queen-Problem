# Eight Queens Search Algorithms

This project solves the classic **Eight Queens Puzzle** using several heuristic
search algorithms.

The objective is to place eight chess queens on an 8 × 8 chessboard so that no
two queens can attack each other. Queens must not share the same row, column, or
diagonal.

The program compares the performance of different search strategies by running
each algorithm repeatedly and displaying statistical results and charts.

## Requirements

- Python 3.12 or later
- pandas
- matplotlib

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/foowengwai/Queen-Problem.git
cd Queen-Problem
```

Install the required Python packages:

```bash
python -m pip install pandas matplotlib
```

## Running the Program

Run the main script:

```bash
python queen.py
```

By default, the program:

1. Runs seven search algorithms.
2. Executes each algorithm 50 times.
3. Allows up to 1,000 iterations per run.
4. Uses an 8 × 8 board.
5. Prints success and iteration statistics.
6. Displays charts comparing algorithm costs and iteration counts.

A graphical environment is required to display the Matplotlib charts.

## Board Representation

A board is represented as a list of integers. Each list position represents a
row, and the value at that position represents the queen's column:

```python
[1, 5, 8, 6, 3, 7, 2, 4]
```

For example, the first value places a queen in row 1, column 1, and the second
value places a queen in row 2, column 5. The `printBoard()` function displays a
board in a chessboard-style layout.

## Objective Function

The `objFunc()` function assigns a cost to each board:

- A cost of `0` means the board is a valid solution.
- A higher cost means the board contains more conflicts.

The cost is calculated from column and diagonal conflicts. Since the search
algorithms normally start with one queen per row, rows are already unique.

## Implemented Algorithms

### Random Search

Generates completely random board configurations and keeps a configuration
when it improves the best cost found so far.

### Swap Random Search

Randomly swaps two queen positions and continues searching while tracking the
best cost.

### Random-Neighbor Hill Climbing

Changes the column of one randomly selected queen. The new board is accepted
when its cost is no worse than the current board.

### Swap Hill Climbing

Swaps two randomly selected queens and accepts the result when the cost does
not increase.

### Neighbor Swap Hill Climbing

Swaps queens around a randomly selected pivot position and accepts the result
when the cost does not increase.

### Simulated Annealing

Uses random swaps and can accept a worse board, allowing the search to explore
more of the solution space.

### Neighbor Simulated Annealing

Uses neighboring queen swaps together with the probabilistic acceptance
behavior used by simulated annealing.

## Output

For each algorithm, the terminal output includes:

- **Founds** - Number of runs that found a valid solution.
- **Founds (%)** - Percentage of successful runs.
- **NFE** - Median number of iterations used by successful runs.

The program also displays two charts:

1. **Algorithm Cost Comparison**
2. **Algorithm Iteration Comparison**

The charts compare the minimum, mode, median, mean, and maximum values
measured across all runs.

## Configuration

The experiment is configured near the bottom of `queen.py`:

```python
compare(runs=50, iterations=1000, bit=8, **algorithms)
```

The parameters are:

| Parameter | Description |
| --- | --- |
| `runs` | Number of times each algorithm is executed |
| `iterations` | Maximum iterations allowed per run |
| `bit` | Board size and number of queens |

For example, to run 100 experiments with up to 2,000 iterations on an 8 × 8
board:

```python
compare(runs=100, iterations=2000, bit=8, **algorithms)
```

The `threshole` variable controls the random acceptance threshold used by the
simulated annealing implementations:

```python
threshole = 0.9
```

## Project Structure

```text
Queen-Problem/
├── queen.py
├── README.md
└── LICENSE
```

### `queen.py`

Contains the objective function, board display utility, search algorithms,
statistical analysis, chart generation, and experiment configuration.

### `LICENSE`

Contains the MIT License for this project.

## Notes

- Search algorithms use random numbers, so results can vary between runs.
- A lower cost indicates a better board.
- A cost of `0` represents a valid Eight Queens solution.
- The charts use summary statistics rather than plotting every individual run.
- The simulated annealing implementations currently use a fixed threshold
  rather than a temperature schedule.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
