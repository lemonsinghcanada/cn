import socket
import random

# Configuration
PACKET_LOSS_PROBABILITY = 0.2  # 20% chance to simulate packet loss
TOTAL_PACKETS = 10

# Set up socket for receiver
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(('localhost', 12345))

expected_seq_num = 0

def simulate_packet_loss():
    """Simulates packet loss based on the defined probability."""
    return random.random() < PACKET_LOSS_PROBABILITY

print("Receiver is ready to receive packets...")

# Go-Back-N protocol for receiver
while expected_seq_num < TOTAL_PACKETS:
    packet, addr = receiver_socket.recvfrom(1024)
    seq_num = int(packet.decode().split()[1])  # Extract sequence number

    # Simulate packet loss
    if simulate_packet_loss():
        print(f"Packet {seq_num} lost (simulated).")
        continue

    print(f"Received: Packet {seq_num}")

    # If the packet is the expected sequence number, send ACK and move to next
    if seq_num == expected_seq_num:
        ack_message = f"ACK {seq_num}"
        receiver_socket.sendto(ack_message.encode(), addr)
        print(f"Sent: {ack_message}")
        expected_seq_num += 1
    else:
        # If packet is out of order, re-send ACK for last correctly received packet
        last_ack = expected_seq_num - 1
        ack_message = f"ACK {last_ack}"
        receiver_socket.sendto(ack_message.encode(), addr)
        print(f"Sent: {ack_message}")

print("All packets received successfully.")
receiver_socket.close()
