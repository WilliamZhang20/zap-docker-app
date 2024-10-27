import socket
import subprocess
import signal

shutdown = False

def signal_handler(sig, frame):
    global shutdown
    shutdown = True

signal.signal(signal.SIGINT, signal_handler)

def start_server():
    report_file = 'my_zap_report.html'
    host = '0.0.0.0'  # Listen on all interfaces
    port = 3030       # The port on which to listen

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Listening for connections on {host}:{port}")

        while not shutdown:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by: {addr}")
                data = conn.recv(1024)  # Buffer size
                if not data:
                    break
                website_link = data.decode('utf-8')
                print(f"Received link: {website_link}")

                response_message = f"Received and processing: {website_link}"
                conn.sendall(response_message.encode('utf-8'))  # Send response

                # Simulate scanning process
                # Made scan running the last task!
                print("Running scan")
                subprocess.run(['zap-full-scan.py', '-t', f'{website_link}', '-r', f'/zap/wrk/{report_file}'])

if __name__ == "__main__":
    start_server()
