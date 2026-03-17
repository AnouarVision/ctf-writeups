# Protocollo Datagramma Utente

**Competizione:** OliCyber<br>
**Categoria:** Network<br>
**Protocollo:** UDP

---

## Descrizione

> Riesci a ricostruire la flag tra tutti questi pacchetti?

---

## Soluzione

La challenge riguarda l'analisi del traffico UDP. Osservando i pacchetti catturati, è possibile ricostruire i messaggi scambiati tra client e server.

### Passo 1 — Osservare Lo Scambio UDP

Analizzando il traffico catturato, si nota uno scambio di messaggi UDP:

**Client → Server:**
```
Hello UDP Server, please s3nd me the s3cret
```

**Server → Client:**
```
Hello UDP Client, I will send you the s3cret fl4g, be ready, and listen till the end
```

### Passo 2 — Ricostruire Il Flusso Completo

A differenza di TCP, UDP è un protocollo senza connessione. I pacchetti UDP arrivano come datagrammi indipendenti. Concatenando i payload UDP in ordine di arrivo, si ottiene il messaggio completo:

```
flag{...}
```

---

## Conclusioni

1. **UDP vs TCP**: TCP mantiene una connessione persistente, UDP invia datagrammi indipendenti
2. **Ricostruzione Di Flussi**: I datagrammi UDP devono essere riassemblati in ordine di timestamp
3. **Analisi Stateless**: UDP non ha garanzie di ordine, diversamente da TCP