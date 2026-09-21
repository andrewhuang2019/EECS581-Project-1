# EECS581-Project-1

## Person Hours: Estimate vs. Actual
How it is measured: estimate how long a task would take in person hours based on estimated workload and then whoever had said task would record how many actual hours the task took.

### John Rader: 
- Estimation: 10 hours 
- Actual: 12 hours

### Peter Barybin: 
- Estimation: 7 hours 
- Actual: 8 hours

### Cooper Wright:
- Estimation: 4 hours
- Actual: 3 hours

### Andrew Huang:
- Estimation: 4 hours
- Actual: 5 hours

### Emily Farley:
- Estimation: 7 hours
- Actual: 8 hours

### Evan Noeth:
- Estimation: 3 hours
- Actual: 5 hours

### Sina Asheghalishahi:
- Estimation: 6 hours
- Actual: 7 hours

## System Architecture
### Purpose
Provides a high-level structural overview of the project architecture to assist Project 2 team in extension creation
### Components
1. Board - 10x10 2d array of Tiles. Handles mines, game state (won/lost), flags total/remaining
2. Tile - hold value (number on tile), revealed boolean, is_mine boolean, is_flagged boolean, row and col of tile on Board
3. Sprite - enum that holds sprite number to name values
4. sprites - dict that maps Sprite enums to their representative Pygame sprite image surfaces.
### Data Flow
1. User selects mine count using arrow buttons --> number sent to board object
2. User tile click --> corresponding click handler (first, left, right) function runs
4. Click handler updates tile state depending on type of action, then recursively updates other tile states if necessary
5. Updates are returned from click handler and shown in GUI
6. Waits for another user click unless game won/lost was returned, in which case GUI shows game over screen
### Key Data Structures
1. Board class: initializes 10x10 2d array - holds tile objects to represent game board, tracks game/board info
2. Tile class: initializes tile objects that are interacted with on the game board - holds tile info like the number of adjacent mines, if tile is mine or flagged or revealed, and the tile's row and column in the 10x10 2d array
3. block_mine set: holds tuples that represent tiles which must be avoided when doing random mine placement
### Assumptions
1. Fixed 10x10 grid of tiles
2. 10-20 mines (user-specified)
3. First-clicked tile as well as its adjacent tiles cannot be mines
