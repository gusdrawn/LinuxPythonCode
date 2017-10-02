import threading
import time
import paramiko
import sys

### Credenciales
port=22
username='root'
password='Tim123'

### PCRF
ip1='10.221.115.19'

### LoadBalancer
ip2='10.221.115.18'

proyecto='test'
nro='5521982137010'

print (""+
    "Nombre del proyecto: "+proyecto+"   "
    "Celular: "+nro[0:2]+" "+nro[2:4]+""+nro[4:6]+" "+nro[6:8]+""+nro[8:10]+" "+nro[10:12]+""+nro[12:13]+
    "")

pid = {}
try:
    def captura1():
        ## QNS
        print ("Iniciando SSH 1")
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip1,port,username,password)
        stdin,stdout,stderr=ssh.exec_command('tail -f /var/log/broadhop/consolidated-qns.log > /home/guguille/'+proyecto+'-qns.log &')
        stdin,stdout,stderr=ssh.exec_command("""ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
        print ("Registrando QNS")
        pid[1] = stdout.readline()
        print ("El PID de QNS es "+pid[1])

        # ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs

    def captura2():
        ## ENGINE
        print ("Iniciando SSH 2")
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip1,port,username,password)
        stdin,stdout,stderr=ssh.exec_command('tail -f /var/log/broadhop/consolidated-engine.log > /home/guguille/'+proyecto+'-engine.log &')
        stdin,stdout,stderr=ssh.exec_command("""ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
        print ("Registrando ENGINE")
        pid[2] = stdout.readline()
        print ("El PID de ENGINE es "+pid[2])
    def captura3():
        ## tracedb
        print ("Iniciando SSH 3")
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip1,port,username,password)
        stdin,stdout,stderr=ssh.exec_command("""/var/qps/bin/control/trace_ids.sh -i '+nro+' -d sessionmgr01:27721/policy_trace ; /var/qps/bin/control/trace.sh -i '+nro+' -d sessionmgr01:27721/policy_trace > /home/guguille/'+proyecto+'-tracedb.log &""")
        stdin,stdout,stderr=ssh.exec_command("""ps -a | grep trace.sh | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
        print ("Registrando TRACE DB")
        pid[3] = stdout.readline()
        print ("El PID del TraceDB es "+pid[3])

        #ps | grep trace.sh | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs

    def captura4():
        ## PCAP
        print ("Iniciando SSH 4")
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip2,port,username,password)
        stdin,stdout,stderr=ssh.exec_command('tcpdump -nni any port 3868 or port 5019 -v -s0 -w /home/guguille/'+proyecto+'.pcap &')
        stdin,stdout,stderr=ssh.exec_command("""ps -a | grep tcpdump | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
        print ("Registrando PCAP")
        pid[4] = stdout.readline()
        print ("El PID de PCAP es "+pid[4])

        # ps -a | grep tcpdump | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs
    def captura5():
        '''
        print ("Iniciando TEST")
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip1,port,username,password)
        print ("Iniciando SSH 4")
        stdin,stdout,stderr=ssh.exec_command('tail -f /var/log/broadhop/consolidated-engine.log > /home/guguille/'+proyecto+'-engine.log &')
        stdin,stdout,stderr=ssh.exec_command("""ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
        print ("Registrando PCAP")
        print (stdout.readline())
        print (stderr.readline())
        pid[5] = stdout.readline()
        print ("SSH 5"+pid[5])
        print ("TEST")
        '''
    captura1()
    captura2()
    captura3()
    captura4()
    '''
    threads = []
    th = threading.Thread(target = captura1)
    th.start()
    threads.append(th)
    th = threading.Thread(target = captura2)
    th.start()
    threads.append(th)
    th = threading.Thread(target = captura3)
    th.start()
    threads.append(th)
    th = threading.Thread(target = captura4)
    th.start()
    threads.append(th)
    for th in threads:
        th.join()
    '''
    while True:
        print ("""
            Deseas detener la captura?
        """)
        ans=input(" ")
        if (ans == "si" or ans == "Si" or ans == "SI" or ans == "s" or ans == "S"): 
            print("Detengo la captura")
            break
        else:
            print("No sirve, dime si lo detengo.")
    print ("PID1: "+pid[1])
    print ("PID2: "+pid[2])
    print ("PID3: "+pid[3])
    print ("PID4: "+pid[4])
    print ("Deteniendo LOGS")
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip1,port,username,password)
    print ("Iniciando Comando")
    stdin,stdout,stderr=ssh.exec_command('kill -9 '+pid[1])
    print ("Detenido 1")
    stdin,stdout,stderr=ssh.exec_command("""ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
    pid[1] = stdout.readline()
    print ("Verificando: "+pid[1])


    stdin,stdout,stderr=ssh.exec_command('kill -9 '+pid[2])
    print ("Detenido 2")
    stdin,stdout,stderr=ssh.exec_command("""ps | grep tail | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
    pid[2] = stdout.readline()
    print ("Verificando: "+pid[2])

    stdin,stdout,stderr=ssh.exec_command('kill -9 '+pid[3])
    print ("Detenido 3")
    stdin,stdout,stderr=ssh.exec_command("""ps -a | grep trace.sh | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
    pid[3] = stdout.readline()
    print ("Verificando: "+pid[3])

    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip2,port,username,password)
    stdin,stdout,stderr=ssh.exec_command('kill -9 '+pid[4])
    print ("Detenido 4")
    stdin,stdout,stderr=ssh.exec_command("""ps -a | grep tcpdump | grep -o '[0-9][0-9][0-9][0-9][0-9]\|[0-9][0-9][0-9][0-9]' | xargs""")
    pid[4] = stdout.readline()
    print ("Verificando: "+pid[4])
    #transport = paramiko.Transport((ip, port))
    #transport.connect(username = username, password = password)

    #sftp = paramiko.SFTPClient.from_transport(transport)
    #path = './THETARGETDIRECTORY/' + sys.argv[1]    #hard-coded
    #print (path)
    #/home/guguille/+'-qns.log'
    #/home/guguille/+'-engine.log'
    #/home/guguille/+'-tracedb.log'    
    #localpath = sys.argv[1]
    #print (localpath)
    #sftp.get(remotepath, localpath)
    #sftp.close()
    #transport.close()
    #print ('Upload done.')


except KeyboardInterrupt:
    print('Te has salido del programa, cancelando los Logs')
    ### REPETIR LOS KILL

