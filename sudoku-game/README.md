# Sudoku Game

A standalone Sudoku game application with a web-based interface.

## Features

- Generate Sudoku puzzles with different difficulty levels
- Interactive web interface for playing
- Input validation and error checking
- Automatic puzzle solving capability
- Dark mode theme consistent with the main project

## How to Run

1. Navigate to the sudoku-game directory:
   ```bash
   cd sudoku-game
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game server:
   ```bash
   python app.py
   ```

4. Open your browser and go to `http://localhost:5001`

## Game Controls

- Click on empty cells to select them
- Use number keys (1-9) to input numbers
- Press Delete or Backspace to clear a cell
- Click "New Game" to generate a new puzzle
- Click "Solve" to see the solution
- Click "Check" to validate your current progress

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Dark mode theme with modern UI elements