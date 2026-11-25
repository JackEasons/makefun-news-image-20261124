# THE WORLD TODAY — Tuesday 24 November 2026

One front page summing up the world's news of Tuesday 24 November 2026:
**33 stories** (3 big features with illustrations, 10 small illustrated
items, 20 briefs), a big-number strip, region counts, a world map with dots
for the 13 illustrated stories, and a DATE CHECK bar. Every story below was
verified against a real published source on 24 November 2026; nothing here
is invented.

**Lead story:** the gas explosion at a hot pot eatery in Hanoi — 6 killed,
10+ in intensive care. The biggest casualty story of the day leads the page.

Region counts: ASIA 11 · EUROPE 5 · MIDDLE EAST 4 · AMERICAS 8 · AFRICA 2 ·
OCEANIA 1 · GLOBAL 2 = 33.

## Big features (illustrated)

1. **HANOI, VIETNAM — 6 KILLED IN HANOI EATERY BLAST.** A gas cylinder
   exploded at a hot pot eatery on Nguyen Van Tuyet Street, Dong Da
   district, at about 8:30am local time. The blast partly collapsed the
   building and trapped diners inside. Six people were killed and at least
   10 more were in intensive care. — *AP / Reuters*
2. **JIUQUAN, CHINA — SHENZHOU 24 LIFTS OFF WITH PAKISTAN'S FIRST
   ASTRONAUT.** China launched Shenzhou 24 to the Tiangong space station
   carrying Tang Hongbo and Wu Yi — and Pakistan's Muhammad Zeeshan Ali,
   the first foreign astronaut to fly on the station. The crew will spend
   about six months in orbit. — *AP*
3. **NEW YORK — HUAWEI GUILTY ON 10 OF 12 COUNTS.** A Brooklyn jury found
   Huawei guilty on 10 of 12 counts — bank fraud, wire fraud, sanctions
   violations and conspiring to steal trade secrets over its Iran business.
   It was acquitted on racketeering and obstruction. Sentencing is set for
   14 September 2027. — *CNN*

## Small illustrated items

4. **WASHINGTON — US READY TO SLAP TARIFFS ON CHINA, EU.** Washington is
   poised to hit China, the EU and others with tariffs after a probe into
   subsidised production. — *AP*
5. **TEHRAN — IRAN SHOWS OFF NEW MISSILE LAUNCHER.** The Revolutionary
   Guard unveiled a launcher firing two liquid-fuelled missiles as Tehran
   ruled out talks until seven US conditions are met. — *Al Jazeera*
6. **BENGHAZI, LIBYA — KYIV: LIBYA STRIKE WAS SELF-DEFENCE.** Ukraine
   defended its naval drone attack on Russian ships off Libya; Tripoli
   demanded explanations. A Russian strike killed 2 and wounded 48. — *AP*
7. **THE HAGUE — 14 NATIONS BACK ICJ ROHINGYA RULING.** The UK, Spain,
   Canada, Australia and 10 more countries recognised the court's genocide
   finding against Myanmar. — *Horizon*
8. **KUALA LUMPUR — MALAYSIA TO RETURN 6,500 ROHINGYA.** More than 6,500
   refugees are to be sent back to Myanmar in a move condemned by rights
   groups. — *All Voices News*
9. **CARACAS — VENEZUELA REVEALS $237.5BN DEBT.** Caracas disclosed its
   debt pile in a key step toward a restructuring of the country's
   obligations. — *Texas Post*
10. **WASHINGTON — GIULIANI GETS MEDAL OF FREEDOM.** President Trump
    awarded the former New York mayor the Presidential Medal of Freedom at
    the White House. — *Washington Post*
11. **BEIJING — CHINA PRESSES MIDDLE EAST PEACE PUSH.** Wang Yi met Iran's
    security chief as Xi hosted Oman's sultan — his first state visit
    since 1978 — signing 14 cooperation deals. — *Al Jazeera*
12. **ZURICH — 2031 WOMEN'S WORLD CUP: FOUR HOSTS.** FIFA picked the US,
    Mexico, Costa Rica and Jamaica to co-host the expanded 48-team
    tournament; the UK hosts 2035. — *AP*
13. **DAKAR — SENEGAL BACK AS AFCON CHAMPIONS.** Senegal were reinstated
    as 2025 Africa Cup of Nations champions after winning their appeal.
    — *Texas Post*

## Briefs

14. **KATHMANDU — 5.6 quake strikes Nepal near the China border.**
    — *Horizon*
15. **HARRISBURG — Pennsylvania measles epidemic claims a 9th death.**
    — *Horizon*
16. **ADEN — Houthis close in on Aden as Saudi strikes kill dozens.** — *AP*
17. **RIYADH — Houthi drone attack on a Riyadh tower injures 11.**
    — *Saudi civil defence*
18. **BEIJING — China bars Bloomberg reporter from Trump–Xi–Putin meet.**
    — *Providence Journal*
19. **SEOUL — South Korea shelter warning as Russian jets near airspace.**
    — *Reuters*
20. **SINGAPORE — Singapore probes Nvidia-linked Megaspeed after US ban.**
    — *Reuters*
21. **JERUSALEM — Israel warns Iran is developing chemical weapons.**
    — *Breitbart*
22. **MINSK — Lukashenko offers to fly with Zelenskiy to Moscow.**
    — *Texas Post*
23. **OTTAWA — Pentagon rebukes Canada over defence and F-35 review.** — *AP*
24. **DHAKA — Bangladesh's Hasina plans return from exile on Dec 16.** — *AP*
25. **LONDON — Two arrested over burglary at William and Kate's home.**
    — *Providence Journal*
26. **ROME — Meloni shocked at death of ex-police chief De Gennaro.**
    — *Providence Journal*
27. **WASHINGTON — Kilmar Abrego Garcia self-deports to Spain.** — *AP*
28. **BEIJING — China sentences official to death for spying.** — *AP*
29. **PYONGYANG — North Korea demands Swiss diplomatic office shut.** — *AP*
30. **HONIARA — Solomon Islands picks Australia as security partner.** — *AP*
31. **WASHINGTON — Washington beats Cincinnati 22–20 on last-second kick.**
    — *NFL*
32. **MUNICH — Bayern Munich posts record €988.2m revenue.**
    — *SportBusiness*
33. **LUSAKA — Zambia opposition leader Mundubile charged with treason.**
    — *Reuters*

## Big numbers

- **6** dead, 10+ hurt — Hanoi eatery blast
- **3** astronauts aboard — Shenzhou 24
- **10/12** counts, guilty — Huawei verdict
- **6,500** Rohingya to return — Malaysia → Myanmar
- **$237.5BN** debt pile revealed — Venezuela

## DATE CHECK — deliberately NOT 24 November news

These nearby stories are easy to mistake for today's news, so the page
names them as excluded:

- The Trump–Xi–Putin trilateral summit met on **23 Nov**; only the
  Bloomberg reporter's barring (story 18) is 24 Nov news.
- COP31 ended with no deal on **23 Nov**.
- Nvidia reinstated Jensen Huang as CEO on **23 Nov**.
- Cyclone Akvan made landfall on **20 Nov**.

## How the page is built

`draw24.py` renders `entry.png` (1024×1024, PNG) with Pillow: masthead,
dateline, big-number strip, region counts, 3 feature rows, 10 small cards
in a 5×2 grid, 20 briefs in two columns, a world map with numbered dots
for the 13 illustrated stories, and the DATE CHECK bar. `main.py` only
copies the pre-rendered `entry.png` to the output directory; it never
renders and never writes to the repository directory.
