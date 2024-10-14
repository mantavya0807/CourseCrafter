import os
import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/")  # Replace with your MongoDB connection string
db = client['CertificatePath']  # Replace with your database name

# Path to the folder containing the CSV files
input_folder = 'certificates_courses'  # Update this to the path of your input minors folder

# Loop through each CSV file in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check if DataFrame is empty
        if df.empty:
            print(f"Skipping empty file: {file_name}")
            continue

        # Convert the DataFrame to a dictionary
        data_dict = df.to_dict(orient='records')

        # Check if the data_dict is empty before inserting into MongoDB
        if not data_dict:
            print(f"No data found in {file_name}. Skipping this file.")
            continue

        # Use the file name (without .csv) as the collection name
        collection_name = os.path.splitext(file_name)[0] + "_collection"
        collection = db[collection_name]  # Create a new collection based on the file name

        # Insert data into the corresponding collection
        collection.insert_many(data_dict)

        print(f"Inserted data from {file_name} into collection: {collection_name}")
