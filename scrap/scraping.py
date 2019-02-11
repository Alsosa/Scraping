# Para el siguiente script es necesario instalar bs4 (Beautiful Soup) y requests en caso de ser necesario.

import requests
from bs4 import BeautifulSoup
from csv import writer

def moneda():       # Defino la primer función.
    
    text = input("Ingrese tipo de moneda: ")    # Se le pide al usuario ingresar tipo de moneda.
    print("Seleccionó: ", text)

    if text == 'dolar' or text == '':     # Dependiendo el tipo de moneda que ingrese el usuario, se obtiene la dirección requerida.
        response = requests.get('http://dolarhoy.com/')        
        text = 'dolar'                      # En caso de que el usuario no ingrese nada, el dolar es la moneda por defecto.
                    
    elif text == 'euro':
        response = requests.get('http://dolarhoy.com/cotizacion-euro')

    elif text == 'peso uruguayo':
        response = requests.get('http://dolarhoy.com/cotizacion-peso-uruguayo')
        
    elif text == 'real brasileño':
        response = requests.get('http://dolarhoy.com/cotizacion-real-brasileno')

    else:           # Si se ingresa otro tipo de moneda o un tipo de texto inválido, se devuelve un mensaje de error.
        print('Los tipos de moneda validos son: dolar, euro, peso uruguayo, real brasileño.')
        return()

    cotizacion(response, text)     # Una vez que tenemos el link, llamamos a la segunda función.   


def cotizacion(response, text):    # Se define la segunda función con los parámetros response y text.

    soup = BeautifulSoup(response.text, 'html.parser')

    monedas = soup.find_all(class_='col-md-8')      # Busco el div col-md-8 que posee los div col-md-6 compra y venta.

    with open('monedas.csv', 'w') as csv_file:      # Se abre el archivo csv en modo escritura.
        csv_writer = writer(csv_file)
        headers = ['Cotizacion promedio del ' + text]   # Agrego el título de la cotización promedio ingresada.
        csv_writer.writerow(headers)

        for moneda in monedas:      # Hacemos el loop para obtener compra y venta, y poder escribirlos en el csv.
            compra = moneda.find(class_='col-md-6 compra').get_text().replace('\n', '')
            venta = moneda.find(class_='col-md-6 venta').get_text().replace('\n', '')
            csv_writer.writerow([compra, venta])

moneda()        #Llamamos a la primer función.