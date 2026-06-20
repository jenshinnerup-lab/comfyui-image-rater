# ComfyUI Image Rater Node

Custom ComfyUI node til automatisk rating og organisering af genererede billeder.

## Funktioner

- **Image Rating**: Bruger ML-model til at rate billeder (1-10 eller custom skala)
- **Auto-organisation**: Flytter billeder til mapper baseret på rating
  - `output/rated/5-10/` - Top kvalitet
  - `output/rated/3-4/` - Acceptabel
  - `output/rated/1-2/` - Kasseret/low quality
- **Batch Processing**: Kan rate hele batches automatisk
- **Configurable**: Tilpas rating kriterier og mappe struktur

## Installation

```bash
cd /home/jens/ComfyUI/custom_nodes/
git clone https://github.com/jenshinnerup-lab/comfyui-image-rater.git
```

## Brug

Node vises i ComfyUI som **"Image Rater"** under "utils" eller "rating" kategorien.

### Inputs
- `images`: Billeder der skal rates
- `rating_model`: Valgfri model override
- `min_rating`: Minimum rating for at beholde (default: 1)

### Outputs
- `rated_images`: Billeder med rating metadata
- `rating_scores`: Numeriske scores
- `organized_paths`: Stier til organiserede filer

## Udvikling

### Struktur
```
comfyui-image-rater/
├── __init__.py           # Node registration
├── nodes/
│   ├── __init__.py
│   ├── image_rater.py    # Hoved node
│   └── image_organizer.py # Mappe organisering
├── models/
│   └── rating_model.py   # ML model integration
├── utils/
│   └── file_ops.py       # Filhåndtering
├── requirements.txt      # Python dependencies
└── examples/
    └── workflow.json     # Eksempel workflow
```

### Krav
- Python 3.10+
- ComfyUI 0.24+
- PyTorch
- Pillow

## Roadmap

- [ ] Grundlæggende node struktur
- [ ] Simple heuristic rating (sharpness, noise, etc.)
- [ ] ML-baseret rating model integration
- [ ] Mappe organisering logic
- [ ] Konfigurations UI
- [ ] Batch processing
- [ ] Workflow eksempler

## License

MIT
