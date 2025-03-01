from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["game_database"]

class BaseModel:
    """Base class for all models to handle common operations."""
    
    def to_dict(self):
        """Convert model instance to dictionary for MongoDB storage."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    
    def save(self, collection_name):
        """Save instance to the corresponding MongoDB collection."""
        collection = db[collection_name]
        collection.insert_one(self.to_dict())

class User(BaseModel):
    """User collection model."""
    
    def __init__(self, username, score=0):
        self.username = username
        self.score = score

class Destination(BaseModel):
    """Destination collection model."""
    
    def __init__(self, city, country, clues, fun_fact, trivia):
        self.city = city
        self.country = country
        self.clues = clues if isinstance(clues, list) else []
        self.fun_fact = fun_fact if isinstance(fun_fact, list) else []
        self.trivia = trivia if isinstance(trivia, list) else []

    @classmethod
    def from_dict(cls, data):
        """Create a Destination instance from a dictionary."""
        return cls(
            city=data.get("city"),
            country=data.get("country"),
            clues=data.get("clues", []),
            fun_fact=data.get("fun_fact", []),
            trivia=data.get("trivia", [])
        )

    @classmethod
    def get_by_id(cls, destination_id):
        """Retrieve a destination by its MongoDB ID."""
        collection = db["destinations"]
        data = collection.find_one({"_id": destination_id})
        return cls.from_dict(data) if data else None

class GameSession(BaseModel):
    """Game session model for tracking user attempts."""
    
    def __init__(self, user_id, destination_id, is_correct):
        self.user_id = user_id
        self.destination_id = destination_id
        self.is_correct = is_correct
