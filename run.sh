#!/bin/bash
echo ----------------------------------------------------------------
echo -------------------Simulacion de un ciclotron-------------------
echo ---------Juan Daniel Castrellon y Maria Sofia Alvarez ----------
echo ----------------------------------------------------------------
echo Escriba el numero de la opcion que desea correr [e.g. 1]
echo 1. Instalar las dependencias del programa
echo 2. Correr la simulacion del ciclotron.
echo 3. Eliminar los datos de simulaciones previas

read line;
    if [ "$line" -eq 1 ];
        then pip install -r requirements.txt;
    elif [ "$line" -eq 2 ]; 
        then python3 ./ciclotron.py;
    elif [ "$line" -eq 3 ]; 
        then rm -rf simulaciones;
    else
        echo Opcion no disponible;
    fi
