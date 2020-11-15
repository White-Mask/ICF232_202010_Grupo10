from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import tkinter.font as tkFont
import requests
import ejemplo2


class Login:
    def __init__(self):
        self.loginWindow = Tk()
        self.loginWindow.title("Login with Python")

        #Screen size
        #self.loginWindow.geometry("%dx%d+0+0" % (self.loginWindow.winfo_screenwidth(), self.loginWindow.winfo_screenheight()))
        self.loginWindow.attributes("-fullscreen",True)

        #Background
        self.frameBackground = Frame(self.loginWindow,bg="white")
        self.frameBackground.pack(fill=BOTH,expand=True)

        self.imageLogin = PhotoImage(file="cross-background.png")
        self.labelImageLogin = Label(self.frameBackground,image=self.imageLogin)
        self.labelImageLogin.pack(fill=BOTH,expand=True)

        self.frameLogin = Frame(self.frameBackground, width=400, height=500, bg="white", relief="groove")
        self.frameLogin.place(anchor="c", relx=.5, rely=.5)


        #Titulo
        fontStyleTitle = tkFont.Font(size=50)
        self.label = Label(self.frameLogin, text="Login", font=fontStyleTitle ,bg="white")
        self.label.place(anchor="c", relx=.5, rely=0.15)

        #Entradas

        fontStyleLogin = tkFont.Font(size=15)
        Label(self.frameLogin,text='USERNAME', bg="white" , font=fontStyleLogin).place(anchor="c", relx=.5, rely=.35)
        self.usernameE = Entry(self.frameLogin, relief="solid")
        self.usernameE.place(anchor="c", relx=.5, rely=.45, relwidth=0.5,relheight=0.07)

        Label(self.frameLogin,text='PASSWORD', bg="white" , font=fontStyleLogin).place(anchor="c", relx=.5, rely=.55)
        self.passwordE = Entry(self.frameLogin, show="*", relief="solid")
        self.passwordE.place(anchor="c", relx=.5, rely=.65, relwidth=0.5,relheight=0.07)

        #Boton
        self.submit = Button(self.frameLogin, text="Submit", bg="white", relief="groove" ,command=self.validate)
        self.submit.place(anchor="c", relx=.5, rely=.85, relwidth=0.4,relheight=0.1)
        
    def validate(self):
        URL= "http://127.0.0.1:8000/"
        data = {
            "username": self.usernameE.get(),
            "password": self.passwordE.get()
        }
        try:
            response = requests.post(URL+'api-token-auth/', data=data)
            #print(response.text) Token
            if response.ok:
                messagebox.showinfo("Successful", "Login Was Successful")
                self.loginWindow.destroy()
                ejemplo2.main()
            else:
                messagebox.showerror("Error", "Wrong Credentials")
        except IndexError:
            messagebox.showerror("Error", "Wrong Credentials")

    def run(self):
        self.loginWindow.mainloop()

def mainlogin():
    LoginTK = Login()
    LoginTK.run()

if __name__ == '__main__':
    mainlogin()