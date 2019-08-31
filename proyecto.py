import pickle
import os
from sys import exit
from os import system
from io import open as op
import time
lista  = []

fecha_doc = None
hora_doc = None
'''-----------------------Clases-------------------------------'''
class producto():
    def __init__(self, precio, costo):
        self.precio = precio
        self.costo = costo
        
class tabloide(producto):
    def __init__(self,precio,costo,tipo,depto,ventas):
        producto.__init__(self, precio, costo)
        self.tipo = tipo
        self.depto = 'Papeleria'
        self.ventas = 0
    def __str__(self):
        return '{}-{}-{}-{}-{}\n'.format(self.precio, self.costo,self.tipo,self.depto,self.ventas)
'''-----------------------Instancias-------------------------------'''
c300 = tabloide(10,None,'Couche 300','Papeleria',0)
c150 = tabloide(8,None,'Couche 150','Papeleria',0)
cr12 = tabloide(13,None,'Cromacote 12pts','Papeleria',0)
cr10 = tabloide(12,None,'Cromacote 10pts','Papeleria',0)
adma = tabloide(12,None,'Adhesivo Mate','Papeleria',0)
adbr = tabloide(13,None,'Adhesivo Brillante','Papeleria',0)
bond = tabloide(5,None,'Bond','Papeleria',0)
'''-----------------------Funciones-------------------------------'''
def menu():
    print('Bienvenido al sistema de registro de ventas de KONEK-T v0.01')
    print('Elige una opcion del siguiente menu')
    print('1.- Couche 300 grs')
    print('2.- Couche 150 grs')
    print('3.- Cromacote 12pts')
    print('4.- Cromacote 10pts')
    print('5.- Adhesivo Mate')
    print('6.- Adhesivo Brillante')
    print('7.- Bond')
    print('8.- Guardar reporte')
    print('9.- Revisar')
    print('0.- Salir')
'''Funcion donde se encuentra la logica de la seleccion del menu'''

def elegir():
    '''Rangos de eleccion minimo y maximo'''
    rango_max = 9
    rango_min = 0
    try:
        opcion = int(input())
        if opcion == 0:
            exit()
        elif opcion == 9:
            cargar()
        elif opcion ==12:
            comparar_fecha()
        elif opcion == 8:
            crear()
        elif opcion ==1:
            tabchoice(c300)
        elif opcion ==2:
            tabchoice(c150)
        elif opcion ==3:
            tabchoice(cr12)
        elif opcion ==4:
            tabchoice(cr10)
        elif opcion ==5:
            tabchoice(adma)
        elif opcion ==6:
            tabchoice(adbr)
        elif opcion ==7:
            tabchoice(bond)
        elif opcion > rango_min or opcion <rango_max:
            limpiar_menu_nuevo('El numero que escribiste no aparece en el rango, intenta nuevamente')
    except ValueError:
        #limpiar()
        #menu()
        print('Esto no es un codigo valido, escribe nuevamente el codigo')
        elegir()
    except:
        print('Ocurrio un error')
        input()
        
def tabchoice(tab):
    print('Elegiste:' ,tab.tipo) 
    try:
        cantidad = input('Cantidad:')
        '''el metodo isnumeric() aplicado a las cadenas de texto o numeros devuelve true
        si en efecto es un numero o esta compuesto de numeros'''
        if cantidad.isnumeric() == True:
            tab.ventas = int(tab.ventas) + int(cantidad)
            print('Has vendido: {} -- {}'.format(cantidad,tab.tipo))
            input('presiona una tecla para continuar vendiendo...')
            limpiar()
            menu()
            print('Elige una opcion( 1 - 9) del menu')
            elegir()
        elif cantidad == 'n':
            limpiar()
            menu()
            print('No se vendio nada')
            print('Elige una opcion( 1 - 9) del menu')
            elegir()
        else:
            limpiar()
            menu()
            print("Error... el dato introducido no es un numero")
            tabchoice(tab)
    except ValueError as err:
        print("Error... favor de consultar al administrador del sistema :L", err)
        exit()
    except:
        print('Ocurrio un error')
        input()

'''implementar guardado en formato binario... 22/07/2019'''
def nuevodoc():
    '''guarda la informacion en formato permanente en fisico'''
    lista=[str(c300),str(c150),str(cr12),str(cr10),str(adma),str(adbr),str(bond)]
    save = op("nuevo.konekt","wb")
    pickle.dump(lista,save)
    save.close()
    print('documento creado...')
    cargar()
    input()
'''funcion que escribe en pantalla el contenido del archivo de guardado
predeterminado'''
def crear():
    lista = [str(c300),str(c150),str(cr12),str(cr10),str(adma),str(adbr),str(bond)]
    archivo = op('save.kt','w')
    for elemento in lista:
        archivo.write(elemento)
    archivo.write(obtener_fecha_pc())
    archivo.write(obtener_hora_pc())
    archivo.close()
    '''añadir la funcion que agregue la fecha al documento'''
    limpiar()
    menu()
    elegir()
    
