# Canular savant (3/3)

**Competition:** 404CTF 2026 <br>
**Category:** OSINT

<img src="canular3.png">

---

## Solution

### Geolocating the crosswalk

From Canular Savant 1 we know the starting point is the **Rond-point des Champs-Élysées-Marcel-Dassault**. From Canular Savant 2 we know the person is moving **northward**.

In the Canular Savant 3 prompt there is an interesting clue: the sun was "resting" on the traffic light diametrically opposite to me.

This image immediately made me think of those iconic photos that circulate online, where the sun aligns perfectly with a monument.

In Paris, the most famous phenomenon of this kind is the **sunset perfectly aligned with the Arc de Triomphe**, visible along the axis of the Champs-Élysées.

<img src="champs-elysees.png">

To confirm the intuition I searched on Google:

```
soleil couchant arc de triomphe paris rond-point
```

and landed on this article from the SAF (https://saf-astronomie.fr/soleil-couchant-paris/):

<img src="SAF.png">

The text confirms exactly what the challenge describes: turning their head westward, the person sees the sun setting perfectly aligned with the Arc de Triomphe, as if it were "resting" on the traffic light on the other side of the street.


### First reasoning mistake

The SAF article clearly states that the sun aligns with the Champs-Élysées axis **twice a year: in May and in August**.

From there I made my first wrong turn: since we're in May, I thought the May window had just passed or was ending, so the next useful occasion would be in August.

At that point I looked among the Bourbaki members for anyone with a birthday around late July to early August:

- Henri Cartan: 29 July 1904
- Jacques Tits: 12 August 1930

The reasoning seemed consistent, so I tried the flag:

```
404CTF{henri-cartan}
```

Wrong, one attempt wasted.

### Trying the May lead

The walk described in the challenge takes place around **10 May 2026**.

<img src="calcsun.png">

To verify the solar alignment I opened SunTrace3D https://www.suntrace3d.com/it/viewer?lat=48.869037&lng=2.309609&q=48.8690%2C+2.3096

I placed the pin exactly on the crosswalk point: **48.8690, 2.3096**.

Setting the date to **10 May 2026** and dragging the time slider toward **21:00**, it's clear: the **yellow line** connecting the point to the sun points precisely northwest, following the axis of the **Champs-Élysées**.

### The Bourbaki members

The phrase "environ une semaine avant" clearly points to a birthday around **3–4 May**.

At this point I opened the Wikipedia page for Nicolas Bourbaki, going through each member's biography:

```
https://en.wikipedia.org/wiki/Nicolas_Bourbaki
```

and started scrolling through the list of known members looking for anyone born **at the beginning of May**.

I found two perfectly compatible candidates:

| Name | Date of birth | Delta from ~10 May |
|------|--------------|---------------------|
| **Claude Chabauty** | 4 May 1910 | ~6 days |
| **André Weil** | 6 May 1906 | ~4 days |

My second (wrong) attempt was **Claude Chabauty**. At that point I crossed my fingers and tried the other name: **André Weil**. Fortunately, it was him.

---

## Flag

```
404CTF{andre-weil}
```