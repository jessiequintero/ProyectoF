#1er intento
import netmiko

def establecer_conexion(ip, usuario, contraseña, router):
    """
    Establece la conexión SSH con el router.
    """
    net_connect = netmiko.ConnectHandler(device_type=router, host=ip, port=22, username=usuario, password=contraseña)
    net_connect.enable()
    return net_connect

def cambiar_hostname(net_connect):
    """
    Cambia el hostname del router.
    """
    new_hostname = input("Ingrese el nuevo hostname: ")
    config_commands = [f'hostname {new_hostname}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def abrir_terminal(net_connect):
    """
    Abrir la terminal del dispositivo
    """
    print("Se abrirá la terminal del dispositivo. Por favor, ingrese las configuraciones directamente.")
    print("Cuando haya terminado, escriba 'exit' para salir de la sesión interactiva.")
    net_connect.send_command("terminal length 0")
    net_connect.send_config_set_interactive()
    print("Configuraciones aplicadas exitosamente.")

def cerrar_conexion(net_connect):
    """
    Cierra la conexión SSH con el router.
    """
    net_connect.disconnect()

# Datos para la conexión
ip = input("Ingrese la ip: ")
usuario = input("Ingrese el usuario: ")
contraseña = input("Ingrese la contraseña: ")
router = 'cisco_ios'

# Establecer conexión
conexion = establecer_conexion(ip, usuario, contraseña, router)

# Cambiar hostname
cambiar_hostname(conexion)

# Cerrar conexión
cerrar_conexion(conexion)
