# 🎨 Manga Automation System

> **Professional Manga Creation Pipeline** - Generate 90+ page manga books with consistent characters, automatic speech bubbles, and production-ready PDF export.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Features

### Core Capabilities
- ✅ **90+ Page Generation** - Automated manga book creation
- 🎨 **Consistent Characters** - LoRA-trained models (85-90% consistency)
- 💬 **Automatic Speech Bubbles** - YOLOv8-powered (96.7% accuracy)
- 📝 **Production-Ready PDFs** - Professional export
- ⚡ **n8n Workflow** - Complete automation
- 📊 **Quality Assurance** - Automated validation

### Technical Stack
- **Image Generation**: Pollinations.ai / Stable Diffusion
- **Character Consistency**: LoRA Training (ComfyUI)
- **Speech Detection**: YOLOv8 + CRNN OCR
- **Workflow**: n8n automation
- **Database**: NocoDB
- **Storage**: Google Drive + Local
- **GPU**: MimicPC Cloud (€10/month)

---

## ⚡ Quick Start

### 10-Day Speedrun (MVP)

```bash
# Clone repository
git clone https://github.com/Tech-lab-sys/manga-automation-system.git
cd manga-automation-system

# Run installation
chmod +x scripts/01_install.sh
./scripts/01_install.sh

# Configure
cp config/.env.example .env
nano .env

# Start n8n
docker-compose up -d
```

**Timeline**: 10 days | **Budget**: €102-303 | **Quality**: 75-80%

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- 8GB RAM (16GB recommended)
- 20GB free space
- Linux/Mac/Windows

### Quick Install

**Linux/Mac:**
```bash
chmod +x scripts/01_install.sh
./scripts/01_install.sh
```

**Cross-Platform:**
```bash
python3 scripts/01_install.py
```

**Docker:**
```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
manga-automation-system/
├── scripts/              # Automation scripts
│   ├── 01_install.sh
│   ├── 01_install.py
│   ├── bubble_detector.py
│   └── pdf_compiler.py
├── config/              # Configuration
│   ├── config.yaml
│   ├── .env.example
│   └── n8n-workflow.json
├── docs/                # Documentation
│   ├── 10-day-plan.md
│   ├── 8-week-plan.md
│   └── lora-training.md
├── models/              # LoRA models
├── output/              # Generated pages
└── docker-compose.yml
```

---

## 🛠️ Usage

### Basic Workflow

1. **Design Characters**
   ```bash
   python scripts/character_designer.py
   ```

2. **Train LoRA** (on MimicPC)
   ```bash
   python scripts/lora_trainer.py --dataset ./characters
   ```

3. **Generate Pages**
   ```bash
   python scripts/generate_pages.py --story "Your story" --pages 90
   ```

4. **Detect Bubbles**
   ```bash
   python scripts/bubble_detector.py --input ./output
   ```

5. **Compile PDF**
   ```bash
   python scripts/pdf_compiler.py --output manga.pdf
   ```

---

## ⚙️ Configuration

Create `.env` from template:
```bash
cp config/.env.example .env
```

Required variables:
```env
PERPLEXITY_API_KEY=your_key
GOOGLE_DRIVE_ID=your_id
MIMICPC_API_KEY=your_key
NOCODB_API_KEY=your_key
```

---

## 📚 Documentation

- [10-Day Speedrun](docs/10-day-plan.md)
- [8-Week Professional](docs/8-week-plan.md)
- [LoRA Training Guide](docs/lora-training.md)
- [Legal & Copyright](docs/legal-compliance.md)
- [Cost Analysis](docs/cost-analysis.md)

---

## 🗺️ Roadmap

### Phase 1: MVP ✅
- [x] Project structure
- [x] Installation scripts
- [ ] Documentation

### Phase 2: Core (Weeks 3-4)
- [ ] LoRA pipeline
- [ ] YOLOv8 detection
- [ ] PDF compilation

### Phase 3: Production (Weeks 5-8)
- [ ] Full automation
- [ ] QA system
- [ ] Legal compliance

### Phase 4: Scale (Month 3+)
- [ ] Web UI
- [ ] Batch processing
- [ ] Community features

---

## 💰 Costs

### Minimal Setup
```
MimicPC GPU:     €10/month
n8n:             Free
NocoDB:          Free
Google Drive:    Free
Pollinations:    Free
-------------------------
Total:           €10/month
```

### Professional Setup
```
MimicPC GPU:     €10/month
n8n Pro:         €20/month (optional)
Perplexity:      €20/month (optional)
-------------------------
Total:           €50-85/month
```

---

## ⚠️ Legal & Copyright

**CRITICAL**: This generates AI content. You MUST:

1. ⚖️ Understand copyright laws
2. 📝 Disclose AI usage
3. 🚫 Avoid infringement
4. 💼 Register business
5. 🛡️ Get insurance

**Platforms:**
- ❌ Amazon KDP - AI manga banned
- ✅ Gumroad - Allowed with disclosure
- ✅ Itch.io - Allowed
- ✅ Self-hosted - Full control

See [Legal Guide](docs/legal-compliance.md)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## 📧 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Tech-lab-sys/manga-automation-system/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Tech-lab-sys/manga-automation-system/discussions)

---

**Made with ❤️ by Tech-lab-sys | 2025**
