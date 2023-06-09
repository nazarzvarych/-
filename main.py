from tkinter import *  # вікно
from tkinter import filedialog as fd  # для шляху до файла
from tkinter import messagebox as mb  # для повідомлень
from tkinter.ttk import Notebook  # для відкривання картинок
from PIL import Image, ImageTk, ImageOps, ImageFilter  # для фото
import os  # для витягання шляху


class PyPhotoEditor:  # фоторедактор основа
    def __init__(self):
        self.root = Tk()
        self.image_tabs = Notebook(self.root)  # мотод для роботи із вкладками
        self.opened_images = []  # список для відкритих зображень

        self.init()

    def init(self):
        self.root.title("PNTL PHOTOSHOP")  # Ім'я додатка

        self.image_tabs.enable_traversal()  # для переключення між вкладками

        self.root.bind("<Escape>", self._close)  # вихід на кнопку

    def run(self):
        self.draw_menu()  # додавання верхного status bar'а
        self.draw_widgets()

        self.root.mainloop()  # безкінечнний цикл

    def draw_menu(self):
        menu_bar = Menu(self.root)  # налаштування  statushlhbar'а

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_new_images)  # додавання зображення для редактування
        file_menu.add_command(label="Save as", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._close)
        menu_bar.add_cascade(label="File", menu=file_menu)


        edit_menu = Menu(menu_bar, tearoff=0)
        transform_menu = Menu(edit_menu, tearoff=0)


        rotate_menu = Menu(transform_menu, tearoff=0)
        rotate_menu.add_command(label="Rotate left by 90", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Rotate right by 90", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Rotate left by 180", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Rotate right by 180", command=lambda: self.rotate_current_image(-180))
        transform_menu.add_cascade(label="Rotate", menu=rotate_menu)

        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="Flip horizontally", command=lambda: self.flip_current_image("horizontally"))
        flip_menu.add_command(label="Flip vertically", command=lambda: self.flip_current_image("vertically"))

        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Blur", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR)) #розмиття
        filter_menu.add_command(label="Sharpen",command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN)) #підвищення контрасності
        filter_menu.add_command(label="Contour",command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))#контрасність контура
        filter_menu.add_command(label="Detail", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))#розмиття деталей
        filter_menu.add_command(label="Smooth", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))#розмитість



        edit_menu.add_cascade(label="Transform", menu=transform_menu)
        edit_menu.add_cascade(label="Flip", menu=flip_menu)
        edit_menu.add_cascade(label="Filter", menu=filter_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.configure(menu=menu_bar)

    def draw_widgets(self):
        self.image_tabs.pack(fill="both", expand=1)

    def open_new_images(self):
        image_paths = fd.askopenfilenames(
            filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))  # додвання користувачем зображення
        for image_path in image_paths:
            self.add_new_image(image_path)

    def add_new_image(self, image_path):  # для відкриття багатьох картинок за раз
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.opened_images.append([image_path, image])

        image_tab = Frame(self.image_tabs)

        image_label = Label(image_tab, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="bottom", fill="both", expand="yes")

        self.image_tabs.add(image_tab, text=image_path.split('/')[-1])
        self.image_tabs.select(image_tab)
    def get_current_working_data(self):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return None, None, None
        tab_number = self.image_tabs.index(current_tab)
        path, image = self.opened_images[tab_number]

        return current_tab, path, image

    def save_current_image(self):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        path, image = self.opened_images[tab_number]
        if path[-1] == '*':
            path = path[:-1]
            self.opened_images[tab_number][0] = path
            image.save(path)
            self.image_tabs.add(current_tab, text=path.split('/')[-1])


    def save_image_as(self):  # зберігання картинок на пк
        current_tab = self.image_tabs.select()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        old_path, old_ext = os.path.splitext(self.opened_images[tab_number][0])
        if '*' in old_ext:
            old_ext = old_ext[:-1]
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))

        if not new_path:
            return

        new_path, new_ext = os.path.splitext(new_path)
        if not new_ext:  # перевіряє чи є якась вкладка
            new_ext = old_ext
        elif old_ext != new_ext:
            mb.showerror("error")
            return

        image = self.opened_images[tab_number][1]
        image.save(new_path + new_ext)
        image.close()

        del self.opened_images[tab_number]
        self.image_tabs.forget(current_tab)

        self.add_new_image(new_path + new_ext)

    def update_image_inside_app(self, current_tab,image):
        tab_number = self.image_tabs.index(current_tab)
        tab_frame = self.image_tabs.children[current_tab[current_tab.rfind('!'):]]
        label = tab_frame.children['!label']

        self.opened_images[tab_number][1] = image

        image_tk = ImageTk.PhotoImage(image)
        label.configure(image=image_tk)
        label.image = image_tk

        image_path = self.opened_images[tab_number][0]  # чи були зміни над зображенням
        if image_path[-1] != '*':
            image_path += '*'
            self.opened_images[tab_number][0] = image_path
            image_name = image_path.split('/')[-1]
            self.image_tabs.tab(current_tab, text=image_name)


    def rotate_current_image(self,degrees):#поворот зображення
        current_tab = self.image_tabs.select()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        image = self.opened_images[tab_number][1]
        image = image.rotate(degrees)

        self.update_image_inside_app(current_tab, image)

    def flip_current_image(self, flip_type):#відзеркалення зображення
        current_tab = self.image_tabs.select()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        image = self.opened_images[tab_number][1]
        if flip_type =="horizontally":#відзеркалити по горизонталі
           image = ImageOps.mirror(image)
        elif flip_type =="vertically":
            image = ImageOps.flip(image)
        self.update_image_inside_app(current_tab, image)

    def apply_filter_to_current_image(self, filter_type):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        image = image.filter(filter_type)
        self.update_image_inside_app(current_tab, image)

    def _close(self, event=None):
        self.root.quit()


if __name__ == "__main__":
    PyPhotoEditor().run()
