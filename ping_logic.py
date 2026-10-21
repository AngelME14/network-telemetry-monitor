import subprocess
import re

def hacer_ping(destino):
    
    comando = ['ping', '-n', '1', destino]
    
    try:
        # Subprocess en lugar de os.system para capturar la salida de texto
        respuesta = subprocess.run(comando, capture_output=True, text=True, timeout=5)
        salida_consola = respuesta.stdout
        
        if respuesta.returncode == 0:
            estado = "UP"
            
            # Busqueda 'tiempo' o 'time' por si el sistema operativo cambia el idioma
            busqueda = re.search(r'(?:tiempo|time)[=<](\d+)', salida_consola.lower())
            
            if busqueda:
                latencia = float(busqueda.group(1))
            else:
                latencia = 0.0
            
            perdida = 0.0
        else:
            estado = "DOWN"
            latencia = 0.0
            perdida = 100.0
        
        return destino, latencia, perdida, estado
    
    except subprocess.TimeoutExpired:
        return destino, 0.0, 100.0, "DOWN"
    except Exception as e:
        print(f"Error detectado: {e}")
        return destino, 0.0, 100.0, "DOWN"
    
if __name__ == "__main__":
    print(hacer_ping("8.8.8.8"))
    print(hacer_ping("192.168.100.1"))
    print(hacer_ping("999.999.999.999"))