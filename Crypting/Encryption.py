from cryptography.fernet import Fernet
from .utils import getFilesAndDirs
import os

class Encryption:
    def __init__(self, key:bytes=b"") -> None:
        self.key = key
        if (not key):
            self.key = Fernet.generate_key()
        self.fernetKey = Fernet(self.key)

    def encryptDir(self, dir: str):
        files, dirs = getFilesAndDirs(dir)
        encrypted = ""

        for file in files:
            self.encryptFile(file)

        dirs.append(dir)
        dirs.sort(key = len, reverse=True)
        for dir in dirs:
            encrypted = self.encryptFilepath(dir)
            os.rename(dir, encrypted)

        return encrypted

    def encryptFile(self, filepath: str):
        with open(filepath, "rb") as file:
            content = file.read()
            encryptedContent = self.encryptBytes(content)

        with open(filepath, "wb") as file:
            file.write(encryptedContent)

        encryptedFilePath = self.encryptFilepath(filepath)
        os.rename(filepath, encryptedFilePath)

        return encryptedFilePath

    def encryptFilepath(self, path: str) -> str:
        filepath, name = os.path.split(path)
        encryptedName = self.encryptBytes(name.encode()).decode()
        return os.path.join(filepath, encryptedName)

    def encryptBytes(self, bytes: bytes):
        return Fernet.encrypt(self.fernetKey, bytes)
