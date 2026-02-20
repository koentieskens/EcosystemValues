# NBS Valuation Tool

A Streamlit web application that produces **site-specific estimates of ecosystem service benefits and restoration costs** for Nature-Based Solutions (NBS) projects.

Users define a project location and area, select a biome, and the tool automatically fetches spatial data from Google Earth Engine and Google Cloud Storage to run calibrated meta-regression models. The result is a set of **per-hectare-per-year benefit estimates** (in current USD) and **intervention cost estimates** for the chosen site.

The tool is designed to support early-stage decision-making, delivering consistent, transparent numbers quickly, without requiring specialist GIS or modeling skills.

---

## Features

- **Five biome models** — Tropical Forest, Temperate Forest, Intensive Land Use, Mangroves, Grassland
- **Automatic spatial variable extraction** from Google Earth Engine (climate, land cover, biodiversity, population, economics)
- **Meta-regression benefit estimates** across multiple SEEA-aligned ecosystem service categories
- **Two cost modeling approaches** — global raster layers (Busch et al. 2024) for forest biomes; NBS-type regression model (WOCAT data) for agricultural biomes
- **PPP-adjusted currency conversion** to 2024 USD via the World Bank Data360 API
- **CSV export** of all variables, benefits, and costs
- **Interactive map** for drawing or manually entering project area

---

## Screenshots


### Biome selection 
![](docs/screenshots/biome_selection.png)
### Project location and spatial variables
![](docs/screenshots/project_location.png) 
### Benefit results
![](docs/screenshots/es_benefits.png)      
### Cost results
![](docs/screenshots/nbs_costs.png)        

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

### 2  Define the project area

Either **draw a polygon** on the interactive satellite map using the drawing tools and click activate polygon, or enter **latitude, longitude, and area (ha)** manually and click **Activate Manual Input**.

Once a location is active, the sidebar shows your coordinates, country, and area.

### 3  Extract spatial variables

Under **Spatial Predictor Variables**, click **Extract Spatial Values from GEE** for the Benefit and/or Cost tabs. This fetches site-specific values (temperature, precipitation, biodiversity intactness, population density, GNI, etc.) from Google Earth Engine and fills the input fields automatically. You can override any value manually, e.g. for simulating interventions.

### 4  Select ecosystem services and calculate benefits

Check the ecosystem services you want to include, then click **Calculate Benefits**. Results appear as USD/ha/yr for two valuation approaches: Exchange Value and Consumer Surplus.


### 5  Select intervention type and calculate costs

Check the intervention types relevant to your project, then click **Calculate Costs**. Total estimated costs are shown in USD/ha/yr.

### 6  Export results

Once benefits are calculated, a **Download CSV** button appears in the sidebar. The exported csv contains location metadata, all spatial variable values, and the full benefit and cost table.

---

## Ecosystem services by biome
NBS Valuation Tool currently supports the benefit estimates for a range of biome specific ecosystem services, following SEEA classification. They are listed below. 

### Tropical Forest
| Ecosystem Service                           | Grouping                     | Value estimation source           |
|---------------------------------------------|------------------------------|-----------------------------------|
| Wood Provision                              | -                            | ESVD meta-analytic value function |  
| Wild Fish Provision                         | -                            | ESVD meta-analytic value function |
| Air Filtration                              | -                            | ESVD meta-analytic value function |
| Pollination                                 | -                            | ESVD meta-analytic value function |
| Wild animals, plants and other provisioning | Non-wood forest products     | Siikamäki et al. 2024 global data |
| Water supply                                | Forest water services        | Siikamäki et al. 2024 global data |
| Rainfall pattern regulation                 | Forest water services        | Siikamäki et al. 2024 global data |
| Soil erosion control                        | Forest water services        | Siikamäki et al. 2024 global data |
| Water purification                          | Forest water services        | Siikamäki et al. 2024 global data |
| Water flow regulation                       | Forest water services        | Siikamäki et al. 2024 global data |
| River flood mitigation                      | Forest water services        | Siikamäki et al. 2024 global data |
| Recreation-related                          | Recreation, hunting, fishing | Siikamäki et al. 2024 global data |
| Ecosystem and species appreciation          | Recreation, hunting, fishing | Siikamäki et al. 2024 global data |
 
