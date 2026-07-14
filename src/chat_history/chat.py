from .base import ChatHistoryRepository
import psycopg2
import json 
from typing import Optional, Dict, List

class PostgresChatHistory(ChatHistoryRepository):
    def __init__(self, host, database, user, password):
        """Stores the connection parameters."""
        self.host = host 
        self.database = database
        self.user = user
        self.password = password

    def save_history(self, question: str, answer: str, metadata: Optional[Dict] = None):
        """Saves the history to PostgreSQL."""
        
        # 1. Serialization
        meta = None 
        if metadata is not None:
            meta = json.dumps(metadata)
            
        # 2. The Bridge (Notice this is NOT indented inside the 'if' statement)
        conn = psycopg2.connect(
            host=self.host, 
            database=self.database, 
            user=self.user, 
            password=self.password
        )
        # Hire the messenger immediately!
        cursor = conn.cursor()
        
        try:
            # 3. The Command
            sql_query = "INSERT INTO chat_history (question, answer, meta_data) VALUES (%s, %s, %s);"
            cursor.execute(sql_query, (question, answer, meta))
            
            # 4. The Handshake
            conn.commit()
            
        finally:
            # 5. Cleanup
            cursor.close()
            conn.close()

    def extract_history(self, limit: int) -> List[Dict]:
        """Fetches the most recent chat history and formats it for the LLM."""
        
        # 1. The Bridge (Open the door and hire the messenger)
        conn = psycopg2.connect(
            host=self.host, 
            database=self.database, 
            user=self.user, 
            password=self.password
        )
        cursor = conn.cursor()
        
        try:
            # 2. The Command (Select newest messages up to the limit)
            sql_query = "SELECT question, answer FROM chat_history ORDER BY created_at DESC LIMIT %s;"
            
            # Note the comma in (limit,) — this forces Python to treat it as a tuple
            cursor.execute(sql_query, (limit,))
            
            # 3. The Retrieval (Grab the raw list of tuples from the database)
            rows = cursor.fetchall()
            
            # 4. Data Transformation (Convert tuples to a clean list of dictionaries)
            formatted_history = []
            for row in rows:
                formatted_history.append({
                    "question": row[0],
                    "answer": row[1]
                })
                
            # 5. The Reversal (Flip the list so the oldest messages are first)
            return formatted_history[::-1]
            
        finally:
            # 6. Cleanup (Always shut the door)
            cursor.close()
            conn.close()