from tempfile import gettempdir
from os import path

class File:
    """ Класс-интерфейс для работы с файлами """

    def __init__(self, path_to_file):
        """ В инициализатор передается путь к нужному файлу. Если файла по такому адресу
        не существует - он создастся. """

        self.path_to_file = path_to_file

        if not path.exists(self.path_to_file):
            open(self.path_to_file, 'w').close()


    def __add__(self, obj):
        """ Перегрузка оператора сложения: создается новый файл в временной директории.
        В него записывается содержание файлов по обе стороны от "+" """

        new_dir = path.join(
            gettempdir(),
            'tmp.txt'
        )
        new_file = File(new_dir)
        new_file.write(self.read() + obj.read())

        return new_file
    
    def __str__(self):
        """ При вызове объекта на печать, возвращается полный путь до файла """

        return self.path_to_file

    def __iter__(self):
        self.cur_pos = 0
        return self

    def __next__(self):
        """ Итератор возвращает по одной строке из файла """
        
        with open(self.path_to_file, 'r') as f:
            f.seek(self.cur_pos)

            line = f.readline()
            if not line:
                raise StopIteration

            self.cur_pos = f.tell()  

            return line       

    def read(self):
        """ Функция записи в файл """

        with open(self.path_to_file, 'r') as f:
            return f.read()

    def write(self, text):
        """ Функция чтения из файла """

        with open(self.path_to_file, 'w') as f:
            return f.write(text)

