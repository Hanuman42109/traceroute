# Python Traceroute Lab

This repository contains a Python implementation of a **traceroute** tool for network path discovery.

## Description
The Python traceroute program determines the route taken by packets across an IP network to a specified destination. It shows each hop along the path and the round-trip time (RTT) for each hop.

## Features
- Sends ICMP or UDP packets with increasing TTL (Time-To-Live)
- Displays IP addresses of intermediate routers/hops
- Measures round-trip time (RTT) for each hop
- Handles unreachable hosts or timeouts gracefully

## Requirements
- Python 3.x
- Administrator privileges (required for raw socket operations on most OS)
- `socket`, `sys`, and `time` Python standard libraries

## Usage
```bash
sudo python3 traceroute.py <destination_host>

## Example
```bash
sudo python3 traceroute.py google.com

## Output
- The program prints each hop with RTT in milliseconds. Example:
```bash
Traceroute to: google.com

  1    rtt=0 ms    172.29.32.1
  2    rtt=2 ms    192.168.0.1
  3    rtt=10 ms   142.250.72.238
  4    rtt=15 ms   108.170.250.193
  ...

## Notes
- Some hops may not respond (*) if ICMP packets are blocked by firewalls.
- Use sudo on Linux/Mac to allow raw socket operations.