# Asset Page Integration - Image Rater

## Brugerflow på Asset Siden

```
┌─────────────────────────────────────────────────────────────┐
│  ComfyUI Asset Page / Gallery                               │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │
│  │ IMG │ │ IMG │ │ IMG │ │ IMG │ │ IMG │  ← Dine billeder │
│  │  1  │ │  2  │ │  3  │ │  4  │ │  5  │                   │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘                   │
│                                                              │
│  [Rate Selected] [Move to Folder] [Batch Process]           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  ImageRater Node (automatisk)                               │
│  - Analyserer hvert billede                                  │
│  - Giver score 1-10                                          │
│  - Gemmer metadata                                           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  ImageOrganizer Node                                        │
│  - excellent/ (8-10) → /output/rated/excellent/             │
│  - good/ (5-7)   → /output/rated/good/                      │
│  - acceptable/ (3-4) → /output/rated/acceptable/            │
│  - rejected/ (1-2) → /output/rated/rejected/                │
└─────────────────────────────────────────────────────────────┘
```

## Integration Muligheder

### 1. **Workflow-baseret** (Nuværende løsning)

Tilføj nodes direkte i dit genererings-workflow:

```
LoadImage → ImageRater → ImageOrganizer → SaveImage
```

**Fordele:**
- Automatisk rating ved hver generation
- Ingen manuel intervention
- Alle billeder bliver rated

### 2. **Batch Processing Node** (Ny feature)

En node der kan rate eksisterende billeder i en mappe:

```python
BatchImageRater:
  - input_directory: "/home/jens/ComfyUI/output/"
  - rating_method: "heuristic"
  - move_to_rated: True
  - output_structure: "by_score"
```

### 3. **Custom Asset Panel Widget** (Avanceret)

Tilføj et panel direkte i ComfyUI's asset side:

```
┌──────────────────────────────────────┐
│  Image Rater Panel                   │
│  ─────────────────────────────────   │
│  Selected: 12 images                 │
│                                      │
│  Rating Method: [heuristic ▼]       │
│  Min Score: [5.0 ─────○────]        │
│                                      │
│  [▶ Rate Selected] [📁 Organize]    │
│                                      │
│  Results:                            │
│  ████████░░ 8/12 rated               │
│  Avg Score: 7.2                      │
└──────────────────────────────────────┘
```

## Foreslåede Tilføjelser til Projektet

### A) Batch Rating Node
```python
class BatchImageRaterNode:
    """Rate alle billeder i en mappe"""
    INPUTS: {
        "input_directory": "STRING",
        "output_base": "STRING", 
        "rating_threshold": "FLOAT",
        "auto_organize": "BOOLEAN"
    }
```

### B) Rating Display Overlay
```python
# Vis score direkte på preview
def add_score_overlay(image, score):
    """Tegner score i hjørnet af billede"""
    - Score: 8.5/10 ⭐
    - Farve: Grøn (8-10), Gul (5-7), Rød (1-4)
```

### C) Quick Action Buttons
```python
# Komprimerede actions til asset panel
- ⭐ Rate All
- 📁 Sort by Score
- 🗑️ Delete < 3.0
- ⭐ Keep Top 10%
```

## Implementation Priority

1. **Fase 1 (Nuværende)** ✅
   - ImageRater node
   - ImageOrganizer node
   - Basis workflow integration

2. **Fase 2 (Asset Panel)** 
   - BatchImageRater node
   - Score overlay på previews
   - Quick action knapper

3. **Fase 3 (Full Integration)**
   - Custom ComfyUI sidebar panel
   - Real-time rating under generation
   - Filter/sort på asset siden

## Næste Skridt

**Vil du have mig til at:**

1. **Oprette BatchImageRater node** - Kan rate hele mapper med eksisterende billeder?

2. **Tilføje score overlay** - Vis rating direkte på PreviewImage nodes?

3. **Lave et komplet eksempel-workflow** - Der matcher dit asset panel setup?

4. **Researche ComfyUI's asset panel API** - Så vi kan lave rigtig integration?

Sig til hvilken retning der giver mest mening for dit use case! 🚀
