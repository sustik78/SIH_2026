# PRAMAN AI (Packaging Regulations & Automated Metrology Audit Network)
> **SIH 2026 Project**: Legal Metrology Compliance Inspection Platform  
> **Core Tagline**: *"From Package Image to Compliance Decision."*  
> **Statutory Ground Truth**: Legal Metrology Act, 2009 & Packaged Commodities Rules, 2011 (40 Official Gazettes Indexed).

---

## 🏛️ Project Overview
**PRAMAN AI** is an AI-powered Legal Metrology compliance inspection platform designed specifically for government enforcement officials, inspectors, and supervisors in India.

The platform processes pre-packaged commodity labels, detects mandatory declarations, runs deterministic rule evaluations against statutory gazettes, generates an explainable compliance score (0–100), highlights violations directly on the product image with color-coded bounding boxes, and generates evidence-backed PDF and editable Word (DOCX) inspection reports.

---

## 🚀 Key Features

1. **AI Computer Vision & OCR Pipeline**:
   - **OpenCV Preprocessing**: Contrast Limited Adaptive Histogram Equalization (CLAHE), bilateral denoising, and skew correction.
   - **Tesseract 5.4 OCR**: Text detection with word-level bounding box coordinates and character confidence scoring.
   - **Deterministic NLP Extraction**: Robust regex and NLP parser extracting Commodity Name, Manufacturer/Packer/Importer Details & Address with Pincode, Net Quantity in SI Units, Manufacturing/Packing Dates, MRP with statutory tax clause, Unit Sale Price (USP), Consumer Care Helpline/Email, Country of Origin, and Garment Sizes.

2. **12 Statutory Legal Metrology Rule Groups (Derived from 40 Dataset PDFs)**:
   - `LM-PCR-01`: Manufacturer / Packer / Importer Complete Address (Rule 6(1)(a) & GSR 226(E))
   - `LM-PCR-02`: Common / Generic Commodity Name (Rule 6(1)(b))
   - `LM-PCR-03`: Metric Net Quantity & Prohibited Misleading Expressions (Rule 6(1)(c), Rule 11-13 & SOP 2023)
   - `LM-PCR-04`: Month & Year of Manufacture / Packing (Rule 6(1)(d))
   - `LM-PCR-05`: Maximum Retail Price (MRP) & Tax Declaration (Rule 6(1)(e) & Rule 18)
   - `LM-PCR-06`: Unit Sale Price (USP) Calculation & Format (Rule 6(1)(11) & GSR 226(E))
   - `LM-PCR-07`: Consumer Care Redressal Details (Rule 6(1)(f) & Rule 2(aa))
   - `LM-PCR-08`: Country of Origin (COO) for Imports/E-commerce (Rule 6(1)(da) & 2026 COO Rules)
   - `LM-PCR-09`: Readymade Garment Size & Count (3rd Amendment 2022 / GSR 858(E))
   - `LM-PCR-10`: Principal Display Panel Legibility & Contrast (Rule 7 & Rule 9)
   - `LM-PCR-11`: QR Code & Digital Declaration Proviso (QR Code Amendment 2023)
   - `LM-PCR-12`: Exemption Verification & Pan Masala Restriction (Rule 26)

3. **Visual Evidence & Bounding Boxes**:
   - Color-coded packaging overlays: **Green** (PASS), **Amber** (WARNING), **Red** (VIOLATION).
   - High-visibility cropped evidence cards for every infraction.

4. **Explainable 0–100 Compliance Score**:
   - Categorized by Declaration Completeness (40%), Value & Metric Units (25%), Pricing & USP (15%), Consumer Protection (10%), and Legibility (10%).

5. **Official Inspection Reports**:
   - **PDF Report**: Official Government of India / Legal Metrology formatted notice with ReportLab.
   - **DOCX Report**: Exportable / editable Word document with python-docx.

6. **Senior-Friendly Accessibility**:
   - Large text mode, high-contrast visual filters, and optional text-to-speech audio guidance.

7. **Role-Based Access Control (RBAC) & Audit Trail**:
   - Roles: `INSPECTOR`, `SUPERVISOR`, `ADMIN`.
   - Immutable audit logging of all scans, reviews, and overrides.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Uvicorn, SQLAlchemy
- **AI / Computer Vision**: OpenCV, Tesseract OCR 5.4.0, Pillow, NumPy
- **Report Engine**: ReportLab (PDF) & python-docx (DOCX)
- **Database**: SQLite (built-in) / PostgreSQL ready

---

## 🏃 Running Locally

### 1. Start Backend Server
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Backend API will run at `http://127.0.0.1:8000` (Swagger docs available at `http://127.0.0.1:8000/docs`).

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```
Frontend UI will run at `http://localhost:5173/`.

### 3. Demo Credentials
- **Inspector**: `inspector` / `Inspect@123`
- **Supervisor**: `supervisor` / `Super@123`
- **Admin**: `admin` / `Admin@123`
*(Or use the 1-click role switcher in the top bar).*

---

## 🏆 Guide to do it

1. Open `http://localhost:5173/`.
2. Click **Start Packaging Scan**.
3. Under **SIH 2026 Instant Demo Samples**, choose:
   - **Sample 1**: *Chakki Fresh Atta (5 kg)* → Score ~96/100 (`COMPLIANT`)
   - **Sample 2**: *Refined Sunflower Oil (1 L)* → Score ~68/100 (`NON-COMPLIANT`, missing tax clause & helpline)
   - **Sample 3**: *Desi Namkeen Pack* → Score ~32/100 (`CRITICAL VIOLATION`, non-standard "Jumbo" quantity)
4. Click **Execute Legal Metrology Inspection** and watch the live 5-stage AI progress.
5. Review the **Score Gauge**, **Visual Evidence Bounding Boxes**, **Declarations Audit**, and **Rule Citations**.
6. Click **Download Official PDF** or **Export DOCX** to inspect the generated report.
7. Open **Rule Library (40 PDFs)** in the sidebar to demonstrate ground-truth traceability.
