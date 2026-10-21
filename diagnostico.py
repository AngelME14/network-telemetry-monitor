import sqlite3

def analizar_estado_actual():
    conexion = sqlite3.connect('data/network_log.db')
    cursor = conexion.cursor()
    
    #Solo los ultimos 3 registros de la BD porque equivale al ultimo escaneo
    cursor.execute('''
        SELECT target_type, status, latency_ms
        FROM network_stats
        ORDER BY timestamp DESC LIMIT 3
        ''')
    
    resultados = cursor.fetchall()
    conexion.close()
    
    if len(resultados) < 3:
        print("Aun no hay suficientes datos para diagnosticar")
        return
    
    datos = {}
    for fila in resultados:
        tipo = fila[0]
        datos[tipo] = {'estado': fila[1], 'latencia':fila[2]}
    
    print("--- DIAGNOSTICO DE RED ---")
    # .get() por si en algun minuto no guarda el codigo no crashea
    estado_router = datos.get('router', {}).get('estado')
    estado_dns = datos.get('DNS', {}).get('estado')
    estado_web = datos.get('Web', {}).get('estado')
    latencia_web = datos.get('Web', {}).get('latencia', 0.0)
    
    if estado_router == 'DOWN':
        print("FALLA LOCAL: El equipo no alcanza el router. Revisa el Wi-Fi, cable o el modem")
    
    elif estado_router == 'UP' and estado_dns == 'DOWN' and estado_web == 'DOWN':
        print("FALLA DEL PROVEEDOR: Tienes conexion al router, pero no hay salida a internet, posible caida de servicio")
    
    elif estado_router == 'UP' and estado_dns == 'UP' and estado_web == 'DOWN':
        print("FALLA DNS/WEB: Hay internet, pero la pagina web de prueba no responde o hay problemas de resolucion")
    
    else:
        if latencia_web > 100.0:
            print(f"SATURACION: Conexion activa pero lenta, latencia a internet muy alta ({latencia_web} ms)")
        else:
            print(f"NORMAL: Red estable, latencia a internet: {latencia_web} ms")       
            

if __name__ == "__main__":
    analizar_estado_actual()

