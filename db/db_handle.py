import sqlite3

DEFAULT_DB_NAME = "searchable"


def init_db(db_name=DEFAULT_DB_NAME):
    """
    Initialize the database with a normal table and an associated FTS5 table.
    Ensures `file_name` is unique across the normal table.
    """
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    # Create the normal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            file_name TEXT,
            page INTEGER NOT NULL,
            text TEXT,
            UNIQUE(file_name, page) ON CONFLICT IGNORE
        )
    ''')

    # Create the FTS5 virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
            text,
            content='items',
            content_rowid='rowid'
        )
    ''')

    # Trigger to sync inserts
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS items_ai AFTER INSERT ON items
        BEGIN
            INSERT INTO items_fts(rowid, text)
            VALUES (new.rowid, new.text);
        END;
    ''')

    # Trigger to sync updates
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS items_au AFTER UPDATE ON items
        BEGIN
            UPDATE items_fts
            SET text = new.text
            WHERE rowid = old.rowid;
        END;
    ''')

    # Trigger to sync deletes
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS items_ad AFTER DELETE ON items
        BEGIN
            DELETE FROM items_fts WHERE rowid = old.rowid;
        END;
    ''')

    conn.commit()
    conn.close()


def add_to_db(data, db_name=DEFAULT_DB_NAME):
    """
    Add items to the database while ensuring `file_name` uniqueness.
    Parameters:
    - data: A list of tuples (file_name, page, text)
    """
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    for item in data:
        file_name, page, text = item
        text = text.replace('\xa0', ' ').replace('\n', ' ')
        try:
            cursor.execute('''
                INSERT INTO items (file_name, page, text) VALUES (?, ?, ?)
            ''', (file_name, page, text))
        except sqlite3.IntegrityError:
            print(f"File {file_name} already exists. Skipping insertion.")
        except sqlite3.Error as e:
            print(f"Error inserting item {item}: {e}")

    conn.commit()
    conn.close()


def search_db(query, db_name=DEFAULT_DB_NAME):
    """
    Search the database using the FTS5 table.
    Parameters:
    - query: The search term(s) to match.
    Returns:
    - List of matching items in the format (file_name, page, text).
    """
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT items.file_name, items.page, items.text
        FROM items
        JOIN items_fts ON items.rowid = items_fts.rowid
        WHERE items_fts MATCH ?
    ''', (query,))

    results = cursor.fetchall()
    conn.close()

    return results

