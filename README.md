# NBS Valuation Tool

A Streamlit web application that produces **site-specific estimates of ecosystem service benefits and restoration costs** for Nature-Based Solutions (NBS) projects.

Users define a project location and area, select a biome, and the tool automatically fetches spatial data from Google Earth Engine and Google Cloud Storage to run calibrated meta-regression models. The result is a set of **per-hectare-per-year benefit estimates** (in current USD) and **intervention cost estimates** for the chosen site.

The tool is designed to support early-stage decision-making — delivering consistent, transparent numbers quickly, without requiring specialist GIS or modelling skills.

---

## Features

- **Five biome models** — Tropical Forest, Temperate Forest, Intensive Land Use, Mangroves, Grassland
- **Automatic spatial variable extraction** from Google Earth Engine (climate, land cover, biodiversity, population, economics)
- **Meta-regression benefit estimates** across multiple SEEA-aligned ecosystem service categories
- **Two cost modelling approaches** — global raster layers (Busch et al. 2024) for forest/mangrove biomes; NBS-type regression model (WOCAT data) for land-use biomes
- **PPP-adjusted currency conversion** to 2024 USD via the World Bank Data360 API
- **CSV export** of all variables, benefits, and costs
- **Interactive map** for drawing or manually entering project area

---

## Screenshots

| Step | View |
|------|------|
| Biome selection | Five clickable biome cards |
| Project location | Draw polygon on satellite map or enter lat/lon/area manually |
| Spatial variables | Extracted GEE values shown per predictor; manual override supported |
| Benefit results | Per-service USD/ha/yr metrics with Exchange Value and Consumer Surplus tabs |
| Cost results | Per-intervention USD/ha/yr metrics |

---

## Requirements

- Python 3.12+
- A Google Cloud service account with **Earth Engine** and **Cloud Storage** read access to the `nbs-tool-public` bucket

---

## Installation

```bash
git clone https://github.com/koentieskens/EcosystemValues.git
cd EcosystemValues
pip install -r requirements.txt
```

---

## Configuration

Create `.streamlit/secrets.toml` and add your Google service account JSON as a dictionary:

```toml
[google_sa_secrets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\n..."
client_email = "your-sa@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```

> **Note:** `.streamlit/secrets.toml` is listed in `.gitignore` and will never be committed.

---

## Running the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How to use

### 1 — Select a biome

Click the biome that best represents your project area. Some biomes require a sub-category selection:

| Biome | Sub-categories |
|-------|---------------|
| Tropical Forest | — |
| Temperate Forest | Temperate evergreen forest · Other |
| Intensive Land Use | Cropland annual · Monoculture perennial · Other |
| Mangroves | — |
| Grassland | — |

### 2 — Define the project area

Either **draw a polygon** on the interactive satellite map using the drawing tools, or enter **latitude, longitude, and area (ha)** manually and click **Activate Manual Input**.

Once a location is active, the sidebar shows your coordinates, country, and area.

### 3 — Extract spatial variables

Under **Spatial Predictor Variables**, click **Extract Spatial Values from GEE** for the Benefit and/or Cost tabs. This fetches site-specific values (temperature, precipitation, biodiversity intactness, population density, GNI, etc.) from Google Earth Engine and fills the input fields automatically. You can override any value manually.

### 4 — Select ecosystem services and calculate benefits

Check the ecosystem services you want to include, then click **Calculate Benefits**. Results appear as USD/ha/yr for two valuation approaches — Exchange Value and Consumer Surplus.

For forest biomes an additional set of globally-mapped values (Siikamäki et al. 2024) is also available.

### 5 — Select intervention type and calculate costs

Check the intervention types relevant to your project, then click **Calculate Costs**. Results are shown in USD/ha/yr.

### 6 — Export results

Once benefits are calculated, a **Download CSV** button appears in the sidebar. The export contains location metadata, all spatial variable values, and the full benefit and cost table.

---

## Ecosystem services by biome

### Tropical Forest
| Service | SEEA Code |
|---------|-----------|
| Wood Provision | 1.5 |
| Wild Fish Provision | 1.6 |
| Air Filtration | 2.4 |
| Pollination | 2.17 |
| *Global layers (Siikamäki):* Recreation · Non-wood forest products · Water services · Habitat & species protection | |

### Temperate Forest
| Service | SEEA Code |
|---------|-----------|
| Wood Provision | 1.5 |
| Air Filtration | 2.4 |
| Soil Quality Regulation | 2.5 |
| *Global layers (Siikamäki):* Recreation · Non-wood forest products · Water services · Habitat & species protection | |

