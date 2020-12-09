from tkinter import *
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter import Scrollbar
import pydicom as dicom
import PIL.Image
import PIL.ImageTk
import numpy as np
import os
import tree
import cv2

class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.image = None
        self.photo = None
        self.canvas = None
        self.imager = None

        self.status = None
        self.right_click_menu = None

        self.mouse_wheel_down = False
        self.last_mouse_pos = None

        self.frame3 = None
        
        self.flagRotate = 0
        self.color = None

        self.dir = None

        self.init_ui()

    def init_ui(self):
        self.parent.title("SigVip")
        
        self.init_toolbar()

        self.frame3 = Frame(self.parent, width = 500, height = 500)
        self.frame3.pack(fill="none", expand=True)

        self.frame3.pack_propagate(0)


        # Image canvas
        self.canvas = Canvas(self.frame3, bd=0, highlightthickness=0)
        self.canvas.pack(side=TOP, expand=1)
        self.canvas.bind("<MouseWheel>", self.scroll_images)
        self.canvas.bind("<B2-Motion>", self.on_mouse_wheel_drag)
        self.canvas.bind("<Button-2>", self.on_mouse_wheel_down)
        self.canvas.bind("<ButtonRelease-2>", self.on_mouse_wheel_up)
        #self.canvas.bind("<Configure>", self.resize)

        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        
        #Default size
        self.scale = 100

        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, 1000, 1000, width=0)

        self.bottomFrame  = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.bottomFrame.pack(expand=True)


        #Label(self.parent,text='0 %').pack()
        self.photozoomin = PhotoImage(file = r"C:\\Users\\Fernando Martinez\\Desktop\\Desktop SigVip Project\\zoom-in.png") 
        self.button = Button(self.bottomFrame,text='+',image=self.photozoomin,command= self.zoomup)
        self.button.pack(side=LEFT,fill=BOTH, expand=True)

        #Label(self.parent,text='50 %').pack()
        self.photozoomout = PhotoImage(file = r"C:\\Users\\Fernando Martinez\\Desktop\\Desktop SigVip Project\\zoom-out-lens.png") 
        self.button = Button(self.bottomFrame,text='-',image=self.photozoomout,command= self.zoomdown)
        self.button.pack(side=LEFT,fill=BOTH, expand=True)
        self.rotateleft = PhotoImage(file = r"C:\\Users\\Fernando Martinez\\Desktop\\Desktop SigVip Project\\reload.png") 
        self.button = Button(self.bottomFrame,text='Izquierda',image=self.rotateleft,command= self.rotar_Imagen_der)
        self.button.pack(side=LEFT,fill=BOTH, expand=True)

        #Label(self.parent,text='50 %').pack()
        self.rotateright = PhotoImage(file = r"C:\\Users\\Fernando Martinez\\Desktop\\Desktop SigVip Project\\rotating-arrow-to-the-right.png") 
        self.button = Button(self.bottomFrame,text='Derecha',image=self.rotateright,command= self.rotar_Imagen_izq)
        self.button.pack(side=LEFT,fill=BOTH, expand=True)

        #Label(self.parent,text='color 1').pack()
        self.button = Button(self.bottomFrame,width=20,text='Gris', command= lambda: self.colormap(cv2.COLOR_RGB2BGRA))
        self.button.pack(side=LEFT,fill=BOTH, expand=True)

        #Label(self.parent,text='color 2').pack()
        self.button = Button(self.bottomFrame,width=20,text='Rosado', command= lambda: self.colormap(cv2.COLOR_RGB2Luv))
        self.button.pack(side=LEFT,fill=BOTH, expand=True)
        #Label(self.parent,text='color 3').pack()
        self.button = Button(self.bottomFrame,width=20,text='Verde', command= lambda: self.colormap(cv2.COLOR_RGB2HLS))
        self.button.pack(side=LEFT,fill=BOTH, expand=True)
        #Data
        self.gg = LabelFrame(self.parent, bd=0, highlightthickness=0)
        self.gg.pack(side=BOTTOM)
        
        self.status = StatusBar(self.parent)
        self.status.pack(side=BOTTOM, fill=X)

    def init_toolbar(self):
        menubar = Menu(self.parent, bd=0)
        self.parent.config(menu=menubar, bd=0)

        filemenu = Menu(menubar, tearoff=False, bd=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open File...", accelerator = 'Control-o', command=self.on_open)
        filemenu.add_command(label="Open Folder...", accelerator = 'Control-k', command=self.open_dir)
        filemenu.add_command(label="Close File", accelerator = 'Control-w', command=self.close_image)

        self.parent.bind_all('<Control-o>', self.on_open)
        self.parent.bind_all('<Control-k>', self.open_dir)
        self.parent.bind_all('<Control-w>', self.close_image)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)

        opciones = Menu(menubar, tearoff=False, bd=0)
        menubar.add_cascade(label="Opciones", menu=opciones)
        opciones.add_command(label="info imagen", command=self.get_imagen_info)

    def get_imagen_info(self):
        try:
            tree.main(self.imager.image_info())
        except:
            pass           

    def show_image(self, numpy_array):
        if numpy_array is None:
            return

        width = int(numpy_array.shape[1]*self.scale/100)
        heigth = int(numpy_array.shape[0]*self.scale/100)
        dim = (width,heigth)
        resized = cv2.resize(numpy_array,dim,interpolation=cv2.INTER_AREA)

        if self.color == None:
            img = resized
        else:
            img = cv2.cvtColor(resized, self.color)

        #if self.image is None:
        #    return
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        
        # get visible area of the canvas
        bbox2 = (self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.canvasx(self.canvas.winfo_width()), self.canvas.canvasy(self.canvas.winfo_height()))
        
        # get scroll region box
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]), max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]

        self.image = PIL.Image.fromarray(img)
        self.photo = PIL.ImageTk.PhotoImage(self.image.rotate(self.flagRotate) )
        self.canvas.delete("IMG")
        self.canvas.create_image(self.frame3.winfo_width()/2, self.frame3.winfo_height()/2, image=self.photo, anchor=CENTER, tags="IMG")
        self.canvas.configure(width=self.frame3.winfo_width(), height=self.frame3.winfo_height())


        #width = max(self.parent.winfo_width(), self.image.width)
        #height = max(self.parent.winfo_height(), self.image.height + StatusBar.height)

        #newsize = "{}x{}".format(width, height)
        #self.parent.geometry(newsize)
        #self.parent.minsize(self.image.width, self.image.height + StatusBar.height)

    def close_image(self,event=None):
        #self.canvas.delete('all')

        self.flagRotate += 90
        if self.flagRotate == 360:
            self.flagRotate = 0

        return self.show_image(self.imager.get_current_image())


    def rotar_Imagen_der(self):

        self.flagRotate += 90
        if self.flagRotate == 360:
            self.flagRotate = 0

        return self.show_image(self.imager.get_current_image())

    def rotar_Imagen_izq(self):

        self.flagRotate -= 90
        if self.flagRotate == -360:
            self.flagRotate = 0

        return self.show_image(self.imager.get_current_image())

    def zoomup(self):
        self.scale += 50
        self.show_image(self.imager.get_current_image())

    def zoomdown(self):
        self.scale -= 50
        self.show_image(self.imager.get_current_image())

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image(self.imager.get_current_image())

    def resize(self, event):
        if self.image is None:
            return

    def colormap(self,pickedColor):
        self.color = pickedColor
        return self.show_image(self.imager.get_current_image())

    def scroll_images(self, e):
        self.imager.index += int(e.delta/120)
        self.show_image(self.imager.get_current_image())

    def on_mouse_wheel_down(self, e):
        self.last_mouse_pos = (e.x, e.y)
        self.mouse_wheel_down = True

    def on_mouse_wheel_up(self, e):
        self.last_mouse_pos = None
        self.mouse_wheel_down = True

    def on_mouse_wheel_drag(self, e):
        if self.mouse_wheel_down:
            delta = (e.x - self.last_mouse_pos[0], e.y - self.last_mouse_pos[1])
            self.last_mouse_pos = (e.x, e.y)

            self.imager.window_width += delta[0] * 5
            self.imager.window_center += delta[1] * 5

            self.show_image(self.imager.get_current_image())

    def on_open(self,event = None):
        try:
            filenames = askopenfilenames(filetypes=(("DICOM files", "*.dcm"),("All files", "*.*")))

            datasets = []
            for file in filenames:
                try:
                    datasets.append(dicom.read_file(file))
                except dicom.errors.InvalidDicomError:
                    num_bad += 1
                    filenames.remove(file)

            self.imager = Imager(datasets)
            self.show_image(self.imager.get_current_image())
        except:
            pass

    def open_dir(self,event = None):
        try:
            f = askdirectory()

            os.chdir(f)
            dirpath = os.path.basename(os.getcwd())
            current_image = dirpath

            datasets = []
            for filenames in os.listdir(os.curdir):
                try:
                    datasets.append(dicom.read_file(filenames))
                except dicom.errors.InvalidDicomError:
                    num_bad += 1
                    filenames.remove(filenames)

            sorted_method = "filenames"
            try:
                datasets.sort(key=lambda x: x.InstanceNumber)
                sorted_method = "instance number"
            except AttributeError:
                try:
                    datasets.sort(key=lambda x: x.SOPInstanceUID)
                    sorted_method = "SOP instance UID"
                except AttributeError:
                    pass

            self.imager = Imager(datasets)
            self.show_image(self.imager.get_current_image())
        except:
            pass

    def on_exit(self):
        self.quit()

