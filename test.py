import time
import os
import subprocess
import argparse
import re

def execute_traceroute(destination):
    """
    Executes a traceroute to the specified destination and returns the output.
    Args:
        destination (str): The hostname or IP address to trace
    Returns:
        str: The raw output from the traceroute command
    """
    # Your code here
    # Hint: Use the subprocess module to run the traceroute command
    # Make sure to handle potential errors
    # Remove this line once you implement the function,
    # and don't forget to *return* the output

    # trace = subprocess.run(["traceroute", "-I", destination], stdout=subprocess.PIPE)
    # return trace.stdout.decode("utf-8")
    try:
        print("Running traceroute...")
        result = subprocess.run(["traceroute", "-I", destination], check=True, text=True)
        # Run the traceroute command and capture the output
        return str(result.stdout)
    except Exception as e:
        print("error {}".format(e))
        return str(e)

def parse_traceroute(traceroute_output):
    """
    Parses the raw traceroute output into a structured format.
    Args:
        traceroute_output (str): Raw output from the traceroute command
    Returns:
        list: A list of dictionaries, each containing information about a hop:
            - 'hop': The hop number (int)
            - 'ip': The IP address of the router (str or None if timeout)
            - 'hostname': The hostname of the router (str or None if same as ip)
            - 'rtt': List of round-trip times in ms (list of floats, None for timeouts)
    Example:
    ```
        [
            {
                'hop': 1,
                'ip': '172.21.160.1',
                'hostname': 'HELDMANBACK.mshome.net',
                'rtt': [0.334, 0.311, 0.302]
            },
            {
                'hop': 2,
                'ip': '10.103.29.254',
                'hostname': None,
                'rtt': [3.638, 3.630, 3.624]
            },
            {
                'hop': 3,
                'ip': None,  # For timeout/asterisk
                'hostname': None,
                'rtt': [None, None, None]
            }
        ]
    ```
    """
    # Your code here
    # Hint: Use regular expressions to extract the relevant information
    # Handle timeouts (asterisks) appropriately
    # Remove this line once you implement the function,
    # and don't forget to *return* the output
    
    # hops = []
    # lines = traceroute_output.splitlines()
    # hop_regex = re.compile(r'^\s*(\d+)\s+(\S+)\s+\((\S+)\)\s+([\d.]+)\s+ms\s+([\d.]+)\s+ms\s+([\d.]+)\s+ms')
    # timeout_regex = re.compile(r'^\s*(\d+)\s+\*')

    # for line in lines:
    #     hop_match = hop_regex.match(line)
    #     timeout_match = timeout_regex.match(line)
    #     if hop_match:
    #         hop = int(hop_match.group(1))
    #         hostname = hop_match.group(2)
    #         ip = hop_match.group(3)
    #         rtt = [float(hop_match.group(4)), float(hop_match.group(5)), float(hop_match.group(6))]
    #         hops.append({'hop': hop, 'ip': ip, 'hostname': hostname, 'rtt': rtt})
    #     elif timeout_match:
    #         hop = int(timeout_match.group(1))
    #         hops.append({'hop': hop, 'ip': None, 'hostname': None, 'rtt': [None, None, None]})

    # return hops
    pass

addresses = execute_traceroute("google.com")
parsed_addresses = parse_traceroute(addresses)
print(parsed_addresses)
