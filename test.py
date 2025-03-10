import subprocess

def execute_traceroute(destination):
    try:
        print("Running traceroute...") 
        # Run the traceroute command and capture the output
        trace = subprocess.run(["traceroute", "-I", destination], stdout=subprocess.PIPE)
        
        return parse_traceroute(str(trace.stdout.decode("utf-8")))
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
    hops = []
    lines = traceroute_output.split("\n")

    for line in lines[1:]:  # Skip the first line
        if line.strip() == "":
            continue
        parts = line.split()
        if len(parts) < 8:
            # Handle lines with missing information (e.g., timeouts)
            hop = int(parts[0])
            ip = parts[1] if len(parts) > 1 else None
            hostname = parts[2] if len(parts) > 2 else None
            rtt = [None, None, None]
            for i, part in enumerate(parts[3:]):
                if part.endswith("ms"):
                    rtt[i] = part.replace("ms", "")
                else:
                    rtt[i] = None
        else:
            hop = int(parts[0])
            ip = parts[1]
            hostname = parts[2]
            rtt = [parts[3].replace("ms", ""), parts[5].replace("ms", ""), parts[7].replace("ms", "")]
        hops.append({
            'hop': hop,
            'ip': ip,
            'hostname': hostname,
            'rtt': rtt
        })
        # Format the output with newlines using f-strings
        formatted_output = "\n".join(
            [f"""
            hop: {hop['hop']}
            ip: {hop['ip']}
            hostname: {hop['hostname']}
            rtt: {hop['rtt']}
            """ for hop in hops]
                )
    return formatted_output
print(execute_traceroute("google.com"))
