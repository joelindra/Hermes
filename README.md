![image](https://github.com/user-attachments/assets/cacf2db8-8028-4749-8235-38259202a7e7)

# XSStunner - Automated XSS Scanning Tool

**XSStunner** is an automated XSS scanning tool designed for ethical hacking and vulnerability assessment. It integrates various scanning utilities such as **gau**, **gf**, **uro**, **Gxss**, **kxss**, and **dalfox** to efficiently detect and filter XSS vulnerabilities from web applications.

This tool allows for scanning a single target or multiple targets concurrently using dynamic threading. It processes results and identifies unique URLs that might be vulnerable to XSS attacks. The tool then runs **Dalfox** with custom payloads to further investigate these vulnerabilities.

## Features

- **Automated XSS scanning** using popular tools and techniques.
- **Support for scanning single or multiple targets**.
- **Dynamic threading** for processing multiple targets simultaneously.
- **Custom payload injection** with **Dalfox** to identify XSS vulnerabilities.
- **Output in well-organized files**, including detailed logs and results.

## Requirements

Before using XSStunner, ensure you have the following dependencies installed:

- **gau** - Get all URLs from a target.
- **gf** - A pattern search tool for filtering.
- **uro** - URL rewriting tool.
- **Gxss** - XSS vulnerability scanner.
- **kxss** - Another XSS scanning tool.
- **dalfox** - A tool for testing XSS vulnerabilities.
- **tee** - Used to output results to files.

You can install the required dependencies manually or through your package manager.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/XSStunner.git
   cd XSStunner
   ```

2. Install dependencies:
   - Make sure **gau**, **gf**, **uro**, **Gxss**, **kxss**, **dalfox**, and **tee** are installed and accessible from the command line.

3. Run the tool:
   - Simply execute the script using Python:
     ```bash
     python3 xsstunner.py
     ```

## Usage

### Run a Single Target

1. When prompted, choose option `1` for a single target.
2. Enter the target domain (e.g., `example.com`) when asked.
3. The tool will process the target and output the results to a new directory in `results/{target}`.

### Run Multiple Targets

1. When prompted, choose option `2` for multiple targets.
2. Provide the path to a file containing a list of target domains (one per line).
3. The tool will scan each target concurrently and save the results in respective directories.

### Example Command:

```bash
python3 xsstunner.py
```

You will be prompted to either choose a single target or multiple targets. The tool will then process the targets and display the results.

## Output

- **xss_output.txt**: The initial output containing XSS-related results.
- **final.txt**: The filtered list of unique URLs suspected of being vulnerable to XSS attacks.
- **dalfox_results.txt**: The results after running Dalfox with a custom payload to test for XSS vulnerabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This tool is intended for ethical hacking and penetration testing only. Please ensure you have proper authorization before scanning any website or web application.
