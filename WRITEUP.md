# 45 of 50: where Toronto's bike-share data is screaming, and the City's plan isn't listening

*A data analysis of 7.8 million 2025 Bike Share Toronto trips. Full interactive site: <https://ttarabula.github.io/bikeshare-od-flows/>*

---

## The finding

Between two stations in Mimico — **Windsor St / Newcastle St** and **Grand Avenue Park**, less than a kilometre apart — Torontonians made **3,229** Bike Share trips in 2025. That's almost nine rides a day, on streets with zero metres of protected bike infrastructure. The City's 2025-2027 Programmed Cycling Projects don't touch this route. Neither does the 2022-2024 program that just finished, or the 2016 10-Year Cycling Network Plan.

That corridor isn't an exception. It's the headline entry in a list of **45 high-demand routes** that nobody has planned to protect. I pulled the City's entire portfolio of committed cycling infrastructure — everything built, everything under construction, and everything on the books through the 10-year plan — and measured how much of each gap route it covers. **Of the top 50 routes where cyclists are riding heavily without a safe lane, only 3 reach 50% coverage when you throw every plan at them. Forty-five are orphans, below 15% combined coverage. The plan doesn't reach them.**

## How I got there

Start with the open dataset. Bike Share Toronto publishes every trip: origin station, destination station, timestamps, user type, bike model. In 2025 that's 7,812,520 rides across 1,030 stations and 9,534 individual bikes. Join by station ID to the live GBFS feed to get coordinates, and suddenly you have a directed graph of the city weighted by revealed cycling demand.

The natural first question is: do certain routes carry more rides than geography alone predicts? Fit a simple gravity model — *expected trips ∝ capacity_A × capacity_B / distance^1.59* — and rank pairs by actual ÷ expected. The top of that ranking is a list of Toronto's **desire lines**: routes where cyclists travel far more than distance and station size alone would explain. Something is pulling them there.

The obvious next question: is "something" protected bike infrastructure? I fetched the City's Cycling Network dataset (1,538 segments across 10 categories), filtered to real protected facilities (cycle tracks, bike lanes, multi-use trails, bridges — excluding sharrows and signed-routes-without-paint), projected everything to a metric CRS, buffered the bike-lane network by 50 m, and measured the fraction of each desire-line straight-line path that falls within the buffer.

I expected a strong positive correlation: desire lines trace bike lanes. The answer was Spearman r = 0.09 and top-50 desire lines average 37% lane coverage vs. 39% for random pairs. The infrastructure and the demand are basically decorrelated.

Which is when the finding flipped into something better: **the top high-demand routes don't sit on bike lanes because the bike lanes aren't there yet**.

## The 15 worst-served corridors

Trim to routes with ≥ 400 trips/year, top-25% affinity, < 20% existing lane coverage, and ≥ 500 m distance. Sort by trip volume. Cross-check against all three plan datasets. What remains are the "orphan" gap routes — high demand, nothing built, nothing planned:

| Station A | Station B | Trips/yr | Dist | Built | Planned |
|---|---|---:|---:|---:|---:|
| Windsor St / Newcastle St | Grand Avenue Park | 3,229 | 0.9 km | **0%** | **0%** |
| College St / Major St | Robert St / Bloor St W | 1,923 | 0.9 km | 13% | 14% |
| Windsor St / Newcastle St | 36 Park Lawn Rd | 1,781 | 1.3 km | **0%** | 16% |
| Union Station | Front St W / Blue Jays Way | 1,755 | 0.9 km | 12% | 23% |
| Dundas St E / Regent Park Blvd | Yonge St / Dundas Sq | 1,656 | 1.6 km | 17% | 7% |
| Dundas St W / Yonge St | Dundas St E / Regent Park Blvd | 1,605 | 1.7 km | 17% | 12% |
| Union Station | Front St W / Spadina Ave | 1,580 | 1.3 km | 16% | 23% |
| King St W / Portland St | Simcoe St / King St W | 1,486 | 1.2 km | 13% | 22% |
| College St / Huron St | Soho St / Queen St W | 1,268 | 1.0 km | 14% | 6% |
| Soho St / Queen St W | Baldwin St / Spadina Ave | 1,159 | 0.7 km | 5% | 3% |
| Yonge St / Dundas Sq | Shuter St / River St | 1,039 | 1.8 km | 10% | 12% |
| Lisgar Park | King St W / Portland St | 936 | 1.9 km | 5% | 16% |
| Dundas St W / Yonge St | Dundas St E / Parliament St | 913 | 1.3 km | 8% | 8% |
| College Park — Yonge St | Wellesley St E / Parliament St | 900 | 1.4 km | 20% | 24% |
| Marilyn Bell Park | Humber Bay Shores / Marine Parade | 877 | 3.3 km | 4% | **0%** |

