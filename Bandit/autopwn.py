#!/usr/bin/env python3

from pwn import *
import signal, paramiko

class SSH:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()

    def connect(self):
        try:
            self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            if not self.client.get_transport().is_active():
                print('Error: La conexión no se estableció correctamente.')
                sys.exit(1)
            else:
                p4.success(password)
        except paramiko.AuthenticationException as e:
            print('Error de autenticación:', e)
            sys.exit(1)
        except Exception as e:
            print('Error en la conexión:', e)
            sys.exit(1)

    def run_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            return output
        except Exception as e:
            print('Error al ejecutar el comando:', e)
            sys.exit(1)

    def close(self):
        self.client.close()

if __name__ == '__main__':
    
    level = 0 

    host = 'bandit.labs.overthewire.org'
    port = 2220
    username = 'bandit'
    password = 'bandit0'
    
    print()
    p1 = log.progress('Output')
    print()

    with open("commands.txt") as commands:
        for command in commands:
            p4 = log.progress(username+str(level))
            ssh = SSH(host,port,username+str(level),password)
            ssh.connect()
            output = ssh.run_command(command)
            p1.status("\n"+output+"\n")
            if re.match("^[a-zA-Z0-9]*$", output.strip()):
                password = output.strip()
                ssh.close()
                level += 1
            else:
                p3.success('\n'+output)
                ssh.close()
                sys.exit(0)
