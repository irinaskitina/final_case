import json
import os
from datetime import datetime

# Блок ввода и проверки даты с помощью ИИ-ассистента
def input_date():
    """Запрашивает дату в формате ДД.ММ.ГГГГ с проверкой."""
    while True:
        date_str = input("Введите дату (ДД.ММ.ГГГГ): ").strip()
        try:
            task_date = datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            print("Ошибка: введите корректную дату (например, 25.12.2026).")
            continue

        if task_date.date() < datetime.now().date():
            print("Ошибка: дата не может быть в прошлом.")
            continue

        return date_str

# Порядок приоритетов: 
PRIORITY_ORDER = {"Высокий": 1, "Средний": 2, "Низкий": 3}

tasks = []

# Блок сохранения в JSON и отбраковка ошибок настроено при помощи ИИ
if os.path.exists('tasks.json'):
    try:
        with open('tasks.json', 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Внимание! Файл поврежден. Начинаем с пустого списка.")
        tasks = []
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")

def save_tasks():
    try:
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

# Блок основного меню и вспомогательные функции сортировки и фильтрации, основаны на рекомендациях ИИ
def filter_tasks(tasks, mode):
    """Фильтрует задачи: all, active или done."""
    if mode == "active":
        return [t for t in tasks if not t.get("done", False)]
    if mode == "done":
        return [t for t in tasks if t.get("done", False)]
    return list(tasks)

def task_deadline_key(task):
    """Сортировка по сроку. Без срока — в конец."""
    deadline = task.get("deadline")
    if not deadline:
        return datetime.max
    try:
        return datetime.strptime(deadline, "%d.%m.%Y")
    except ValueError:
        return datetime.max

def sort_tasks(tasks, mode):
    if mode == "deadline":
        return sorted(tasks, key=task_deadline_key)
    if mode == "priority":
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority"), 99))
    if mode == "status":
        return sorted(tasks, key=lambda t: t.get("done", False))
    return list(tasks)

def show_tasks(tasks):
    if not tasks:
        print("Список пуст!")
        return

    print("\n1. Все задачи\n2. Только активные\n3. Только выполненные")
    f_choice = input("Что показать? (1-3): ").strip()
    f_map = {"1": "all", "2": "active", "3": "done"}
    f_mode = f_map.get(f_choice, "all")
    if f_choice not in f_map:
        print("Неверный выбор, показываю все.")

    print("\nСортировка:\n1 - По сроку\n2 - По приоритету\n3 - По статусу\n4 - Без сортировки")
    s_choice = input("Ваш выбор (1-4): ").strip()
    s_map = {"1": "deadline", "2": "priority", "3": "status", "4": "none"}
    s_mode = s_map.get(s_choice, "none")
    if s_choice not in s_map:
        print("Неверный выбор сортировки.")

    result = sort_tasks(filter_tasks(tasks, f_mode), s_mode)
    
    print("\n ВАШИ ЗАДАЧИ ")
    if not result:
        print("Нет задач по вашему фильтру.")
        return

    for i, task in enumerate(result, start=1):
        status = "[x]" if task.get("done", False) else "[ ]"
        deadline = task.get("deadline", "—")
        print(f"{i}. {status} {task['title']} | Приоритет: {task['priority']} | Срок: {deadline}")

# Основной цикл программы
while True:
    print("\n МЕНЕДЖЕР ЗАДАЧ ")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Отметить задачу выполненной")
    print("4. Удалить")
    print("5. Выход")
    
    choice = input("Выберите действие (1-5): ").strip()
    
    if choice == "1": # Блок добавления задачи
        title = input("Введите название: ").strip()
        if not title:
            print("Ошибка: Название не может быть пустым!")
            continue
        description = input("Введите описание: ").strip()
        
        print("Выберите приоритет:\n1 - Высокий\n2 - Средний\n3 - Низкий")
        priority_choice = input("Ваш выбор (1-3): ")
        
        if priority_choice == "1":
            priority = "Высокий"
        elif priority_choice == "2":
            priority = "Средний"
        elif priority_choice == "3":
            priority = "Низкий"
        else:
            print("Ошибка! Введите 1, 2 или 3")
            continue
        
        deadline = input_date()
        
        new_task = {
            "title": title,
            "description": description,
            "priority": priority,
            "done": False,
            "deadline": deadline
        }
        
        tasks.append(new_task)
        save_tasks()
        print("Задача успешно добавлена!")

    # Блок демонстрации всех задач в менеджере
    elif choice == "2":
        show_tasks(tasks)

    elif choice == "3": # Блок отметки выполнения задачи
        if len(tasks) == 0:
            print("Список пуст, нечего отмечать.")
        else:
            print("\n- ВАШИ ЗАДАЧИ -")
            for i, task in enumerate(tasks, start=1):
                status = "[x]" if task.get("done", False) else "[ ]"
                print(f"{i}. {status} {task['title']}")
            
            try:
                num = int(input("Введите номер задачи: "))
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue
                
            if num < 1 or num > len(tasks):
                print("Ошибка: такой задачи нет!")
            else:
                tasks[num - 1]["done"] = True
                save_tasks()
                print(f"Задача №{num} выполнена!")

    elif choice == "4": # Блок удаления с подтверждением
        if len(tasks) == 0:
            print("Список пуст, нечего удалять.")
        else:
            print("\n- ВАШИ ЗАДАЧИ -")
            for i, task in enumerate(tasks, start=1):
                status = "[x]" if task.get("done", False) else "[ ]"
                print(f"{i}. {status} {task['title']}")
            
            try:
                num = int(input("Введите номер для удаления: "))
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue
                
            if num < 1 or num > len(tasks):
                print("Ошибка: такой задачи нет!")
            else:
                task_title = tasks[num - 1]['title']
                confirm = input(f"Удалить '{task_title}'? (да/нет): ")
                if confirm.lower() == "да":
                    tasks.pop(num - 1)
                    save_tasks()
                    print("Задача удалена.")
                else: 
                    print("Удаление отменено.")              

    elif choice == "5": # Блок выхода и сохранения
        save_tasks()
        print("Данные сохранены!")
        break