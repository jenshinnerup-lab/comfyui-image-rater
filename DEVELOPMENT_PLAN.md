# Udviklingsplan - ComfyUI Image Rater

## Fase 1: Grundstruktur (UGT 1) ✅

- [x] Repository oprettet
- [x] Projektstruktur sat op
- [x] Basic ImageRater node (heuristic rating)
- [x] Basic ImageOrganizer node (mappe organisering)
- [x] File utilities
- [ ] Installation testet i ComfyUI
- [ ] Eksempel workflow fungerende

## Fase 2: Forbedret Rating (UGE 2-3)

### 2.1 Avancerede Heuristics
- [ ] Edge detection baseret rating
- [ ] Histogram analyse
- [ ] Face detection integration (valgfrit)
- [ ] NSFW detection filter (valgfrit)

### 2.2 ML Model Integration
- [ ] Research på pre-trained quality assessment models
  - BRISQUE (Blind/Referenceless Image Spatial Quality Evaluator)
  - NIQE (Natural Image Quality Evaluator)
  - HIFI (High-Fidelity Image Quality)
  - Custom CNN model
- [ ] Model loading og caching
- [ ] Batch inference optimering
- [ ] Model konfigurations options

## Fase 3: Brugerflade (UGE 4)

- [ ] Custom widget for rating visualization
- [ ] Real-time preview med score overlay
- [ ] Batch progress indicator
- [ ] Konfigurations panel
- [ ] Category editor UI

## Fase 4: Avancerede Funktioner (UGE 5-6)

### 4.1 Batch Processing
- [ ] Queue system til store batches
- [ ] Parallel processing
- [ ] Resume efter afbrydelse
- [ ] Progress tracking

### 4.2 Filhåndtering
- [ ] Duplicate detection
- [ ] Metadata bevaring (EXIF)
- [ ] Backup før move/copy
- [ ] Undo funktion

### 4.3 Integration
- [ ] ComfyUI Manager support
- [ ] Requirements auto-install
- [ ] Version checking
- [ ] Auto-update notification

## Fase 5: Testing & Dokumentation (UGE 7)

- [ ] Unit tests for nodes
- [ ] Integration tests
- [ ] Performance benchmarks
- [ ] Brugermanual på dansk/engelsk
- [ ] Video tutorial
- [ ] Eksempel workflows

## Research Opgaver

### ML Models til Image Quality Assessment

1. **BRISQUE**
   - Reference-less quality assessment
   - Lightweight, CPU-friendly
   - GitHub: `liveq/brisque`

2. **HyperIQA**
   - Deep learning based
   - No reference needed
   - Paper: "Blind Image Quality Assessment via Deep Learning"

3. **MusIQ**
   - Multi-scale image quality
   - Works on mobile photos
   - TensorFlow Hub available

4. **Custom Training**
   - Træne på eget dataset
   - Fine-tune existing model
   - Label data med egne kriterier

### Anbefalet Tilgang

**Start:** Heuristic metoder (hurtigt, ingen dependencies)
**Mellemlang:** BRISQUE + heuristics kombination
**Langsigtet:** Custom ML model trænet på dine præferencer

## Næste Skridt

1. **Test installation** i ComfyUI
2. **Saml feedback** på heuristic rating
3. **Vælg ML model** til fase 2
4. **Opret GitHub Issues** for hver feature

## Agents der kan hjælpe

Hvis du vil ansætte en agent med specifik viden:

- **ML Engineer agent**: Træne/customize quality models
- **ComfyUI Expert**: Node architecture best practices
- **Python Performance**: Optimize batch processing

Spørg mig om at oprette en agent rollebeskrivelse til skill workshop!
