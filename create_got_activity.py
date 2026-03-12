import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def connect_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

def create_activity_table():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 1. Create table `plc_oee_got_activity`
            print("Creating table plc_oee_got_activity...")
            create_sql = """
            CREATE TABLE IF NOT EXISTS plc_oee_got_activity (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device VARCHAR(50) NOT NULL,
                value VARCHAR(50) DEFAULT '0',
                komen TEXT,
                start_time DATETIME DEFAULT NULL,
                end_time DATETIME DEFAULT NULL,
                update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_device (device)
            ) ENGINE=InnoDB;
            """
            cursor.execute(create_sql)
            print("Table plc_oee_got_activity created successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_activity_table()
