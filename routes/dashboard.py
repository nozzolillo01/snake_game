from flask import Blueprint, render_template, jsonify, request, abort
from database import save_score, get_top_scores, get_total_players
from http import HTTPStatus
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

dashboard = Blueprint('dashboard', __name__)
limiter = Limiter(key_func=get_remote_address)

@dashboard.route('/')
def index():
    return render_template('dashboard.html')

@dashboard.route('/save_score', methods=['POST'])
@limiter.limit("30 per minute")  # Limit score submissions
def save_player_score():
    try:
        data = request.json
        if not data or 'player_name' not in data or 'score' not in data:
            abort(HTTPStatus.BAD_REQUEST, description="Missing player_name or score")
        
        if not isinstance(data['score'], int) or data['score'] < 0:
            abort(HTTPStatus.BAD_REQUEST, description="Invalid score value")
            
        if not isinstance(data['player_name'], str) or len(data['player_name']) > 50:
            abort(HTTPStatus.BAD_REQUEST, description="Invalid player name")

        save_score(data['player_name'], data['score'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@dashboard.route('/top_scores')
@limiter.limit("60 per minute")  # Limit leaderboard requests
def top_scores():
    try:
        scores = get_top_scores()
        return jsonify(scores)
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@dashboard.route('/total_players')
@limiter.limit("60 per minute")  # Limit player count requests
def total_players():
    try:
        count = get_total_players()
        return jsonify(count)
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@dashboard.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request(e):
    return jsonify({'error': str(e.description)}), HTTPStatus.BAD_REQUEST

@dashboard.errorhandler(429)  # Rate limit exceeded error handler
def ratelimit_handler(e):
    return jsonify({
        'error': 'Too many requests',
        'message': str(e.description)
    }), 429