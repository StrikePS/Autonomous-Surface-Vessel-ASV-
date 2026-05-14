class XbusPacket:
    def __init__(self, on_data_available=None):
        self.on_data_available = on_data_available
        self.reset()

    def reset(self):
        self.buffer = []

    def feed_byte(self, byte):
        b = byte[0]

        self.buffer.append(b)

        # Resynchronize to FA FF
        while len(self.buffer) >= 2 and not (self.buffer[0] == 0xFA and self.buffer[1] == 0xFF):
            self.buffer.pop(0)

        # Need at least header + id + length
        if len(self.buffer) < 4:
            return

        msg_id = self.buffer[2]
        length = self.buffer[3]

        total_len = 2 + 1 + 1 + length + 1  # FA FF | ID | LEN | PAYLOAD | CHECKSUM

        if len(self.buffer) < total_len:
            return

        packet = self.buffer[:total_len]

        if self.validate_checksum(packet):
            packet_bytes = [bytes([b]) for b in packet]
            if self.on_data_available:
                self.on_data_available(packet_bytes)
            del self.buffer[:total_len]
        else:
            # Drop first byte and try to resync
            del self.buffer[0]

    def is_packet_complete(self):
        # Ensure expected_length is an integer
        return self.length_valid and len(self.buffer) == (3 + 1 + self.expected_length + 1)

    def compute_checksum(self, packet):
        return (-sum(packet[1:-1])) & 0xFF

    def validate_checksum(self, packet):
        return self.compute_checksum(packet) == packet[-1]
