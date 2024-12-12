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
    level_description = """
    Вы очнулись в темной, пыльной комнате.
    Стены из серого камня, воздух тяжелый от сырости.
    Перед вами массивная дубовая дверь, запертая на три замка. На полу разбросаны различные предметы.
    За облупившейся штукатуркой что-то скрыто..."""

    room = Room(level_description, room_items, puzzle)
    return play_room(room, "золотой ключ")

def play_room(room, hidden_item, riddle_answer = None):
    player = Player()
    print(room.description)

    while True:
        if room.items:
            print("\nВ комнате лежат:", ", ".join(room.items))
        else:
            print("\nВ комнате не осталось предметов.")

        if hidden_item and hidden_item not in room.items and hidden_item not in player.inventory:
            action = input("Что вы хотите сделать? (взять предмет / осмотреть комнату / выйти): ").lower().strip()
        else:
            action = input("Что вы хотите сделать? (взять предмет / выйти): ").lower().strip()

        if action == "взять предмет":
            item = input("Какой предмет вы хотите взять? ").lower().strip()

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


def level_2():
    monster_info = ("Грязный гоблин", 100)
    monster_name, monster_health = monster_info
    level_description = f"""
    Вы входите в огромный зал, освещенный лишь тусклым светом из проемов в потолке.
    В центре зала стоит {monster_name}, его глаза горят злобой. У вас есть ржавый меч и старый факел."""
    puzzle = lambda player: player.health > 0

    room = Room(level_description, ["ржавый меч", "старый факел"], puzzle)
    return fight_monster(room, monster_name, monster_health)

def fight_monster(room, monster_name, monster_health):
    player = Player()
    player.inventory.extend(room.items)
    print(room.description)

    while monster_health > 0 and player.health > 0:
        print(f"\nЗдоровье грязного гоблина: {monster_health}\nВаше здоровье: {player.health}")
        print("У вас есть:", ", ".join(player.inventory) or "Ничего нет.")

        available_actions = {"атаковать", "сбежать"}
        if "старый факел" in player.inventory:
            available_actions.add("использовать факел")
        action = input(f"Что вы хотите сделать? ({', '.join(available_actions)}): ").lower().strip()

        if action == "атаковать":
            damage = random.randint(10, 20)
            monster_health -= damage
            print(f"\nВы нанесли {damage} урона! {monster_name} рычит от боли.")

            monster_attack = random.randint(5, 15)
            player.health -= monster_attack
            print(f"{monster_name} нанес вам {monster_attack} урона!")

        elif action == "использовать факел" and "старый факел" in player.inventory:
            damage = random.randint(3, 7)
            monster_health -= damage
            player.inventory.remove("старый факел")
            print("\nВы бросаете факел в монстра, обжигая его.")

        elif action == "сбежать":
            print("Вы пытаетесь сбежать, но монстр блокирует вам путь!")
            monster_attack = random.randint(10, 20)
            player.health -= monster_attack
            print(f"\n{monster_name} нанес вам {monster_attack} урона за попытку побега!")

        else:
            print("Неизвестное действие.")

    if monster_health <= 0:
        print("\nВы победили грязного гоблина! Его тело безжизненно обрушивается на пол.")
        return True

    else:
        print("\nВы погибли...")
        return False


def level_3():
    library_info = {
        "description": ("Вы оказываетесь в библиотеке. Пыльные тома повсюду, полки тянутся до самого потолка. "
                             "На столе лежит старая книга с выцветшими страницами, а на ней надпись:"),
        "riddle": """    Что может шептать, но не говорит,
    имеет много страниц, но не видит,
    и всегда открывает новые миры?""",
        "answer": "книга"
    }

    room = Room(library_info["description"], [], lambda guess: guess == library_info["answer"])
    return play_riddle_room(room, library_info["riddle"])

def play_riddle_room(room, riddle):
    print("\n" + room.description)
    print(riddle)

    while True:
        guess = input("Отгадайте загадку: ").lower().strip()

        if room.puzzle(guess):
            print("\nПравильно! Вы открываете книгу, и на ее страницах находите карту, указывающую на тайный проход в стене.")
            return True

        else:
            print("Неправильно. Попробуйте еще раз.")


def main():
    print("\nДобро пожаловать в игру 'Замок'!")
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