import json
import os
from datetime import datetime 

# блок проверки даты с помощью ИИ-ассистента
def input_date():
    """Запрашивает дату в формате ДД.ММ.ГГГГ с проверкой."""
    while True:
        date_str = input("Введите дату (ДД.ММ.ГГГГ): ").strip()
        try:
            task_date = datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            print("Ошибка: введите корректную дату в формате ДД.ММ.ГГГГ (например, 25.12.2026).")
            continue

        if task_date.date() < datetime.now().date():
            print("Ошибка: дата не может быть в прошлом. Попробуйте снова.")
            continue

        return date_str

tasks = []
# Порядок приоритетов: чем меньше число, тем важнее
PRIORITY_ORDER = {"Высокий": 1, "Средний": 2, "Низкий": 3}

# блок сохранения в JSON при использовании ИИ
if os.path.exists('tasks.json'):
    try:
        with open('tasks.json', 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Внимание! Файл с задачами поврежден. Создан новый пустой список.")
        tasks = []
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла: {e}")

def save_tasks():
    try:
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

# блок основное меню
def filter_tasks(tasks, mode):
    """Фильтрует задачи: 'all' | 'active' | 'done'.
    Возвращает новый список, не меняя исходный."""
    if mode == "active":
        return [t for t in tasks if not t.get("done", False)]
    if mode == "done":
        return [t for t in tasks if t.get("done", False)]
    return list(tasks)


def task_deadline_key(task):
    """Ключ сортировки по сроку. Задачи без срока — в конец."""
    deadline = task.get("deadline")
    if not deadline:
        return datetime.max
    try:
        return datetime.strptime(deadline, "%d.%m.%Y")
    except ValueError:
        return datetime.max   # битая дата — тоже в конец


def sort_tasks(tasks, mode):
    """Сортирует задачи: 'deadline' | 'priority' | 'status' | 'none'.
    Возвращает новый список."""
    if mode == "deadline":
        return sorted(tasks, key=task_deadline_key)
    if mode == "priority":
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority"), 99))
    if mode == "status":
        # сначала активные (False → 0), потом выполненные (True → 1)
        return sorted(tasks, key=lambda t: t.get("done", False))
    return list(tasks)


def show_tasks(tasks):
    """Выводит задачи с учётом выбранной пользователем фильтрации и сортировки."""
    if not tasks:
        print("Список пуст!")
        return

    # --- выбор фильтра ---
    print("\n1. Показать все задачи")
    print("2. Только активные")
    print("3. Только выполненные")
    filter_choice = input("Что показать? (1-3): ").strip()
    filter_map = {"1": "all", "2": "active", "3": "done"}
    filter_mode = filter_map.get(filter_choice, "all")
    if filter_choice not in filter_map:
        print("Неверный выбор фильтра, показываю все задачи.")

    # --- выбор сортировки ---
    print("\nСортировка:")
    print("1 - По сроку")
    print("2 - По приоритету")
    print("3 - По статусу")
    print("4 - Без сортировки")
    sort_choice = input("Ваш выбор (1-4): ").strip()
    sort_map = {"1": "deadline", "2": "priority", "3": "status", "4": "none"}
    sort_mode = sort_map.get(sort_choice, "none")
    if sort_choice not in sort_map:
        print("Неверный выбор сортировки, оставляю исходный порядок.")

    # --- фильтр, затем сортировка ---
    result = sort_tasks(filter_tasks(tasks, filter_mode), sort_mode)

    # --- вывод ---
    print("\n- ВАШИ ЗАДАЧИ -")
    if not result:
        print("Нет задач, соответствующих фильтру.")
        return

    for i, task in enumerate(result, start=1):
        status = "[x]" if task.get("done", False) else "[ ]"
        deadline = task.get("deadline", "—")
        print(f"{i}. {status} Название: {task['title']} | "
              f"Приоритет: {task['priority']} | Срок: {deadline}")
while True:
    print("\n--- МЕНЕДЖЕР ЗАДАЧ ---")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Отметить задачу выполненной")
    print("4. Удалить")
    print("5. Выход")
    
    choice = input("Выберите действие (1-5): ")
    
    if choice == "1": # блок ввода задачи и пользовательский выбор приоритета
        title = input("Введите название: ").strip()
        if not title:
            print("Ошибка: Название задачи не может быть пустым!")
            continue
        description = input("Введите описание: ").strip()
        
        print("Выберите приоритет:\n1 - Высокий\n2 - Средний\n3 - Низкий")
        priority_choice = input("Ваш выбор (1-3): ")
        
        if priority_choice == "1": priority = "Высокий"
        elif priority_choice == "2": priority = "Средний"
        elif priority_choice == "3": priority = "Низкий"
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
        print("Задача добавлена!")

    # блок сортировки и фильтрации
    elif choice == "2":
        show_tasks(tasks)

    elif choice == "3": # блок отметки задачи по выполнению
        if len(tasks) == 0:
            print("Список пуст, нечего отмечать.")
        else:
            print(" ВАШИ ЗАДАЧИ ")
            for i, task in enumerate(tasks, start=1):
                status = "[x]" if task["done"] else "[ ]"
                print(f"{i}. {status} {task['title']}")
            
            try:
                num = int(input("Введите номер задачи для отметки: "))
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue
                
            if num < 1 or num > len(tasks):
                print("Ошибка: задачи с таким номером не существует!")
            else:
                tasks[num - 1]["done"] = True
                save_tasks()
                print(f"Задача №{num} отмечена как выполненная!")

    elif choice == "4": #блок удаления и подтверждения задачи
        if len(tasks) == 0:
            print("Список пуст, нечего удалять.")
        else:
            print("- ВАШИ ЗАДАЧИ -")
            for i, task in enumerate(tasks, start=1):
                status = "[x]" if task["done"] else "[ ]"
                print(f"{i}. {status} {task['title']}")
            
            try:
                num = int(input("Введите номер задачи для удаления: "))
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue
                
            if num < 1 or num > len(tasks):
                print("Ошибка: задачи с таким номером не существует!")
            else:
                confirm = input(f"Вы уверены, что хотите удалить '{tasks[num-1]['title']}'? (да/нет): ")
                if confirm.lower() == "да":
                    tasks.pop(num - 1)
                    save_tasks()
                    print("Удалено")
                else: 
                    print("Удаление отменено")              

    elif choice == "5": # блок выхода и сохранения
        save_tasks()
        print("Задачи сохранены! До свидания.")
        break