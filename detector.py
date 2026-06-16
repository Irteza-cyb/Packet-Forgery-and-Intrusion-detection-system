from dataclasses import dataclass
from datetime import datetime


@dataclass
class PacketInfo:
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    sequence_number: int


class Detector:
    """
    Simulated Packet Response Engine

    Demonstrates packet analysis and response generation
    without transmitting any real network traffic.
    """

    def build_response(self, packet: PacketInfo):

        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": packet.source_ip,
            "source_port": packet.source_port,
            "target_port": packet.destination_port,
            "response_type": "SYN-ACK",
            "ack_number": packet.sequence_number + 1
        }

        return response

    def process_packet(self, packet: PacketInfo):

        result = self.build_response(packet)

        print("\n[Detector Engine]")
        print(f"Source IP      : {packet.source_ip}")
        print(f"Source Port    : {packet.source_port}")
        print(f"Target Port    : {packet.destination_port}")
        print("Response Type  : SYN-ACK (Simulated)")
        print(f"ACK Number     : {result['ack_number']}")

        return result


if __name__ == "__main__":

    sample_packet = PacketInfo(
        source_ip="192.168.1.100",
        source_port=45678,
        destination_ip="192.168.1.10",
        destination_port=80,
        sequence_number=1000
    )

    detector = Detector()
    detector.process_packet(sample_packet)
