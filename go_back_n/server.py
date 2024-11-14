import socket
import random
import time

# Configuration
WINDOW_SIZE = 4
TOTAL_PACKETS = 10
PACKET_LOSS_PROBABILITY = 0.2  # 20% chance to simulate packet loss

# Set up socket for sender
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.settimeout(2)
server_address = ('localhost', 12345)

def send_packet(seq_num):
    """Sends a packet with the given sequence number."""
    message = f"Packet {seq_num}"
    sender_socket.sendto(message.encode(), server_address)
    print(f"Sent: {message}")

def simulate_ack_loss():
    """Simulates ACK loss based on the defined probability."""
    return random.random() < PACKET_LOSS_PROBABILITY

# Go-Back-N protocol
base = 0
next_seq_num = 0

while base < TOTAL_PACKETS:
    # Send packets in the window
    while next_seq_num < base + WINDOW_SIZE and next_seq_num < TOTAL_PACKETS:
        send_packet(next_seq_num)
        next_seq_num += 1
    
    # Wait for acknowledgments
    try:
        ack, _ = sender_socket.recvfrom(1024)
        ack = int(ack.decode().split()[1])  # Extract ACK number
        print(f"Received ACK: {ack}")

        # Slide the window if ACK is within the current window range
        if ack >= base:
            base = ack + 1  # Slide the window

    except socket.timeout:
        print("Timeout! Resending window...")
        # Resend all packets in the current window
        for seq in range(base, next_seq_num):
            send_packet(seq)

print("All packets sent successfully.")
sender_socket.close()
