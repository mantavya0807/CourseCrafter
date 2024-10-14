#!/bin/bash

# Variables
DB_NAME=“MajorPath“        # Replace with your actual MongoDB database name
MONGO_URI="mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/"   # Replace with your actual MongoDB URI
FOLDER_PATH="/Data/majors"  # Path to the folder containing collection files

# Loop through all files in the folder
for FILE in "$FOLDER_PATH"/*; do
    # Extract the filename without extension to use as the collection name
    COLLECTION_NAME=$(basename "$FILE" | cut -f 1 -d '.')
    
    # Import the file to MongoDB
    mongoimport --uri "$MONGO_URI" --db "$DB_NAME" --collection "$COLLECTION_NAME" --file "$FILE" --jsonArray
    
    echo "Imported $FILE into collection $COLLECTION_NAME"
done
