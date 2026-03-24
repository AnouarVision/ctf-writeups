# Ma che bello era il 2013...

**Competizione:** ITSCyberGame<br>
**Categoria:** Misc<br>
**Zip:** segreti.zip

---
## Descrizione

> L'estate del 2013 è stata una bomba, avevo salvato tutto in quella cartella segreta, se solo mi ricordassi la password...

Viene fornito uno zip `segreti.zip` protetto da password. All'interno è presente un singolo file nascosto: `.flag.txt`.

---

## Soluzione

### 1. Ispezione del file

```bash
unzip -l segreti.zip
```

```
Archive:  segreti.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        69  2026-02-02 15:12   .flag.txt
---------                     -------
        69                     1 file
```

Il file è protetto da password e contiene un solo file nascosto (`.flag.txt`).

### 2. Interpretazione

Il testo fa riferimento all'**estate del 2013** e a una "cartella segreta". La hint suggerisce di usare una wordlist con password comuni dell'epoca, `rockyou.txt` è perfetta perché contiene milioni di password reali trapelate nel 2009, incluse tutte quelle più in voga nei primi anni 2010.

### 3. Cracking della password con John the Ripper

Prima si estrae l'hash dal file zip:

```bash
zip2john segreti.zip > hash.txt
```

Poi si decomprime `rockyou.txt` (su Kali ad esempio è compressa di default):

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

Infine si lancia John con la wordlist:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

Output:
```
Loaded 1 password hash (PKZIP [32/64])
monkey           (segreti.zip/.flag.txt)
1g 0:00:00:00 DONE (2026-03-24 19:45) 9.090g/s 37236p/s
```

Verifica:
```bash
john --show hash.txt
# segreti.zip/.flag.txt:monkey:.flag.txt:segreti.zip::segreti.zip
# 1 password hash cracked, 0 left
```

**Password trovata: `monkey`**, craccata in meno di un secondo.

### 4. Decodifica della flag

Il contenuto di `.flag.txt` è una stringa esadecimale:

```
666c61677b546831735f5a31705f5734735f5072307433637433645f4234646c797d
```

Decodificandola:

```python
bytes.fromhex("666c61677b546831735f5a31705f5734735f5072307433637433645f4234646c797d").decode()
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

La challenge insegna una lezione fondamentale: **una protezione con password debole equivale a nessuna protezione**. Usare una password come `monkey`, anche nel 2013, rendeva il file facilmente violabile con un semplice dizionario delle password più comuni