#1er intento
import netmiko

def establecer_conexion(ip, usuario, contraseña, router):
    """
    Establece la conexión SSH con el router.
    """
    net_connect = netmiko.ConnectHandler(device_type=router, host=ip, port=22, username=usuario, password=contraseña)
    net_connect.enable()
    return net_connect

def cambiar_hostname(net_connect, new_hostname):
    """
    Cambia el hostname del router.
    """
    config_commands = [f'hostname {new_hostname}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def cambiar_banner(net_connect, banner_text):
    """
    Cambia el banner del router.
    """
    config_commands = ["banner motd #"+banner_text+"#"]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def cambiar_descripcion_interfaz(net_connect, interfaz, descripcion):
    """
    Cambia la descripción de una interfaz.
    """
    config_commands = [f'interface {interfaz}', f'description {descripcion}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_contraseña(net_connect, contraseña):
    """
    Configura la contraseña de modo ejecutivo privilegiado (modo enable).
    """
    config_commands = f"enable secret {contraseña}"
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def agregar_usuario(net_connect, username, password, privilege_level):
    """
    Agrega un usuario al dispositivo con la contraseña especificada y nivel de privilegio.
    """
    config_commands = [f'username {username} privilege {privilege_level} secret {password}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def crear_acl(net_connect, acl_number, acl_type, source, destination=None, permit=True):
    """
    Crea una lista de acceso en el dispositivo.
    
    Parámetros:
        - acl_number: El número de la lista de acceso
        - acl_type: El tipo de lista de acceso
        - source: La dirección IP de origen
        - destination: La dirección IP de destino
        - permit: Booleano, permitir o denegar el tráfico
    """
    if acl_type == 'standard':
        if permit:
            action = 'permit'
        else:
            action = 'deny'
        config_commands = [f'access-list {acl_number} {action} {source}']
    elif acl_type == 'extended':
        if permit:
            action = 'permit'
        else:
            action = 'deny'
        config_commands = [f'access-list {acl_number} {action} {source} {destination}']
    else:
        print("Tipo de lista de acceso no válido. Debe ser 'standard' o 'extended'.")
        return
    
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def cambiar_ipv4(net_connect, interfaz, nueva_ip, mascara):
    """
    Cambia la dirección IPv4 de una interfaz del dispositivo.
    """
    config_commands = [f'interface {interfaz}', f'ip address {nueva_ip} {mascara}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def cambiar_ipv6(net_connect, interfaz, nueva_ipv6, mascara_prefix):
    """
    Cambia la dirección IPv6 de una interfaz del dispositivo.
    """
    config_commands = [f'interface {interfaz}', f'ipv6 address {nueva_ipv6}/{mascara_prefix}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def activar_enrutamiento_ipv6(net_connect):
    """
    Activa el enrutamiento IPv6 unicast en el dispositivo.
    """
    config_commands = ['ipv6 unicast-routing']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def excluir_dhcp_ipv4(net_connect, start_ip, end_ip):
    """
    Excluye un rango de direcciones IP del servidor DHCPv4.
    """
    config_commands = [f'ip dhcp excluded-address {start_ip} {end_ip}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_dhcp_ipv4(net_connect, pool_name, network, subnet_mask, default_router, dns_server, domain_name):
    """
    Configura un servidor DHCPv4 en el dispositivo.
    """
    config_commands = [
        f'ip dhcp pool {pool_name}',
        f'network {network} {subnet_mask}',
        f'default-router {default_router}',
        f'dns-server {dns_server}',
        f'domain-name {domain_name}',
        f'end'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_dhcp_ipv6(net_connect, pool_name, prefix, dns_server, domain_name, interface_ip, dhcp_server_name, stateful_stateless):
    """
    Configura un servidor DHCPv6 en el dispositivo.
    """
    config_commands = [
        'ipv6 unicast-routing',  # Activar enrutamiento IPv6 unicast si no está activado
        f'ipv6 dhcp pool {pool_name}',
        f'address prefix {prefix}',
        f'dns-server {dns_server}',
        f'domain-name {domain_name}',
        f'interface {interface_ip}',
        f'ipv6 dhcp server {dhcp_server_name}',
        f'ipv6 nd {stateful_stateless}'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_nat(net_connect, nat_type, inside_local, access_list, pool_name=None, inside_global=None, outside_global=None, netmask=None):
    """
    Configura NAT en el dispositivo.
        net_connect: Objeto de conexión netmiko.
        nat_type: Tipo de NAT: 'estatico', 'dinamico' o 'pat'.
        inside_local: Dirección IP local dentro de la red privada.
        access_list: Nombre de la lista de acceso para el tráfico.
        pool_name: Nombre de la pool para NAT dinámico.
        inside_global: Dirección IP global dentro de la red privada (solo para NAT estático).
        outside_global: Dirección IP global fuera de la red privada (solo para NAT dinámico y PAT).
        netmask: Máscara de red para NAT dinámico (solo si se especifica una pool).
    """
    config_commands = []
    
    if nat_type == 'estatico':
        config_commands.append(f'ip nat inside source static {inside_local} {inside_global}')
    elif nat_type == 'dinamico':
        if not pool_name:
            print("Se requiere especificar un nombre de pool para NAT dinámico.")
            return
        config_commands.append(f'ip nat pool {pool_name} {outside_global} {outside_global} netmask {netmask}')
        config_commands.append(f'ip nat inside source list {access_list} pool {pool_name}')
    elif nat_type == 'pat':
        config_commands.append(f'ip nat inside source list {access_list} interface {outside_global} overload')
    else:
        print("Tipo de NAT no válido. Debe ser 'estatico', 'dinamico' o 'pat'.")
        return
    
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_interfaz_nat(net_connect, interface, direction):
    """
        net_connect: Objeto de conexión netmiko.
        interface (str): Nombre de la interfaz.
        direction (str): Dirección de la interfaz para NAT: 'inside' o 'outside'.
    """
    if direction not in ['inside', 'outside']:
        print("Dirección de la interfaz no válida. Debe ser 'inside' o 'outside'.")
        return
    
    config_commands = [f'interface {interface}', f'ip nat {direction}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_ip_switch(net_connect, interface, ip_address, subnet_mask):
    """
    Configura una dirección IP en una interfaz de administración de un switch Cisco.
        interface: Nombre de la interfaz vlan
        ip_address: Dirección IP que se asignará a la interfaz de administración.
        subnet_mask: Máscara de subred para la dirección IP.
    """
    config_commands = [
        f'interface {interface}',
        f'ip address {ip_address} {subnet_mask}',
        'no shutdown'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_default_gateway(net_connect, gateway):
    """
    Configura la puerta de enlace predeterminada en un switch Cisco.

        net_connect: Objeto de conexión netmiko.
        gateway: Dirección IP de la puerta de enlace predeterminada.
    """
    config_commands = [f'ip default-gateway {gateway}']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_troncales(net_connect, interface_range):
    """
    Configura un rango de interfaces como troncales en un switch Cisco.
        net_connect: Objeto de conexión netmiko.
        interface_range (str): Rango de interfaces a configurar como troncales (por ejemplo, 'GigabitEthernet0/1-24').
    """
    config_commands = [f'interface range {interface_range}', 'switchport mode trunk']
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_vtp_server(net_connect, vtp_domain, vtp_password):
    """
    Configura el dominio VTP y la contraseña en un switch Cisco.
        net_connect: Objeto de conexión netmiko.
        vtp_domain: Nombre del dominio VTP.
        vtp_password: Contraseña del dominio VTP.
    """
    config_commands = [
        f'vtp domain {vtp_domain}',
        f'vtp password {vtp_password}'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def configurar_vtp(net_connect, vtp_domain, vtp_password, mode):
    """
        net_connect: Objeto de conexión netmiko.
        vtp_domain: Nombre del dominio VTP.
        vtp_password: Contraseña del dominio VTP.
        mode: Modo de operación del dispositivo VTP
    """
    if mode not in ['server', 'client']:
        print("Modo de operación VTP no válido. Debe ser 'server' o 'client'.")
        return
    
    config_commands = [
        f'vtp mode {mode}',
        f'vtp domain {vtp_domain}',
        f'vtp password {vtp_password}'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)

def crear_vlan(net_connect, vlan_id, vlan_name, interface_range):
    """
        net_connect: Objeto de conexión netmiko.
        vlan_id: ID de la VLAN a crear.
        vlan_name: Nombre de la VLAN.
        interface_range: Rango de interfaces a configurar en modo de acceso
    """
    config_commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        f'interface range {interface_range}',
        'switchport mode access',
        f'switchport access vlan {vlan_id}'
    ]
    comando = net_connect.send_config_set(config_commands)
    print(comando)


def abrir_terminal(net_connect):
    """
    Abrir la terminal del dispositivo
    """
    print("Se abrirá la terminal del dispositivo. Por favor, ingrese las configuraciones directamente.")
    print("Cuando haya terminado, escriba 'exit' para salir de la sesión interactiva.")
    net_connect.send_command("terminal length 0")
    net_connect.enter_config_mode()
    net_connect.send_config_set_interactive()
    print("Configuraciones aplicadas exitosamente.")

def cerrar_conexion(net_connect):
    """
    Cierra la conexión SSH con el router.
    """
    net_connect.disconnect()

# Datos para la conexión
ip = '192.168.69.1'
usuario = 'gmedina'
contraseña = 'cisco'
router = 'cisco_ios'

# Establecer conexión
conexion = establecer_conexion(ip, usuario, contraseña, router)

configurar_dhcp_ipv4(conexion, 'POOLPRUEBA', '192.168.69.0', '255.255.255.0', '192.168.69.1', '', 'redes.uag.mx')

# Cambiar hostname
cambiar_hostname(conexion, 'RouterJ')

cambiar_hostname(conexion, 'RouterJ')

abrir_terminal(conexion)

# Cerrar conexión
#cerrar_conexion(conexion)
