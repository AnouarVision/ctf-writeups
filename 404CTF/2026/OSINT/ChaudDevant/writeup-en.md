# Chaud Devant

**Competition:** 404CTF 2026
**Category:** OSINT

<img src="chaud_devant.png">

---
## Solution

### Image Geolocation
<img src='cimetiere.jpeg'>
The image provided as an attachment, as you can see, shows the entrance to a cemetery with:

- a **green sign** that, once zoomed in, reads **COMMUNE DE PFASTATT**;
- a **metal gate** with no-vehicle-access signs;
- a **church with a bell tower** clearly visible in the background.

Uploading the image to Google's "Search by image" feature (which uses Google Lens), the first visually similar match we get is the following:

<img src="pfastatt.png">

We can confirm that the cemetery is located in **Pfastatt**, a municipality in Haut-Rhin in Alsace, in the northwestern outskirts of Mulhouse.

### Identification of the Scientist

Searching Google for scientists connected to Pfastatt, the first result that appears is the Wikipedia page dedicated to Katia and Maurice Krafft.

<img src="query.png">

From the page we get all the information needed to reconstruct the flag.

<img src="maria_krafft.png">

One curious aspect is the challenge title itself, which immediately caught my attention since I'm not a French native speaker. After a brief search I discovered that **Chaud devant** is a French expression used mainly in kitchens to warn that someone is passing by with a hot dish. In this context, it's clearly a pun referring to the extreme heat typical of volcanic eruptions and pyroclastic flows (nuées ardentes).

---

## Flag

```
404CTF{1991_Unzen_Krafft_17_03}
```