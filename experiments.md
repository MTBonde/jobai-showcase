# Eksperimenter

Her står det, jeg undersøger. Det, der kører i drift, står i [Teknisk forklaring](tech.md).
Et eksperiment kommer først i drift, når det har bevist sig i en måling.

## Jev, en beslutningsmodel (3. nov 2026)

Jev er en system 1-model, også kaldet en beslutningsmodel. Den skriver ingen tekst. Den
svarer på typede spørgsmål med sandsynligheder: vælg et svar, giv en score på en skala,
ja eller nej. Første forsøg: kan Jev afgøre antal hjemmedage i et opslag og samtidig pege på
den sætning, der beviser det?

Testen: 14 rigtige opslag, ét felt (hjemmedage). Facit er flertallet af tre Claude-modeller,
ikke et menneske, så det er en håndtest og ikke en benchmark.

| Model | Ramte facit |
|---|---|
| Claude Fable 5.1 | 14/14 |
| Claude Opus 5.5 | 13/14 |
| Claude Sonnet 5 | 13/14 |
| Jev, første formulering | 8/14 |
| Jev, efter én rettelse i spørgsmålet | 10/14 |

Rettelsen fra 8 til 10 kom fra at læse fejlene og give Jev den samme præcisering, som
Claude-modellerne allerede fik i produktionsprompten.

| Lærdom | Hvad det betyder |
|---|---|
| Beviset kom altid som en ordret sætning | Citatet kan komme fra samme kald som svaret |
| To af de tre fejl lå, hvor svaret skulle udledes af sammenhængen; den tredje var et opslag, hvor et andet opslags tekst var havnet i fuldteksten | Høj sikkerhed (0,96+) på alle tre forkerte svar; sikkerhed alene kan ikke sortere |
| Regex-krydstjekket fangede ingen af fejlene | Et billigt tjek hjælper kun, når det fejler anderledes end det, det tjekker |
| Testen blev lavet i hånden, før noget blev bygget | Den væltede planen om at styre efter sikkerhed |
