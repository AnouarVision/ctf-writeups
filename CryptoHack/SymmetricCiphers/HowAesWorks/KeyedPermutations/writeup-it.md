# Keyed Permutations

**Competizione:** CryptoHack<br>
**Categoria:** Crypto

---

## Descrizione

> AES esegue una "permutazione con chiave", mappando ogni possibile blocco di input a un unico blocco di output. Qual è il termine matematico per una corrispondenza uno-a-uno?

La challenge verifica la conoscenza di un concetto fondamentale della matematica e del suo ruolo nella progettazione dei cifrari a blocchi.

---

## Fondamenti teorici

### Funzioni, iniezioni, suriezioni, biiezioni

Sia $f : A \to B$ una funzione tra due insiemi $A$ e $B$.

- $f$ è **iniettiva** (uno-a-uno) se elementi distinti dell'input producono output distinti:
$$a_1 \neq a_2 \implies f(a_1) \neq f(a_2)$$

- $f$ è **suriettiva** (su) se ogni elemento di $B$ è l'immagine di almeno un elemento di $A$:
$$\forall\, b \in B,\ \exists\, a \in A : f(a) = b$$

- $f$ è **biettiva** se è sia iniettiva che suriettiva. Una biiezione stabilisce una perfetta **corrispondenza uno-a-uno** tra $A$ e $B$: ogni elemento di $A$ si mappa esattamente su un elemento di $B$, e ogni elemento di $B$ ha esattamente una preimmagine in $A$.

Una biiezione da un insieme finito in se stesso è detta **permutazione**.

### Perché i cifrari a blocchi devono essere biiezioni

Un cifrario a blocchi $E_k : \{0,1\}^n \to \{0,1\}^n$ mappa blocchi di input a $n$ bit in blocchi di output a $n$ bit usando una chiave $k$. Affinché la decifratura sia possibile, $E_k$ deve essere **invertibile**, dato un blocco cifrato $c$, deve esistere un unico blocco in chiaro $m$ tale che $E_k(m) = c$.

Questo è esattamente il requisito di biettività. Se $E_k$ non fosse iniettiva, due testi in chiaro diversi produrrebbero lo stesso testo cifrato, rendendo la decifratura ambigua. Se $E_k$ non fosse suriettiva, alcuni blocchi cifrati non avrebbero alcun testo in chiaro corrispondente, rendendoli non decodificabili.

Poiché $E_k$ mappa un insieme finito in sé stesso (dominio e codominio sono entrambi $\{0,1\}^n$), biettività equivale a essere una permutazione. La chiave $k$ seleziona quale permutazione specifica applicare, da cui il termine **permutazione con chiave**.

### AES-128 come permutazione con chiave

AES-128 opera su blocchi da 128 bit (16 byte) con una chiave da 128 bit. Dominio e codominio sono entrambi $\{0,1\}^{128}$, un insieme di $2^{128}$ elementi. Per ogni chiave $k$, AES-128 definisce una permutazione distinta su questo insieme, una delle molte biiezioni possibili da $\{0,1\}^{128}$ in se stesso.

Il numero totale di permutazioni possibili di $2^{128}$ elementi è $(2^{128})!$, un numero astronomicamente grande. Un cifrario a blocchi sicuro dovrebbe comportarsi come se la sua chiave stesse selezionando una permutazione uniformemente a caso da questo insieme, un ideale noto come **permutazione pseudocasuale (PRP)**.

---

### Flag

```
crypto{bijection}
```

---

## Conclusioni

Il concetto di biiezione è fondamentale per l'intera teoria della cifratura simmetrica. Ogni cifrario a blocchi sicuro: AES, DES, Camellia, PRESENT, è una permutazione con chiave. L'obiettivo di sicurezza è che senza conoscere la chiave, la permutazione sia computazionalmente indistinguibile da una permutazione scelta casualmente nello spazio dei blocchi.