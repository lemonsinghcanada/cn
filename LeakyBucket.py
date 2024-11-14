import time

class Packet:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def getSize(self):
        return self.size

    def getId(self):
        return self.id

class LeakyBucket:
    def __init__(self, leakRate, size):
        self.leakRate = leakRate
        self.bufferSizeLimit = size
        self.buffer = []
        self.currBufferSize = 0

    def addPacket(self, newPacket):
        if self.currBufferSize + newPacket.getSize() > self.bufferSizeLimit:
            print("Bucket is full. Packet rejected.")
            return
        self.buffer.append(newPacket)
        self.currBufferSize += newPacket.getSize()
        print("Packet with id = " + str(newPacket.getId()) + " added to bucket.")

    def transmit(self):
        if len(self.buffer) == 0:
            print("No packets in the bucket.")
            return False  # Buffer is empty, so return False

        n = self.leakRate
        while len(self.buffer) > 0 and n > 0:
            topPacket = self.buffer[0]
            topPacketSize = topPacket.getSize()
            if topPacketSize > n:
                break
            self.currBufferSize -= topPacketSize
            self.buffer.pop(0)
            n -= topPacketSize
            print("Packet with id = " + str(topPacket.getId()) + " transmitted.")

        # Check if the buffer is empty after transmission
        return len(self.buffer) > 0

if __name__ == '__main__':
    bucket = LeakyBucket(1500, 10000)  # Increased leakRate for faster emptying

    # Add a fixed batch of packets
    packets = [Packet(1, 200), Packet(2, 500), Packet(3, 400), Packet(4, 500), Packet(5, 300)]
    for packet in packets:
        bucket.addPacket(packet)

    # Transmit loop
    while True:
        bufferNotEmpty = bucket.transmit()
        if not bufferNotEmpty:
            print("All packets transmitted. Buffer is empty.")
            break
        print("Waiting for next tick.")
        time.sleep(1)
