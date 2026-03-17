import pymysql
import os

def export_schema():
    target_path = r"h:\2026\mc_protocol_python\SUZUKI_INSTALLER\database\plc_db_v2.sql"
    try:
        conn = pymysql.connect(
            host='localhost', 
            user='root', 
            password='', 
            database='plc_db'
        )
        cursor = conn.cursor()
        
        # Ambil daftar tabel
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write("CREATE DATABASE IF NOT EXISTS plc_db;\n")
            f.write("USE plc_db;\n\n")
            
            for table in tables:
                # Get Create Table
                cursor.execute(f"SHOW CREATE TABLE {table}")
                create_stmt = cursor.fetchone()[1]
                f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                f.write(f"{create_stmt};\n\n")
                
                # Opsi: Export data master (non-activity)
                if '_master' in table or table == 'plc_oee_seat_result_detail':
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    if rows:
                        # Get column names
                        cursor.execute(f"DESCRIBE {table}")
                        cols = [r[0] for r in cursor.fetchall()]
                        col_str = ", ".join([f"`{c}`" for c in cols])
                        
                        for row in rows:
                            # Sanitize values
                            vals = []
                            for v in row:
                                if v is None: vals.append("NULL")
                                elif isinstance(v, (int, float)): vals.append(str(v))
                                else: vals.append(f"'{conn.escape_string(str(v))}'")
                            
                            val_str = ", ".join(vals)
                            f.write(f"INSERT INTO `{table}` ({col_str}) VALUES ({val_str});\n")
                        f.write("\n")

        print(f"Schema and master data exported to: {target_path}")
        return True
    except Exception as e:
        print(f"Export failed: {e}")
        return False
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    export_schema()
