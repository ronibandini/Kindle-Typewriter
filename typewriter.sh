#!/bin/bash
# TypeWriter - Roni Bandini 4/2026
# TypeWriter for the Kindle Paperwhite

# Settings
RPI_IP=""   
RPI_PORT="5000"
ENDPOINT="http://${RPI_IP}:${RPI_PORT}/imprimir"

# Banner
clear
echo ""
echo "**********************************************"
echo "*                                            *"
echo "*           KINDLE TYPEWRITER                *"
echo "*           1.00 Roni Bandini                *"
echo "*                                            *"
echo "**********************************************"
echo ""

BUFFER=""

while true; do
    printf "> "
    read LINE

    # Salida
    if [ "$LINE" = "/salir" ] || [ "$LINE" = "exit" ] || [ "$LINE" = "quit" ]; then
        echo ""
        echo "Hasta la vista!"
        exit 0
    fi

    # Linea vacia: imprimir lo acumulado en el buffer
    if [ -z "$LINE" ]; then
        if [ -z "$BUFFER" ]; then
            continue
        fi
        TEXTO="$BUFFER"
        BUFFER=""
    else
        # Acumular linea en buffer
        if [ -z "$BUFFER" ]; then
            BUFFER="$LINE"
        else
            BUFFER="${BUFFER}
${LINE}"
        fi
        continue
    fi

    # Escapar el texto para JSON con awk
    ESCAPED=$(printf '%s' "$TEXTO" | awk '{
        out = ""
        for (i=1; i<=length($0); i++) {
            c = substr($0,i,1)
            if      (c == "\\") out = out "\\\\"
            else if (c == "\"") out = out "\\\""
            else if (c == "\n") out = out "\\n"
            else if (c == "\r") out = out "\\r"
            else if (c == "\t") out = out "\\t"
            else out = out c
        }
        printf "%s", out
    }')

    # Enviar al endpoint
    echo ""
    echo "Sending to the printer..."

    HTTP_CODE=$(curl -s -o /tmp/rpi_resp.json -w "%{http_code}" \
        -X POST "$ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "{\"texto\":\"${ESCAPED}\"}" \
        --connect-timeout 5 \
        --max-time 30)

    if [ "$HTTP_CODE" = "200" ]; then
        echo "Printed!"
    elif [ "$HTTP_CODE" = "000" ]; then
        echo "ERROR: Connection error ${RPI_IP}:${RPI_PORT}"
        echo "Check the IP, WiFi Connection and RpiZero Python script running."
    else
        echo "ERROR HTTP $HTTP_CODE"
        cat /tmp/rpi_resp.json 2>/dev/null
    fi

    echo ""
done
