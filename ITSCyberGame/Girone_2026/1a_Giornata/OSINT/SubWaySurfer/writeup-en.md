# SubWaySurfer

**Competition:** ITSCyberGame
**Category:** OSINT
**Target:** `@alinacustoza65`

---

## Description

> This Instagram profile sent me a strange message: @alinacustoza65

---

## Solution

### Step 1 — Google search for indexed comments

Start from the Instagram handle `@alinacustoza65`. Instead of manually inspecting the profile, search Google for the username together with the word `commented` to find public comments indexed on other sites:

```
"alinacustoza65" "commented"
```

The top result points to a Reddit profile:

```
https://www.reddit.com/user/alinacustoza65
What are your most essential PSP mods? alinacustoza65 commented 2 mo. ago.
Has anyone managed to run Linux on a PSP?
```

### Step 2 — Inspect the Reddit profile

Visiting `u/alinacustoza65` on Reddit reveals a post in `r/itscybergame` where the user pasted a suspicious string:

> I received a strange message, I can't understand what's written
> `c3ludHtFM3FxMWdfTnkxNGZfMWFfR3UzX1AwenozYWdmfQ==`

### Step 3 — Base64 decode

The string is Base64-encoded:

```bash
$ echo "c3ludHtFM3FxMWdfTnkxNGZfMWFfR3UzX1AwenozYWdmfQ==" | base64 -d
synt{E3qq1g_Ny14f_1a_Gu3_P0zz3agf}
```

### Step 4 — ROT13 decode

The result still appears encoded. The `synt{...}` pattern is a typical ROT13 transformation of `flag{...}`. Apply ROT13 to get the flag:

```bash
$ python3 -c "import codecs; print(codecs.decode('synt{E3qq1g_Ny14f_1a_Gu3_P0zz3agf}', 'rot13'))"
flag{...}
```

---

## Flag

```
flag{...}
```
