import sys
import pydicom
import main_copia
import tkinter.tix as tkinter_tix

class Tree:
    def __init__(self,imagen):
        self.root = tkinter_tix.Tk()
        self.root.geometry("{0:d}x{1:d}+{2:d}+{3:d}".format(1200, 900, 0, 0))
        self.root.title("DICOM tree viewer")

        self.RunTree(self.root, imagen)

    def RunTree(self ,w, filename):
        top = tkinter_tix.Frame(w, relief=tkinter_tix.RAISED, bd=1)
        tree = tkinter_tix.Tree(top, options="hlist.columns 2")
        tree.pack(expand=1, fill=tkinter_tix.BOTH, padx=10, pady=10,
                side=tkinter_tix.LEFT)
        # print(tree.hlist.keys())   # use to see the available configure() options
        tree.hlist.configure(bg='white', font='Courier 10', indent=30)
        tree.hlist.configure(selectbackground='light yellow', gap=150)

        box = tkinter_tix.ButtonBox(w, orientation=tkinter_tix.HORIZONTAL)
        # box.add('ok', text='Ok', underline=0, command=w.destroy, width=6)
        box.add('exit', text='Exit', underline=0, command=w.destroy, width=6)
        box.pack(side=tkinter_tix.BOTTOM, fill=tkinter_tix.X)
        top.pack(side=tkinter_tix.TOP, fill=tkinter_tix.BOTH, expand=1)
        # https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
        tree.bind_all('<MouseWheel>', lambda event:  # Wheel in Windows
                    tree.hlist.yview_scroll(int(-1 * event.delta / 120.),
                                            "units"))
        tree.bind_all('<Button-4>', lambda event:  # Wheel up in Linux
                    tree.hlist.yview_scroll(int(-1), "units"))
        tree.bind_all('<Button-5>', lambda event:  # Wheel down in Linux
                    tree.hlist.yview_scroll(int(+1), "units"))

        self.show_file(filename, tree)


    def show_file(self ,filename, tree):
        tree.hlist.add("root", text='Imagen DICOM - '+str(filename.PatientName))
        #ds = pydicom.dcmread(numpy_array)
        filename.decode()  # change strings to unicode
        self.recurse_tree(tree, filename, "root", False)
        tree.autosetmode()


    def recurse_tree(self ,tree, dataset, parent, hide=False):
        # order the dicom tags
        for data_element in dataset:
            node_id = parent + "." + hex(id(data_element))
            if isinstance(data_element.value, str):
                tree.hlist.add(node_id, text=str(data_element))
            else:
                tree.hlist.add(node_id, text=str(data_element))
            if hide:
                tree.hlist.hide_entry(node_id)
            if data_element.VR == "SQ":  # a sequence
                for i, dataset in enumerate(data_element.value):
                    item_id = node_id + "." + str(i + 1)
                    sq_item_description = data_element.name.replace(
                        " Sequence", "")  # XXX not i18n
                    item_text = "{0:s} {1:d}".format(sq_item_description, i + 1)
                    tree.hlist.add(item_id, text=item_text)
                    tree.hlist.hide_entry(item_id)
                    self.recurse_tree(tree, dataset, item_id, hide=True)

    def run(self):
        self.root.mainloop()

def main(imagen):
    main = Tree(imagen)
    main.run()