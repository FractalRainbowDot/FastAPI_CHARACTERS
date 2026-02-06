from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(max_length=100)
    char_class: str


class Character:
    def __init__(self, name):
        self.name = name
        self.alive = True
        self.health = 100
        self.damage = 10

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, target):
        target.take_damage(self.damage)

    def death(self):
        if self.health <= 0:
            self.alive = False


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self.armour = 50

    def take_damage(self, damage):
        if self.armour < damage:
            self.health -= damage - self.armour


class Mage(Character):
    def __init__(self, name):
        super().__init__(name)
        self.magic_damage = 10
        self.damage = 1
        self.mana = 50


    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(self.magic_damage)
        target.take_damage(self.damage)


players_list = [Warrior('Sergey'), Mage('Viktoria')]

def show_players():
    return [player for player in players_list]