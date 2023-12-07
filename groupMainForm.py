import selector
import os

from tkinter import *
from tkinter import ttk

from tkinter.ttk import Combobox

class MainForm:
    # pass
    def __init__(self):
        # Список названий вариаций генетического алгоритма
        self.__GA_algorithms_name_list = [
            'Genetic Algorithm',
            'Genetic Algorithm Genitor',
            'Genetic Algorithm Punctuated Equilibrium',
            'Genetic Algorithm Unfixed Population Size']

        # Соответствующие индексы названиям генетическим алгоритмам
        self.__GA_algorithms_index = [
            0,
            1, 
            2,
            3
        ]
        
        # Лист возможных количеств возможных итераций
        self.__GA_possible_try_list = [i for i in range(1, 16)]

        # Сущность исходных данных Генетических алгоритмов
        self.__GA_init_data = selector.Data()

        # Сущность решателя Генетически алгоритмом
        self.__GA_solver = selector.Solver(data = self.__GA_init_data)

        # Главное окно
        self.mainWindow = Tk()
        
        # Состояние Флага ЛОГИРОВАНИЕ РЕШЕНИЯ В КОНСОЛЬ
        self.__var_logger_flag = IntVar()
        self.__var_logger_flag.set(0)

        # Имя файла для сохранения решения
        self.__output_file_path = StringVar()
        self.__output_file_path.set("{}\Output.xlsx".format(os.path.dirname(__file__)))

        # Переменная хранения состояния кнопки "Решить"
        self.__solve_button_state = 'normal'

        # Настройка главного окна
        self.mainWindow.title('Приложение подбора проектных групп')
        self.mainWindow.geometry("450x250")
        self.mainWindow.resizable(False, False)
        # self.mainWindow.iconbitmap(default="favicon.ico")
    
        # Кнопка "Рассчитать"
        self.__solve_button = ttk.Button(
            self.mainWindow, 
            text = "Рассчитать", 
            command = self.__solve_button_push,
            state = self.__solve_button_state
        )

        # Выпадающий список генетических алгоритмов
        self.__GA_selection_combobox = Combobox(
            self.mainWindow,
            state="readonly", 
            textvariable = self.__GA_algorithms_index, 
            values = self.__GA_algorithms_name_list
        )
        self.__GA_selection_combobox.current(0)

        # Выпадающий список количества возможных итераций решения
        self.__GA_try_selection_combobox = Combobox(
            self.mainWindow,
            state="readonly",
            textvariable = self.__GA_possible_try_list,
            values = self.__GA_possible_try_list
        )
        self.__GA_try_selection_combobox.current(0)

        # Чекбокс флага логирования
        self.__logger_check = ttk.Checkbutton(
            variable=self.__var_logger_flag,
            onvalue=1, 
            offvalue=0,
            text="Логирование в консоль")

        # Поле ввода пути сохранения файла
        self.__output_file_path_entry = Entry(
            textvariable = self.__output_file_path
        )

        #
        self.__label_ga_selection_combobox = Label(text="Генетический алгоритм для решения")
        self.__label_try_selection_combobox = Label(text="Количество попыток подсчета")
        self.__label_output_entry = Label(text="Путь сохранения результата")

        # Отображение элементов интерфейса 
        self.__label_ga_selection_combobox.grid()
        self.__GA_selection_combobox.grid()                     # TODO: Положение  элементов
        self.__label_try_selection_combobox.grid()
        self.__GA_try_selection_combobox.grid()                 # TODO: Положение  элементов
        self.__logger_check.grid()                              # TODO: Положение  элементов
        self.__solve_button.grid()                              # TODO: Положение  элементов

        self.__label_output_entry.grid()
        self.__output_file_path_entry.grid()

    # Событие нажатие кнопки "Решить"
    def __solve_button_push(self):

        if self.__var_logger_flag.get() == 1:
            self.__GA_solver.enable_logger()
 
        self.__GA_solver.set_try_count(self.__GA_try_selection_combobox.get())
        self.__GA_solver.set_output_file_name(self.__output_file_path.get())
        self.__solve_button_state = 'disabled'
        self.__GA_solver.solve()
        self.__solve_button_state = 'normal'


        # print(self.__var_logger_flag.get())
        # print(self.__GA_selection_combobox.get())
        # print(self.__GA_iter_selection_combobox.get())
        # print(self.__output_file_path.get())
    