# Super Market

**Competizione:** OliCyber<br>
**Categoria:** Software<br>
**Servizio:** `nc market.challs.olicyber.it 10005`

---

## Descrizione

> Voglio diventare il cliente del mese di questo supermercato, puoi darmi una mano?

Viene fornito un binario C che simula un supermercato. Il catalogo contiene tre prodotti, tra cui una `flag` dal costo di 1.000.000€, con un saldo iniziale di soli 10€. L'obiettivo è acquistarla.

---

## Analisi del codice

Il binario definisce una struttura `Product` con un puntatore a funzione `foo`:

```c
typedef struct {
    char name[64];
    int price;
    void (*foo)();
} Product;
```

Il catalogo contiene tre prodotti, ognuno con la propria funzione associata:

```c
Product ps[] = {
    {"Penna rossa",            1,       pennaRossa},
    {"Pasticciotto alla crema",3,       pasticciotto},
    {"flag",                   1000000, flag}
};
```

La funzione `flag()` legge e stampa il contenuto del file `flag` su disco. Il controllo sul saldo è:

```c
cost = ps[choice-1].price * amount;

if(cost >= saldo){
    puts("Ci hai provato, mi dispiace!");
    exit(1);
}
else{
    saldo -= cost;
    ps[choice-1].foo();
}
```

---

## Soluzione

### Step 1 — Identificazione della vulnerabilità: integer overflow

La variabile `amount` è dichiarata come `int`, un intero con segno a 32 bit, il cui intervallo è:

$$[-2^{31},\ 2^{31}-1] = [-2147483648,\ 2147483647]$$

Il costo viene calcolato come:

$$\texttt{cost} = \texttt{price} \times \texttt{amount}$$

Se `amount` è negativo, `cost` è negativo. Il check `cost >= saldo` diventa:

$$\text{(numero negativo)} \geq 10 \implies \text{False}$$

Il controllo viene superato e `flag()` viene chiamata.

### Step 2 — Scelta dell'input

Il controllo `amount == 0` è l'unica guardia sul valore, ma non esclude i negativi. Si sceglie il valore minimo rappresentabile:

$$\texttt{amount} = -2^{31} = -2147483648$$

Il costo calcolato è:

$$\texttt{cost} = 1000000 \times (-2147483648) = -2147483648000000$$

che è certamente minore di 10 → il check `cost >= saldo` è falso → si entra nel ramo `else` → `flag()` viene eseguita.

---

## Interaction

```
nc market.challs.olicyber.it 10005

cosa vuoi comprare?
> 3
Quante ne vuoi comprare?
> -2147483648
```

**Output:**
```
flag{...}
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

> Validare solo che `amount != 0` non è sufficiente: i numeri interi con segno ammettono valori negativi, e moltiplicare un prezzo positivo per una quantità negativa produce un costo negativo.

Due osservazioni fondamentali:

1. **Integer overflow e signed arithmetic:** in C il tipo `int` è un intero con segno a 32 bit. Il prodotto `1000000 * (-2147483648)` non solo è negativo, ma produce un overflow il cui comportamento è **undefined behavior** secondo lo standard C, in pratica, su architetture x86/x86-64 con compilatori comuni, il risultato è un numero negativo che passa il controllo. La correzione corretta è validare `amount > 0` prima di calcolare il costo.

2. **Pointer a funzione come primitiva di exploit:** la struttura `Product` contiene un puntatore a funzione `foo`. In scenari più avanzati (heap overflow, use-after-free), sovrascrivere un puntatore a funzione è una tecnica classica per redirigere il flusso di esecuzione verso funzioni arbitrarie, in questo caso `flag()` è già presente nel binario (*ret2win*). Qui non era necessario sovrascriverlo, ma la sua presenza è un segnale che chi ha scritto il codice ha pensato a questo vettore.