import logging
from .components.cpu import CPU
from .components.gpu import GPU
from .components.ram import RAM
from .components.motherboard import Motherboard
from .components.psu import PSU
from .compatibility import CompatibilityChecker

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PCBuilder:

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.selected_components = {
            'cpu': None,
            'gpu': None,
            'ram': None,
            'motherboard': None,
            'psu': None
        }
        self.compatibility_checker = CompatibilityChecker()
        logging.info("PCBuilder initialized")

    def select_component(self, component_type, component_id):
        component = self.db_manager.get_component_by_id(component_id)
        if not component:
            logging.warning(f"Component with id {component_id} not found")
            return False

        try:
            if component_type == 'cpu':
                self.selected_components['cpu'] = CPU(**component.__dict__)
            elif component_type == 'gpu':
                self.selected_components['gpu'] = GPU(**component.__dict__)
            elif component_type == 'ram':
                self.selected_components['ram'] = RAM(**component.__dict__)
            elif component_type == 'motherboard':
                self.selected_components['motherboard'] = Motherboard(**component.__dict__)
            elif component_type == 'psu':
                self.selected_components['psu'] = PSU(**component.__dict__)
            logging.info(f"Component {component.name} selected for {component_type}")
            return True
        except Exception as e:
            logging.error(f"Error selecting component {component.name} for {component_type}: {e}", exc_info=True)
            return False

    def check_compatibility(self):
        cpu = self.selected_components.get('cpu')
        motherboard = self.selected_components.get('motherboard')
        ram = self.selected_components.get('ram')
        psu = self.selected_components.get('psu')

        if not cpu or not motherboard or not ram or not psu:
            logging.warning("Compatibility check: not all mandatory components are selected")
            return False, "Не выбраны все обязательные компоненты (CPU, Motherboard, RAM, PSU)"

        if not self.compatibility_checker.is_cpu_compatible(cpu, motherboard):
            logging.warning("Compatibility check: CPU is not compatible with motherboard")
            return False, "CPU несовместим с материнской платой"

        if not self.compatibility_checker.is_ram_compatible(ram, motherboard):
            logging.warning("Compatibility check: RAM is not compatible with motherboard")
            return False, "RAM несовместима с материнской платой"

        total_components = [cpu, motherboard, ram]
        if self.selected_components.get('gpu'):
            total_components.append(self.selected_components.get('gpu'))
        if not self.compatibility_checker.check_power_supply(total_components, psu):
            logging.warning("Power supply is not sufficient")
            return False, "Мощность блока питания недостаточна"
        logging.info("Compatibility check successful")
        return True, "Компоненты совместимы"

    def get_selected_components(self):
        return self.selected_components