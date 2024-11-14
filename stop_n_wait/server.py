import socket
import struct
import logging

packets_received = 0
packets_limit = 5

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(message)s",
                    datefmt="%H:%M:%S")

# Create a TCP/IP socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 3300)
server_sock.bind(server_address)

# Listen for incoming connections
server_sock.listen(1)
print("Server is listening on port 3300...")

# Wait for a connection
connection, client_address = server_sock.accept()
print(f"Connection from {client_address}")

# Pack a packet with sequence number and data
def pack_packet(seq_no, data):
    data_bytes = data.encode()
    return struct.pack("!II", seq_no, len(data_bytes)) + data_bytes

# Start communication with the client
seq_no = 0
while seq_no < packets_limit:
    try:
        # Send a packet
        message = f"Message {seq_no}"
        packet = pack_packet(seq_no, message)
        connection.sendall(packet)
        logging.info(f"Sent packet: {message}")

        # Receive acknowledgment
        ack = connection.recv(1024)
        if not ack:
            break

        ack_seq_no, ack_type = struct.unpack("!I 3s", ack)
        logging.info(f"Received ACK for packet: {ack_seq_no}")

        # Increment sequence number
        seq_no += 1

    except Exception as e:
        logging.error(f"Server error: {e}")
        break

connection.close()
server_sock.close()
print("Server connection closed.")
