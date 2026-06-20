# Test Environment Setup - ComfyUI Image Rater

## Formål

Isoleret testmiljø til at udvikle og teste custom nodes uden at påvirke produktions-ComfyUI.

## Struktur

```
/home/jens/ComfyUI-test/           # Isoleret test installation
├── ComfyUI/                        # ComfyUI core (ny clone)
├── custom_nodes/
│   └── comfyui-image-rater/       # Vores nodes (symlink eller clone)
├── output/                         # Test output
├── input/                          # Test input
├── models/                         # Separate model cache
└── run_test.sh                     # Start script
```

## Installation Steps

### 1. Opret Test Directory

```bash
# Base directory
mkdir -p /home/jens/ComfyUI-test
cd /home/jens/ComfyUI-test

# Clone ComfyUI (fresh installation)
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install base requirements
pip install -r requirements.txt
```

### 2. Installer Image Rater Nodes

```bash
# Go to custom_nodes
cd /home/jens/ComfyUI-test/ComfyUI/custom_nodes/

# Clone our image rater (or symlink from dev)
git clone https://github.com/jenshinnerup-lab/comfyui-image-rater.git

# Install dependencies
cd comfyui-image-rater
pip install -r requirements.txt
```

### 3. Konfigurer Port (undgå konflikt)

Standard ComfyUI kører på port **8188**. Test installationen bruger **8189**.

Edit `ComfyUI/main.py` eller brug command line flags:

```bash
# Start test ComfyUI on different port
python main.py --port 8189 --listen
```

### 4. Test Script

Opret `run_test.sh`:

```bash
#!/bin/bash

# ComfyUI Test Environment Starter
# Runs on port 8189 (production is 8188)

TEST_DIR="/home/jens/ComfyUI-test/ComfyUI"
cd "$TEST_DIR"

# Activate venv
source venv/bin/activate

# Clear any stale processes
pkill -f "python.*main.py.*8189" || true

# Start ComfyUI test instance
echo "🧪 Starting ComfyUI TEST instance on port 8189..."
echo "Production instance should be on port 8188"
echo ""
echo "Access: http://localhost:8189"
echo "Output: $TEST_DIR/output/"
echo ""

python main.py --port 8189 --listen --output-directory output --input-directory input
```

### 5. Test Workflow

1. **Start test environment:**
   ```bash
   cd /home/jens/openclaw-projects/comfyui-image-rater
   ./run_test.sh
   ```

2. **Åbn browser:** http://localhost:8189

3. **Test nodes:**
   - Load Image → ImageRater → PreviewImage
   - BatchImageRater → test på eksisterende output mappe

4. **Valider output:**
   ```bash
   ls -lt /home/jens/ComfyUI-test/ComfyUI/output/rated/
   ```

## Adgang til Test

| Instance | Port | URL | Purpose |
|----------|------|-----|---------|
| **Production** | 8188 | http://localhost:8188 | Din normale ComfyUI |
| **Test** | 8189 | http://localhost:8189 | Image Rater udvikling |

## Fordele ved Isoleret Test

✅ **Ingen risiko** for produktions-workflows  
✅ **Test nye versions** før deploy  
✅ **Debug uden påvirkning** af andre brugere  
✅ **Hurtig reset** hvis noget går galt  
✅ **Parallel testing** mens production kører  

## Cleanup

```bash
# Stop test instance
pkill -f "python.*main.py.*8189"

# Remove test environment (if needed)
rm -rf /home/jens/ComfyUI-test
```

## Next Steps

1. [ ] Create test directory structure
2. [ ] Clone ComfyUI
3. [ ] Setup virtual environment
4. [ ] Install image-rater nodes
5. [ ] Configure port 8189
6. [ ] Create startup script
7. [ ] Test with sample images
8. [ ] Validate rating functionality
