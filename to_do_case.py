import json
import os
from datetime import datetime #внедрение и проверка даты с помощью ИИ-ассистента
tasks = []
if os.path.exists('tasks.json'): # создание JSON для возможности сохранения при выходе из планировщика
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
def save_tasks():   # для сохранения после внесенных изменений
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)        

while True:
    print("\n--- МЕНЕДЖЕР ЗАДАЧ ---")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Отметить задачу выполненной")   # для отметки done
    print("4. Удалить")
    print("5. Выход")                       
    
    choice = input("Выберите действие (1-5): ")
    
    if choice == "1":
        title = input("Введите название: ")
        description = input("Введите описание: ")
        
        print("Выберите приоритет:")
        print("1 - Высокий")
        print("2 - Средний")
        print("3 - Низкий")
        
        priority_choice = input("Ваш выбор (1-3): ")
        
        if priority_choice == "1":
            priority = "Высокий"
        elif priority_choice == "2":
            priority = "Средний"
        elif priority_choice == "3":
            priority = "Низкий"
        else:
            print("Ошибка! Введите 1, 2 или 3")

        # Создание словаря уже с приоритетом
        new_task = {
            "title": title,
            "description": description,
            "priority": priority,
            "done": False
        }
        
        tasks.append(new_task)
        save_tasks ()
        print("Задача добавлена!")
    elif choice == "2":
        print("- ВАШИ ЗАДАЧИ -")
        if len(tasks) == 0:
            print("Список пуст!")
        else:
            for task in tasks:
                if task["done"] == True:
                    status = "[x]"
                else:
                    status = "[ ]"
                
                print(f"{status} Название: {task['title']} | Приоритет: {task['priority']}")
    elif choice == "3": # блок для отметки задачи
        if len(tasks) == 0:
            print("Список пуст, нечего отмечать.")
        else:
            num = int(input("Введите номер задачи для отметки: "))
            if num < 1 or num > len(tasks):
                print("Ошибка: задачи с таким номером не существует!")
            else:
                tasks[num - 1]["done"] = True
                save_tasks()
                print("Задача отмечена как выполненная!")
    elif choice == "4": #блок для удаления задачи
        if len(tasks) == 0:
            print ("Список пуст, нечего удалять.")
        else:
            num = int(input("Введите номер задачи для удаления: "))
            if num < 1 or num > len(tasks):
                print("Ошибка: задачи с таким номером не существует!")
            else:
                confirm = input("Вы уверены? (да/нет): ")
                if confirm.lower() == "да":
                    tasks.pop(num - 1)
                    save_tasks ()
                    print("Удалено")
                else: print("Удаление отменено")                
    elif choice == "5": # блок выхода и сохранения
        save_tasks ()
        print("Задачb сохранены!")
        break