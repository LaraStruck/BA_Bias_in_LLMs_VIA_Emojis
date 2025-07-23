import os
import dotenv
def getDatabasePath():
    dotenv.load_dotenv()
    return os.getenv("DATABASE_EMOJI_RESULTS")

def getApiKey():
    dotenv.load_dotenv()
    return os.getenv("OPENROUTER_API_KEY")
def getCSVPath():
    dotenv.load_dotenv()
    return os.getenv("CSV_PATH")
def getPartiesCSV():
    dotenv.load_dotenv()
    return os.getenv("Parties_CSV")

