import os
import logging
from core.database import DatabaseManager
from core.builder import PCBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    db_manager = DatabaseManager()
    db_manager.load_components_from_csv("data/components.csv")
    builder = PCBuilder(db_manager)

    while True:
        print("\nВыберите действие:")
        print("1. Выбрать CPU")
        print("2. Выбрать GPU")
        print("3. Выбрать RAM")
        print("4. Выбрать Motherboard")
        print("5. Выбрать PSU")
        print("6. Проверить совместимость")
        print("7. Посмотреть выбранные компоненты")
        print("8. Поиск компонентов")
        print("0. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            select_component(builder, db_manager, 'cpu')
        elif choice == "2":
            select_component(builder, db_manager, 'gpu')
        elif choice == "3":
            select_component(builder, db_manager, 'ram')
        elif choice == "4":
            select_component(builder, db_manager, 'motherboard')
        elif choice == "5":
            select_component(builder, db_manager, 'psu')
        elif choice == "6":
            check_compatibility(builder)
        elif choice == "7":
            show_selected_components(builder)
        elif choice == "8":
            search_components(db_manager)
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


def check_compatibility(builder):
    is_compatible, message = builder.check_compatibility()
    if is_compatible:
        print("Совместимость: OK")
        logging.info("Compatibility check passed.")
    else:
        print("Совместимость: Ошибка -", message)
        logging.warning(f"Compatibility check failed. Message: {message}")


def show_selected_components(builder):
    components = builder.get_selected_components()
    print("Выбранные компоненты:")
    for key, component in components.items():
        if component:
            print(f'{key}: {component.name} ({component.manufacturer} {component.model})')
    logging.info(f"Showing selected components: {components}")
    def select_component(builder, db_manager, component_type):
         while True:
            print(f"Доступные {component_type}:")
            components = get_filtered_components(db_manager, component_type)
            if not components:
              print(f'Нет доступных {component_type}')
              logging.warning(f"No available components of type {component_type}")
              return

            for component in components:
                 print(f"{component.id}. {component.name} ({component.manufacturer} {component.model})")


            try:
                component_id = int(input(f"Выберите ID {component_type}: "))
                if builder.select_component(component_type, component_id):
                   print(f'{component_type} успешно выбран')
                   logging.info(f"Component with id {component_id} selected")
                   break
                else:
                    print(f"Некорректный ID {component_type}. Попробуйте еще раз.")
                    logging.warning(f"Invalid ID {component_id} for {component_type}")

            except ValueError:
                print("Неверный ввод. Введите число.")
                logging.warning("Invalid input (not a number).")

    def get_filtered_components(db_manager, component_type):
        while True:
           manufacturer = input("Введите производителя (оставьте пустым для всех): ")
           search_term = input("Введите имя или модель для поиска (оставьте пустым для всех): ")

           components = db_manager.get_components(component_type=component_type, search_term=search_term, manufacturer=manufacturer)
           if components:
            return components
           else:
             print("Нет компонентов, отвечающих критериям")
             if input("Попробовать еще раз? (y/n)") != 'y':
               return []

    def search_components(db_manager):
        while True:
            component_type = input("Введите тип компонента для поиска (cpu, gpu, ram, motherboard, psu) или пустую строку для поиска по всем типам: ")
            if component_type not in ['', 'cpu', 'gpu', 'ram', 'motherboard', 'psu']:
                 print("Неверный тип компонента")
                 continue

            components = get_filtered_components(db_manager, component_type)
            if not components:
              return

            for component in components:
                 print(f"{component.id}. {component.name} ({component.manufacturer} {component.model})")
            if input("Поиск завершен. Продолжить поиск (y/n)") != 'y':
                return
        logging.info(f"Search component of type {component_type}")

    if __name__ == "__main__":
        main()