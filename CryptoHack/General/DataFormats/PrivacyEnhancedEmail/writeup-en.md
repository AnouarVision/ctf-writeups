# Privacy-Enhanced Mail?

**Competition:** CryptoHack<br>
**Category:** Crypto

---

## Description

> Extract the private key exponent `d` as a decimal integer from a PEM-formatted RSA key.

A `.pem` file containing an RSA private key is provided. The goal is to parse it and read the value of the private exponent `d`.

---

## Theoretical Background

### The PEM format

**PEM** (*Privacy-Enhanced Mail*) is a container format for cryptographic material: keys, certificates, certificate signing requests. Originally defined in RFC 1421 (1993) and still widely used today. Its structure is straightforward:

```
-----BEGIN <LABEL>-----
<base64-encoded DER data>
-----END <LABEL>-----
```

The header and footer delimit the content and indicate its type. The exact number of hyphens (five on each side) is mandatory; any deviation causes cryptographic tools to reject the file.

### DER and ASN.1

The data inside the PEM envelope is **Base64-encoded DER**. DER (*Distinguished Encoding Rules*) is a binary serialisation of **ASN.1** (*Abstract Syntax Notation One*) structures. ASN.1 is a schema language that describes the layout of structured data; DER is one specific binary encoding of that layout.

For an RSA private key, the ASN.1 structure (defined in PKCS#1, RFC 8017) is:

```
RSAPrivateKey ::= SEQUENCE {
  version           Version,
  modulus           INTEGER,  -- n
  publicExponent    INTEGER,  -- e
  privateExponent   INTEGER,  -- d
  prime1            INTEGER,  -- p
  prime2            INTEGER,  -- q
  exponent1         INTEGER,  -- d mod (p-1)
  exponent2         INTEGER,  -- d mod (q-1)
  coefficient       INTEGER   -- q^{-1} mod p
}
```

All nine components of the RSA key are stored in the file. PyCryptodome's `RSA.import_key()` parses this structure and exposes each field as a Python attribute.

### The RSA private exponent

Recall that in RSA, the private exponent $d$ is defined as the modular inverse of the public exponent $e$ modulo the Carmichael totient $\lambda(n)$:

$$d = e^{-1} \bmod \lambda(n), \qquad \lambda(n) = \text{lcm}(p-1, q-1)$$

It satisfies $e \cdot d \equiv 1 \pmod{\lambda(n)}$, which ensures decryption is the inverse of encryption:

$$c^d = (m^e)^d = m^{ed} \equiv m \pmod{n}$$

---

## Solution

### Script

```python
#!/usr/bin/env python3

from Crypto.PublicKey import RSA

with open("privacy_enhanced_mail.pem", "rb") as f:
    key = RSA.import_key(f.read())

print("n =", key.n)
print("e =", key.e)
print("d =", key.d)
```

`RSA.import_key()` automatically detects the PEM envelope, Base64-decodes the payload, parses the DER-encoded ASN.1 structure and returns an `RsaKey` object. The private exponent is accessible as `key.d`.

### Output

```
n = 26124679192169889396930934594832586381657134721686408924896834485060090555447728243939971092349402332074454486145878854389143530141373933722653891290019906610577753022692077234140341656358959283765125231270643044696534867962805725825537895613786330008756084561171245956707982250227295378042076449176123946956113645318308358321054079310928155027500387749858456348127116165713751772907631453999182598166262185646676504916701909739665176036875153096733843037813451945185657285876119684429491038512154912202328310916557054320574419560706752579862983046984243934133129484246182865617610979022586832515264075436754108666379
e = 65537
d = 15682700288056331364787171045819973654991149949197959929860861228180021707316851924456205543665565810892674190059831330231436970914474774562714945620519144389785158908994181951348846017432506464163564960993784254153395406799101314760033445065193429592512349952020982932218524462341002102062063435489318813316464511621736943938440710470694912336237680219746204595128959161800595216366237538296447335375818871952520026993102148328897083547184286493241191505953601668858941129790966909236941127851370202421135897091086763569884760099112291072056970636380417349019579768748054760104838790424708988260443926906673795975104689
```

---

### Flag

```
15682700288056331364787171045819973654991149949197959929860861228180021707316851924456205543665565810892674190059831330231436970914474774562714945620519144389785158908994181951348846017432506464163564960993784254153395406799101314760033445065193429592512349952020982932218524462341002102062063435489318813316464511621736943938440710470694912336237680219746204595128959161800595216366237538296447335375818871952520026993102148328897083547184286493241191505953601668858941129790966909236941127851370202421135897091086763569884760099112291072056970636380417349019579768748054760104838790424708988260443926906673795975104689
```

---

## Conclusions

This challenge introduces two essential skills for working with RSA in practice: recognising the PEM container format and extracting structured key material from it programmatically.

The PEM/DER/ASN.1 stack is ubiquitous in real-world cryptography. TLS certificates, SSH keys, code-signing keys and email encryption keys are all commonly distributed in PEM format. Being able to inspect and manipulate these files, with tools such as `openssl` on the command line or `PyCryptodome` in Python, is a prerequisite for the RSA challenges that follow.

The private exponent $d$ is the most sensitive component of an RSA key. Its secrecy is what makes decryption possible only by the intended recipient. Extracting it from a key file is trivial when the file is unencrypted, which is why RSA private keys should always be stored encrypted at rest (using a passphrase) in any real deployment.