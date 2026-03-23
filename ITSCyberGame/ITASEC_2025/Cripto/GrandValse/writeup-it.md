# Grande Valse

**Competizione:** ITSCyberGame<br>
**Categoria:** Crittografia<br>

---

## Descrizione

> Un vecchio telefono è stato ritrovato nella sede di un noto gruppo di hacker. Tra i suoi messaggi uno sembra particolarmente interessante: `843 3524 47 3524 9484 4 4678323 63 2`

---

## Soluzione

Il titolo **"Grande Valse"** e il riferimento a un **vecchio telefono** sono gli indizi chiave: si tratta del metodo di inserimento testo **T9** (Predictive Text), utilizzato sui telefoni cellulari degli anni '90-2000.

### Passo 1 — Riconoscere il cifrario

Nella tastiera T9, ogni tasto numerico corrisponde a più lettere:

```
2=ABC  3=DEF  4=GHI  5=JKL
6=MNO  7=PQRS 8=TUV  9=WXYZ
```

In modalità T9 **predictive**, ogni sequenza di cifre (separata da spazio) corrisponde a una parola intera, senza bisogno di premere lo stesso tasto più volte. Il sistema indovina la parola in base alle combinazioni possibili.

### Passo 2 — Decodifica

Si analizza ogni gruppo separato da spazio:

| Sequenza | Lettere possibili | Parola |
|----------|-------------------|--------|
| `843`    | t/u/v + g/h/i + d/e/f | **THE** |
| `3524`   | d/e/f + j/k/l + a/b/c + g/h/i | **FLAG** |
| `47`     | g/h/i + p/q/r/s | **IS** |
| `3524`   | d/e/f + j/k/l + a/b/c + g/h/i | **FLAG** |
| `9484`   | w/x/y/z + g/h/i + t/u/v + g/h/i | **WITH** |
| `4`      | g/h/i | **4** *(cifra singola)* |
| `4678323`| i + n + s + t + e + a + d | **INSTEAD** |
| `63`     | m/n/o + d/e/f | **OF** |
| `2`      | a/b/c | **A** |

Il messaggio in chiaro è:

```
THE FLAG IS FLAG WITH 4 INSTEAD OF A
```

### Passo 3 — Costruire la flag

La frase è una istruzione letterale: prendi la parola **FLAG** e sostituisci la lettera **A** con il numero **4**:

```
FLAG → FL4G
```

---

## Flag

```
flag{...}
```