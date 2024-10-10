from threading import Thread
from time import sleep
from random import randint
import queue

class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *args):
        self.tables = args
        self.queue = queue.Queue()

    def guest_arrival(self, *guests):
        i = 0
        for tb in self.tables:
            if i in range(len(guests)):
                tb.guest = guests[i]
                tb.guest.start()
                print(f'{tb.guest.name} сел(-а) за стол номер {tb.number}')
                i += 1
        while i in range(len(guests)):
            self.queue.put(guests[i])
            print(f'{guests[i].name} в очереди')
            i += 1

    def discuss_guests(self):
        while (not self.queue.empty()) or (not self.tables_is_emty()):
            for tb in self.tables:
                if (not (tb.guest is None)) and (not tb.guest.is_alive()):
                    print(f'{tb.guest.name} покушал(-а) и ушёл(ушла)')
                    tb.guest = None
                    print(f'Стол номер {tb.number} свободен')
                    if not self.queue.empty():
                        tb.guest = self.queue.get()
                        print(f'{tb.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {tb.number}')
                        tb.guest.start()

    def tables_is_emty(self):
        for tb in self.tables:
            if not (tb.guest is None):
                return False
        return True

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
