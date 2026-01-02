# SVD Register Decoder

**SVD Register Decoder** is a high-performance command-line tool designed for MCU developers and embedded security researchers. It bridges the gap between raw hardware data and human-readable information.

> **Current Version:** 0.1  
> **Status:** Stable Release - Focus on Performance & Caching

---

## Features (v0.1)

- **Instant Loading (JSON Database):** Features a smart caching mechanism. If a JSON version of the SVD doesn’t exist in the `database/` directory, the tool generates it during the first run. Subsequent executions load data directly from JSON, providing near-instant startup.
- **Vast STM32 Support:** Comes with an extensive pre-loaded SVD database for almost the entire STM32 family (F0, F1, F3, F4, G0, L0, H7, etc.).
- **Efficient Bit-Level Decoding:** Accurately extracts bitfields from raw register values using optimized bitwise operations.
- **Aesthetic Terminal UI:** I hate boring software engineer aesthetic and yes I am using light mode.

---

## Installation

Follow these steps to set up the environment:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ubeydullahsu/svd-register-decoder
   cd svd-register-decoder
   ```

2. **Install dependencies:**

   It is highly recommended to install the required libraries using the provided `requirements.txt` file to ensure compatibility:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the tool by providing the SVD file, target address, and the value you want to decode:

```bash
python src/main.py --svd [svd_file] --addr [address] --val [raw_value]
```

### **Workflow:**

1. **Database Check:** The tool checks for a cached JSON in the `database/` folder.
2. **Auto-Generate:** If the JSON is missing, it parses the `.svd` (XML) file and saves the processed data as a JSON file for future use.
3. **Decode & Display:** Extracts field names, bit ranges, and descriptions, then displays them in a beautifully formatted table.

---

## Project Structure

```text
.
├── database/       # Optimized JSON cache (Auto-generated)
├── src/
│   ├── main.py     # CLI entry point and orchestration
│   ├── parser.py   # SVD-to-JSON and Memory Map logic
│   └── decoder.py  # Bitwise engine and output formatting
├── requirements.txt # Project dependencies
└── README.md       # Project documentation
```

---

## Roadmap (TO DO)

- [ ] **v0.2 - Interactive Mode:** Continuous loop to query multiple registers without restarting.
- [ ] **v0.2 - GDB-Python Integration:** "Live View" feature to monitor registers directly via GDB-Python API.
- [ ] **XML Namespace Handling:** Enhanced parsing for complex vendor-specific XML schemas.
- [ ] **Unified Rich Output:** Transitioning all status messages to a unified `rich.console` system.

---

## Contributing

Contributions are welcome! If you have ideas for new features, want to add more SVD files, or have UI improvement suggestions, feel free to open a Pull Request.

---