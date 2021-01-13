# Simple Sudoku Solver
A toy project for my application to [the Recurse Center](https://www.recurse.com/).

This is a plain Python sudoku solver that can solve any sudoku puzzle through a
combination of constraint satisfaction and brute force search.

## Usage
To see how the program works, simply type:

`python sudoku_solver.py`

It will print out an example puzzle and a solution to that puzzle. 

The program reads in a puzzle like this:
```
__2 | ___ | __5
7_8 | 6_9 | _2_
534 | 782 | ___
----+-----+-----
___ | 5__ | 4__
19_ | 2_4 | _83
__5 | __8 | ___
----+-----+-----
___ | 321 | 658
_5_ | 9_6 | 7_2
6__ | ___ | 9__
```

in the following format:

`..2.....57.86.9.2.534782......5..4..19.2.4.83..5..8......321658.5.9.67.26.....9..`

That is - Type all 81 characters of the puzzle from left to right, top to bottom with dots
as empty squares. We can call this format a "puzzle string".

It's recommend you put the puzzle string in a `.txt` file, but you can also feed this string into to the
`solve()` function directly. The solve function is the only function you need to use.

## Implementation Details
This program represents the sudoku puzzle internally as a dictionary where the keys are one of 
81 boxes (labeled A1, A1, ... I9) and the values are a string (like "1359") of all the possible 
numbers that could be in that box. A box is considered solved if there is only one possible number 
for that box. 

Each box is part of multiple "peer groups". A "peer group" consists of 9 boxes that must contain the 
numbers 1 through 9 exactly once. If two boxes are in the same "peer group" we can call them "peers", 
thus "A1" and "A8" are peers because they both in the first row.

This solver works by first trying three types of constraint satisfaction on the Sudoku puzzle, and then
if the puzzle is still not solved, it finds the box with the fewest possibilities and then does a brute 
force search on those possibilities. (This could also be described as tree traversal.)

The three constraint satisfaction heuristics we use are:
    
`elimination` - If a box is solved, eliminate it's value from all it's peer's possibilities. For example,
                if `C6` is `4`, then eliminate `4` as a possibility for all the boxes in the C row or 6th column
                or the central box of the Sudoku puzzle.
                
`only_choice` - If is the only box in a peer group to contain a specific number then it must be that number.
                For example if `E3` has possibilities `278`, but it is the only box in the E row to contain a `2`, 
                then `E3` must contain `2`.
                
`naked_twins` - Our most complicated constraint satisfaction heuristic. If there are 3 boxes unsolved in a peer group 
                and 2 of the 3 boxes in a group only have two possibilities, the possibility in the third box that is 
                not in the other two must be the value of the third box. For example suppose grid looks like 
                `{"A1": "157", "A2": "57", "A3": "57", ...}`. Then `A1` contain value `1` because `A2` and `A3` must
                contain `5` and `7`.
                
Note that, we could, of course, solve puzzle using the brute force search, but it would be much less efficient than
applying the constraint satisfaction heuristics. In the test file, we test the solver with the constraint satisfaction 
heuristics as well as without.

Note this code was original written as part of the [Udacity Artificial Intelligence Nanodegree](https://github.com/udacity/AIND-Sudoku)
and cleaned up to apply to the Recurse Center. Some of the stubs may look similar to the Udacity repo.
