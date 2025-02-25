import logging


class CompatibilityChecker:
    @staticmethod
    def is_cpu_compatible(cpu, motherboard):
        if not cpu or not motherboard:
            logging.warning("Compatibility check: CPU or motherboard is None")
            return False

        is_compatible = cpu.socket == motherboard.socket
        logging.info(
            f"CPU compatibility check: CPU socket {cpu.socket}, Motherboard socket {motherboard.socket}, Compatible: {is_compatible}")
        return is_compatible

    @staticmethod
    def is_ram_compatible(ram, motherboard):
        if not ram or not motherboard:
            logging.warning("Compatibility check: RAM or motherboard is None")
            return False

        is_compatible = ram.memory_type == motherboard.memory_type
        logging.info(
            f"RAM compatibility check: RAM memory type {ram.memory_type}, Motherboard memory type {motherboard.memory_type}, Compatible: {is_compatible}")
        return is_compatible

    @staticmethod
    def check_power_supply(components, psu):
        if not components or not psu:
            logging.warning("Power supply check: components or psu is None")
            return False

        total_power = sum(c.power for c in components if c.power)
        is_sufficient = total_power <= psu.power
        logging.info(
            f"Power supply check: Total power {total_power}, PSU power {psu.power}, Sufficient: {is_sufficient}")
        return is_sufficient