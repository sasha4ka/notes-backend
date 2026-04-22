import socket
import time
import os


def wait_for_port(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"Port {port} is available!")
                break
        except OSError:
            print(f"Waiting for database at {host}:{port}...")
            time.sleep(1)


if __name__ == "__main__":
    db_host = os.getenv("DB_HOST", "postgres_db")
    wait_for_port(db_host, 5432)
