# Privacy-Enhanced Mail?

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Estrarre l'esponente privato `d` come intero decimale da una chiave RSA in formato PEM.

Viene fornito un file `.pem` contenente una chiave privata RSA. L'obiettivo è analizzarlo e leggere il valore dell'esponente privato `d`.

---

## Fondamenti teorici

### Il formato PEM

**PEM** (*Privacy-Enhanced Mail*) è un formato contenitore per materiale crittografico: chiavi, certificati, richieste di firma di certificati. Definito originariamente nell'RFC 1421 (1993) e ancora ampiamente utilizzato oggi. La sua struttura è semplice:

```
-----BEGIN <ETICHETTA>-----
<dati DER codificati in Base64>
-----END <ETICHETTA>-----
```

L'intestazione e il piè di pagina delimitano il contenuto e ne indicano il tipo. Il numero esatto di trattini (cinque per lato) è obbligatorio; qualsiasi deviazione causa il rifiuto del file da parte degli strumenti crittografici.

### DER e ASN.1

I dati all'interno dell'involucro PEM sono **DER codificato in Base64**. DER (*Distinguished Encoding Rules*) è una serializzazione binaria di strutture **ASN.1** (*Abstract Syntax Notation One*). ASN.1 è un linguaggio di schema che descrive la disposizione dei dati strutturati; DER è una specifica codifica binaria di tale disposizione.

Per una chiave privata RSA, la struttura ASN.1 (definita in PKCS#1, RFC 8017) è:

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

Tutti e nove i componenti della chiave RSA sono memorizzati nel file. La funzione `RSA.import_key()` di PyCryptodome analizza questa struttura ed espone ogni campo come attributo Python.

### L'esponente privato RSA

In RSA, l'esponente privato $d$ è definito come l'inverso modulare dell'esponente pubblico $e$ modulo il totiente di Carmichael $\lambda(n)$:

$$d = e^{-1} \bmod \lambda(n), \qquad \lambda(n) = \text{mcm}(p-1, q-1)$$

Soddisfa $e \cdot d \equiv 1 \pmod{\lambda(n)}$, il che garantisce che la decifratura sia l'inverso della cifratura:

$$c^d = (m^e)^d = m^{ed} \equiv m \pmod{n}$$

---

## Soluzione

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

`RSA.import_key()` rileva automaticamente l'involucro PEM, decodifica il payload in Base64, analizza la struttura ASN.1 codificata in DER e restituisce un oggetto `RsaKey`. L'esponente privato è accessibile come `key.d`.

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

## Conclusioni

Questa challenge introduce due competenze essenziali per lavorare con RSA in pratica: riconoscere il formato contenitore PEM ed estrarre programmaticamente il materiale chiave strutturato al suo interno.

Lo stack PEM/DER/ASN.1 è onnipresente nella crittografia del mondo reale. I certificati TLS, le chiavi SSH, le chiavi di firma del codice e le chiavi di cifratura delle email vengono tutte comunemente distribuite in formato PEM. Saper ispezionare e manipolare questi file, con strumenti come `openssl` da riga di comando o `PyCryptodome` in Python, è un prerequisito per le challenge RSA che seguono.

L'esponente privato $d$ è il componente più sensibile di una chiave RSA. La sua segretezza è ciò che rende la decifratura possibile solo al destinatario previsto. Estrarlo da un file di chiave è banale quando il file non è cifrato, motivo per cui le chiavi private RSA devono sempre essere conservate cifrate a riposo (tramite una passphrase) in qualsiasi distribuzione reale.