
Este script es un escáner de red que permite escanear hosts activos en un rango de direcciones IP y puertos abiertos en una dirección IP específica. Utiliza la librería `scapy` para escanear hosts y `nmap` para escanear puertos.

Para utilizar este script, es necesario tener instaladas las librerías `scapy`, `colorama`, `argparse`, `nmap` y `pyfiglet`. Puedes instalarlas con el comando `pip install <nombre_de_la_libreria>`.

El script cuenta con los siguientes argumentos:

- `-r` o `--rango`: permite especificar un rango de direcciones IP a escanear.
- `-p` o `--ports`: permite especificar una lista de puertos a escanear junto con el argumento `-s`.
- `-s` o `--scan`: permite especificar una dirección IP a la cual se le realizará un escaneo de puertos abiertos.

Ejemplo de uso:

```python script.py -r 192.168.1.0/24```

Este comando escaneará todos los hosts activos en el rango de direcciones `192.168.1.0/24` y mostrará su dirección IP y dirección MAC.

```python script.py -s 192.168.1.5```

Este comando escaneará todos los puertos abiertos en el host especificado, en este caso `192.168.1.5`

```python script.py -s 192.168.1.5 -p "[53, 80, 139, 443, 445]"```

Este comando escaneará la dirección IP `192.168.1.5` en busca de los puertos especificados en la lista y mostrará información sobre cada puerto abierto encontrado.


Acciones necesarias antes de ejecutar el script:

**Instalar XCLIP en linux con:**

```sudo apt install xclip```


**Instalar nmap en linux con:**

```sudo apt install nmap```
