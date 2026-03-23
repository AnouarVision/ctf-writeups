# The 1337 Vault

**Competition:** ITSCyberGame
**Category:** Misc
**File:** the_1337_vault.7z

---

## Description

> Only true hackers know what it means to be 1337.
> In front of you is a digital vault with 1337 layers of compressed encryption. Each layer you unlock brings you closer to a secret guarded by those who speak leet.
> Can you prove you are worthy and find the hidden flag?

---

## Solution

The title and description explicitly refer to **1337 layers of compression**. The strategy is straightforward: automate recursive extraction until the final content is reached.

### Step 1 — Initial file analysis

```bash
$ file the_1337_vault.7z
the_1337_vault.7z: 7-zip archive data, version 0.3

$ 7z l the_1337_vault.7z
Path = the_1337_vault.7z
Type = 7z
Method = LZMA:23

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2025-02-03 ...                  167469       169287  layer_1336.7z
```

The archive contains a file named `layer_1336.7z`. The name suggests each layer contains the previous one, down to layer 1 which holds the flag.

### Step 2 — Recursive extraction

Extracting 1337 archives by hand is impractical. Use the provided Python script saved in the same folder as [the_1337_vault.py](the_1337_vault.py). The script copies the first archive into a temporary directory, extracts nested `.7z` files recursively, and prints the content of the final file.

### Step 3 — Execution

Run the script from the folder containing the archives:

```bash
$ python3 the_1337_vault.py
Content of flag.txt:
flag{...}
```

After 1337 extractions, layer 1 contains `flag.txt` with the flag in plaintext; the script prints it directly.
