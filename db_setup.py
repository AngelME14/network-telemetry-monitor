import sqlite3
import os

def inicializar_bd():
    #Carpeta 'data' primero para que SQLite no tire error
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conexion = sqlite3.connect('data/network_log.db')
    
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            target_type TEXT,
            target_address TEXT,
            latency_ms REAL,
            packet_loss_percent REAL,
            status TEXT
        )
    ''')

    conexion.commit()
    conexion.close()
    
    print("Base de datos lista y configurada.")
    
if __name__ == "__main__":
    inicializar_bd()

