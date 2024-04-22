import netmiko
#datos para poder solicitar la conexión hacia el router
ip = input("Ingrese la ip: ")
usuario = input("Ingrese el usuario: ")
contraseña = input("Ingrese la contraseña: ")
router = 'cisco_ios'

#establece la conexción de SSH con el router
net_connect = netmiko.ConnectHandler(device_type = router, host = ip, port = 22, username = usuario, password = contraseña)
net_connect.enable()

#se ingresa el nuevo nombre asignado
new_hostname = input("Ingrese el nuevo hostname: ")
#comando para cambiar el hostname
config_commands = [f'hostname {new_hostname}']
#envío del comando
comando = net_connect.send_config_set(config_commands)
#imprimir comando
print(comando)
#cerrar conexión
net_connect.disconnect()