The geography is a tell. Two distinct clusters:

**The West End** (Mimico, Humber Bay Shores, Parkdale, Liberty Village, High Park) shows up as the single most under-served part of the city. Windsor/Newcastle pairs appear three times in the table. Park Lawn, Humber Bay Shores, Marilyn Bell Park — all cycling-dead-zone addresses where cyclists are riding anyway.

**Downtown cross-axis trips** — Regent Park ↔ Yonge-Dundas, Union Station ↔ King West, Chinatown (Baldwin, Soho, Huron) — are the second cluster. These are short, dense, business-district routes where the plan provides 5–25% coverage on corridors that carry 900-1700 annual trips each.

## The caveats

The straight-line A→B is a proxy for the actual ride path. A routing engine (OSRM, GraphHopper) would give a more accurate lane-coverage measure; I bet the signal would get *stronger*, not weaker, because cyclists often detour to find protection. Still, straight-line is a conservative baseline and worth naming.

The gravity baseline uses dock capacity as a "mass" proxy — it under-predicts trips to destinations like parks and transit hubs where people don't live but do arrive. The Marilyn Bell Park / Humber Bay Shores pair has inflated affinity for that reason. The finding survives anyway because trip volumes are large and the West End/downtown clustering dominates.

"Covered by a plan" means: the straight-line path falls within 50 m of a planned facility that's a real protected type (cycle track, bike lane, multi-use trail, buffered lane, bridge, tunnel). I dropped every item categorised as "Study or Design" from the 2025-2027 program, because a study isn't a commitment. I also dropped "Signed and marked route" from the 10-year plan, because that's signage, not infrastructure.

Finally: `End_Station_Name` in the Bike Share CSVs is a corrupt column — it frequently echoes `Start_Station_Name` rather than the true destination. Join by `End_Station_Id` against the GBFS feed and you're fine. If you're working with this data, that gotcha will save you an afternoon.

## What's there to do

The City's cycling program runs on three-year rolling plans. The next one will be 2028-2030. If you're at the City, this data is an argument for a West End initiative and for densifying downtown cross-axis protection. If you're at Cycle Toronto or a councillor's office, these 15 specific addresses are a concrete list — one that came out of measured demand, not out of a map-room exercise. If you just want to ride on these streets tomorrow, well — the data is already screaming on your behalf.

All thirteen maps from this project, plus the notebooks that produced them, are at <https://ttarabula.github.io/bikeshare-od-flows/>. Source on GitHub: <https://github.com/ttarabula/bikeshare-od-flows>. Data from [open.toronto.ca](https://open.toronto.ca) and the GBFS feed at bikesharetoronto.com. Unaffiliated with Bike Share Toronto, PBSC Urban Solutions, or the City of Toronto.

---

## Twitter / Mastodon thread version

Seven posts, roughly.

**1/**
I analyzed 7.8 million Bike Share Toronto rides from 2025 and overlaid the top high-demand routes on the City's cycling plans.

45 of 50 top routes where cyclists are riding without protected infrastructure are **not covered by any current City plan**.

🧵 https://ttarabula.github.io/bikeshare-od-flows/

**2/**
Method: fit a gravity model to the OD matrix (expected trips ∝ capacity × capacity / distance^1.59). Rank station pairs by actual ÷ expected. Top of that list is Toronto's "desire lines" — routes cyclists pick far more than geography would predict.

**3/**
Initial hypothesis: desire lines should track the existing bike-lane network.

They don't. Top-50 desire lines average 37% lane coverage. Random-50 average 39%. Spearman r = 0.09.

The finding flipped: *the top-demand routes don't sit on bike lanes because the bike lanes aren't there yet.*

**4/**
The worst orphan gap in Toronto: **Windsor/Newcastle ↔ Grand Avenue Park in Mimico**. 3,229 trips/year, 0% built infrastructure, 0% planned infrastructure. Less than a kilometre apart. Nobody is building this.

**5/**
Two distinct clusters of orphan routes:

— The **West End** (Mimico, Humber Bay Shores, Parkdale, Liberty Village, High Park)
— **Downtown cross-axis** (Regent Park ↔ Yonge-Dundas, Union Station, Chinatown)

Full 15-row table, affinity scores, and maps at the site link.

**6/**
Map: magenta arcs = high-demand orphan routes. Green lines = existing protected infrastructure. Amber = what's planned. The orphans don't overlap either.

(Embed: the gap_vs_plans_map screenshot or the OG image.)

**7/**
Code + notebooks: https://github.com/ttarabula/bikeshare-od-flows

All data is from open.toronto.ca (Bike Share ridership, cycling network, near-term program, 10-year plan). One gotcha that cost me a day: `End_Station_Name` is unreliable — always join by `End_Station_Id` via GBFS.

/end
