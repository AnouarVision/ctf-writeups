# Resisting Bruteforce

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> Qual è il nome del miglior attacco a chiave singola contro AES?

La challenge verifica la conoscenza dello stato attuale della crittoanalisi di AES.

---

## Fondamenti teorici

### La sicurezza di AES-128

AES-128 opera su uno spazio delle chiavi a 128 bit, il che significa che esistono $2^{128}$ chiavi possibili. Per attaccare AES-128 a forza bruta, un attaccante dovrebbe provare fino a $2^{128} \approx 3.4 \times 10^{38}$ chiavi. Per dare un'idea concreta, è stato stimato che anche con la potenza combinata dell'intera rete di mining Bitcoin, la ricerca esaustiva nello spazio delle chiavi a 128 bit richiederebbe oltre **100 volte l'età dell'universo**.

Un cifrario a blocchi è considerato **computazionalmente sicuro** se non esiste alcun attacco significativamente più veloce della ricerca esaustiva della chiave. Più precisamente, un cifrario è teoricamente "rotto" se viene trovato un attacco che richiede meno di $2^k$ operazioni per una chiave a $k$ bit, anche se quell'attacco rimane praticamente non realizzabile.

### L'attacco Biclique

Il miglior attacco a chiave singola noto contro AES è l'**attacco biclique**, pubblicato da Bogdanov et al. nel 2011. Si applica a tutte e tre le varianti di AES:

| Variante | Dimensione chiave | Sicurezza classica | Dopo biclique |
|:---:|:---:|:---:|:---:|
| AES-128 | 128 bit | $2^{128}$ | $2^{126.1}$ |
| AES-192 | 192 bit | $2^{192}$ | $2^{189.7}$ |
| AES-256 | 256 bit | $2^{256}$ | $2^{254.4}$ |

L'attacco riduce il livello di sicurezza di AES-128 di soli **1.9 bit**, un margine trascurabile. Non è stato migliorato in oltre un decennio e non è considerato una minaccia pratica credibile.

L'attacco biclique funziona costruendo strutture algebriche chiamate **biclique** nel key schedule e nella funzione di round di AES, consentendo il riutilizzo di certi calcoli tra più candidati chiave. Si tratta di una tecnica meet-in-the-middle applicata a un piccolo numero di round di AES, combinata con la ricerca esaustiva sui bit di chiave rimanenti.

### Attacchi quantistici ad AES

I computer quantistici non rompono completamente i criptosistemi simmetrici come fanno con RSA (tramite l'algoritmo di Shor). Invece, l'**algoritmo di Grover** fornisce una velocizzazione quadratica per la ricerca non strutturata, dimezzando effettivamente il livello di sicurezza:

$$\text{Sicurezza quantistica di AES-}k = \frac{k}{2} \text{ bit}$$

| Variante | Sicurezza classica | Sicurezza quantistica (Grover) |
|:---:|:---:|:---:|
| AES-128 | 128 bit | 64 bit |
| AES-256 | 256 bit | 128 bit |

Ecco perché **AES-256 è raccomandato** per la sicurezza post-quantistica: anche dopo la velocizzazione di Grover, mantiene 128 bit di sicurezza, gli stessi di AES-128 in un contesto classico, ampiamente considerati sufficienti.

---

## Soluzione

La challenge chiede il nome del miglior attacco a chiave singola contro AES. La risposta è fornita direttamente nella descrizione della challenge: l'**attacco biclique**.

---

### Flag

```
crypto{biclique}
```

---

## Conclusioni

Questa challenge analizza l'attuale postura di sicurezza di AES da tre angolazioni:

**Sicurezza classica:** AES-128 fornisce 128 bit di sicurezza meno una riduzione trascurabile di 1.9 bit dall'attacco biclique. A tutti gli effetti pratici, AES-128 è inattaccabile con la forza bruta.

**Rotture teoriche vs. pratiche:** in senso accademico, qualsiasi attacco più veloce della ricerca esaustiva "rompe" un cifrario. L'attacco biclique si qualifica, ma il miglioramento è così piccolo da non porre alcuna minaccia nel mondo reale. La distinzione tra una rottura teorica e una pratica è cruciale nella crittografia applicata.

**Sicurezza quantistica:** l'algoritmo di Grover dimezza la lunghezza effettiva della chiave, rendendo AES-128 equivalente a un cifrario a 64 bit in uno scenario quantistico, potenzialmente vulnerabile. AES-256 mantiene 128 bit di sicurezza quantistica, motivo per cui è la scelta raccomandata per la protezione dei dati a lungo termine in un mondo post-quantistico.