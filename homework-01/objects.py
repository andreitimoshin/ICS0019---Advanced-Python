import random


class Die:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self):
        number = random.randint(1, self.sides)
        return number


class Student:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.student_code = first_name.lower()[:3] + last_name.lower()[:3]


class Book:
    def __init__(self, title: str):
        self.title = title

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title
        return False


class BookShelf:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.books = []

    def add_book(self, book: Book):
        if len(self.books) < self.capacity:
            self.books.append(book)
        else:
            print("This bookshelf can't store any more books.")

    def take_book_by_title(self, title: str):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                return book
        print(f"This bookshelf does not contain a book called {title}.")


class Weapon:
    def __init__(self, name: str, damage: float):
        self.name = name
        self.damage = damage


class Warrior:
    def __init__(self, name: str, health: float):
        self.name = name
        self.health = health
        self.weapon = None

    def warcry(self):
        if self.health > 0:
            print("RAAARGH")

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def attack(self, enemy: "Warrior"):
        if self.health <= 0:
            return
        if self.weapon is not None:
            enemy.health -= self.weapon.damage
        else:
            enemy.health -= 2

        enemy.health = max(enemy.health, 0)


if __name__ == '__main__':
    four_sided_die = Die(4)
    print(four_sided_die.roll())  # 3
    print(four_sided_die.roll())  # 1
    print(four_sided_die.roll())  # 4

    twenty_sided_die = Die(20)
    print(twenty_sided_die.roll())  # 20
    print(twenty_sided_die.roll())  # 1
    print(twenty_sided_die.roll())  # 13

    student1 = Student('John', 'Smith')
    print(student1.student_code)  # -> johsmi

    student2 = Student('Tom', 'Tree')
    print(student2.first_name)  # -> Tom
    print(student2.last_name)  # -> Tree
    print(student2.student_code)  # -> tomtre

    book1 = Book("Harry Potter and the Philosopher's Stone")
    book2 = Book("Dune")

    bookshelf = BookShelf(1)

    bookshelf.add_book(book1)
    bookshelf.add_book(book2)  # -> This bookshelf can't store any more books.

    book = bookshelf.take_book_by_title("Harry Potter and the Philosopher's Stone")
    print(book == book1)  # -> True

    bookshelf.take_book_by_title("Dune")  # -> This bookshelf does not contain a book called Dune.

    warrior1 = Warrior('Beir', 70.0)

    warrior2 = Warrior('Uldiir', 120.0)
    battleaxe = Weapon('Battleaxe', 75.0)
    warrior2.equip_weapon(battleaxe)

    warrior1.warcry()  # -> RAAARGH

    warrior1.attack(warrior2)
    print(warrior2.health)  # -> 118.0

    warrior2.attack(warrior1)
    print(warrior1.health)  # -> 0.0

    warrior1.warcry()  # ->
