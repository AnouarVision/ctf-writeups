# Girolamo Trombetta

**Competition:** ITSCyberGame
**Category:** OSINT

---

## Description

> An international hacker is hampering humanitarian aid in high-fire-risk areas. After long research and investigation we found the username of his laptop — can you help find his password? We only know that one of the areas he leaves almost undisturbed is the one in the photo (taken a few weeks ago). It seems his password is the scientific name of an animal species extinct in the nearby area plus the year of its extinction. flag{genus_species_year}

The required format is `flag{genus_species_year}`, where `genus_species` is the binomial scientific name (underscore-separated) of a species extinct in the zones near the image, and `year` is the year the extinction was declared.

---

## Solution

### 1. Initial reconnaissance — image analysis

The provided image is a screenshot from a satellite fire-monitoring system (NASA FIRMS / MODIS/VIIRS). Recognizable elements:

- **Red hotspots**: active fire detections
- **Dense green vegetation**: hilly/montane forests
- **A lake**: near the center-north of the frame
- **An urban settlement**: east of the lake with a radial road pattern
- **Areas with fewer hotspots**: protected or less fire-prone forest

Tools and signals used for geolocation:
- Vegetation morphology (subtropical/monsoonal forest)
- Typical urban pattern for a medium-sized Asian city
- Arrangement of lake + city + roads

### 2. Geolocation — China

The area is in **China**, likely within the Yangtze basin or southern/southwestern provinces (Sichuan/Yunnan/Hunan), regions known for:

- High seasonal fire frequency (dry season winter–spring)
- Riverine ecosystems with endemic species
- International humanitarian activity

The lake plus the east-lying urban center matches several urban areas along the Yangtze river.

### 3. Identification of the extinct species

Search criterion: a species documented as extinct in the geographic area shown. The most iconic species documented as extinct in the Yangtze is the **Baiji**, the Yangtze river dolphin.

| Field | Detail |
|-------|--------|
| Common name | Baiji / Yangtze dolphin |
| Scientific name | *Lipotes vexillifer* (Miller, 1918) |
| Habitat | Yangtze River (Changjiang), China |
| Causes of extinction | Industrialization, electrofishing, fishing nets, Three Gorges dam, pollution |
| Year declared extinct | **2006** |
| IUCN status | Critically Endangered (Possibly Extinct) / functionally extinct |

**Extinction timeline:**
- Pre-1950: ~6,000 estimated individuals
- 1980: ~400 individuals
- 1997–1999: only 13 counted
- November 2001: last verified sighting (pregnant female stranded at Zhenjiang)
- May 2002: last photographed individual (Tongling area)
- **December 2006**: a 6-week international survey across the historic range found zero baiji → declared extinct
- 2007: unconfirmed alleged sighting

Etymology: *Lipotes* (Greek) "left behind"; *vexillifer* (Latin) "flag-bearer" (referring to the small dorsal fin).

### 4. Building the flag

The flag format is `flag{genus_species_year}` with underscores between genus and species:

```
Lipotes_vexillifer → genus + '_' + specific epithet
2006 → year of extinction declaration
```

---

## Flag

```
flag{Lipotes_vexillifer_2006}
```

---

## Conclusions

This OSINT challenge required three main phases:

1. **Image geolocation**: recognize the screenshot as FIRMS/VIIRS with fire hotspots and identify the region (China/Yangtze basin) via terrain morphology, urban pattern and vegetation.
2. **Research the locally extinct species**: given the region, identify the most iconic extinct species, the Baiji (*Lipotes vexillifer*), declared extinct after a 2006 survey.
3. **Correct formatting**: apply the `flag{genus_species_year}` format with year = 2006.