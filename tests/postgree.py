from src.chat_history.chat import PostgresChatHistory

repo = PostgresChatHistory(
    host="localhost",
    database="documind",
    user="myuser",
    password="123"
)

# 1. Save works perfectly (metadata defaults to None)
print("Saving data...")
repo.save_history("what is mango ?", "a fruit")

# 2. Extract requires a limit
print("Extracting data...")
history = repo.extract_history(limit=5)

# 3. Print the result so you can see it
print(history)