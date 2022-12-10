from scapy.all import *
from socket import *
from colorama import Fore, Style
import argparse
import time
import re
import threading
import pyperclip
import nmap
import signal
import sys
import pyfiglet

def handler(signum, frame):
    print(Fore.RED + "\nHas pulsado Ctrl+C, saliendo de forma segura\n")
    exit(1)
 
 
signal.signal(signal.SIGINT, handler)


def ip_scan(ip):
    inicio=time.time()
    range_ip = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    final_packet = broadcast/range_ip
    print("\n")
    res = srp(final_packet, timeout=2, verbose=False)[0]
    print(Fore.GREEN+ "\n[+]"+Fore.YELLOW+" Mostrando hosts activos\n")
    for n in res:
        print(Fore.GREEN+"HOST: "+Fore.WHITE+" {:<15} ".format(n[1].psrc)+Fore.GREEN+"   MAC:  "+Fore.WHITE+"{}".format(n[1].hwsrc))
    fin=time.time() - inicio
    print(Fore.GREEN+ "\n[-]"+Fore.YELLOW+" El escaneo de hosts ha tardado"+Fore.CYAN+" {}".format(fin)+Fore.YELLOW+" segundos\n")


o = []

def port_scan(ip, port):
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((ip, port))
        setdefaulttimeout(1)
        if (conn == 0):
            serviceName = getservbyport(port, "tcp");
            print(Fore.WHITE+"  {:<5}".format(port)+Fore.GREEN+"WITH SERVICE "+Fore.WHITE+" {:<20}".format(serviceName)+ Fore.GREEN+"OPEN")
            o.append(port)
        s.close

def scan(ip, port):
    scanner = nmap.PortScanner()
    scan = scanner.scan(hosts="{}".format(ip), arguments="-sC -sV -p {}".format(port))
    if scanner[ip]['tcp'][int(port)]['version']:
        print(Fore.GREEN+"PORT "+Fore.WHITE+"{:<5}".format(port)+Fore.GREEN+"APP "+Fore.WHITE+"{:<25}".format(scanner[ip]['tcp'][int(port)]['product'])+Fore.GREEN+"SERVICE "+Fore.WHITE+"{}".format(scanner[ip]['tcp'][int(port)]['name'])+"VERSION "+Fore.WHITE+"{}".format(scanner[ip]['tcp'][int(port)]['version']))
    else:
        print(Fore.GREEN+"PORT "+Fore.WHITE+"{:<5}".format(port)+Fore.GREEN+"APP "+Fore.WHITE+"{:<25}".format(scanner[ip]['tcp'][int(port)]['product'])+Fore.GREEN+"SERVICE "+Fore.WHITE+"{}".format(scanner[ip]['tcp'][int(port)]['name']))

def main():
    parse = argparse.ArgumentParser(description="SpecialistSmartScan help")
    parse.add_argument("-r","--rango",help="Rango de direcciones a escanear, ej.- 192.168.1.0/24")
    parse.add_argument("-p","--ports",help="Escanear mas información de cada puerto especificado (Requiere del parametro -s), ej.- \"[53, 80, 139, 443, 445]\"")
    parse.add_argument("-s","--scan",help="Escanear puertos abiertos del host especificado, ej.- 192.168.1.111")
    parse = parse.parse_args()
    print("\n")
    print(pyfiglet.figlet_format("S.S.S", font = "isometric1"))
    print("{:<20}Specialist Smart Scan".format(""))
    if parse.rango:
        if re.match("^(25[0-5]|2[0-4][0-9]|[01][0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([1-9][0-9]?)", parse.rango):
            ip_scan(parse.rango)
            exit(0)
        else:
            print(Fore.RED+"\n[-]"+Fore.YELLOW+" Tienes que introducir un rango valido ej.-"+Fore.CYAN+" 192.168.1.0/24\n")
            exit(1)
    elif parse.scan:
        if parse.ports:
            if re.match("(\d|\[(\d|,\s*)*])", parse.ports):
                print('\n')
                ports = parse.ports.strip('][').split(', ')
                inicio=time.time()
                print(Fore.GREEN+ "\n[+]"+Fore.YELLOW+" Procesando información de cada puerto abierto en el host "+Fore.WHITE+"{}".format(parse.scan)+Fore.YELLOW+":\n")
                for port in ports:
                    thread1 = threading.Thread(target=scan, args=(parse.scan, port), daemon=True)
                    thread1.start()
                thread1.join()
                fin=time.time() - inicio
                print(Fore.GREEN+ "\n[-]"+Fore.YELLOW+" El escaneo de puertos ha tardado"+Fore.CYAN+" {}".format(fin)+Fore.YELLOW+" segundos\n")
                exit(0)
            else:
                print(Fore.RED + "\n[-] Tienes que introducir el parametro correctamente, ej.- \"[53, 80, 139, 443, 445]\"\n")
                exit(1)
        else:
            if re.match("^(25[0-5]|2[0-4][0-9]|[01][0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?$)", parse.scan):
                inicio=time.time()
                print("\n")
                print(Fore.GREEN+"\n[+]"+Fore.YELLOW+" Mostrando los puertos escaneados:\n")
                for i in range(1, 1024):
                    thread1 = threading.Thread(target=port_scan, args=(parse.scan, i), daemon=True)
                    thread1.start()
                print(Fore.GREEN+ "\n[-]"+Fore.YELLOW+" Copiando al clipboard los siguientes puertos: "+Fore.CYAN+"\"{}\"".format(str(o))+Fore.YELLOW+" para poder usar el parametro -p correctamente\n")
                thread1.join()
                portsToCopy = "\"{}\"".format(str(o))
                pyperclip.copy(portsToCopy)
                fin=time.time() - inicio
                print(Fore.GREEN+ "\n[-]"+Fore.YELLOW+" El escaneo de los puertos abiertos ha tardado"+Fore.CYAN+" {}".format(fin)+Fore.YELLOW+" segundos\n")
                exit(0)
            else:
                print(Fore.RED + "[-] Tienes que introducir una ip valida")
                exit(1)
    else:
        print(Fore.RED + "\n[-] "+ Fore.YELLOW+"Por favor, introduce el comando de forma correcta, '"+Fore.CYAN +"--help"+Fore.YELLOW+"' para ver la ayuda\n")
        exit(1)

if __name__ == "__main__":
    main()