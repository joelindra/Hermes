# XSSFvck - Advanced XSS Scanning Tool

## Overview
**XSSFvck** is a powerful, automated tool designed for detecting **Cross-Site Scripting (XSS)** vulnerabilities in web applications. It integrates multiple open-source tools and custom techniques to perform comprehensive scanning, including **DOM-based XSS detection**, **payload mutation**, and **HTTP parameter pollution testing**. With features like parallel processing, smart filtering, and detailed reporting, XSSFvck is ideal for security researchers and penetration testers.

## Features
- **DOM XSS Detection**: Identifies potential DOM-based XSS vulnerabilities by analyzing JavaScript patterns.
- **Payload Mutation**: Includes a variety of XSS payloads (basic, AngularJS, Vue.js, filter bypass).
- **Smart Filtering**: Uses `gf`, `uro`, `Gxss`, and `kxss` to refine potential XSS vectors.
- **HTTP Parameter Pollution Testing**: Injects payloads into URL parameters to test for vulnerabilities.
- **Custom Header Testing**: Checks for XSS via custom HTTP headers.
- **Asynchronous Discord Notifications**: Sends real-time alerts for detected vulnerabilities via Discord webhooks.
- **Comprehensive Reporting**: Generates JSON, text reports for easy analysis.
- **Multi-Target Support**: Scans single targets or multiple targets from a file.
- **Parallel Processing**: Configurable thread counts for faster scanning.

## Requirements
- **Python 3.6+**
- **Python Packages**:
  ```bash
  pip install requests beautifulsoup4
  ```
- **External Tools** (automatically checked by the script):
  - `gau`
  - `gf`
  - `uro`
  - `Gxss`
  - `kxss`
  - `dalfox`
  - `waybackurls`
  - `hakrawler`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/anonre/XSSFvck.git
   cd XSSFvck
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install external tools:
   ```bash
   GO111MODULE=on go install github.com/lc/gau/v2/cmd/gau@latest
   GO111MODULE=on go install github.com/tomnomnom/gf@latest
   pip install uro
   GO111MODULE=on go install github.com/KathanP19/Gxss@latest
   GO111MODULE=on go install github.com/Emoe/kxss@latest
   GO111MODULE=on go install github.com/hahwul/dalfox/v2@latest
   GO111MODULE=on go install github.com/tomnomnom/waybackurls@latest
   GO111MODULE=on go install github.com/hakluke/hakrawler@latest
   ```

4. (Optional) Configure Discord webhook for notifications:
   Create a `config.json` file in the project root:
   ```json
   {
       "discord_webhook_url": "https://discord.com/api/webhooks/your-webhook-url"
   }
   ```

## Usage
Run XSSFvck with the following command-line options:

```bash
python xssfuck.py [-h] [-t TARGET] [-l LIST] [-o OUTPUT] [-p PAYLOAD] [-T THREADS] [-v]
```

### Options
- `-t, --target`: Single target to scan (e.g., `example.com`).
- `-l, --list`: File containing multiple targets (one per line).
- `-o, --output`: Output directory for results (defaults to `results/<target>`).
- `-p, --payload`: Custom XSS payload.
- `-T, --threads`: Number of threads for parallel processing (default: 5).

### Examples
- Scan a single target:
  ```bash
  python xssfuck.py -t example.com -o results/example
  ```

- Scan multiple targets from a file:
  ```bash
  python xssfuck.py -l targets.txt -T 10
  ```

- Use a custom payload:
  ```bash
  python xssfuck.py -t example.com -p '<script>alert("custom")</script>'
  ```

## Output
Results are saved in the specified output directory (or `results/<target>` by default):
- `all_urls.txt`: Crawled URLs from the target.
- `xss_filtered.txt`: Filtered URLs with potential XSS vectors.
- `final_candidates.txt`: Final list of XSS candidates.
- `final_results.json`: Raw JSON results from Dalfox.
- `readable_results.txt`: Human-readable vulnerability report.
- `XSSFvck.log`: Log file with detailed execution information.

## Example HTML Report
The HTML report provides a clean, professional overview of findings:
- Scan timestamp
- List of vulnerabilities with URLs, payloads, and proof-of-concept details
- Responsive design with hover effects for better readability

## Notes
- **Responsible Use**: This tool is for **authorized security testing only**. Always obtain permission before scanning any target.
- **SSL Warnings**: The tool disables SSL warnings (`verify=False`) for testing purposes. Use with caution.
- **Dependencies**: Ensure all external tools are installed and accessible in your system's PATH.
- **Discord Notifications**: Configure a Discord webhook in `config.json` for real-time alerts.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please submit bug reports or feature requests via [GitHub Issues](https://github.com/anonre/XSSFvck/issues).

## License
This project is licensed under the [MIT License](LICENSE).

## Disclaimer
XSSFvck is provided for **educational and ethical security testing purposes only**. The author is not responsible for any misuse or damage caused by this tool.

## Acknowledgments
- Built with inspiration from the security community.
- Leverages open-source tools: `gau`, `gf`, `uro`, `Gxss`, `kxss`, `dalfox`, `waybackurls`, `hakrawler`.

---

<p align="center">
  <strong>Created by anonre</strong> | <a href="https://github.com/anonre/XSSFvck">Star us on GitHub! ⭐</a>
</p>
