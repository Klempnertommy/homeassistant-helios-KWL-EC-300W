import logging
import argparse
import sys
import re
import struct
import time
from pymodbus.client import ModbusTcpClient as ModbusClient

SLAVE_ID = 180
FIRST_REGISTER_ADDR = 0x01

def main(ip, variable, rtr):
    client = None
    try:
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.ERROR)

        rtr = rtr + 3
        if rtr < 8:
            rtr = 8

        client = ModbusClient(host=ip, port=502)
        if not client.connect():
            return

        # Sende-String mit Null-Byte abschliessen
        send_string = (variable + '\0').encode('ascii')
        if len(send_string) % 2 != 0:
            send_string += b'\x00'

        # Verpackt den Text mathematisch korrekt fuer das Helios-Register
        payload = []
        for i in range(0, len(send_string), 2):
            register_value = struct.unpack('>H', send_string[i:i+2])[0]
            payload.append(register_value)

        # Telegramm an die KWL senden
        client.write_registers(address=FIRST_REGISTER_ADDR, values=payload, device_id=SLAVE_ID)
        
        # WENN EIN BEFEHL GESCHRIEBEN WIRD (z.B. v00084=1)
        if '=' in variable:
            time.sleep(0.1)
            return

        # WENN GELESEN WIRD (z.B. Fühlerabfrage)
        # Wir geben der KWL in einer Schleife kurz Zeit, die Antwort ins Register zu schreiben
        for _ in range(5):
            time.sleep(0.1)
            result = client.read_holding_registers(address=FIRST_REGISTER_ADDR, count=rtr, device_id=SLAVE_ID)

            if not result.isError() and result.registers:
                response_bytes = bytearray()
                for reg in result.registers:
                    response_bytes.extend(struct.pack('>H', reg))

                output = response_bytes.decode('ascii', errors='ignore')
                output = re.sub(r'[\x00-\x1F\x7F]', "", output)

                # Nur ausgeben, wenn das Postfach nicht leer ist
                if output.strip():
                    print(output)
                    return

    except Exception as e:
        pass
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Helios KWL Modbus interface')
    parser.add_argument('ip', help='IP address of Modbus slave')
    parser.add_argument('registers', type=int, help='Number of registers to read')
    parser.add_argument('variable', help='Variable to read')

    args = parser.parse_args()
    main(args.ip, args.variable, args.registers)
