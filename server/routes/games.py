from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/games', methods=['POST'])
def create_game() -> tuple[Response, int]:
    try:
        # Get JSON data from request
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract required fields
        title = data.get('title')
        description = data.get('description')
        category_id = data.get('category_id')
        publisher_id = data.get('publisher_id')
        star_rating = data.get('star_rating')  # Optional field
        
        # Validate required fields
        if not title:
            return jsonify({"error": "Title is required"}), 400
        if not description:
            return jsonify({"error": "Description is required"}), 400
        if not category_id:
            return jsonify({"error": "Category ID is required"}), 400
        if not publisher_id:
            return jsonify({"error": "Publisher ID is required"}), 400
        
        # Check if category exists
        category = db.session.query(Category).filter(Category.id == category_id).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        # Check if publisher exists
        publisher = db.session.query(Publisher).filter(Publisher.id == publisher_id).first()
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 404
        
        # Create new game
        new_game = Game(
            title=title,
            description=description,
            category_id=category_id,
            publisher_id=publisher_id,
            star_rating=star_rating
        )
        
        # Add to database
        db.session.add(new_game)
        db.session.commit()
        
        # Return created game
        return jsonify(new_game.to_dict()), 201
        
    except ValueError as e:
        # Handle validation errors from the model
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@games_bp.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id: int) -> tuple[Response, int]:
    try:
        # Get JSON data from request
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        # Find the game to update
        game = db.session.query(Game).filter(Game.id == id).first()
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Extract fields that can be updated
        title = data.get('title')
        description = data.get('description')
        category_id = data.get('category_id')
        publisher_id = data.get('publisher_id')
        star_rating = data.get('star_rating')
        
        # Update fields if provided
        if title is not None:
            game.title = title
        if description is not None:
            game.description = description
        if star_rating is not None:
            game.star_rating = star_rating
            
        # Check category exists if being updated
        if category_id is not None:
            category = db.session.query(Category).filter(Category.id == category_id).first()
            if not category:
                return jsonify({"error": "Category not found"}), 404
            game.category_id = category_id
        
        # Check publisher exists if being updated
        if publisher_id is not None:
            publisher = db.session.query(Publisher).filter(Publisher.id == publisher_id).first()
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 404
            game.publisher_id = publisher_id
        
        # Save changes
        db.session.commit()
        
        # Return updated game
        return jsonify(game.to_dict()), 200
        
    except ValueError as e:
        # Handle validation errors from the model
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
@games_bp.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id: int) -> tuple[Response, int]:
    try:
        # Find the game to delete
        game = db.session.query(Game).filter(Game.id == id).first()
        if not game:
            return jsonify({"error": "Game not found"}), 404
        
        # Delete the game
        db.session.delete(game)
        db.session.commit()
        
        # Return 204 No Content for successful deletion
        return jsonify({}), 204
        
    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
