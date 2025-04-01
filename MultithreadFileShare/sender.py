import socket
import threading
import os
import argparse
from config import CHUNK_SIZE, CHUNKS_PER_PACKAGE, PORT, debug
from tqdm import tqdm

def send_package(sock, data):
    try:
        sock.sendall(data)
    except Exception as e:
        debug(f"Error while sending data: {e}")

def start_sender(ip, port=PORT, file_path='file_to_send.txt'):
    if not os.path.isfile(file_path):
        print(f"[Error] File '{file_path}' not found.")
        return

    file_size = os.path.getsize(file_path)
    debug(f"Connecting to {ip}:{port}")
    debug(f"File size: {file_size} bytes")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        debug("Connected to receiver.")
    except Exception as e:
        print(f"[Error] Could not connect to {ip}:{port} — {e}")
        return

    with open(file_path, 'rb') as f:
        threads = []
        pbar = tqdm(total=file_size, unit="B", unit_scale=True, desc="Sending")

        while True:
            chunks = []
            for _ in range(CHUNKS_PER_PACKAGE):
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                chunks.append(chunk)

            if not chunks:
                break

            package = b''.join(chunks)

            def send_and_update(data):
                send_package(sock, data)
                pbar.update(len(data))

            t = threading.Thread(target=send_and_update, args=(package,))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

        pbar.close()
        debug("All data sent.")

    sock.close()
    print("[Sender] File transfer completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a file to a receiver over TCP.")
    parser.add_argument("ip", help="Receiver IP address")
    parser.add_argument("file_path", help="Path to the file to send")
    parser.add_argument("--port", type=int, default=PORT, help="Port number (default: 5001)")

    args = parser.parse_args()

    start_sender(ip=args.ip, port=args.port, file_path=args.file_path)
