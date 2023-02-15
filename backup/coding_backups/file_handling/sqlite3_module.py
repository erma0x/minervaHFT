import sqlite3
'''
    1499040000000,      // Kline open time
    "0.01634790",       // Open price
    "0.80000000",       // High price
    "0.01575800",       // Low price
    "0.01577100",       // Close price
    "148976.11427815",  // Volume
    1499644799999,      // Kline Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "0"                 // Unused field, ignore.
'''

HEADER_TABLE = ['open_time', 'high', 'low', 'close',
                'volume', 'close_time', 'quote_asset_volume', '']


def print_all(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    rows = cursor.execute(
        "SELECT id, date, sender, message, placed FROM price").fetchall()
    print(rows)
    connection.close()


def create_db(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, date TEXT, sender TEXT, message TEXT, placed TEXT)")
    conn.close()


def print_changes(db):
    conn = sqlite3.connect(db)
    print("TOTAL CHANGES: ", conn.total_changes)
    conn.close()


def delete_id(id_, db):
    old_id = id_
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (old_id,))
    connection.commit()
    connection.close()


def write_message(id_message, message_date, sender_group, text_message, NAME_DB):
    conn = sqlite3.connect(NAME_DB)
    c = conn.cursor()
    query = """ INSERT INTO messages VALUES ({0},'{1}','{2}','{3}','ok')""".format(
        id_message, message_date, sender_group, text_message)
    c.execute(query)
    conn.commit()
    print('TOTAL CHANGES WRITE MESSAGES : ', conn.total_changes)
    conn.close()


def get_new_id(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    last_id = cursor.execute(
        "SELECT id FROM messages ORDER BY id DESC LIMIT 1").fetchall()
    connection.commit()
    connection.close()
    if last_id:
        return last_id[0][0] + 1
    else:
        return 1


def get_all_messages(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT id, date, sender, message, placed FROM messages ORDER BY id DESC").fetchall()
    connection.close()
    return data


# create_db('pluto.db')
write_message(id_message=6, message_date='10.10', sender_group='b',
              text_message='test', NAME_DB='pluto.db')
print_all('pluto.db')
print(get_new_id('pluto.db'))
