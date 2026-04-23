# Kindle Typewriter 
# Roni Bandini 4/2026
# MIT License

import serial
import time
import socket
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
uart = None

BANNER = r"""
 _  ___        _ _   _____                     _ _            
| |/ (_)_ __  __| | |__|_  _|   _ _ __   _____   _| (_)_ __ ___  
| ' /| | '_ \ / _` | |/ _ \| || | | | '_ \ / _ \ \ /\ / / | | '__/ _ \ 
| . \| | | | | (_| | |  __/| || |_| | |_) |  __/\ V  V /| | | | |  __/ 
|_|\_\_|_| |_|\__,_|_|\___||_| \__, | .__/ \___| \_/\_/ |_|_|_|  \___| 
                                |___/|_|                                
"""

CREDITS = """
  Author  : Roni Bandini
  Date    : April 2026
  License : MIT
  -------------------------------------------------------------------------
"""

PRINTER_WIDTH = 30
LOG_DIR = "/home/"


def save_to_file(texto):
    """Guarda texto impreso en un txt."""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(LOG_DIR, f"{timestamp}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(texto)
        print(f"[OK] Saved {filepath}")
    except Exception as e:
        print("[ERROR] Cannot save:", e)


def wrap_text(texto, ancho=PRINTER_WIDTH):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ''
    for palabra in palabras:
        if len(palabra) > ancho:
            if linea_actual:
                lineas.append(linea_actual)
                linea_actual = ''
            lineas.append(palabra)
            continue
        candidato = linea_actual + (' ' if linea_actual else '') + palabra
        if len(candidato) <= ancho:
            linea_actual = candidato
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return '\n'.join(lineas)


def print_bitmap(path):
    if uart is None:
        print("[WARN] UART no disponible. Bitmap no impreso")
        return
    try:
        from escpos.printer import Dummy
        d = Dummy()
        d.image(path, impl='bitImageRaster', fragment_height=960)
        uart.write(d.output)
        uart.flush()
        uart.write(b'\n\n')
        print(f"[OK] Bitmap printed ({len(d.output)} bytes)")
    except Exception as e:
        print("[ERROR] Bitmap:", e)


def init_uart():
    global uart
    try:
        uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=5)
        print("[OK] UART started /dev/serial0")
        return True
    except Exception as e:
        print("[ERROR] Cannot open UART:", e)
        uart = None
        return False


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def efecto_maquina(texto, ancho=PRINTER_WIDTH):
    texto_wrapped = wrap_text(texto, ancho)
    save_to_file(texto_wrapped)
    if uart is None:
        print("[WARN] UART not available. Texto not printed:")
        print(texto_wrapped)
        return
    try:
        for char in texto_wrapped:
            uart.write(char.encode('ascii', errors='ignore'))
            time.sleep(0.02)
        uart.write(b'\n\n\n')
    except Exception as e:
        print("[ERROR] Error writing UART:", e)


@app.route('/imprimir', methods=['POST'])
def endpoint_imprimir():
    data = request.get_json()
    if not data or 'texto' not in data:
        return jsonify({"error": "Missing field 'texto'"}), 400
    texto = data['texto']
    efecto_maquina(texto)
    return jsonify({
        "status": "ok",
        "uart": uart is not None
    }), 200


if __name__ == '__main__':
    print(BANNER)
    print(CREDITS)
    print("  Starting server...")
    print("  -------------------------------------------------------------------------")
    init_uart()
    if uart:
        try:
            uart.write(b'\x1b\x40')
        except Exception as e:
            print("[ERROR] Printer reset error:", e)
    print_bitmap("/home/roni/images/logosmall.jpg")
    print("[INFO] Flask 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)