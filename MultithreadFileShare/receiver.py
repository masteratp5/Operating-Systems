import socket
from config import CHUNK_SIZE, CHUNKS_PER_PACKAGE, PORT, debug
from tqdm import tqdm

def handle_client(conn, output_file):
    with open(output_file, 'wb') as f:
        total_received = 0
        pbar = tqdm(unit="B", unit_scale=True, desc="Receiving")

        while True:
            data = conn.recv(CHUNK_SIZE * CHUNKS_PER_PACKAGE)
            if not data:
                break
            f.write(data)
            total_received += len(data)
            pbar.update(len(data))

        pbar.close()
        debug(f"Total bytes received: {total_received}")

    conn.close()
    debug("Connection closed.")

def start_receiver(ip='0.0.0.0', port=PORT, output_file='received_file.txt'):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(f"[Receiver] Listening on {ip}:{port}...")

    conn, addr = server.accept()
    print(f"[Receiver] Connected by {addr}")
    handle_client(conn, output_file)

    server.close()

if __name__ == "__main__":
    start_receiver()