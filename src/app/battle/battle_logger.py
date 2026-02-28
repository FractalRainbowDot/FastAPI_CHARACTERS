class BattleLogger:
    def __init__(self):
        self.messages = []

    def log_ability_use(self, message: str):
        self.messages.append(message)

    def log_damage(self, attacker_id: int, target_id: int, damage: int):
        self.messages.append(f"Пользователь {attacker_id} нанес {damage} урона пользователю {target_id}. ")

    def log_xp(self, message: str):
        self.messages.append(message)

    def log_level_up(self, message: str):
        self.messages.append(message)

    def log_counter_attack(self, damage: int):
        self.messages.append(f"Контратака на {damage} урона! ")

    def log_death(self, target_id: int):
        self.messages.append(f"Пользователь {target_id} пал в бою. ")

    def log_final_health(self, attacker, target):
        self.messages.append(f"Здоровье {attacker.id}: {attacker.current_health}/{attacker.max_health}. ")
        self.messages.append(f"Здоровье {target.id}: {target.current_health}/{target.max_health}. ")

    def get_full_log(self) -> str:
        return "".join(self.messages)
