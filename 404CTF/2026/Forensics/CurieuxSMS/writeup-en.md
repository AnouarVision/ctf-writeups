# Curieux SMS

**Competition:** 404CTF 2026 <br>
**Category:** Forensics

<img src="curieux_sms.png">

---

## Solution

### Analysis
Three SQLite databases are extracted from the provided ZIP archive, all named `mmssms.db`. This is the standard database used by Android to store SMS and MMS, normally located at: `/data/data/com.android.providers.telephony/databases/mmssms.db`.

<img src="analysezip.png">

To understand the origin of the three devices, it suffices to compare the **schema** of each database:

<img src="db1.png">
<img src="db2.png">
<img src="db3.png">

When you look at the three databases, it becomes immediately clear that they come from very different devices.

The first clearly belongs to a **legacy smartphone**, an old generation Android (probably pre-Lollipop). The schema is the historical Android one:

- `sms` table

- no MMS table (`pdu`, `part`, `addr`)

- no modern structure (`conversations`, `participants`, etc.)

It is the **reduced** version of the original AOSP schema.

The official AOSP reference (TelephonyProvider) is:
https://android.googlesource.com/platform/packages/providers/TelephonyProvider/

MmsSmsDatabaseHelper is a Java file containing the original CREATE TABLE statements:
https://android.googlesource.com/platform/packages/providers/TelephonyProvider/+/refs/heads/main/src/com/android/providers/telephony/MmsSmsDatabaseHelper.java

The second database comes from a **modern phone**, typically Android 10 or higher. It no longer uses the AOSP schema, but the one introduced by Google Messages (also adopted by Samsung).

The source code of the **modern schema**:
https://cs.android.com/android/platform/superproject/+/main:packages/apps/Messaging/

File with the CREATE TABLE statements:
https://cs.android.com/android/platform/superproject/+/main:packages/apps/Messaging/src/com/android/messaging/datamodel/DatabaseHelper.java

The third represents a **stock AOSP device**, pure Android without OEM customizations:
https://android.googlesource.com/platform/packages/providers/TelephonyProvider/

Unlike db1 (reduced version), here the AOSP schema is complete:

- `pdu`
- `part`
- `addr`
- `threads`
- MMS attachment management via `app_parts/`

### Phone 1 (`1/mmssms.db`)

<img src="phone1.png">

In the first device, based on a legacy AOSP schema, messages are stored in the `sms` table.

The sixth message contains the **first part of the flag**: `404CTF{m4r13_`

### Phone 2 (`2/mmssms.db`)

<img src="phone2.png">

In the second device the suspect attempted to delete messages from the `parts` table, but did not consider that the modern Google Messages schema maintains a **persistent cache** in the `conversations` table.

**Second part of the flag**: `cur13_`

### Phone 3 (`3/mmssms.db`)

The third device uses the complete AOSP schema for MMS, split into:

- **`pdu`**: the message envelope (sender, date, subject, MIME type)
- **`part`**: the body parts (text, images, attachments)
- **`app_parts/`**: the binary files of the attachments on the filesystem

The `part` table reveals a JPEG attachment:

The file `app_parts/62` corresponds to the `labo.jpg` attachment.

Opening the image clearly shows the text:

<img src="phone3_part1.png">

**Third part of the flag**: `r4d1um_`


During the analysis, another clue emerges from the `pdu` table itself: the `sub` field (subject) contains a value that ends with a closing brace, a detail **too suspicious** to ignore

<img src="phone3_part2.png">

**Fourth and final part of the flag**: `1898}`

---

## Flag

```
404CTF{m4r13_cur13_r4d1um_1898}
```