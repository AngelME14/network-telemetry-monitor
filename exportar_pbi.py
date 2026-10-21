import sqlite3
import csv

def exportar_a_csv():
    
    conexion = sqlite3.connect('data/network_log.db')
    cursor = conexion.cursor()
    # 'localtime' porque sin esto Power BI muestra los datos con horario diferente
    cursor.execute('''
        SELECT datetime(timestamp, 'localtime'), target_type, target_address, latency_ms, packet_loss_percent, status 
        FROM network_stats
    ''')
    
    filas = cursor.fetchall()
    # 'with open' para cerrar el archivo csv automaticamente al terminar para evitar bloqueos o fugas 
    with open('data/datos_powerbi.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        
        escritor.writerow(['Fecha_Hora', 'Tipo', 'Destino', 'Latencia_ms', 'Perdida_Paquetes', 'Estado'])
        
        escritor.writerows(filas)
    
    print(f"Exportacion exitosa. {len(filas)} registros guardados en data/datos_powerbi.csv")
    
    conexion.close()

if __name__ == "__main__":
    exportar_a_csv()


        