def leer():
    lectura = op("nuevo.konekt","rb+")
    lectenc = pickle.load(lectura)
    print(str(lectenc))
    
def guardar():
    pass
    
def cargar():
    '''carga un archivo con informacion permanente en el disco'''
    lista_tab = [c300,c150,cr12,cr10,adma,adbr,bond]
    try:
        archivo = op('save.kt','r')
        print(' Ventas totales\n','***********************************************')
        '''Agregue un ciclo for para obtener cada uno de los tipos de tabloides'''
        for papel in lista_tab:
            cuenta = 0 
            for linea in archivo:
                if cuenta <7:
                    '''Esta linea es la que le asigna a cada propiedad el valor correspondiente'''
                    papel.precio,papel.costo,papel.nombre,papel.depto,papel.ventas = linea.rstrip('\n').split('-')
                    print(' ',papel.nombre,'-',papel.ventas)
                    cuenta = cuenta + 1
                if cuenta>=7 and cuenta <8:
                    comparar_fecha(archivo)
                    '''La siguiente linea obtiene la fecha y hora de creacion del archivo'''
        archivo.close()
        elegir()
    except FileNotFoundError as Error:
        print("El archivo no se ha encontrado... Guarde el reporte antes de leerlo\n ",Error)
        input()
       # limpiar()
       
    except ValueError as error:
        print("Error en la lectura del archivo ", error)
        '''El error viene a causa de las ultimas 2 lineas del archivo de respaldo a causa de que solo es un argumento'''
        
'''funcion que muestra en pantalla los tabloide vendidos tomando como parametro
un objeto instancia dela clase tabloide.'''
def vendidos():
    lista2 = [c300,c150,cr12,cr10,adma,adbr,bond]
    limpiar()
    menu()
    for tabl in lista2:
        print('  has vendido: {} de {}'.format(tabl.ventas,tabl.tipo))
    elegir()
    
def limpiar():
    system('cls')

def limpiar_menu_nuevo(mensaje = ""):
    '''la linea system("<comando>") escribe 1 comando descrito entre comillas '''
    system('cls')
    menu()
    '''Mensaje en formato cadena de texto... o con format...'''
    print(mensaje)
    elegir()
    
def obtener_fyh_doc(archivo):
    '''necesita antes haber leido las filas de los tabloides.'''
    fecha_doc = archivo.readline()
    hora_doc = archivo.readline()
    '''Recuerda que el return devuelve una tupla de los valores que le ponga al final...'''
    return fecha_doc, hora_doc
    
def obtener_fecha_pc():
    '''La cadena de texto dentro del metodo utilizado es estandar del modulo time'''
    fecha = time.strftime("%d/%m/%y")
    return fecha + "\n"

def obtener_hora_pc():
    hora = time.strftime("%H:%M:%S")
    return hora + "\n"

def comparar_fecha(archivo):
    '''Obtengo los valores de la funcion que necesito (Recuerda que el return devuelve una tupla de los valores que le ponga al final..)'''
    print("Entraste a la funcion...")
    fecha1,hora_doc = obtener_fyh_doc(archivo)
    fechaListaDoc = fecha1.rstrip('\n')
    horaListaDoc = hora_doc.rstrip('\n')
    '''La siguiente linea obtiene las horas, los minutos y los segundos de la cadena de teexto hora...'''
    horas_doc,minutos_doc,segundos_doc = horaListaDoc.split(':')
    fechaListaPc = obtener_fecha_pc().rstrip('\n')
    horaListaPc = obtener_hora_pc().rstrip('\n')
    print("La hora del sistema es: ", horaListaPc)
    #print('Fecha dentro de comparar fecha',fecha1.rstrip('\n').rstrip(' '),'check') -------- pruebas para comparar fechas
    if fechaListaPc == fechaListaDoc:
        print("La fecha se cargo correctamente... y son iguales, se debe cargar el archivo solamente")
        '''Cargar documento y no reemplazarlo'''
    else:
        print("Fechas no iguales...")
        print(obtener_fecha_pc().rstrip('\n'))
    '''Con este condicional se compara que turno es actualmente'''
    if int(horas_doc) >=5 and int(horas_doc)<15:
        print("Turno Matutino ")
    elif int(horas_doc) >= 15 and int(horas_doc) < 24 :
        print("Turno Vespertino ")
    elif int(horas_doc) <5:
        print("Estas trabajando tan temprano???... Lo siento no se pueden registrar productos aun")
    '''Crear el documento...'''
    '''Obtener la fecha de creacion del archivo para determinar si se creara el
       archivo o solo se agregaran las ventas totales'''

if __name__ == '__main__':
    # menu()
##    elegir()
    
    cargar()
    #comparar_fecha()

