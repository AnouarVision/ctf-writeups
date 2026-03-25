# But it was cheap!

**Competition:** ITSCyberGame
**Category:** Network
**File:** `blindspot_3.pcap`

---

## Description

> I'm contacting you because I bought this extremely cheap camera — could it be hiding something?

A network capture is provided. The goal is to analyze it and discover suspicious behaviors of the IP camera.

---

## Solution

### 1. Traffic overview

Open the file in Wireshark (`File → Open`). The status bar shows 4795 packets.

To get a protocol breakdown use `Statistics → Protocol Hierarchy`:

- UDP → 4662 packets (video RTP traffic)
- TCP → HTTP / XML / RTSP

To view active conversations and spot anomalous flows use `Statistics → Conversations → IPv4`.

Notable flows:

- `192.168.1.10 ↔ 192.168.1.50`: local RTSP/RTP streaming, expected.
- `192.168.1.50 → 203.0.113.77:8080`: the camera (`192.168.1.50`) opens TCP connections to a public IP on port 8080. Very suspicious.

### 2. Isolating the suspicious traffic

Filter traffic to the external IP in the Wireshark filter bar:

```
ip.addr == 203.0.113.77
```

Five packets appear, all with `HTTP/1.1 200 OK` responses. The camera is responding to ONVIF queries from the external IP, an unauthorized remote server is querying the device using the ONVIF protocol (Open Network Video Interface Forum), the standard used by IP cameras for discovery and configuration.

### 3. Inspecting the XML payload

Select one of the packets and expand the HTTP/soap payload under `Hypertext Transfer Protocol → Line-based text data: application/soap+xml`.

To read the full body conveniently choose `Follow → TCP Stream` on the packet.

The response body contains a `GetDeviceInformationResponse` (ONVIF):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
  <s:Body>
    <tds:GetDeviceInformationResponse>
      <tds:Manufacturer>HikvXion</tds:Manufacturer>
      <tds:Model>DS-2CD2143G2-I</tds:Model>
      <tds:FirmwareVersion>VEVMRU1FVFJZLU9LLTE3MDAwMDAwNDI=</tds:FirmwareVersion>
      <tds:SerialNumber>Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk=</tds:SerialNumber>
      <tds:HardwareId>88</tds:HardwareId>
    </tds:GetDeviceInformationResponse>
  </s:Body>
</s:Envelope>
```

The `FirmwareVersion` and `SerialNumber` fields contain values that do not look like normal firmware versions or serials; they are Base64 strings.

### 4. Decoding the suspicious fields

FirmwareVersion:

```
VEVMRU1FVFJZLU9LLTE3MDAwMDAwNDI=
  → Base64 →
TELEMETRY-OK-1700000042
```

This is a telemetry beacon with a Unix timestamp (`1700000042` = 14 Nov 2023), indicating the device checked in to a command-and-control server.

SerialNumber (double Base64):

```
Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk=
  → Base64 (level 1) →
ZmxhZ3tkMHVibDNfYjRzM19zM2NyM3R9
  → Base64 (level 2) →
flag{...}
```

The serial number is actually an exfiltrated payload hidden using two layers of Base64 inside an ONVIF field.

Example Python to decode:

```python
import base64

serial = "Wm14aFozdGtNSFZpYkROZllqUnpNMTl6TTJOeU0zUjk="
layer1 = base64.b64decode(serial).decode()
layer2 = base64.b64decode(layer1).decode()
print(layer2)
```

---

## Flag

```
flag{...}
```

---

## Conclusions

The challenge simulates a real-world attack observed on cheap IP cameras (often rebranded Hikvision or clones): the firmware contains a C2 backdoor that uses the ONVIF protocol to exfiltrate data and check in to a remote server, hiding payloads in metadata fields. Double Base64 is a basic obfuscation to evade cursory traffic inspections.

Indicators in the PCAP:
1. Outgoing TCP connections from the camera to a public IP on port 8080.
2. Unsolicited ONVIF responses (camera replies to external queries).
3. Anomalous Base64 values in `FirmwareVersion` and `SerialNumber` instead of standard identifiers.