### Temperate Forest
| Ecosystem Service                           | Grouping                     | Value estimation source           |
|---------------------------------------------|------------------------------|-----------------------------------|
| Wood Provision                              | -                            | ESVD meta-analytic value function |
| Air Filtration                              | -                            | ESVD meta-analytic value function |
| Soil quality regulation                     | -                            | ESVD meta-analytic value function |
| Wild animals, plants and other provisioning | Non-wood forest products     | Siikamäki et al. 2024 global data |
| Water supply                                | Forest water services        | Siikamäki et al. 2024 global data |
| Rainfall pattern regulation                 | Forest water services        | Siikamäki et al. 2024 global data |
| Soil erosion control                        | Forest water services        | Siikamäki et al. 2024 global data |
| Water purification                          | Forest water services        | Siikamäki et al. 2024 global data |
| Water flow regulation                       | Forest water services        | Siikamäki et al. 2024 global data |
| River flood mitigation                      | Forest water services        | Siikamäki et al. 2024 global data |
| Recreation-related                          | Recreation, hunting, fishing | Siikamäki et al. 2024 global data |
| Ecosystem and species appreciation          | Recreation, hunting, fishing | Siikamäki et al. 2024 global data |

### Intensive Land Use
| Ecosystem Service    | Value estimation source           |
|----------------------|-----------------------------------|
| Crop Provision       | ESVD meta-analytic value function |
| Wood Provision       | ESVD meta-analytic value function |
| Livestock Provision  | ESVD meta-analytic value function |
| Pollination          | ESVD meta-analytic value function |
| Soil Erosion Control | ESVD meta-analytic value function |
| Recreation           | ESVD meta-analytic value function |
| Visual Amenity       | ESVD meta-analytic value function |

### Mangroves
| Ecosystem Service      | Value estimation source                    |
|------------------------|--------------------------------------------|
| Wild Fish Provision    | ESVD meta-analytic value function          |
| Aquaculture Provision  | ESVD meta-analytic value function          |
| Livestock Provision    | ESVD meta-analytic value function          |
| Wood Provision         | ESVD meta-analytic value function          |
| Wild Animals Provision | ESVD meta-analytic value function          |
| Soil Erosion Control   | ESVD meta-analytic value function          |
| Coastal Protection     | Menendez et al, (2020) process based model |


### Grassland
| Ecosystem Service        | Value estimation source            |
|--------------------------|------------------------------------|
| Water Supply             | ESVD meta-analytic value function  |
| Wild Animals Provision   | ESVD meta-analytic value function  |
| Grazed Biomass Provision | ESVD meta-analytic value function  |
| Livestock Provision      | ESVD meta-analytic value function  |
| Pollination              | ESVD meta-analytic value function  |
| Nutrient Retention       | ESVD meta-analytic value function  |
| River Flood Mitigation   | ESVD meta-analytic value function  |
| Soil Erosion Control     | ESVD meta-analytic value function  |
| Recreation               | ESVD meta-analytic value function  |

---

## Cost models

| Biome              | Model                            | Source                          |
|--------------------|----------------------------------|---------------------------------|
| Tropical Forest    | Global raster layers             | Busch et al. (2024)             |
| Temperate Forest   | Global raster layers             | Busch et al. (2024)             |
| Mangroves          | Global raster layers             | Busch et al. (2024) global data |
| Intensive Land Use | Meta-regression                  | Reynolds et al. (2024) / WOCAT  |
| Grassland          | Meta-regression                  | Reynolds et al. (2024) / WOCAT  |


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

## Data sources

| Data                                   | Source                                      |
|----------------------------------------|---------------------------------------------|
| ESVD Ecosystem service value functions | Brander et al. (2025)                       |
| Forest global benefit layers           | Siikamäki et al. (2024)                     |
| Mangrove coastal protection            | Menendez et al. (2020)                      |
| Forest/mangrove cost layers            | Busch et al. (2024)                         |
| Land use cost model                    | Reynolds et al. (2024) / WOCAT SLM database |
| Biodiversity Intactness Index          | Newbold et al. (2016)                       |
| Human Modification Index               | Kennedy et al. (2020)                       |
| Population density                     | CIESIN GPWv4                                |
| Climate variables                      | ERA5-Land (ECMWF)                           |
| Land cover                             | ESA CCI Global Land Cover                   |
| PPP conversion                         | World Bank Data360 / IMF WEO                |

---

## License

TBD
