# XSStunner v2.0

## 🔥 Advanced XSS Scanning & Detection Tool

XSStunner is a comprehensive, automated tool designed to detect cross-site scripting (XSS) vulnerabilities in web applications with minimal false positives. It combines multiple reconnaissance techniques with intelligent payload testing to find exploitable XSS vectors.

## ✨ Features

- **Advanced Crawling**: Uses multiple tools (gau, waybackurls, hakrawler) to discover hidden endpoints
- **Smart Filtering**: Multi-stage filtering process to identify potential XSS vectors
- **DOM XSS Detection**: Identifies vulnerable JavaScript patterns in the DOM
- **Parameter Pollution Testing**: Tests for HTTP parameter pollution vulnerabilities
- **Payload Mutation**: Intelligently mutates XSS payloads to bypass filters
- **Custom Header Testing**: Tests for XSS via HTTP headers
- **Comprehensive Reporting**: Generates JSON, plain text, and HTML reports
- **Discord Integration**: Real-time vulnerability notifications via Discord webhooks
- **Multi-Threading**: Concurrent scanning for faster results

## 📋 Prerequisites

XSStunner requires the following tools to be installed:

- [gau](https://github.com/lc/gau): `GO111MODULE=on go install github.com/lc/gau/v2/cmd/gau@latest`
- [gf](https://github.com/tomnomnom/gf): `GO111MODULE=on go install github.com/tomnomnom/gf@latest`
- [uro](https://github.com/s0md3v/uro): `pip install uro`
- [Gxss](https://github.com/KathanP19/Gxss): `GO111MODULE=on go install github.com/KathanP19/Gxss@latest`
- [kxss](https://github.com/Emoe/kxss): `GO111MODULE=on go install github.com/Emoe/kxss@latest`
- [dalfox](https://github.com/hahwul/dalfox): `GO111MODULE=on go install github.com/hahwul/dalfox/v2@latest`
- [waybackurls](https://github.com/tomnomnom/waybackurls): `GO111MODULE=on go install github.com/tomnomnom/waybackurls@latest`
- [hakrawler](https://github.com/hakluke/hakrawler): `GO111MODULE=on go install github.com/hakluke/hakrawler@latest`

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/xsstunner.git
cd xsstunner

# Make the script executable
chmod +x xsstunner

# Install Python dependencies
pip install -r requirements.txt

# Run the tool
./xsstunner -h
```

## 📥 Dependencies

```
requests
beautifulsoup4
urllib3
pathlib
```

## 💻 Usage

### Basic Usage

```bash
# Scan a single target
./xsstunner -t example.com

# Scan multiple targets from a file
./xsstunner -l targets.txt

# Scan with a custom output directory
./xsstunner -t example.com -o my_results

# Use a custom XSS payload
./xsstunner -t example.com -p '"><img src=x onerror=confirm(1)>'

# Increase thread count for faster scanning
./xsstunner -t example.com -T 10

# Enable verbose output
./xsstunner -t example.com -v
```

### Command Line Arguments

| Option | Description |
|--------|-------------|
| `-t, --target` | Single target to scan (e.g., example.com) |
| `-l, --list` | File containing multiple targets |
| `-o, --output` | Output directory for results |
| `-p, --payload` | Custom XSS payload |
| `-T, --threads` | Number of threads to use (default: 5) |
| `-v, --verbose` | Enable verbose output |

## 🛠️ Discord Integration

XSStunner can send real-time notifications when vulnerabilities are discovered. To enable this feature:

1. Create a `config.json` file in the XSStunner directory
2. Add your Discord webhook URL:

```json
{
    "discord_webhook_url": "https://discord.com/api/webhooks/your-webhook-url"
}
```

## 📊 Results Structure

After scanning, results will be saved in the `results/` directory (or custom output directory if specified):

```
results/example.com_/
├── all_urls.txt            # All discovered URLs
├── crawled_urls.txt        # Raw crawler output
├── dom_xss_candidates.txt  # Potential DOM XSS vulnerabilities
├── final_candidates.txt    # Final XSS candidates
├── final_results.json      # Detailed vulnerability data in JSON format
├── gxss_output.txt         # Output from Gxss
├── payloads.txt            # XSS payloads used in the scan
├── processed_targets.txt   # Processed target URLs
├── readable_results.txt    # Human-readable vulnerability report
├── report.html             # HTML vulnerability report
├── xss_filtered.txt        # Filtered XSS vectors
├── xss_vectors.txt         # Potential XSS vectors
└── xsstunner.log           # Scan log
```

## 📄 Sample Reports

### Plain Text Report

```
XSStunner - Detailed Vulnerability Report
=====================================

Scan Date: 2025-04-24 12:30:45
Total Vulnerabilities Found: 2

Vulnerability #1
-------------------
Target URL: https://example.com/search?q=test
Payload: "><svg/onload=alert(1)>
Proof of Concept: https://example.com/search?q=%22%3E%3Csvg/onload=alert(1)%3E

Vulnerability #2
-------------------
Target URL: https://example.com/profile?id=123
Payload: "><img src=x onerror=alert(1)>
Proof of Concept: https://example.com/profile?id=%22%3E%3Cimg%20src=x%20onerror=alert(1)%3E
```

### HTML Report

The tool generates a comprehensive HTML report with detailed vulnerability information that can be easily shared with team members or clients.

## 🔒 XSS Payloads

XSStunner includes a variety of XSS payload types:

- Basic payloads
- AngularJS-specific payloads
- Vue.js-specific payloads
- DOM-based payloads
- Filter bypass payloads
- HTML5-specific payloads
- Encoded payloads

## ⚠️ Disclaimer

This tool is intended for security professionals to test their own systems or systems they have permission to test. Always obtain proper authorization before scanning any website. The authors are not responsible for any misuse of this tool.


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **anonre** - *Initial work and enhancements*

## 🙏 Acknowledgments

- All the authors of the tools that XSStunner depends on
- The security community for sharing techniques and payloads

![image](https://github.com/user-attachments/assets/26fd9abd-7b5f-4f7a-a440-28f5d3690321)
