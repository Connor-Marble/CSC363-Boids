import argparse
import random
import time


from pythonosc import udp_client


if __name__ == "__main__":
    client = udp_client.SimpleUDPClient("127.0.0.1",5892)
    
    while True:
        client.send_message("/process", input())
                        







                        
