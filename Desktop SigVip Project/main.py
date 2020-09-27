from tkinter import *
from tkinter.filedialog import askopenfilenames, askdirectory
import pydicom as dicom
import PIL.Image
import PIL.ImageTk
import numpy as np
import os

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

        self.init_ui()

    def init_ui(self):
        self.parent.title("SigVip")
        
        self.init_toolbar()

        # Image canvas
        self.canvas = Canvas(self.parent, bd=0, highlightthickness=0)
        self.canvas.pack(side=TOP, expand=1)
        self.canvas.bind("<MouseWheel>", self.scroll_images)
        self.canvas.bind("<B2-Motion>", self.on_mouse_wheel_drag)
        self.canvas.bind("<Button-2>", self.on_mouse_wheel_down)
        self.canvas.bind("<ButtonRelease-2>", self.on_mouse_wheel_up)
        #  self.canvas.bind("<Configure>", self.resize)
        
        self.status = StatusBar(self.parent)
        self.status.pack(side=BOTTOM, fill=X)

    def init_toolbar(self):
        menubar = Menu(self.parent, bd=0)
        self.parent.config(menu=menubar, bd=0)

        filemenu = Menu(menubar, tearoff=False, bd=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open File...", command=self.on_open)
        filemenu.add_command(label="Open Folder...", command=self.open_dir)
        
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)

    def show_image(self, numpy_array):
        if numpy_array is None:
            return

        self.image = PIL.Image.fromarray(numpy_array)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.delete("IMG")
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW, tags="IMG")
        self.canvas.configure(width=self.image.width, height=self.image.height)

        width = max(self.parent.winfo_width(), self.image.width)
        height = max(self.parent.winfo_height(), self.image.height + StatusBar.height)

        newsize = "{}x{}".format(width, height)
        self.parent.geometry(newsize)
        self.parent.minsize(self.image.width, self.image.height + StatusBar.height)

    def resize(self, event):
        if self.image is None:
            return

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

    def on_open(self):
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

    def open_dir(self):
        f = askdirectory()

        os.chdir(f)
        dirpath = os.path.basename(os.getcwd())
        current_image = dirpath

        datasets = []
        for filenames in os.listdir(os.curdir):
            if filenames.__contains__(".dcm"):
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
        
    def on_exit(self):
        self.quit()

class Imager:
    def __init__(self, datasets):
        self.datasets = datasets
        self._index = 0
        self._window_width = 1
        self._window_center = 0

        self.size = (int(datasets[0].Rows), int(datasets[0].Columns), len(datasets))
        self.spacings = (float(datasets[0].PixelSpacing[0]),
                         float(datasets[0].PixelSpacing[1]),
                         float(datasets[0].SliceThickness))

        self.axes = (np.arange(0.0, (self.size[0] + 1) * self.spacings[0], self.spacings[0]),
                     np.arange(0.0, (self.size[2] + 1) * self.spacings[2], self.spacings[2]),
                     np.arange(0.0, (self.size[1] + 1) * self.spacings[1], self.spacings[1]))

        self.values = np.zeros(self.size, dtype='int32')
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
    root.geometry("600x400+150+25")
    root.iconbitmap('img/favicon_96.ico')
    app = MainWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()
