# This small app connects to a ssh and check if an existing
# folder has the permission that we looking for
# in order to use, please install paramiko, using:
# 'pip install paramiko' (you can find pip.exe in python scripts folder)
import paramiko

folder_name = "temp"
folder_permission = b'755'
ssh_host = "158.69.201.134"
ssh_user = "ConKia"
ssh_psswd = "97383ffbfb50daa71aa173d7"
client = paramiko.client.SSHClient()

def con_SSH(ssh_host, ssh_user, ssh_psswd):
	client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
	try:
		client.connect(hostname=ssh_host, username=ssh_user, password=ssh_psswd)
	except paramiko.ssh_exception.AuthenticationException:
		print("Username or Password is incorrect!")
		end()
	except TimeoutError:
		print("Timeout error, please provide a working SSH host")
		end()
	except:
		print("Error during connection")
		end()
	print("Successfully connected to " + ssh_host + "\n")
	check_permission(folder_name, folder_permission)
	client.close()
	print("Disconnected from " + ssh_host)
	end()

def check_permission(folder_name, folder_permission):
	stdin_, stdout_, stderr_ = client.exec_command("ls -d " + folder_name)
	# Check for folder
	if folder_name in stdout_.read().decode('utf-8'):
		print("OK: Folder exist, proceed to the next step")
		stdin_, stdout_, stderr_ = client.exec_command("stat --format '%a' "+ folder_name)
		line = stdout_.read()
		# Check for permission match
		if folder_permission in line:
				print("OK: The folder permission is the expected value: " + line.decode('utf-8'))
		else:
				print("ERROR: The folder permission is not the expected value: " +
          line.decode('utf-8') + " <> " + folder_permission.decode('utf-8'))
	else:
		print("ERROR: Folder does not exist")
	return

def end():
	print("Program ended")
	exit()

con_SSH(ssh_host, ssh_user, ssh_psswd)
