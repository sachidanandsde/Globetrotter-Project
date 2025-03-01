from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from bson import ObjectId
from .models import User, Destination, GameSession
from pymongo import MongoClient
from datetime import datetime, timedelta
from .utils import generate_shareable_link, generate_qr_code

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["game_database"]


@api_view(['GET'])
def get_random_destination(request):
    """Fetches a random destination and excludes ones served in the last 24 hours for a user."""
    username = request.query_params.get("username")
    if not username:
        return Response({"error": "Username is required"}, status=400)

    users_collection = db["users"]
    games_collection = db["game_sessions"]
    destinations_collection = db["destinations"]

    # Fetch user from DB
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        return Response({"error": "User not found"}, status=404)

    # Get the timestamp for 24 hours ago
    time_threshold = datetime.now() - timedelta(days=1)

    # Get recently served destinations for this user
    recent_destinations = games_collection.find(
        {"user_id": user_data["_id"], "timestamp": {"$gte": time_threshold}},
        {"destination_id": 1}
    )
    recent_destination_ids = {entry["destination_id"] for entry in recent_destinations}

    # Fetch destinations excluding recent ones
    destinations = list(destinations_collection.find(
        {"_id": {"$nin": list(recent_destination_ids)}},
        {"_id": 1, "city": 1, "clues": 1}
    ))

    if not destinations or len(destinations) < 3:
        return Response({"message": "Not enough destinations available"}, status=404)

    # Select a random destination
    correct_destination = random.choice(destinations)

    # Select two additional incorrect destinations
    incorrect_options = random.sample(
        [d for d in destinations if d["_id"] != correct_destination["_id"]],
        2
    )

    # Prepare answer choices (shuffle order)
    options = [correct_destination["city"], incorrect_options[0]["city"], incorrect_options[1]["city"]]
    random.shuffle(options)

    # Prepare response data
    data = {
        "id": str(correct_destination["_id"]),
        "clue": random.choice(correct_destination["clues"]),
        "options": options  # One correct and two incorrect options
    }

    return Response(data)

@api_view(['POST'])
def check_answer(request):
    """Checks if the user's guess is correct and logs the game session."""
    users_collection = db["users"]
    destinations_collection = db["destinations"]

    username = request.data.get("username")
    destination_id = request.data.get("destination_id")
    guessed_destination = request.data.get("guessed_destination")

    # Fetch user from DB
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        return Response({"error": "User not found"}, status=404)
    
    user = User(username=user_data["username"], score=user_data["score"])

    # Fetch destination from DB
    try:
        destination_data = destinations_collection.find_one({"_id": ObjectId(destination_id)})
    except Exception:
        return Response({"error": "Invalid destination ID"}, status=400)

    if not destination_data:
        return Response({"error": "Destination not found"}, status=404)

    # Check answer correctness
    is_correct = guessed_destination.lower() == destination_data.get('city').lower()

    # Save game session
    game_session = GameSession(user_id=user_data["_id"], destination_id=destination_data["_id"], is_correct=is_correct)
    game_session.save("game_sessions")

    # Update user score if correct
    if is_correct:
        users_collection.update_one({"username": username}, {"$inc": {"score": 1}})
        response_data = {
            "correct": is_correct,
            "fun_fact": random.choice(destination_data.get('fun_fact',['No fun facts available'])),
            "message": "Great Job!"
        }
    else:
        response_data = {"correct": is_correct, "fun_fact": "", "message": "Please try again"}    
    return Response(response_data)

@api_view(['POST'])
def create_user(request):
    """Creates a new user or retrieves an existing one."""
    users_collection = db["users"]
    username = request.data.get("username")

    if not username:
        return Response({"error": "Username required"}, status=400)

    user_data = users_collection.find_one({"username": username})
    if not user_data:
        user = User(username=username)
        user.save("users")
        user_data = users_collection.find_one({"username": username})

    return Response({"username": user_data["username"], "score": user_data["score"]})

@api_view(['GET'])
def get_leaderboard(request):
    """Fetches the top 10 users sorted by score."""
    users_collection = db["users"]
    users = list(users_collection.find({}, {"_id": 0, "username": 1, "score": 1}).sort("score", -1).limit(10))
    return Response(users)

@api_view(['GET'])
def get_user_score(request):
    """Fetches the score of the user"""
    username= request.query_params.get("username")
    if not username:
        return Response({"error": "Username is required"}, status=400)    
    users_collection = db["users"]
    users_data = list(users_collection.find({"username":username}))
    if not users_data:
         return Response({"error": "User does not exists!"}, status=200) 
    users_data= users_data[0] 
    return Response({"username": users_data["username"], "score": users_data["score"]},status=200)

@api_view(['POST'])
def challenge_friend(request):
    """Creates an invite link and registers the friend."""
    users_collection = db["users"]
    
    inviter_username = request.data.get("username")
    friend_username = request.data.get("friend_username")

    if not inviter_username or not friend_username:
        return Response({"error": "Both usernames are required"}, status=400)

    # Register the friend if not exists
    friend = users_collection.find_one({"username": friend_username})
    if not friend:
        new_friend = User(username=friend_username)
        new_friend.save("users")

    # Fetch inviter details
    inviter = users_collection.find_one({"username": inviter_username})
    if not inviter:
        return Response({"error": "Inviter not found"}, status=404)

    inviter_score = inviter.get("score", 0)

    # Generate shareable link
    share_link = generate_shareable_link(inviter_username, friend_username)
    
    # Generate QR code
    qr_code_path = generate_qr_code(share_link)

    response_data = {
        "message": "Challenge link created successfully!",
        "inviter": inviter_username,
        "inviter_score": inviter_score,
        "share_link": share_link,
        "qr_code": qr_code_path
    }

    return Response(response_data)
