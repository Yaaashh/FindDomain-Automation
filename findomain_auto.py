import subprocess
import argparse
import time

def run_findomain(domain, output_file, resolved=False, pscan=False, verbose=False, ip=False, ipv6_only=False, screenshots_path=None):
    """Runs findomain for the specified domain and saves the output to a file.

    Args:
        domain (str): The target domain.
        output_file (str): The output file path.
        resolved (bool): Resolve subdomains to IP addresses if True.
        pscan (bool): Enable port scanner if True.
        verbose (bool): Enable verbose mode if True.
        ip (bool): Show/write the IP address of resolved subdomains if True.
        ipv6_only (bool): Perform an IPv6 lookup only if True.
        screenshots_path (str): Path to save screenshots if provided.
        query_database (bool): Query the findomain database to search subdomains if True.
    """
    # Construct the command
    command = ["findomain", "-t", domain, "-u", output_file]
    if resolved:
        command.append("--resolved")
    if pscan:
        command.append("--pscan")
    #if query_database:
    #    command.append("--query-database")
    if verbose:
        command.append("--verbose")
    if ip:
        command.append("--ip")
    if ipv6_only:
        command.append("--ipv6-only")
    if screenshots_path:
        command.extend(["-s", screenshots_path])

    try:
        # Run the findomain command
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Findomain completed successfully. Output saved to {output_file}")
            if verbose:
                print(result.stdout)
        else:
            print(f"Findomain failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automate Findomain with various options.")
    parser.add_argument("domain", help="The target domain")
    parser.add_argument("-o", "--output", default=None, help="Output file path")
    parser.add_argument("-resolved", action="store_true", help="Resolve subdomains to IP addresses")
    #parser.add_argument("--query-database", action="store_true", help="Query the findomain database to search subdomains that have already been discovered")
    parser.add_argument("-pscan", action="store_true", help="Enable port scanner")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-ip", "--ip", action="store_true", help="Show/write the IP address of resolved subdomains")
    parser.add_argument("-ipv6", "--ipv6_only", action="store_true", help="Perform an IPv6 lookup only")
    parser.add_argument("-s", "--screenshots_path", help="Path to save screenshots of HTTP(S) websites")

    args = parser.parse_args()

    # Generate a default output file name if not provided
    if args.output is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        args.output = f"{args.domain}_{timestamp}.txt"

    run_findomain(args.domain, args.output, args.resolved, args.pscan, args.verbose, args.ip, args.ipv6_only, args.screenshots_path)

if __name__ == "__main__":
    main()