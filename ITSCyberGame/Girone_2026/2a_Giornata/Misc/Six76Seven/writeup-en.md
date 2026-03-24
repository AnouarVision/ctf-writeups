# six76seven

**Competition:** ITSCyberGame
**Category:** Misc
**File:** six76seven.tar.gz

---

## Description

> git gud

An archive containing a git repository is provided. The goal is to find the flag by analysing the commit history and object store.

---

## Solution

### 1. Extract the archive

```bash
tar -xf six76seven.tar.gz
cd six76seven
```

The repository contains a single file: `README.md`.

### 2. Inspect the commit history

```bash
git log --oneline --all
```

Example output (minor README edits):

```
9c478bc Ritocca ritmo e punteggiatura
c4d5e20 Aggiungi una nota di energia
f841ba4 Semplifica la chiusura
744bc94 Rendi "memorabilli" più evocativo
d681c47 Espandi la comunità
d09e666 Rafforza collaborazione
03c32d5 Cambio forme verbali
5e9d8e1 Dettagli sul quartiere
28652c4 Incipit più scorrevole
44b5dbe Primo Commit
```

Nothing suspicious in the visible history.

### 3. Enumerate all git objects

Git keeps every object ever created in the object store, even objects not referenced by any commit. List all objects and check blob sizes:

```bash
git cat-file --batch-all-objects --batch-check
```

Look for blobs with an unusual size. In this repository there is one extra blob larger than the others (example id `0a81b8ab`). Inspect it:

```bash
git cat-file blob 0a81b8ab8a3c8906ea433503ec60cec1d29c2dd3
```

The blob contains a paragraph and the hidden flag embedded in the text:

```
# six76seven

... Forte Umanità
Costruisce Kermesse flag{...} Inclusive Creative
Elettrizzanti ...
```

The flag is inside the orphan blob.

---

## Flag

```
flag{...}
```

---

## Conclusion

Git keeps objects in its object store even if they are not reachable from current commits. An orphan blob created but never referenced can still be recovered with `git cat-file`. The challenge hints (`six76seven`, `git gud`) suggested inspecting git internals beyond the visible commit history.