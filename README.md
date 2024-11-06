# Latest CISA Vulnerabilities

### CVE-2024-8956

**Vendor Project**:
PTZOptics

**Product**:
PT30X-SDI/NDI Cameras

**Vulnerability Name**:
PTZOptics PT30X-SDI/NDI Cameras Authentication Bypass Vulnerability

**Published Date**:
2024-11-04

**Description**:
PTZOptics PT30X-SDI/NDI cameras contain an insecure direct object reference (IDOR) vulnerability that allows a remote, attacker to bypass authentication for the /cgi-bin/param.cgi CGI script. If combined with CVE-2024-8957, this can lead to remote code execution as root.

**Required Action**:
Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.

**Due Date**:
2024-11-25

**Severity**:
Unknown

**Known Ransomware Campaign Use**:
Unknown

**Notes**:
https://ptzoptics.com/firmware-changelog/ ; https://nvd.nist.gov/vuln/detail/CVE-2024-8956

### CVE-2024-8957

**Vendor Project**:
PTZOptics

**Product**:
PT30X-SDI/NDI Cameras

**Vulnerability Name**:
PTZOptics PT30X-SDI/NDI Cameras OS Command Injection Vulnerability

**Published Date**:
2024-11-04

**Description**:
PTZOptics PT30X-SDI/NDI cameras contain an OS command injection vulnerability that allows a remote, authenticated attacker to escalate privileges to root via a crafted payload with the ntp_addr parameter of the /cgi-bin/param.cgi CGI script. 

**Required Action**:
Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.

**Due Date**:
2024-11-25

**Severity**:
Unknown

**Known Ransomware Campaign Use**:
Unknown

**Notes**:
https://ptzoptics.com/firmware-changelog/ ; https://nvd.nist.gov/vuln/detail/CVE-2024-8957

