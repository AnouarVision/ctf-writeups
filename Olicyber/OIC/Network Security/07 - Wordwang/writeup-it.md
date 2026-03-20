# WordWang
**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**File:** `capture.pcap`

---

## Descrizione

> Dopo lo spettacolare successo di NumberWang siamo qui con una nuova edizione del gioco preferito dalle persone dai 25 ai 25 anni e mezzo: WordWang! Riuscirai ad ottenere il WordWang?
>
> `nc wordwang.challs.olicyber.it 10601`

---

## Soluzione

### Passo 1 — Analizzare il PCAP

Il file `capture.pcap` contiene una sessione TCP verso il servizio WordWang. Estraendo i payload si ricostruisce la conversazione completa tra client e server:

```
[SERVER] Welcome to Wordwang! The show where the words are wanged!
[SERVER] speech
[SERVER] provide

[CLIENT] speech       -> That's NOT wordwang!
[CLIENT] SPEECH       -> That's NOT wordwang!
[CLIENT] PROVIDE      -> That's NOT wordwang!
[CLIENT] provide?     -> That's NOT wordwang!
[CLIENT] SPEECH?      -> That's NOT wordwang!
[CLIENT] PROVIDE!     -> That's NOT wordwang!
[CLIENT] !PROVIDE?    -> That's NOT wordwang!
[CLIENT] ?SPEECH!     -> That's wordwang! Here's the flag: [REDACTED]
```

### Passo 2 — Identificare il pattern vincente

Analizzando la sequenza di tentativi falliti e il tentativo vincente emerge la regola:

| Tentativo    | Risultato |
|--------------|-----------|
| `speech`     | X         |
| `SPEECH`     | X         |
| `SPEECH?`    | X         |
| `PROVIDE!`   | X         |
| `!PROVIDE?`  | X         |
| `?SPEECH!`   | ✔         |

**La formula vincente è: `?<PAROLA_MAIUSCOLA>!`**

- `?` come prefisso
- Parola in **MAIUSCOLO**
- `!` come suffisso

### Passo 3 — Scrivere lo script di exploit

Per uno script già pronto che automatizza la soluzione, vedi il file [`wordwang.py`](wordwang.py) nella cartella della challenge.

### Passo 4 — Eseguire e ottenere la flag

```
$ python3 wordwang.py
Parole trovate: ['brother']
Invio: '?brother!\n'  -> "That's NOT wordwang!"
Invio: '?BROTHER!\n'  -> "That's wordwang! Here's the flag: flag{...}"
```

---

## Conclusioni

1. **Analisi del traffico di rete**: Il file PCAP conteneva una sessione di gioco completa che ha permesso di ricostruire per tentativi ed errori il pattern corretto, senza dover fare brute force cieco sul servizio live.

2. **Pattern nascosto**: La regola `?<PAROLA>!` non è documentata dal servizio, l'unico modo per scoprirla è osservare la sessione catturata e confrontare sistematicamente i tentativi falliti con quello vincente.

3. **Automazione necessaria**: Poiché la parola cambia ad ogni connessione, la soluzione manuale non è praticabile. Lo script deve leggere la parola dinamicamente e applicare il pattern corretto in modo automatico.