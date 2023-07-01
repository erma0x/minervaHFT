import socket
import threading
import statistics
from binance.client import Client

# Definisci la porta su cui i nodi si connetteranno
PORT = 5000

# Definisci la chiave API e il segreto per accedere all'API di Binance
API_KEY = 'YOUR_BINANCE_API_KEY'
API_SECRET = 'YOUR_BINANCE_API_SECRET'

# Crea un oggetto Client per interagire con l'API di Binance
client = Client()

# Lista per i dati ricevuti dai nodi
received_data = []

# Funzione per gestire la connessione di un nodo
def handle_connection(conn, addr):
    global received_data

    # Ottieni i dati dell'orderbook da Binance
    orderbook_data = client.get_order_book(symbol='BNBBTC', limit=5)

    # Ricevi i dati inviati dal nodo
    received_orderbook_data = conn.recv(1024).decode()

    # Aggiungi i dati ricevuti alla lista
    received_data.append(eval(received_orderbook_data))

    # Chiudi la connessione
    conn.close()

# Funzione per avviare il nodo e iniziare l'ascolto delle connessioni
def start_node():
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Collega il socket alla porta specificata
    server_socket.bind(('localhost', PORT))

    # Inizia l'ascolto delle connessioni in arrivo
    server_socket.listen()

    while True:
        # Accetta una connessione in arrivo
        conn, addr = server_socket.accept()

        # Avvia un thread per gestire la connessione
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()

# Funzione per connettersi ai nodi e inviare i dati dell'orderbook
def send_data_to_nodes():
    # Indirizzi IP dei nodi
    nodes = ['localhost', 'localhost', 'localhost']

    for node in nodes:
        # Crea un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connetti il socket all'indirizzo del nodo
        client_socket.connect((node, PORT))

        # Ottieni i dati dell'orderbook da Binance
        orderbook_data = client.get_order_book(symbol='BNBBTC', limit=5)

        # Invia i dati dell'orderbook al nodo
        client_socket.send(str(orderbook_data).encode())

        # Chiudi la connessione
        client_socket.close()

# Avvia i nodi in background
node_thread = threading.Thread(target=start_node)
node_thread.start()

# Invia i dati dell'orderbook ai nodi
send_data_to_nodes()

# Attendi che tutti i nodi inviino i dati
node_thread.join()

# Calcola la stima più affidabile utilizzando la media dei dati
estimated_data = statistics.mean(received_data)

# Stampa la stima più affidabile
print("Stima più affidabile:", estimated_data)

