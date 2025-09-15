# MongoDB Configuration
# Update these settings according to your MongoDB setup

# For local MongoDB
MONGO_URI = 'mongodb://localhost:27017'

# For MongoDB Atlas (replace with your connection string)
# MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority'

MONGO_DATABASE = 'chanhtuoi_db'
MONGO_COLLECTION = 'articles'

# Example usage in settings.py:
# from mongodb_config import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION
