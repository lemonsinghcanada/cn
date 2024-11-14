import socket
import sys
import struct
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(message)s",
                    datefmt="%H:%M:%S")

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_port = int(sys.argv[1]) if len(sys.argv) > 1 else 3300
sock.connect(("localhost", server_port))

# Variables
recvd_data = []
expected_seq_no = 0

def to_network_layer(data):
    recvd_data.append(data)

def unpack_packet(packet):
    """Unpacks the packet and returns seq_no, data, and a corrupt flag."""
    try:
        seq_no, data_length = struct.unpack("!II", packet[:8])
        data = packet[8:8 + data_length].decode()
        return seq_no, data, False  # In this case, we assume no corruption
    except Exception as e:
        logging.debug(f"Failed to unpack packet: {e}")
        return None, None, True

def create_ack_packet(seq_no):
    """Creates an ACK packet with the sequence number."""
    return struct.pack("!II", seq_no, 1)  # 1 represents ACK type for simplicity

# Main loop
while True:
    try:
        # Receive packet
        packet = sock.recv(1024)
        if not packet:
            break

        # Unpack the received packet
        seq_no, data, corrupt = unpack_packet(packet)

        if corrupt:
            logging.debug("Dropping corrupt packet")
            continue

        # Check sequence number
        if seq_no == expected_seq_no:
            # Process the correct packet
            to_network_layer(data)
            logging.info("Packet received: %s", data)

            # Increment expected sequence number for next packet
            expected_seq_no += 1
        else:
            logging.info("Packet arrived out of order")

        # Send acknowledgment for the last correctly received packet
        ack_packet = create_ack_packet(expected_seq_no - 1)
        sock.send(ack_packet)
        logging.info("Sent ACK for packet: %d", expected_seq_no - 1)

    except ConnectionResetError:
        logging.error("Connection reset by peer.")
        break
    except KeyboardInterrupt:
        break
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        break

logging.info("Closing connection..")
sock.close()

logging.info("Data received: %s", ''.join(recvd_data))
sys.exit(0)
