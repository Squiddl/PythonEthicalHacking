import paramiko


# TODO authentication with SSH key
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    '''
    Set the policy to accept the SSH key for the SSH server 
    because of controlling both ends of this connection.
    '''
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())


if __name__ == '__main__':
    import getpass
    # gets the username from the environment
    username = getpass.getuser()
    username = username if username else input('Username: ')
    password = getpass.getpass()

    ip_addr = input('Enter server IP: ') or '192.168.178.69'
    port_number = input('Enter port or <CR>: ') or 2222
    command = input('Enter command or <CR>') or 'id'
    # response will not be displayed to frustrate any shoulder-surfers
    ssh_command(ip_addr, port_number, password, command)
