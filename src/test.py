# verify_db.py
from sqlalchemy import create_engine, inspect
from database import DATABASE_URL

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# List all tables
tables = inspector.get_table_names()
print(f"Tables: {tables}")

# Check columns in the quizzes table
if 'quizzes' in tables:
    columns = inspector.get_columns('quizzes')
    print(f"Columns in 'quizzes': {[column['name'] for column in columns]}")
else:
    print("Table 'quizzes' does not exist.")