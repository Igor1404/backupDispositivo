# CLASSES COM FUNÇÕES PARA CRIAR BACKUPS E EXPORTAR EM JSON
#AUTOR: IGOR RODRIGUES CARDOSO - ENGENHARIA DE COMPUTAÇÃO - ONLINE TELECOM

from paramiko import SSHClient, SSHConfig, SSHException
import paramiko
import subprocess
import time
import re
import json
import sys
# import request
import datetime
import json
from ftplib import FTP



# A Classe com funções criadas já estão sendo executadas
# from elasticsearch import Elasticsearch (Ainda não efetuado)
# from elasticsearch.connection import RequestsHttpConnection

#CLASSE MODELO BACKUP
class MikoDisp:

        # Inicialização das variaveis (MÉTODO CONSTRUTOR)
        def __init__(self, ipback, nameback, passwdback, portback):
            self.__ipback = ipback
            self.__nameback = nameback
            self.__passwdback = passwdback
            self.__portback = portback

            # Getters (Property) e setters
            @property
            def IpBackup(self):
                return self.__ipback

            @IpBackup.setter
            def IpBackup(self, ipback):
                self.__ipback = ipback

            @property
            def NameBackup(self):
                return self.__nameback

            @NameBackup.setter
            def NameBackup(self, nameback):
                self.__nameback = nameback

            @property
            def PassBackup(self):
                return self.__passwdback

            @PassBackup.setter
            def PassBackup(self, passback):
                self.__passwdback = passback

            @property
            def PortBackup(self):
                return self.__portback

            @PortBackup.setter
            def PortBackup(self, portback):
                self.__portbackup = portback

# Classe de conexão que é filha da classe MikoDisp
# ATRIBUTOS ENTRADA: ipback, nameback, passwdback, portback, cmddisp
# ATRIBUTOS DE RETORNO: Comandoinicial, resultado
tempoatual = time.strftime("%Y-%m-%d -- %H-%M-%S")
dataBackup = "Backup"

class connDisp(MikoDisp):
    def __init__(self, ipback, nameback, passwdback, portback, cmddisp):
        self.ipback = ipback
        self.nameback = nameback
        self.passwdback = passwdback
        self.portback = portback
        self.cmddisp = cmddisp

        # MÉTODO TRY PARA EXECUTAR A FUNÇÃO DE CONECTAR E GERAR ERRO CASO NÃO DÊ CERTO.

        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # VAI LER TODOS AS CHAVES CADASTRADAS
            self.ssh.connect(hostname=ipback, username=nameback, password=passwdback, port=portback, look_for_keys=False, allow_agent=False)
            stdin, stdout, stderr = self.ssh.exec_command(cmddisp)
            #
            # HABILITA O SERVIÇO FTP (FILE TRANSFER PROTOCOL) ATRAVÉS DOS COMANDOS PARAMIKO, CASO NÃO TENHA
            # stdin, stdout, stderr = self.ssh.exec_command("ip service set ftp port=21")
            # stdin, stdout, stderr = self.ssh.exec_command("ip service enable ftp")



            # Caso o comando seja de exportação de arquivo de backup/
            if (cmddisp == "export file=" + dataBackup):
                print("\n")
                print("Processo de comando de exportação...")
                #USANDO O TEMPO DE ESPERA DE 12 SEGUNDOS PARA SE CONECTAR
                # time.sleep(12)

                # CRIA OS DOIS ARQUIVOS, O PRIMEIRO GUARDARÁ O BACKUP O SEGUNDO É PARA RECONHECER O ARQUVI DENTRO DO MIKROTIK
                arqbackup = open("../backuparquivossrc/Backup__ip__"+ipback+"__time__"+tempoatual+".rsc","wb")
                arqmikroback = dataBackup+".rsc"

                #UTILIZANDO A BIBLIOTECA FTPLIB PARA INICIAR A TRANSFERÊNCIA
                with FTP(ipback.replace(" ","")) as ftpcmd:
                    # ftpcmd.connect(host=ipback, port=21)
                    ftpcmd.login(user=nameback, passwd=passwdback)
                    executarftp = ftpcmd.retrbinary('RETR ' + arqmikroback, arqbackup.write, 1024)
                    ftpcmd.quit()
                    arqbackup.close()


            # CASO NÃO SEJA A FUNÇÃO DE BACKUP, UTILIZAR ESSA CONDIÇÃO
            else:
                print("\n")
                # entradatexto = str(stdin.read())
                print("Processo de execução de comando"+cmddisp+"...\n")
                saidaresult = (stdout.read())
                # print(str(saidaresult).replace("\\r\\n","\r\n"))
                saidatexto = str(saidaresult).replace("\\r\\n","\r\n")
                # CRIANDO UM ARQUIVO DE TEXTO DO RESULTADO DA PESQUISA
                f = open("../backuparquivossrc/resultado__ip__"+ipback+"__time__"+tempoatual+".txt","w")
                f.write(saidatexto)
                f.close()

                local=("resultado__ip__"+ipback+"__time__"+tempoatual+".txt")
                localiz=("/Documentos/Projetos/funcoesrbbackcup/"+local)

        except Exception as e:
            print(e)
            raise

        except ValueError as e2:
            print(e2)
            raise

        except paramiko.ssh_exception.NoValidConnectionsError as mikoerr:
            print(mikoerr)
            raise

        except paramiko.ssh_exception.AuthenticationException as mikoerr2:
            print(mikoerr2)
            raise


        finally:

            resultadojson = {
                "Ip-Dispositivo":ipback,
                "User": nameback,
                "Password": passwdback,
                "Port": portback,
                "Saida Backup": saidatexto

            }

            # print(resultadojson)
            result = json.dumps(resultadojson, indent=1, skipkeys=True)
            print(result.replace("\\r\\n", "\n"))
            print("\n")
            print("Programa Executado com Sucesso!!!\n")
            self.ssh.close()

# disp01 = connDisp("ip da RB", "usuario", "senha","2225 (Porta Padrão)",'Digite o Comando')








