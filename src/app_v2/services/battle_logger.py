"""Логгирование боя"""


class BattleLogger:
    def __init__(self):
        self.messages = []

    def log_ability_use(self, message: str):
        self.messages.append(message)

    def log_damage_to_player(self, attacker_name: str, target_name: str, damage: float):
        self.messages.append(f"Игрок {attacker_name} нанес {damage:.2f} урона {target_name}. ")

    def log_xp(self, message: str):
        self.messages.append(message)

    def log_level_up(self, message: str):
        self.messages.append(message)

    def log_counter_attack(self, damage: float):
        self.messages.append(f"Контратака на {damage:.2f} урона! ")

    def log_death(self, target_name: str):
        self.messages.append(f"Игрок {target_name} пал в бою. ")

    def log_final_health(self, attacker, target):
        self.messages.append(f"Здоровье {attacker.name}: {attacker.current_health:.2f}/{attacker.max_health:.2f}. ")
        self.messages.append(f"Здоровье {target.name}: {target.current_health:.2f}/{target.max_health:.2f}. ")

    def log_npc_death(self, npc_name: str):
        self.messages.append(f'NPC {npc_name} убит! ')

    def get_full_log(self) -> str:
        return "".join(self.messages)
