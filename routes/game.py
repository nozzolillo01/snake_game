from flask import Blueprint, render_template, jsonify
from http import HTTPStatus
from typing import Dict, Any

game = Blueprint('game', __name__)

@game.route('/game')
def play_game() -> str:
    """
    Render the Snake game page.
    
    Returns:
        str: Rendered HTML template for the game page.
    """
    return render_template('game.html')

@game.errorhandler(HTTPStatus.NOT_FOUND)
def handle_not_found(e) -> tuple[Dict[str, Any], int]:
    """
    Handle 404 Not Found errors.
    
    Args:
        e: The error that occurred.
        
    Returns:
        tuple: JSON response with error details and 404 status code.
    """
    return jsonify({'error': 'Resource not found'}), HTTPStatus.NOT_FOUND