@echo off
set DB_NAME=MajorPath
set MONGO_URI=mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/
set FOLDER_PATH=C:\Users\Mantavya\OneDrive\Desktop\hack 2024\Data\majors

for %%F in (%FOLDER_PATH%\*) do (
    set FILE=%%F
    for %%I in ("%%~nF") do set COLLECTION_NAME=%%~nI
    mongoimport --uri "%MONGO_URI%" --db %DB_NAME% --collection %COLLECTION_NAME% --file "%FILE%" --jsonArray
    echo Imported %%F into collection %COLLECTION_NAME%
)