"""
Sudoku Game Flask Application

A web-based Sudoku game server providing puzzle generation and game management.
"""

from flask import Flask, render_template, request, jsonify
from typing import Dict, Any
import json
from sudoku_logic import SudokuGame

app = Flask(__name__)
sudoku_game = SudokuGame()

# Store current game state
current_puzzle = None
current_solution = None


@app.route('/')
def index() -> str:
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/api/new-game', methods=['POST'])
def new_game() -> Dict[str, Any]:
    """
    Create a new Sudoku puzzle.
    
    Returns:
        JSON response with the new puzzle grid
    """
    global current_puzzle, current_solution
    
    data = request.get_json() or {}
    difficulty = data.get('difficulty', 'medium')
    
    if difficulty not in ['easy', 'medium', 'hard']:
        difficulty = 'medium'
    
    current_puzzle, current_solution = sudoku_game.create_puzzle(difficulty)
    
    return jsonify({
        'success': True,
        'puzzle': current_puzzle,
        'message': f'New {difficulty} puzzle created!'
    })


@app.route('/api/validate', methods=['POST'])
def validate_puzzle() -> Dict[str, Any]:
    """
    Validate the current puzzle state.
    
    Returns:
        JSON response with validation results
    """
    data = request.get_json()
    if not data or 'grid' not in data:
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    grid = data['grid']
    validation_result = sudoku_game.check_current_state(grid)
    
    return jsonify({
        'success': True,
        **validation_result
    })


@app.route('/api/solve', methods=['POST'])
def solve_puzzle() -> Dict[str, Any]:
    """
    Get the solution for the current puzzle.
    
    Returns:
        JSON response with the solution grid
    """
    global current_solution
    
    if current_solution is None:
        return jsonify({
            'success': False,
            'message': 'No active puzzle to solve'
        })
    
    return jsonify({
        'success': True,
        'solution': current_solution,
        'message': 'Here\'s the solution!'
    })


@app.route('/api/check-move', methods=['POST'])
def check_move() -> Dict[str, Any]:
    """
    Check if a specific move is valid.
    
    Returns:
        JSON response indicating if the move is valid
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['grid', 'row', 'col', 'value']):
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    grid = data['grid']
    row = data['row']
    col = data['col']
    value = data['value']
    
    is_valid = sudoku_game.is_valid_move(grid, row, col, value)
    
    return jsonify({
        'success': True,
        'is_valid': is_valid,
        'message': 'Valid move!' if is_valid else 'Invalid move - number conflicts with row, column, or box'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')