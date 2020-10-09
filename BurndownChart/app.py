from tkinter import *
from tkcalendar import *
from tkinter import messagebox
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def mkchrt():
    try:
        points = int(points_label.cget("text"))
        if points == 0:
            file = open("burndownchart.csv","w")
            file.write('Fecha,Esperado\n')
            for i in range(len(dias)):
                if len(Hpoints) <= i:
                   file.write(str(dias[i])+',NaN\n')
                else:
                    if Hpoints[i] >= 0:
                         file.write(str(dias[i])+','+str(Hpoints[i])+'\n')
        file.close()
        df = pd.read_csv("burndownchart.csv")
        print(Hpoints[0])
        fig = plt.figure(figsize=(15,10))

        with plt.style.context('fivethirtyeight'):
            print('si')
            plt.plot(df["Fecha"],df["Esperado"],label="Esperado")
            plt.xticks(rotation=60)
            #plt.xticks(dias,rotation=60)
            plt.yticks(range(0,Hpoints[0]+1))
            plt.xlabel("\n Día en el Sprint")
            plt.ylabel("History points pendientes \n")
            plt.title("Burndown Chart \n",fontsize=40)
            plt.legend(loc="upper right")
            fig.savefig("BurndownChart.jpg")

    except:
        messagebox.showinfo("Error","Aun quedan puntos de historias no asignados.\nPor favor, asigne esos puntos a un dia.")

def mkpoints():
    def save_data(total_points,esperado,dias):
        total_points = int(entry_points.get())
        if total_points > 0:
            Hpoints.append(total_points)

            start=star_cal.get_date()
            end=finish_cal.get_date()
            current=start
            while current <= end:
                dias.append(current)
                print(dias)
                current += datetime.timedelta(days=1)
            dias.append(current)
            print(dias)

            esperado.append(start)
            startdate_label.configure(text=start)
            finishdate_label.configure(text=end)
            points_label.configure(text=total_points)

            top.destroy()
        else:
            messagebox.showinfo("Error","Error.\nVerifica si los puntos fueron ingresados o si los puntos ingresados son los correctos.")
            top.destroy()

    top = Toplevel(root)
    ##### start the proyect #####
    star_label = Label(top,text="Inicio del Sprint")
    star_label.pack()
    star_cal = DateEntry(top)
    star_cal.pack(pady=20)

    ##### finish the proyect #####
    finish_label = Label(top,text="Entrega del Sprint")
    finish_label.pack()
    finish_cal = DateEntry(top)
    finish_cal.pack(pady=20)

    info_points_label = Label(top,text="Total de puntos del Sprint")
    info_points_label.pack()
    entry_points = Entry(top)
    entry_points.pack(pady=5)
    
    ##### save button #####
    save_button = Button(top,text="Guardar", command=lambda:save_data(Hpoints,esperado,dias))
    save_button.pack(pady=20)
    
def mkidealwk():
    def prosesado(points,esperado):
        Hpoint = Historia_box.get()
        hdate = hdate_cal.get_date()
        if points > 0:
            points = int(points)-int(Hpoint)
            diferencia = hdate - esperado[len(esperado)-1]
            for sin_trabajo in range(diferencia.days-1):
                Hpoints.append(Hpoints[len(Hpoints)-1])
            print(diferencia)
            Hpoints.append(points)
            esperado.append(hdate)

            print(esperado)
            print(Hpoints)
            points_label.configure(text=points)
            top.destroy()
        else:
            messagebox.showinfo("Error","Error.\nVerifica si los puntos fueron ingresados o si los puntos ingresados son los correctos.")
            top.destroy()

    ##### Total points #####
    top = Toplevel(root)
    Historia_label = Label(top,text="Ingresar la cantidad de puntos que tiene la historia")
    Historia_label.pack()
    Historia_box = Entry(top)
    Historia_box.pack(pady=5)

    ##### Fecha de la Hitoria #####
    hdate_label = Label(top,text="Fecha")
    hdate_label.pack()
    hdate_cal = DateEntry(top)
    hdate_cal.pack(pady=20)

    points = int(points_label.cget("text"))
    print(points)
    ##### save button #####
    save_button = Button(top,text="Guardar", command=lambda:prosesado(points,esperado))
    save_button.pack(pady=20)

def quit():
    root.destroy()

root = Tk()
root.title("Burndownchart Maker")
root.geometry("400x400")

now = datetime.datetime.now()
dias = []
esperado = []
Hpoints = []

##### start the proyect #####
starttitulo_label = Label(root,text="Fecha de inicio")
starttitulo_label.pack()
startdate_label = Label(root,text="")
startdate_label.pack()

##### finish the proyect #####
finishtitulo_label = Label(root,text="Fecha de entrega")
finishtitulo_label.pack()
finishdate_label = Label(root,text="")
finishdate_label.pack()

##### Total points #####
pointstitulo_label = Label(root,text="Puntos del Sprint")
pointstitulo_label.pack()
points_label = Label(root,text="")
points_label.pack()

##### add data button #####
mkchrt_button = Button(root,text="Agregar las fechas y los puntos del Sprint", command=mkpoints)
mkchrt_button.pack(pady=20)

##### make perfect work button #####
ideal_work_button = Button(root,text="Seleccionar dia de trabajo", command=mkidealwk)
ideal_work_button.pack(pady=10)

##### make chart button #####
mkchrt_button = Button(root,text="Crear el grafico", command=mkchrt)
mkchrt_button.pack(pady=20)

##### exit button #####
mkchrt_button = Button(root,text="Salir", command=quit)
mkchrt_button.pack(pady=20)

root.mainloop()