### Intensive Land Use
| Service | SEEA Code |
|---------|-----------|
| Crop Provision | 1.1 |
| Wood Provision | 1.5 |
| Livestock Provision | 1.3 |
| Pollination | 2.17 |
| Soil Erosion Control | 2.6 |
| Recreation | 3.1 |
| Visual Amenity | 3.2 |

### Mangroves
| Service | SEEA Code |
|---------|-----------|
| Wild Fish Provision | 1.6 |
| Aquaculture Provision | 1.4 |
| Wood Provision | 1.5 |
| Wild Animals Provision | 1.7 |
| Soil Erosion Control | 2.6 |
| Coastal Protection (Menendez et al. 2020) | 2.14 |

### Grassland
| Service | SEEA Code |
|---------|-----------|
| Wild Animals Provision | 1.7 |
| Water Supply | 1.9 |
| Grazed Biomass Provision | 1.2 |
| Livestock Provision | 1.3 |
| Pollination | 2.17 |
| Nutrient Retention | 2.9 |
| River Flood Mitigation | 2.14 |
| Soil Erosion Control | 2.6 |
| Recreation | 3.1 |

---

## Cost models

| Biome | Model | Source |
|-------|-------|--------|
| Tropical Forest | Global raster layers (opportunity cost + implementation cost) | Busch et al. (2024) *Nature Climate Change* |
| Temperate Forest | Global raster layers | Busch et al. (2024) |
| Mangroves | Global raster layers | Busch et al. (2024) |
| Intensive Land Use | Meta-regression (NBS type × site variables) | Reynolds et al. (2024) / WOCAT |
| Grassland | Meta-regression (NBS type × site variables) | Reynolds et al. (2024) / WOCAT |

All outputs are converted to **2024 USD/ha/yr** using World Bank PPP conversion factors and local inflation adjustment.

---

## Architecture

```
app.py  (EcoApp)
│
├── initialize()        GCP auth, session state
├── welcome()           Title + instructions
├── biomes()            Biome selection
├── location()          Interactive map + manual input
├── benefits()          ES selection + meta-regression
└── costs()             Intervention selection + cost prediction

src/
├── models/
│   ├── benefit_models.py   One class per biome (constants, variables, ES)
│   └── cost_models.py      Cost model classes
├── predictions/
│   └── meta_regression.py  Predict class (log, IHS transforms + regression)
├── app_utils/
│   ├── calculation_engine.py   Orchestrates benefits + costs + currency
│   ├── session_states.py       SessionStateManager (all st.session_state keys)
│   ├── ui_components.py        All non-map UI widgets
│   └── utils.py                St_Utils, CurrencyConverter
├── extract_data/
│   └── get_images.py       Google Earth Engine image extraction
└── utils/
    ├── spatial.py          CRS, circle geometry, COG raster reading
    └── wb360.py            World Bank Data360 API wrapper
```

---

## Running the tests

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-mock

# Run all tests
pytest tests/ -v

# Run only unit tests (no Streamlit runner)
pytest tests/ -v --ignore=tests/test_app_streamlit.py

# Run Streamlit integration tests
pytest tests/test_app_streamlit.py -v
```

The test suite (51 tests) runs fully offline — all GEE, GCS, World Bank, and Streamlit session state calls are mocked.

| File | Coverage |
|------|----------|
| `test_meta_regression.py` | Math helpers, prediction pipeline, area limiter |
| `test_spatial.py` | CRS detection, circle geometry, WB gap-fill, COG value extraction |
| `test_utils.py` | Geodesic area, location lookup, PPP/USD conversion, WB360 API |
| `test_calculation_engine.py` | CalculationEngine with all external deps mocked |
| `test_app_streamlit.py` | Full app via `streamlit.testing.v1.AppTest` — biome buttons, location, benefits, costs, GEE extract |

---

## Data sources

| Data | Source |
|------|--------|
| Ecosystem service value functions | Brander et al. (2025) |
| Forest global benefit layers | Siikamäki et al. (2024), World Bank |
| Mangrove coastal protection | Menendez et al. (2020) |
| Forest/mangrove cost layers | Busch et al. (2024), *Nature Climate Change* |
| Land use cost model | Reynolds et al. (2024) / WOCAT SLM database |
| Biodiversity Intactness Index | Newbold et al. (2016) |
| Human Modification Index | Kennedy et al. (2020) |
| Population density | CIESIN GPWv4 |
| Climate variables | ERA5-Land (ECMWF) |
| Land cover | ESA CCI Global Land Cover |
| PPP conversion | World Bank Data360 / IMF WEO |

---

## License

This project is developed by the World Bank Group. Please refer to the repository for licence terms.
