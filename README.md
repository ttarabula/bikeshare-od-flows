# Bike Share Toronto — 2025 data explorations

Thirteen maps and analyses built from the City of Toronto's public Bike Share ridership data (7.8 million trips in 2025) and the live GBFS station feed.

**Live site:** <https://ttarabula.github.io/bikeshare-od-flows/>

## Headline findings

- **45 of 50** top high-demand routes without protected bike infrastructure are **not covered by any current City plan** (built + 2025-2027 near-term + 10-year). The worst offender is *Windsor/Newcastle ↔ Grand Avenue Park* in Mimico: 3,229 trips/year, 0% built, 0% planned.
- **Downtown Toronto is three bike-neighbourhoods, not one**, in Louvain-community terms — Financial District, Annex/Midtown, and East Downtown/Harbourfront each hang together as functional zones.
- **Toronto's peak moment is Saturday 7:18 PM**, not Monday 8 AM. On Jun 14, 2025 at that time, **2,017 bikes were simultaneously in flight** across the city.
- **The Toronto Islands have their own permanent bike sub-fleet** — a handful of bikes (e.g. Bike #9200) that live exclusively on Centre Island / Ward's Island / Hanlan's Point and never cross to the mainland.
- **Casuals round-trip 4.8× more than members** and cluster on the waterfront/Islands; members commute downtown core.
- **Polson Pier is the nightlife champion** — 46% of its weekday activity happens after 8 PM.

## Data gotcha worth flagging

The `End_Station_Name` column in the ridership CSVs is unreliable — it frequently echoes `Start_Station_Name` rather than the true destination. All analyses here join by `End_Station_Id` against the GBFS station feed to recover the true coordinates and names.

## Reproducing

```sh
uv sync
uv run jupyter lab
```

Open `notebooks/01_first_look.ipynb` → `notebooks/10_gap_vs_plans.ipynb`. Every HTML artifact in `docs/` is reproduced by running the corresponding notebook.

## Layout

```
notebooks/       # EDA, one per analytical layer
src/bikeshare/   # reusable fetch helpers (CKAN, GBFS)
data/raw/        # downloaded CSVs / GeoJSON / shapefiles (gitignored — re-fetch)
data/processed/  # HTML maps (mirrored into docs/ for GitHub Pages)
docs/            # deployed artifact
```

## Data sources

All from [open.toronto.ca](https://open.toronto.ca):

- **Bike Share Toronto Ridership Data** — historical trip-level CSVs (2014-2026)
- **Bike Share Toronto** (GBFS feed) — live station information (id/name/lat/lon/capacity)
- **Cycling Network** — existing protected bike lanes, cycle tracks, multi-use trails
- **Near-term Cycling Program (2025-2027 and 2022-2024)** — committed plans
- **10 Year Cycling Network Plan (2016)** — trails + on-street

Unaffiliated with Bike Share Toronto, PBSC Urban Solutions, or the City of Toronto.
