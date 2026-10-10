import os
import gzip
from datetime import datetime, timedelta, timezone

def generate_novaeventos():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    epg_dir = os.path.join(base_dir, "epg")
    os.makedirs(epg_dir, exist_ok=True)

    gz_output = os.path.join(epg_dir, "novaeventos.xml.gz")

    # Canales de eventos
    channels = [
        {"id": "evento.1", "name": "Evento 1"},
        {"id": "evento.2", "name": "Evento 2"},
        {"id": "evento.3", "name": "Evento 3"},
        {"id": "evento.4", "name": "Evento 4"},
        {"id": "evento.5", "name": "Evento 5"}
    ]

    # Generar programación continua 24/7 desde 7 días atrás hasta 30 días en el futuro
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=7)
    end_time = now + timedelta(days=30)

    with gzip.open(gz_output, 'wt', encoding='utf-8', compresslevel=9) as gz:
        gz.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="NovaEPG-Eventos">\n')

        # 1. Escribir Canales
        for c in channels:
            gz.write(f'  <channel id="{c["id"]}"><display-name>{c["name"]}</display-name></channel>\n')

        # 2. Escribir Programas en bloques de 2 horas 24/7
        curr = start_time
        while curr < end_time:
            next_curr = curr + timedelta(hours=2)
            start_str = curr.strftime("%Y%m%d%H%M%S") + " +0000"
            stop_str = next_curr.strftime("%Y%m%d%H%M%S") + " +0000"

            for c in channels:
                gz.write(f'  <programme start="{start_str}" stop="{stop_str}" channel="{c["id"]}">\n')
                gz.write(f'    <title lang="es">24/7 (Eventos)</title>\n')
                gz.write(f'    <desc lang="es">Transmisión permanente 24/7 de eventos especiales</desc>\n')
                gz.write(f'  </programme>\n')

            curr = next_curr

        gz.write('</tv>')
    print(f"✅ epg/novaeventos.xml.gz generado con éxito.")

if __name__ == "__main__":
    generate_novaeventos()
