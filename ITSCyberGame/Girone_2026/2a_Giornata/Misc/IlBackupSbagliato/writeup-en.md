# The Wrong Backup

**Competition:** ITSCyberGame
**Category:** Misc
**File:** backup_server.tar.gz

---

## Description

> A legacy backup server performed an incomplete restore. We provide an export of the filesystem. Analyze the layout and recover the flag.

You are given an archive containing a partial filesystem export. The goal is to inspect the structure and recover the flag.

---

## Solution

### 1. Extraction and filesystem inspection

Extract the archive:

```bash
tar -xzf backup_server.tar.gz
```

The extracted layout:

```
backup_server/
├── tmp/
│   ├── .backup.enc          ← hidden encrypted file
│   └── restore.log
├── var/backups/
│   └── backup.sh            ← script with hardcoded password
├── etc/cron.d/
│   └── backup_job
└── home/sysadmin/
    ├── note.txt
    └── .hidden_backup/
        └── old_credentials.txt
```

### 2. Collecting hints

`note.txt` provides initial hints:

```
- The script in /var/backups/backup.sh might contain obsolete credentials.
- Check the restore logs in /tmp/restore.log.
```

`restore.log` shows a leftover encrypted dump:

```
[2024-08-02 03:10:45] Incomplete cleanup: encrypted dump not removed.
[2024-08-02 03:10:45] Hint: search for hidden files in /tmp (name like .backup.*)
```

`old_credentials.txt` reveals the password:

```
Service: backup_restore
User: backup-operator
Password (historical restore): Summer2024!
Note: remove hardcoded credentials from backup.sh
```

`backup.sh` confirms the password and shows the decryption command:

```bash
ARCHIVE_IN="/tmp/.backup.enc"
RESTORE_OUT="/tmp/restore_output.tar.gz"
PASS="Summer2024!"  # TODO: remove hardcoded password

openssl enc -d -aes-256-cbc -pbkdf2 -in "$ARCHIVE_IN" -out "$RESTORE_OUT" -pass pass:"$PASS"
```

### 3. Decrypt the backup

Run the decryption command using the collected password:

```bash
openssl enc -d -aes-256-cbc -pbkdf2 \
  -in backup_server/tmp/.backup.enc \
  -out restore_output.tar.gz \
  -pass pass:"Summer2024!"
```

The decrypted file is a tar.gz containing `flag.txt`:

```bash
tar -xzf restore_output.tar.gz -O flag.txt
```

---

## Flag

```
flag{...}
```

---

## Conclusions

This challenge teaches three backup security lessons. First: **hardcoded credentials** in scripts should never be left in production — the password `Summer2024!` was present in both `backup.sh` and `old_credentials.txt`. Second: **leftover encrypted temporary files** can expose sensitive data if not removed. Third: **logs** should not include hints about where to find hidden files.
