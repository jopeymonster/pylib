import os
import subprocess
import socket
import argparse

def get_local_ip():
    try:
        # Get the local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def get_user_input():
    # Ask for server type
    print("Which type of server would you like to run?\n"
          "1. Multi-device local network server\n"
          "2. Secure local host\n")
    server_type = input("Type 1 or 2: ")
    while server_type not in ['1', '2']:
        print("Invalid input. Please enter 1 or 2.")
        server_type = input("Type 1 or 2: ")
    # Ask for port
    print("What port would you like to run on?\n"
          "Indicate '8xxx' with x being numbers for a port format: 8xxx\n")
    port = input("Enter port (Leave blank for default, 8000): ")
    if not port:
        port = '8000'
    elif not (port.isdigit() and len(port) == 4 and port.startswith('8')):
        print("Invalid port format. Using default port 8000.")
        port = '8000'
    # Ask for file path
    file_path = input("Enter the file path or leave blank to use 'index.html' in current working directory: ")
    if not file_path:
        file_path = 'index.html'
    return server_type, port, file_path

def construct_command(server_type, port, local_ip, file_path):
    if server_type == '1':
        command = f"python -m http.server {port}"
    else:
        command = f"python -m http.server {port} --bind {local_ip}"
    return command

def main():
    go_server = False
    parser = argparse.ArgumentParser(description="Start a simple HTTP server.")
    parser.add_argument('--instant', type=bool, default=False, help="Start up a server with all default values immediately")
    parser.add_argument('--type', type=int, choices=[1, 2], default=2, help="1 for Multi-device local network server, 2 for Secure local host")
    parser.add_argument('--port', type=str, default='8000', help="Port number to run the server on (default: 8000)")
    parser.add_argument('--file', type=str, help="File path to serve (default: index.html)")
    args = parser.parse_args()
    if args.instant:
        go_server = True
        server_type = '2' 
        port = '8000'
        file_path = 'index.html'
    elif args.type and args.port and args.file:
        server_type = str(args.type)
        port = args.port
        file_path = args.file
    else:
        local_ip = get_local_ip()
        if not local_ip:
            print("Could not determine the local IP address. Exiting.")
            return
        server_type, port, file_path = get_user_input()
    command = construct_command(server_type, port, get_local_ip(), file_path)
    # check for instant server
    if go_server == True:
        print(f"Running the command: {command}")
        try:
            # Change directory to the path containing the file if specified
            if file_path != 'index.html':
                os.chdir(os.path.dirname(file_path))
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        # Confirm the command with the user
        if server_type == '1': 
            server_secure = 'No'
        else: 
            server_secure = 'Yes'
        print(f"Server IP: {get_local_ip()}\n"
              f"Server Port: {port}\n"
              f"Server Local Device Only? {server_secure}\n"
              f"Server file to use: {file_path}")
        confirmation = input("Is this correct? (y/n): ")
        if confirmation.lower() == 'y':
            # Run the command
            print(f"Running the command: {command}")
            try:
                # Change directory to the path containing the file if specified
                if file_path != 'index.html':
                    os.chdir(os.path.dirname(file_path))
                subprocess.run(command, shell=True)
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Command execution cancelled.")

if __name__ == "__main__":
    main()
