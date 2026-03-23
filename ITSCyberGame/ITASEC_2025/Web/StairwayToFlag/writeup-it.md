# Stairway to Flag

**Competizione:** ITSCyberGame<br>
**Categoria:** Web<br>
**File:** login_stairway_to_flag.html

---

## Descrizione

> Solo i veri rocker possono accedere al backstage. Trova la flag nascosta nel codice di login e dimostra di avere lo spirito giusto per entrare!

---

## Soluzione

La challenge fornisce direttamente il codice sorgente di una pagina di login. In queste situazioni il primo passo è sempre leggere il JavaScript lato client, tutta la logica di autenticazione è eseguita nel browser, quindi è completamente esposta.

### Passo 1 — Analisi del controllo credenziali

Nel sorgente HTML si trova subito la funzione `checkLogin()`:

```javascript
if (username === 'admin' && password === 'flag{r0ck_4nd_r0l1_...}') {
    message.innerHTML = 'Access Granted! Welcome to the backstage!<br>' + decryptString('iru3yhu');
```

La password è hardcoded in chiaro. Questo rivela la **prima parte della flag**:

```
flag{r0ck_4nd_r0l1_...}
```

I `...` suggeriscono che la flag non è completa, il resto viene costruito dinamicamente da `decryptString('iru3yhu')`.

### Passo 2 — Analisi di `decryptString`

La funzione `decryptString` è eseguita lato client e viene utilizzata dalla pagina per costruire la parte finale della flag durante il flusso di login. Nel contesto di questa writeup non riportiamo il risultato decifrato: dopo il login la pagina aggiunge automaticamente il suffisso decifrato e mostra la parte rimanente della flag, ma qui omettiamo tale parte per non rivelarla direttamente.

### Passo 3 — Ricostruzione della flag

La prima parte della flag è visibile nel sorgente (password hardcoded). La seconda parte viene ottenuta dinamicamente dalla pagina dopo il login: non la riportiamo qui. Unendo la parte mostrata nel sorgente con il suffisso rivelato dalla pagina si ottiene la flag completa.

---

## Flag

```
flag{r0ck_4nd_r0l1_...}
```