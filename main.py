import time
import sqlite3
from ping_logic import hacer_ping

# Diccionario con los destinos
OBJETIVOS = {
    'Router': '192.168.100.1',
    'DNS': '8.8.8.8',
    'Web': 'google.com'
}

def registrar_datos():
    conexion = sqlite3.connect('data/network_log.db')
    cursor = conexion.cursor()
    
    print(f"\n--- Evaluando red: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    for tipo, direccion in OBJETIVOS.items():
        destino, latencia, perdida, estado = hacer_ping(direccion)
        # Signos de interrogacion para pasar los datos para prevenir errores
        cursor.execute('''
            INSERT INTO network_stats (target_type, target_address, latency_ms, packet_loss_percent, status)
            VALUES (?, ?, ?, ?, ?)
            ''', (tipo, destino, latencia, perdida, estado))
        print(f"[{tipo}] {destino} -> Estado: {estado} | Latencia: {latencia}ms")
    
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    print("Iniciando monitor de red... (Presiona Ctrl+C para detener)")
    try:
        while True:
            registrar_datos()
            # Pausa de un minuto para no hacer pings seguidos
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario")
        

        
    