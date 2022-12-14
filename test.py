"""
Creates a MongoDB database
"""
import tkinter as tk
from tkinter import font, ttk
from pymongo import MongoClient

# pylint: disable=C0103
# pylint: disable=W0603
def into_dict(dic):
    """Insert into dictionary"""
    new_dic = {}
    for new_key, new_value in dic.items():
        if isinstance(new_value, dict):
            first = []
            second = []
            third = []
            min_size = 18000000
            for new_i, new_j in new_value.items():
                second.append(new_j)
                third.append(new_i)
                if len(new_j) < min_size:
                    min_size = len(new_j)
            for place in range(min_size):
                dictionary = {}
                for r in range(len(second)):
                    dictionary.update({third[r]: second[r][place]})
                first.append(dictionary)
            new_dic.update({new_key: first})
        else:
            new_dic.update({new_key: new_value})
    return new_dic

def remember_element():
    """Remember element from database"""
    key = key_name.get().split('.')
    element = list(filter(None, element_name.get(1.0, tk.END).split('\n')))
    if len(key) > 1:
        saved_document[key[0]][key[1]] = element
    else:
        if isinstance(saved_document[key[0]], list):
            saved_document[key[0]] = element
        else:
            if not element:
                element = ['']
            saved_document[key[0]] = element[0]
    string_for_inserting = str(into_dict(saved_document))
    out.configure(state=tk.NORMAL)
    out.delete('1.0', tk.END)
    out.insert(1.0, string_for_inserting)
    out.configure(state=tk.DISABLED)


def task():
    """Check where we are"""
    global check_doc_point
    global check_kol_point
    global saved_document
    global team_list

    if key_name.get() != check_doc_point:
        check_doc_point = key_name.get()
        key_assignment = check_doc_point.split('.')
        if len(key_assignment) > 1:
            text = saved_document[key_assignment[0]][key_assignment[1]]
        else:
            text = saved_document[key_assignment[0]]
        if isinstance(text, list):
            text = '\n'.join(text)
            if text != '':
                text = text + '\n'
        element_name.delete('1.0', tk.END)
        element_name.insert(1.0, text)

    if kol_name.get() != check_kol_point:
        if kol_name.get() == 'Футбольные_команды':
            check_kol_point = 'Футбольные_команды'
            saved_document = {"Название": "", "Город": "",
            "ФИО тренера": "", "Стартовый состав игроков": {"ФИО": [],
            "Позиция": []}, "Запасные игроки": []}

            team_list = []
            for k, v in saved_document.items():
                if isinstance(v, dict):
                    for tuple_v in v.items():
                        team_list.append(k + '.' + tuple_v[0])
                else:
                    team_list.append(k)
            check_doc_point = ''
            key_name.configure(values=team_list)
            key_name.current(newindex=0)
            element_name.delete('1.0', tk.END)
            out.configure(state=tk.NORMAL)
            out.delete('1.0', tk.END)
            out.configure(state=tk.DISABLED)

        if kol_name.get() == 'Игры':
            check_kol_point = 'Игры'
            saved_document = {'Дата проведения': '', 'Счет': '',
            'Нарушения правил': {'Цвет карточки': [], 'Кому выдана': [],
            'На какой минуте выдана': [], 'За что': []}, 'Забитые мячи':
            {'С какого положения забит': [], 'Минута': [],  'Автор': [],
            'Передача': []},'Пенальти ': {'С какого положения забит': [], 'Минута': [],
            'Автор': [], 'Передача': []}, 'Количество ударов по воротам':
            {'С какого положения забит': [], 'Минута': [], 'Автор': [], 'Передача': []}
                              }

            team_list = []
            for k, v in saved_document.items():
                if isinstance(v, dict):
                    for tuple_v in v.items():
                        team_list.append(k + '.' + tuple_v[0])
                else:
                    team_list.append(k)
            check_doc_point = ''
            key_name.configure(values=team_list)
            key_name.current(newindex=0)
            element_name.delete('1.0', tk.END)
            out.configure(state=tk.NORMAL)
            out.delete('1.0', tk.END)
            out.configure(state=tk.DISABLED)
    window.after(200, task)

# Show collected strings
def show_collection():
    a = ''
    i = 1
    for e in db[check_kol_point].find({}, {"_id": 0}):
        a = a + str(i) + ' документ: ' + str(e) + '\n'
        i = i + 1
    out.configure(state=tk.NORMAL)
    out.delete('1.0', tk.END)
    out.insert(1.0, a)
    out.configure(state=tk.DISABLED)

def save_document():
    """Save database in a document"""
    global saved_document
    global check_kol_point
    print(into_dict(saved_document))
    db[check_kol_point].insert_one(into_dict(saved_document))
    element_name.delete('1.0', tk.END)
    if check_kol_point == 'Футбольные_команды':
        saved_document = {"Название": "", "Город": "", "ФИО тренера": "",
        "Стартовый состав игроков": {"ФИО": [], "Позиция": []},
        "Запасные игроки": []}
    if check_kol_point == 'Игры':
        saved_document = {'Дата проведения': '', 'Счет': '',
        'Нарушения правил': {'Цвет карточки': [], 'Кому выдана': [],
        'На какой минуте выдана': [], 'За что': []},
        'Забитые мячи': {'С какого положения забит': [], 'Минута': [],
        'Автор': [], 'Передача': []}, 'Пенальти ': {'С какого положения забит': [], 'Минута': [],
         'Автор': [], 'Передача': []}, 'Количество ударов по воротам':
        {'С какого положения забит': [], 'Минута': [], 'Автор': [], 'Передача': []}
        }
    show_collection()

client = MongoClient("localhost", 27017)

db = client["polikarp"]
print(str(db))
collection_team = db["Футбольные_команды"]
print(collection_team)
collection_match = db["Игры"]
databases = client.list_database_names()


window = tk.Tk()
window.title("СУБД MongoDB 1")
window.geometry("1225x500")

saved_document = {}

team_list = []

check_doc_point = ''

check_kol_point = ''

kol_name = ttk.Combobox(window, values=['Футбольные_команды', 'Игры'], state="readonly")
kol_name.current(newindex=0)
kol_name.place(x=20, y=20, width=250)

key_name = ttk.Combobox(window, values=team_list, state="readonly")
key_name.place(x=20, y=60, width=250)

element_name = tk.Text(window)
ysb = tk.Scrollbar(window)
ysb.configure(command=element_name.yview)
element_name.configure(yscrollcommand=ysb.set, font=font.nametofont("TkDefaultFont"))
element_name.place(x=300, y=20, height=100, width=200)
ysb.place(x=500, y=20, height=100)

button_add_element = tk.Button(window, text="Добавить ключ-значение", command=remember_element)
button_add_element.place(x=550, y=20, width=150)

button_show_collection = tk.Button(window, text="Показать документы", command=show_collection)
button_show_collection.place(x=550, y=90, width=150)

button_save_document = tk.Button(window, text="Сохранить документ", command=save_document)
button_save_document.place(x=550, y=55, width=150)

out = tk.Text(window)
out.configure(state=tk.DISABLED)
out.place(x=20, y=130, height=350, width=1190)

window.after(200, task)

window.mainloop()

client.close()