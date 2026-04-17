# Software 06 - Strings 3

**Competizione:** OliCyber<br>
**Categoria:** Software

---

## Descrizione

> Questa challenge è simile alla precedente, con la differenza che questa volta la flag non viene salvata in chiaro. Analizza la funzione `main` con Ghidra e prova a capire come avviene il check tra input e flag.

Viene fornito un binario `sw-06` che verifica una stringa in input. Questa volta né `strings` né `objdump -s` rivelano la flag in chiaro: è cifrata con XOR.

---

## Analisi del codice decompilato

### Codice originale prodotto da Ghidra

```c
undefined8 main(void)
{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  size_t local_128;
  undefined8 local_120;
  byte local_118 [264];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_118,0,0x100);
  do {
    printf(&DAT_00102026);
    fgets((char *)local_118,0x100,stdin);
    sVar2 = strlen((char *)local_118);
    if (sVar2 != 0) {
      local_128 = sVar2;
      if (local_118[sVar2 - 1] == 10) {
        local_128 = sVar2 - 1;
        local_118[sVar2 - 1] = 0;
      }
      if (local_128 == 0xe) {
        for (local_120 = 0; local_120 < 0xe; local_120 = local_120 + 1) {
          local_118[local_120] = local_118[local_120] ^ key[local_120];
        }
        iVar1 = memcmp(local_118,flag,0xe);
        if (iVar1 == 0) {
          puts(&DAT_0010205b);
          if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
            __stack_chk_fail();
          }
          return 0;
        }
      }
    }
    puts(&DAT_0010203f);
  } while( true );
}
```

### Codice con variabili rinominate

Dopo aver analizzato il flusso e applicato **Rename Variable** alle variabili automatiche:

```c
undefined8 main(void)
{
  int risultato_memcmp;
  size_t sVar2;
  long in_FS_OFFSET;
  size_t lunghezza_input;
  undefined8 i;
  byte input_utente [264];
  long stack_canary;

  stack_canary = *(long *)(in_FS_OFFSET + 0x28);
  memset(input_utente, 0, 0x100);
  do {
    printf(&DAT_00102026);                              // "Qual è la flag? : "
    fgets((char *)input_utente, 0x100, stdin);
    sVar2 = strlen((char *)input_utente);
    if (sVar2 != 0) {
      lunghezza_input = sVar2;
      if (input_utente[sVar2 - 1] == 10) {             // 10 = '\n'
        lunghezza_input = sVar2 - 1;
        input_utente[sVar2 - 1] = 0;                   // rimuove il newline
      }
      if (lunghezza_input == 0xe) {                    // accetta solo input di 14 char
        for (i = 0; i < 0xe; i = i + 1) {
          input_utente[i] = input_utente[i] ^ key[i];  // XOR input con la chiave
        }
        risultato_memcmp = memcmp(input_utente, flag, 0xe);  // confronta con flag cifrata
        if (risultato_memcmp == 0) {
          puts(&DAT_0010205b);                          // "Giusto!"
          if (stack_canary != *(long *)(in_FS_OFFSET + 0x28)) {
            __stack_chk_fail();
          }
          return 0;
        }
      }
    }
    puts(&DAT_0010203f);                               // "Sbagliato! Prova ancora"
  } while( true );
}
```

---

## La vulnerabilità: XOR è invertibile

Il meccanismo di verifica si riduce a tre passaggi:

```
1. Leggi input (14 byte)
2. input[i] = input[i] XOR key[i]   per ogni i
3. Confronta il risultato con flag[]
```

Il programma accetta l'input se e solo se:

$$\text{input}[i] \oplus \text{key}[i] = \text{flag}[i] \qquad \forall i \in \{0, \ldots, 13\}$$

Invertendo la relazione e ricordando che XOR è la propria inversa, cioè $a \oplus b \oplus b = a$. La flag in chiaro è:

$$\text{flag\_plaintext}[i] = \text{flag}[i] \oplus \text{key}[i]$$

Non c'è nulla da bruteforzare. Bastano i due array `flag[]` e `key[]` dal binario.

---

## Estrazione degli array con `objdump`

```bash
$ objdump -s -j .rodata sw-06

Contenuto della sezione .rodata:
 2000 01000200 00000000 d45cdcbb 6b1ed34a  .........\..k..J
 2010 4a5ed2df ac7c0000 b230bddc 107ae17b  J^...|...0...z.{
 2020 2c3be2ec 9901f09f 9aa92051 75616c27  ,;........ Qual'
```

A partire dall'offset `0x2008` si trovano due array contigui di 14 byte ciascuno (separati da 2 byte di padding `\x00\x00`):

```
key[]  @ 0x2008: d4 5c dc bb 6b 1e d3 4a 4a 5e d2 df ac 7c
flag[] @ 0x201a: b2 30 bd dc 10 7a e1 7b 2c 3b e2 ec 99 01
```

## Script di decifratura

```python
key  = bytes.fromhex("d45cdcbb6b1ed34a4a5ed2dfac7c")
flag = bytes.fromhex("b230bddc107ae17b2c3be2ec9901")

plaintext = bytes([f ^ k for f, k in zip(flag, key)])
print(plaintext.decode())
# Output: flag{...}
```

---

### Flag

```
flag{...}
```

---

## Conclusioni

Questa challenge introduce il concetto di **cifratura XOR** applicata alla protezione di dati statici in un binario, e mostra perché è insufficiente:

**XOR con chiave nota è trasparente** — se entrambi gli array (`flag` cifrata e `key`) sono presenti in chiaro nel binario, il XOR non aggiunge alcuna protezione reale. Un analista con `objdump` recupera il plaintext in pochi secondi. La chiave dovrebbe essere segreta e mai memorizzata insieme al dato che protegge.

**`memcmp` vs `strcmp`**: rispetto alle challenge precedenti, qui viene usato `memcmp` invece di `strcmp`. La differenza è sottile ma importante: `strcmp` si ferma al primo byte nullo `\x00`, mentre `memcmp` confronta esattamente `n` byte indipendentemente dal loro valore. Questo permette alla flag cifrata di contenere byte nulli senza problemi, un dettaglio che sarebbe stato impossibile con `strcmp`.

**La struttura del check rivela la trasformazione**: anche senza conoscere i valori di `flag[]` e `key[]`, il codice decompilato mostra esattamente come viene costruita la stringa di confronto. Capire la trasformazione è il passo fondamentale: una volta nota la formula `input ^ key == flag`, l'inversione `flag ^ key == input` è immediata.