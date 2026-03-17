# Easy Stream

**Competition:** OliCyber<br>
**Category:** Network<br>
**File:** easystream.pcapng

---

## Description

> Can you follow the stream?

---

## Solution

The challenge provides a PCAP file with HTTP traffic. As the name suggests, simply "following" the stream is enough to find the flag.

### Step 1 — Extracting HTTP Objects

Wireshark can automatically reassemble and save objects transferred over HTTP:

1. Go to **File → Export Objects → HTTP...**
2. In the dialog that appears, select the file named `Echo`
3. Click **Save**

### Step 2 — Reading the File Contents

The `Echo` file is an HTML page with the following content:

```html
<!DOCTYPE html>
<html>
<head>
  <title>benvenuti nel server della flag</title>
</head>
<body>
  <h1>flag trovata flag{...}</h1>
</body>
</html>
```

The flag is directly visible in the `<h1>` heading of the page.

---

## Conclusions

1. **Export HTTP Objects**: Wireshark's "Export Objects" feature automatically reassembles files carried over HTTP, avoiding manual packet-by-packet analysis.
2. **Cleartext Traffic**: HTTP does not encrypt data; all transmitted content is readable directly in the PCAP.
3. **Follow TCP Stream**: As an alternative to "Export Objects", right-click any packet and choose **Follow → TCP Stream** to read the full HTTP response.
