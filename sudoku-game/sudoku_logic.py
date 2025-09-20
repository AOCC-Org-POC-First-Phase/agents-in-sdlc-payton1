"""
Sudoku Game Logic Module

This module provides functionality for generating, solving, and validating Sudoku puzzles.
"""

import random
from typing import List, Tuple, Optional


class SudokuGame:
    """A Sudoku game implementation with puzzle generation and solving capabilities."""
    
    def __init__(self):
        """Initialize a new Sudoku game."""
        self.grid: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.solution: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]
    
    def is_valid_move(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """
        Check if placing a number at the given position is valid.
        
        Args:
            grid: The current game grid
            row: Row index (0-8)
            col: Column index (0-8)
            num: Number to place (1-9)
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Check row
        for c in range(9):
            if grid[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if grid[r][col] == num:
                return False
        
        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if grid[r][c] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, grid: List[List[int]]) -> bool:
        """
        Solve a Sudoku puzzle using backtracking.
        
        Args:
            grid: The puzzle grid to solve
            
        Returns:
            True if the puzzle is solvable, False otherwise
        """
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(grid, row, col, num):
                            grid[row][col] = num
                            
                            if self.solve_sudoku(grid):
                                return True
                            
                            # Backtrack
                            grid[row][col] = 0
                    
                    return False
        return True
    
    def generate_complete_grid(self) -> List[List[int]]:
        """
        Generate a complete, valid Sudoku grid.
        
        Returns:
            A 9x9 grid filled with a valid Sudoku solution
        """
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal boxes first
        for box in range(0, 9, 3):
            self._fill_diagonal_box(grid, box, box)
        
        # Solve the rest
        self.solve_sudoku(grid)
        return grid
    
    def _fill_diagonal_box(self, grid: List[List[int]], row: int, col: int) -> None:
        """Fill a 3x3 diagonal box with random valid numbers."""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for r in range(3):
            for c in range(3):
                grid[row + r][col + c] = numbers[r * 3 + c]
    
    def create_puzzle(self, difficulty: str = "medium") -> Tuple[List[List[int]], List[List[int]]]:
        """
        Create a Sudoku puzzle with the specified difficulty.
        
        Args:
            difficulty: Difficulty level ("easy", "medium", "hard")
            
        Returns:
            Tuple of (puzzle_grid, solution_grid)
        """
        # Generate complete solution
        solution = self.generate_complete_grid()
        puzzle = [row[:] for row in solution]  # Deep copy
        
        # Determine number of cells to remove based on difficulty
        cells_to_remove = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }.get(difficulty, 45)
        
        # Remove cells randomly
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        for r, c in cells[:cells_to_remove]:
            puzzle[r][c] = 0
        
        return puzzle, solution
    
    def is_complete(self, grid: List[List[int]]) -> bool:
        """
        Check if the puzzle is completely filled and valid.
        
        Args:
            grid: The game grid to check
            
        Returns:
            True if complete and valid, False otherwise
        """
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return False
                # Create temporary grid without current cell to test validity
                temp_grid = [r[:] for r in grid]
                temp_grid[row][col] = 0
                if not self.is_valid_move(temp_grid, row, col, grid[row][col]):
                    return False
        return True
    
    def check_current_state(self, grid: List[List[int]]) -> dict:
        """
        Check the current state of the puzzle and return validation info.
        
        Args:
            grid: The current game grid
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0:
                    # Temporarily remove the cell value to test if it's valid in this position
                    temp_value = grid[row][col]
                    grid[row][col] = 0
                    
                    if not self.is_valid_move(grid, row, col, temp_value):
                        errors.append((row, col))
                    
                    # Restore the value
                    grid[row][col] = temp_value
        
        is_complete = self.is_complete(grid)
        
        return {
            "is_valid": len(errors) == 0,
            "is_complete": is_complete,
            "errors": errors,
            "message": self._get_status_message(len(errors), is_complete)
        }
    
    def _get_status_message(self, error_count: int, is_complete: bool) -> str:
        """Get a status message based on the current game state."""
        if is_complete:
            return "Congratulations! Puzzle solved correctly!"
        elif error_count > 0:
            return f"Found {error_count} error(s). Please check your entries."
        else:
            return "Looking good! Keep going!"