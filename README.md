[Uploading README.md…]()
# 🧮 Calculator v3.0

A feature-rich, multi-platform calculator built in Python (desktop) and HTML/CSS/JS (web). Designed with a clean dark UI inspired by iOS, with full support for Windows, macOS, Android, and iOS.

---

## ✨ Features

### 🧮 Basic Calculator
- Standard arithmetic operations
- Scientific mode (sin, cos, tan, log, sqrt, factorial, and more)
- Calculation history (last 5 results)

### 📐 Unit Converter
- **Length** — km, miles, meters, feet, cm, inches
- **Weight** — kg, lbs, stones, grams, oz
- **Temperature** — °C, °F, Kelvin
- **Area** — m², ft², hectares, acres
- **Speed** — km/h, mph, m/s, knots (kn)
- **Data** — MB, GB, TB, KB

### 📊 Percentage Calculator
- X% of Y
- X is what % of Y
- Percentage change from X to Y

### 💪 Fitness Tab
| Tool | Description |
|------|-------------|
| **BMI** | Body Mass Index with visual bar |
| **Calories** | Daily TDEE based on activity & goal |
| **Protein** | Daily protein intake by goal |
| **Macros** | Protein / Carbs / Fat split |
| **Water** | Daily water intake |
| **Body Fat %** | Navy Method (male & female) |
| **Ideal Weight** | Devine & Robinson formulas |
| **1RM** | One rep max + percentage table |
| **HR Zones** | Heart rate zones Z1–Z5 |

### 🏦 Loan Calculator
- Monthly payment
- Total amount paid
- Total interest

---

## 🖥️ Desktop App (Python)

### Requirements
- Python 3.x
- tkinter (included with Python)
- PyInstaller (for building .exe)

### Run
```bash
python calculator_v3.py
```

### Build .exe (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole calculator_v3.py
```
The `.exe` will be in the `dist/` folder.

---

## 🌐 Web App (HTML)

Single file — no dependencies, no frameworks, no installation needed.

### Run locally
Just open `calculator_v3.html` in any browser.

### Deploy online (Netlify — free)
1. Go to [netlify.com](https://netlify.com)
2. Drag & drop `calculator_v3.html`
3. Get a public link instantly ✅

### iOS / iPhone
Open the deployed link in Safari → Share → **Add to Home Screen** for a native app experience.

---

## 📁 Project Structure

```
Calculator/
├── calculator_v3.py        # Desktop app (Python + tkinter)
├── calculator_v3.html      # Web app (HTML/CSS/JS)
├── dist/
│   └── calculator_v3.exe   # Windows executable
└── README.md
```

---

## 🗺️ Version History

| Version | Description |
|---------|-------------|
| v1.0 | Basic terminal calculator (Python) |
| v2.0 | Desktop GUI with tkinter, dark theme |
| v2.5 | English UI, kg/lbs/stones, refined design |
| v3.0 | Full Fitness tab, web app, cross-platform |

---

## 🛠️ Built With

- **Python 3** + **tkinter** — Desktop app
- **HTML5 / CSS3 / Vanilla JS** — Web app
- **PyInstaller** — Windows executable
- **Netlify** — Web hosting

---

## 👤 Author

**nemanja-byte88**
- GitHub: [@nemanja-byte88](https://github.com/nemanja-byte88)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
