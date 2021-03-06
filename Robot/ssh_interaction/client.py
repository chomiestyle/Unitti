
from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
from .log import logger


class RemoteClient:


    """self.client : atributo que servirá en última instancia 
    como la objeción de conexión en nuestra clase, similar a 
    cómo ha tratado con terminología como conn en bibliotecas 
    de bases de datos. Nuestra conexión será Ninguna hasta que 
    nos conectemos explícitamente a nuestro host remoto. """

    """self.scp: Similar a self.client, pero maneja exclusivamente conexiones para transferir archivos. """

    """self .__ upload_ssh_key () no es una variable, sino una función que se ejecuta automáticamente cada vez
     que se crea una instancia de nuestro cliente. Llamar a __upload_ssh_key () le está diciendo a nuestro objeto 
     RemoteClient que verifique las claves ssh locales inmediatamente después de la creación para que podamos intentar
      pasarlas a nuestro host remoto. De lo contrario, no podríamos establecer ninguna conexión. """

    def __init__(self, host, user, ssh_key_filepath, remote_path):
        self.host = host
        self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        self.conn = None
        self._upload_ssh_key()

    @logger.catch
    def _get_ssh_key(self):

        """El primero buscará una clave pública almacenada localmente  """

        ##verifica que existe una clave SSH en la ruta que especificamos en nuestra configuración para
        # ser utilizada para conectarse a nuestro host. Si el archivo existe, felizmente configuramos nuestra variable self.ssh_key
        try:
            # Paramiko nos proporciona un submódulo llamado RSAKey para manejar fácilmente
            # todo lo relacionado con la clave RSA, como analizar un archivo de clave privada
            #  en una autenticación de conexión utilizable.

            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            logger.info(f'Found SSH key at self {self.ssh_key_filepath}')
        except SSHException as error:
            logger.error(error)
        return self.ssh_key



    @logger.catch
    def _upload_ssh_key(self):
        """entregará la clave publica encontrada por _get_ssh_key()  a nuestro host remoto"""
        try:
            system(f'ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1')
            system(f'ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')
            logger.info(f'{self.ssh_key_filepath} uploaded to {self.host}')
        except FileNotFoundError as error:
            logger.error(error)

    @logger.catch
    def _connect(self):
        """Open connection to remote host. """
        if self.conn is None:
            try:
                #client = SSHClient () prepara el escenario para
                # crear un objeto que represente a nuestro cliente SSH.
                self.client = SSHClient()
                #load_system_host_keys () indica a nuestro cliente que busque
                # todos los hosts a los que nos hemos conectado en el pasado mirando el archivo known_hosts
                # de nuestro sistema y encontrando las claves SSH que nuestro host espera.
                # Nunca nos hemos conectado a nuestro host en el pasado, por lo que debemos especificar nuestra clave SSH explícitamente.
                self.client.load_system_host_keys()
                #set_missing_host_key_policy () le dice a Paramiko qué hacer en caso de un par de claves desconocido.
                # Se espera una "política" integrada en Paramiko, a la que vamos a especificar AutoAddPolicy ().
                # Establecer nuestra política para "agregar automáticamente" significa que si intentamos conectarnos a un host no reconocido,
                # Paramiko agregará automáticamente la clave faltante localmente.

                self.client.set_missing_host_key_policy(AutoAddPolicy())
                #connect () es el método más importante de SSHClient (como puede imaginar).
                # Finalmente podemos pasar nuestro host, usuario y clave SSH para lograr lo que todos estábamos esperando:
                # ¡una gloriosa conexión SSH en nuestro servidor!
                # El método connect () permite una gran flexibilidad a través de una amplia gama de argumentos de palabras clave opcionales
                # también. Sucede que paso algunos aquí: configurar look_for_keys en True le da a Paramiko permiso para mirar alrededor en
                # nuestra carpeta ~ / .ssh para descubrir las claves SSH por sí mismo, y configurar el tiempo de espera cerrará automáticamente
                # las conexiones que probablemente olvidaremos cerrar. Incluso podríamos pasar variables para cosas como puerto y contraseña,
                # si hubiéramos elegido conectarnos a nuestro host de esta manera.
                self.client.connect(
                    self.host,
                    username=self.user,
                    key_filename=self.ssh_key_filepath,
                    look_for_keys=True,
                    timeout=5000
                )
                self.scp = SCPClient(self.client.get_transport())
            except AuthenticationException as error:
                logger.error(f'Authentication failed: did you remember to create an SSH key? {error}')
                raise error
        return self.client

    def disconnect(self):
        """Close ssh connection."""
        #establecer self.client.close () en realidad establece self.client en None,
        # lo cual es útil en los casos en los que es posible que desee verificar si una conexión ya está abierta
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    @logger.catch
    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of paths to local files.
        :type files: List[str]
        """
        self.conn = self._connect()
        uploads = [self._upload_single_file(file) for file in files]
        logger.info(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}')

    def _upload_single_file(self, file):
        """Upload a single file to a remote directory."""
        upload = None
        try:
            self.scp.put(
                file,
                recursive=True,
                remote_path=self.remote_path
            )
            upload = file
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            logger.info(f'Uploaded {file} to {self.remote_path}')
            return upload

    def download_file(self, file):
        """Download file from remote host."""
        self.conn = self._connect()
        self.scp.get(file)

    @logger.catch
    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        self.conn = self._connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')