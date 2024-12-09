import random

class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100

class Room:
    def __init__(self, description, items, puzzle):
        self.description = description
        self.items = items
        self.puzzle = puzzle


def level_1():
    room_items = ["ржавая монета", "старый пергамент", "железный ключ", "серебряный ключ"]
    puzzle = lambda inv: all(key in inv for key in ["железный ключ", "серебряный ключ", "золотой ключ"])
    level_description = """Вы очнулись в темной, пыльной комнате.
    Стены из серого камня, воздух тяжелый от сырости.
    Перед вами массивная дубовая дверь, запертая на три замка. На полу разбросаны различные предметы.
    За облупившейся штукатуркой что-то скрыто..."""
    room = Room(level_description, room_items, puzzle)
    return play_room(room, "золотой ключ")

def level_2():
    monster_name = "Грязный гоблин"
    monster_health = 100
    level_description = f"""Вы входите в огромный зал, освещенный лишь тусклым светом из проемов в потолке.
В центре зала стоит {monster_name}, его глаза горят злобой. У вас есть ржавый меч и старый факел."""
    puzzle = lambda player: player.health > 0
    room = Room(level_description, ["ржавый меч", "старый факел"], puzzle)

    return fight_monster(room, monster_name, monster_health)


def level_3():
    riddle = ("Что имеет голос, но не может говорить,\n"
              "много глаз, но не может видеть,\n"
              "и всегда показывает вам путь?\n")
    answer = "книга"
    level_description = """Вы оказываетесь в библиотеке. Пыльные тома повсюду, полки тянутся до самого потолка. На столе лежит старая книга с выцветшими страницами, а на ней надпись:"""
    room = Room(level_description, [], lambda guess: guess.lower() == answer)
    return play_riddle_room(room, riddle, answer)


def play_riddle_room(room, riddle, answer):
    player = Player()
    print("\n" + room.description)
    print(riddle)

    while True:
        guess = input("Отгадайте загадку: ").lower()
        if room.puzzle(guess):
            print("\nПравильно! Книга открывается, и вы обнаруживаете тайный проход за ней. Вы выбрались из замка!")
            return True
        else:
            print("Неправильно. Попробуйте еще раз.")


def play_room(room, hidden_item, riddle_answer = None):
    player = Player()
    print("\n" + room.description)

    while True:
        print("\nВ комнате лежат:", ", ".join(room.items) or "Ничего нет.")
        if hidden_item and hidden_item not in room.items and hidden_item not in player.inventory:
            action = input("Что вы хотите сделать? (взять предмет / осмотреть комнату / выйти): ").lower()
        else:
            action = input("Что вы хотите сделать? (взять предмет / выйти): ").lower()

        if action == "взять предмет":
            item = input("Какой предмет вы хотите взять? ").lower()
            if item in room.items:
                player.inventory.append(item)
                room.items.remove(item)
                print(f"Вы взяли {item}.")
            else:
                print("Здесь нет такого предмета.")
        elif action == "осмотреть комнату" and hidden_item and hidden_item not in player.inventory:
            print("Вы внимательно осматриваете комнату...")
            room.items.append(hidden_item)
            print(f"Вы обнаружили спрятанный {hidden_item}!")

        elif action == "выйти":
            if room.puzzle(player.inventory) if riddle_answer is None else room.puzzle(riddle_answer):
                return True
            else:
                print("Дверь заперта. Вам нужно найти все три ключа.")

        else:
            print("Неизвестное действие.")

def fight_monster(room, monster_name, monster_health):
    player = Player()
    player.inventory.extend(room.items)
    print("\n" + room.description)

    while monster_health > 0 and player.health > 0:
        print(f"\nЗдоровье:\n{monster_name}: {monster_health}\nВаше здоровье: {player.health}")
        print("У вас есть:", ", ".join(player.inventory) or "Ничего нет.")

        available_actions = ["атаковать", "сбежать"]
        if "старый факел" in player.inventory:
            available_actions.append("использовать факел")
        action = input(f"Что вы хотите сделать? ({', '.join(available_actions)}): ").lower()

        if action == "атаковать":
            damage = random.randint(10, 20)
            monster_health -= damage
            print(f"Вы нанесли {damage} урона! {monster_name} рычит от боли.")
            monster_attack = random.randint(5, 15)
            player.health -= monster_attack
            print(f"{monster_name} нанес вам {monster_attack} урона!")
        elif action == "использовать факел" and "старый факел" in player.inventory:
            print("Вы бросаете факел в монстра, обжигая его.")
            monster_health -= 5
            player.inventory.remove("старый факел")
        elif action == "сбежать":
            print("Вы пытаетесь сбежать, но монстр блокирует вам путь!")
            monster_attack = random.randint(10, 25)
            player.health -= monster_attack
            print(f"{monster_name} нанес вам {monster_attack} урона за попытку побега!")
        else:
            print("Неизвестное действие.")

    if monster_health <= 0:
        print(f"\nВы победили {monster_name}! Его тело безжизненно обрушивается на пол.")
        return True
    else:
        print("\nВы погибли...")
        return False


def main():
    print("Добро пожаловать в игру 'Замок'!")
    if level_1():
        if level_2():
            if level_3():
                print("Поздравляем! Вы выбрались из замка!")
            else:
                print("Игра окончена.")
        else:
            print("Игра окончена.")
    else:
        print("Игра окончена.")


if __name__ == "__main__":
    main()