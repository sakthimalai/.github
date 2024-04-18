# import pymongo

# uri = "mongodb+srv://unisysveterinaryassistant:VAYbcqWTXJoWPBIn@cluster0.bni0uww.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Connect to the MongoDB server
# client = pymongo.MongoClient(uri)

# # Access a specific database
# db = client['Animaldisease']

# # Access a specific collection within the database
# collection = db["Animaldetails"]



# document = {"name": "John", "age": 30}
# collection.insert_one(document)

# # Or querying documents
# query = {"name": "John"}
# result = collection.find_one(query)
# print(result)

# # Don't forget to close the connection when you're done
# client.close()
import pymongo

class MongoDBManager:
    # MongoDB URI and credentials
    URI = "mongodb+srv://unisysveterinaryassistant:VAYbcqWTXJoWPBIn@cluster0.bni0uww.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "Animaldisease"
    COLLECTION_NAME = "Animaldetails"

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.URI)
            self.db = self.client[self.DB_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
            print("Connected to MongoDB")
        except Exception as e:
            print("Connection to MongoDB failed:", e)

    def insert_document(self, document:dict):
        try:
            # Check if the document already exists based on the date
            existing_doc = self.collection.find_one({"date": document["date"]})
            if existing_doc:
                # Update the fields other than the date
                update_data = {key: value for key, value in document.items() if key != "date"}
            
                # Add the additional value to mouth_disease_count if present in the update data
                if "mouth_disease_count" in update_data:
                    existing_mouth_count = existing_doc.get("mouth_disease_count", 0)
                    update_data["mouth_disease_count"] += existing_mouth_count
                
                # Add the additional value to lumpy_skin_count if present in the update data
                if "lumpy_skin_count" in update_data:
                    existing_lumpy_count = existing_doc.get("lumpy_skin_count", 0)
                    update_data["lumpy_skin_count"] += existing_lumpy_count
                
                self.collection.update_one({"date": document["date"]}, {"$set": update_data})
                print("Document updated successfully")
            else:
                # Insert the new document
                self.collection.insert_one(document)
                print("Document inserted successfully")
        except Exception as e:
            print("Failed to insert/update document:", e)



            

