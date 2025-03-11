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
    hops = []
    lines = traceroute_output.split("\n")

    for line in lines[1:]:  # Skip the first line
        if line.strip() == "":
            continue
        try:
            parts = line.split()
            if len(parts) < 8:
                # Handle lines with missing information (e.g., timeouts)
                hop = int(parts[0])
                ip = None if len(parts) > 1 else parts[1]
                hostname = None if len(parts) > 2 else parts[2]
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
        except Exception as e:
            print(f"Error parsing line: {line}. Error: {e}")
            continue 
        # Format the output with newlines using f-strings
        formatted_output = "\n".join(
[f"""{{
    hop: {hop['hop']}
    ip: {hop['ip']}
    hostname: {hop['hostname']}
    rtt: {hop['rtt']}
}}""" for hop in hops]
                )
    return formatted_output
print('google.com')
print(execute_traceroute("google.com"))

print('github.com')
print(execute_traceroute("github.com"))

print('mixed-hostnames.example.com')
print(execute_traceroute("mixed-hostnames.example.com"))

print('example.com')
print(execute_traceroute("example.com"))