class Imager:
    def __init__(self, datasets):
        self.datasets = datasets
        self._index = 0
        self._window_width = 300
        self._window_center = 0

        self.size = (int(datasets[0].Rows), int(datasets[0].Columns), len(datasets))
        self.spacings = (float(datasets[0].PixelSpacing[0]),
                         float(datasets[0].PixelSpacing[1]),
                         float(datasets[0].SliceThickness))

        self.axes = (np.arange(0.0, (self.size[0] + 1) * self.spacings[0], self.spacings[0]),
                     np.arange(0.0, (self.size[2] + 1) * self.spacings[2], self.spacings[2]),
                     np.arange(0.0, (self.size[1] + 1) * self.spacings[1], self.spacings[1]))

        self.values = np.zeros(self.size, dtype='int16')
        for i, d in enumerate(datasets):
            np.copyto(self.values[:, :, i], d.RescaleSlope * np.flipud(d.pixel_array) + d.RescaleIntercept, 'unsafe')

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):

        while value < 0:
            value += self.size[2]

        self._index = value % self.size[2]

    @property
    def window_width(self):
        return self._window_width

    @window_width.setter
    def window_width(self, value):
        self._window_width = max(value, 1)

    @property
    def window_center(self):
        return self._window_center

    @window_center.setter
    def window_center(self, value):
        self._window_center = value

    def get_image(self, index):
        img = self.values[:, :, index]

        w_left = (self._window_center - self._window_width / 2)
        w_right = (self._window_center + self._window_width / 2)
        mask_0 = img < w_left
        mask_1 = img > w_right
        mask_2 = np.invert(mask_0 + mask_1)

        res = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        res[:, :, 0] = res[:, :, 1] = res[:, :, 2] = \
            mask_0 * 0 + mask_1 * 255 + mask_2 * (255 * (img - w_left) / (w_right - w_left))

        return res

    def get_current_image(self):
        return self.get_image(self.index)

    def image_info(self):
        return self.datasets[self.index]

class StatusBar(Frame):
    height = 19

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=BOTH)

    def set(self, format_str, *args):
        self.label.config(text=format_str % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def main():
    root = Tk()
    root.minsize(1000, 600)
    root.geometry("1000x600+150+25")
    root.iconbitmap('img/favicon_96.ico')
    app = MainWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()