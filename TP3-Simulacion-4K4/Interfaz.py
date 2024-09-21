from tkinter import *
from tkinter import ttk
from tp import *


def Mensaje_Error(mensaje, titulo, resultado):
    raiz2 = Tk()
    raiz2.title(titulo)
    raiz2.geometry("400x50")

    raiz2.resizable(width=False, height=False)
    if resultado == True:
        back2 = "green3"
    else:
        back2 = "red2"
    raiz2.configure(background=back2)
    nombreMensaje=Label(raiz2, text=mensaje, font=("Arial bold", 13), background=back2)
    nombreMensaje.pack()

def llamar_TP():
    dias = cuadroDias.get()
    intInicial = cuadroIntervaloInicial.get()
    intFinal = cuadroIntervaloFinal.get()
    while True:
        if int(dias) >= 0 \
                and int(intInicial) > 0 \
                and int(intFinal) >= 0:
            Mensaje_Error("Ingreso satisfactorio", "¡¡Bien Hecho!!", True)
            tp_tkinter(int(dias))
            break
        else:
            Mensaje_Error("INGRESO INCORRECTO", "¡¡ERROR!!", False)
            return

raiz = Tk()
raiz.title("Grupo 6 - Venta Callejera")
raiz.geometry("1500x900")
ventana = Frame(raiz)
ventana.pack()
raiz.configure(background="#dedede")
#raiz.resizable(width=False, height=False) Para MAXIMIZAR Y MINIMIZAR la interfaz
back = "#c1c1c1"
ventana.configure(background=back)

cuadroDias=Entry(ventana, font=("Arial bold", 13))
cuadroDias.grid(row=1,column=1)
nombreDias=Label(ventana, text="Cantidad de Días a Simular (X): ", font=("Arial bold", 13), background=back)
nombreDias.grid(row=1, column=0)

cuadroIntervaloInicial=Entry(ventana, font=("Arial bold", 13))
cuadroIntervaloInicial.grid(row=2,column=1)
nombreIntervaloInicial=Label(ventana, text="Intervalo Inicial a Mostrar (i): ", font=("Arial bold", 13), background=back)
nombreIntervaloInicial.grid(row=2, column=0)

cuadroIntervaloFinal=Entry(ventana, font=("Arial bold", 13))
cuadroIntervaloFinal.grid(row=3,column=1)
nombreIntervaloFinal=Label(ventana, text="Intervalo Final a Mostrar (j): ", font=("Arial bold", 13), background=back)
nombreIntervaloFinal.grid(row=3, column=0)

boton = Button(ventana, text="Aceptar", font=6, command=llamar_TP, width=8, background="#b0b0b0")
boton.grid(row=9, column=1)

raiz.mainloop()