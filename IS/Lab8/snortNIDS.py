from scapy.all import sniff, IP, TCP, UDP
import re

# User input for Snort rules
print("Enter Snort rules (format: alert protocol any any -> any port (msg:'message'; content:'pattern';))")
print("Example: alert tcp any any -> any 80 (msg:'HTTP Attack'; content:'GET';)")
rules = []
while True:
    rule = input("Rule (or 'done'): ").strip()
    if rule.lower() == 'done':
        break
    rules.append(rule)

# Parse rules
parsed_rules = []
for rule in rules:
    match = re.search(r'alert (\w+) .* -> .* (\d+) .*msg:\'([^\']+)\'; content:\'([^\']+)\'', rule)
    if match:
        parsed_rules.append({
            'protocol': match.group(1).upper(),
            'port': int(match.group(2)),
            'msg': match.group(3),
            'content': match.group(4)
        })

# Packet analyzer
def analyze_packet(packet):
    if IP in packet:
        proto = packet[IP].proto
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        for rule in parsed_rules:
            if (rule['protocol'] == 'TCP' and TCP in packet and packet[TCP].dport == rule['port']) or \
               (rule['protocol'] == 'UDP' and UDP in packet and packet[UDP].dport == rule['port']):
                payload = bytes(packet[TCP].payload if TCP in packet else packet[UDP].payload)
                if rule['content'].encode() in payload:
                    print(f"\n[ALERT] {rule['msg']}")
                    print(f"  {src_ip} -> {dst_ip}:{rule['port']}")
                    print(f"  Content matched: {rule['content']}")

# Capture traffic
interface = input("\nEnter network interface (e.g., eth0, wlan0): ").strip()
packet_count = int(input("Enter number of packets to capture: "))
print(f"\nCapturing {packet_count} packets on {interface}...\n")
sniff(iface=interface, prn=analyze_packet, count=packet_count)
print("\nCapture complete. Logs analyzed.")
