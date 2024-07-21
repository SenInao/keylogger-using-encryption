from cryptography.fernet import Fernet
from .utils import getFilesAndDirs
import os

class Decryption:
    def __init__(self, key:bytes) -> None:
        self.key = key
        self.fernetKey = Fernet(self.key)

    def decryptDir(self, dir:str):
        files, dirs = getFilesAndDirs(dir)
        decrypted = ""

        for file in files:
            self.decryptFile(file)

        dirs.append(dir)
        dirs.sort(key=len, reverse=True)
        for dir in dirs:
            decrypted = self.decryptFilepath(dir)
            os.rename(dir, decrypted)

        return decrypted

    def decryptFile(self, filepath: str):
        with open(filepath, "rb") as file:
            content = file.read()
            decryptedContent = self.decryptBytes(content)

        with open(filepath, "wb") as file:
            file.write(decryptedContent)

        decryptedFilepath = self.decryptFilepath(filepath)
        os.rename(filepath, decryptedFilepath)

        return decryptedFilepath

    def decryptFilepath(self, path: str) -> str:
        filepath, name = os.path.split(path)
        decryptedName = self.decryptBytes(name.encode()).decode()
        return os.path.join(filepath, decryptedName)

    def decryptBytes(self, bytes: bytes):
        return Fernet.decrypt(self.fernetKey, bytes)
