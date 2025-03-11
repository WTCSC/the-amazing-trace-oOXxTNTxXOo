import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import time
import os
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

# ============================================================================ #
#                    DO NOT MODIFY THE CODE BELOW THIS LINE                    #
# ============================================================================ #
def visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output'):
    """
    Runs multiple traceroutes to a destination and visualizes the results.

    Args:
        destination (str): The hostname or IP address to trace
        num_traces (int): Number of traces to run
        interval (int): Interval between traces in seconds
        output_dir (str): Directory to save the output plot

    Returns:
        tuple: (DataFrame with trace data, path to the saved plot)
    """
    all_hops = []

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Running {num_traces} traceroutes to {destination}...")

    for i in range(num_traces):
        if i > 0:
            print(f"Waiting {interval} seconds before next trace...")
            time.sleep(interval)

        print(f"Trace {i+1}/{num_traces}...")
        output = execute_traceroute(destination)
        hops = parse_traceroute(output)

        # Add timestamp and trace number
        timestamp = time.strftime("%H:%M:%S")
        for hop in hops:
            hop['trace_num'] = i + 1
            hop['timestamp'] = timestamp
            all_hops.append(hop)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_hops)

    # Calculate average RTT for each hop (excluding timeouts)
    df['avg_rtt'] = df['rtt'].apply(lambda x: np.mean([r for r in x if r is not None]) if any(r is not None for r in x) else None)

    # Plot the results
    plt.figure(figsize=(12, 6))

    # Create a subplot for RTT by hop
    ax1 = plt.subplot(1, 1, 1)

    # Group by trace number and hop number
    for trace_num in range(1, num_traces + 1):
        trace_data = df[df['trace_num'] == trace_num]

        # Plot each trace with a different color
        ax1.plot(trace_data['hop'], trace_data['avg_rtt'], 'o-',
                label=f'Trace {trace_num} ({trace_data.iloc[0]["timestamp"]})')

    # Add labels and legend
    ax1.set_xlabel('Hop Number')
    ax1.set_ylabel('Average Round Trip Time (ms)')
    ax1.set_title(f'Traceroute Analysis for {destination}')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Make sure hop numbers are integers
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    # Save the plot to a file instead of displaying it
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_dest = destination.replace('.', '-')
    output_file = os.path.join(output_dir, f"trace_{safe_dest}_{timestamp}.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to: {output_file}")

    # Return the dataframe and the path to the saved plot
    return df, output_file

# Test the functions
if __name__ == "__main__":
    # Test destinations
    destinations = [
        "google.com",
        "amazon.com",
        "bbc.co.uk"  # International site
    ]

    for dest in destinations:
        df, plot_path = visualize_traceroute(dest, num_traces=3, interval=5)
        print(f"\nAverage RTT by hop for {dest}:")
        avg_by_hop = df.groupby('hop')['avg_rtt'].mean()
        print(avg_by_hop)
        print("\n" + "-"*50 + "\n")
