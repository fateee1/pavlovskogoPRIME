import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Файл для хранения расходов
FILENAME = 'expenses.json'


# Функция для загрузки расходов из файла
def load_expenses():
    try:
        with open(FILENAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Функция для сохранения расходов в файл
def save_expenses(expenses):
    with open(FILENAME, 'w') as f:
        json.dump(expenses, f)


# Функция для добавления расхода
def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()

    # Проверка корректности ввода
    validation_message = validate_input(amount, date)
    if validation_message != True:
        messagebox.showerror("Ошибка", validation_message)
        return

    # Добавление расхода
    expenses.append({
        'amount': float(amount),
        'category': category,
        'date': date
    })

    save_expenses(expenses)
    amount_entry.delete(0, tk.END)
    category_entry.set('')
    date_entry.delete(0, tk.END)

    update_expense_list()


# Функция для валидации ввода
def validate_input(amount, date):
    try:
        if float(amount) <= 0:
            return "Сумма должна быть положительным числом."
        # Проверка формата даты
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return "Дата должна быть в формате YYYY-MM-DD."


# Функция для обновления списка расходов
def update_expense_list():
    expense_list.delete(0, tk.END)
    for expense in expenses:
        expense_list.insert(tk.END, f"{expense['date']} - {expense['category']}: {expense['amount']}")


# Инициализация основного окна
root = tk.Tk()
root.title("Expense Tracker")

# Поля ввода
tk.Label(root, text="Сумма").grid(row=0, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1)

tk.Label(root, text="Категория").grid(row=1, column=0)
category_entry = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения"])
category_entry.grid(row=1, column=1)

tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1)

# Кнопка для добавления расхода
tk.Button(root, text="Добавить расход", command=add_expense).grid(row=3, column=0, columnspan=2)

# Список для отображения расходов
tk.Label(root, text="Список расходов:").grid(row=4, column=0, columnspan=2)
expense_list = tk.Listbox(root, width=50)
expense_list.grid(row=5, column=0, columnspan=2)

# Загрузка существующих расходов
expenses = load_expenses()
update_expense_list()

# Запуск приложения
root.mainloop()