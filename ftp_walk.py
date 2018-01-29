from os import path as ospath


class FTPWalk:
    """
    Класс реализующий функцию walk (os.walk) для FTP
    """
    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        """
        Возвращает файлы и имена каталогов для пути
        """
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception:
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def walk(self, path='/'):
        """
        Перемещение по дереву каталогов FTP сервера
        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = ospath.join(path, name)
            yield from self.walk(path)
            self.connection.cwd('..')
            path = ospath.dirname(path)
