from __future__ import annotations
import re
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

import fitz  # PyMuPDF
import pdfplumber

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sci-extract")

class SciExtractor:
    """
    Unified extractor for scientific papers.
    Combines core insights extraction and figure detection.
    """

    CAPTION_PATTERNS = [
        re.compile(r"^(Fig\.?\s*(\d+))\s*[\.:\s]", re.IGNORECASE),
        re.compile(r"^(Figure\s+(\d+))\s*[\.:\s]", re.IGNORECASE),
        re.compile(r"^(FIGURE\s+(\d+))\s*[\.:\s]"),
        re.compile(r"^(图\s*(\d+))\s*[\.:\s。]"),
    ]

    SUBLABEL_PATTERN = re.compile(r"\(([a-z])\)")

    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        self.doc_fitz = fitz.open(self.pdf_path)
        self.pdf_plumber = pdfplumber.open(self.pdf_path)

        self.keywords = {
            'problem': ['research question', 'research objective', 'propose', 'aim', 'goal', 'problem', 'challenge'],
            'methodology': ['propose', 'method', 'algorithm', 'model', 'approach', 'develop', 'design', 'implement'],
            'results': ['result', 'finding', 'show', 'demonstrate', 'achieve', 'obtain', 'measure'],
            'innovation': ['novel', 'first', 'unlike', 'compared to', 'superior', 'advantage', 'new', 'innovative'],
            'application': ['application', 'potential', 'prospect', 'value', 'use', 'deployment', 'practical'],
            'limitations': ['limitation', 'challenge', 'future work', 'drawback', 'constraint', 'issue', 'problem']
        }

    def close(self):
        self.doc_fitz.close()
        self.pdf_plumber.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # --- Core Insights Logic ---

    def extract_insights(self) -> Dict[str, Any]:
        """Extract metadata and 6 core insights."""
        start_time = datetime.now()

        # 1. Extract Text
        full_text = ""
        for page in self.pdf_plumber.pages:
            full_text += page.extract_text() or ""

        if not full_text:
            return {"status": "error", "message": "No text extracted"}

        # 2. Metadata
        metadata = self._extract_metadata(full_text)

        # 3. Sections
        sections = self._identify_sections(full_text)

        # 4. Insights
        insights = {
            'research_problem': self._extract_field(sections['introduction'], 'problem'),
            'methodology': self._extract_field(sections['methodology'], 'methodology'),
            'key_results': self._extract_results(sections['results']),
            'innovation': self._extract_field(sections['discussion'] + sections['conclusion'], 'innovation', limit=3),
            'application': self._extract_field(sections['conclusion'] + sections['discussion'], 'application'),
            'limitations': self._extract_field(sections['discussion'] + sections['conclusion'], 'limitations', limit=2)
        }

        elapsed = (datetime.now() - start_time).total_seconds()

        return {
            'metadata': metadata,
            'core_insights': insights,
            'extraction_time': int(elapsed),
            'status': 'success'
        }

    def _extract_metadata(self, text: str) -> Dict[str, Any]:
        meta = self.doc_fitz.metadata or {}
        return {
            'title': meta.get('title', 'Unknown'),
            'authors': self._regex_extract(text[:2000], r'[A-Z][a-z]+ [A-Z][a-z]+', limit=5),
            'journal': self._regex_search(text[:1000], [
                r'(?:Published in|Journal:|In )\s*([A-Z][^,\n]+)',
                r'([A-Z][a-zA-Z\s&]+)\s*(?:Volume|Vol\.|Issue|No\.)'
            ]),
            'year': self._regex_search(text[:1000], [r'\b(20\d{2})\b']),
            'doi': self._regex_search(text[:2000], [r'(?:DOI|doi)[\s:]*([^\s\n]+)']),
            'pdf_path': str(self.pdf_path)
        }

    def _identify_sections(self, text: str) -> Dict[str, str]:
        sections = {'introduction': "", 'methodology': "", 'results': "", 'discussion': "", 'conclusion': ""}
        patterns = {
            'introduction': r'(?:^|\n)\s*(?:1\.?\s+)?(?:Introduction|Background)',
            'methodology': r'(?:^|\n)\s*(?:2\.?\s+)?(?:Method|Methodology|Approach)',
            'results': r'(?:^|\n)\s*(?:3\.?\s+)?(?:Result|Findings)',
            'discussion': r'(?:^|\n)\s*(?:4\.?\s+)?(?:Discussion)',
            'conclusion': r'(?:^|\n)\s*(?:5\.?\s+)?(?:Conclusion|Summary)',
        }

        text_lower = text.lower()
        indices = []
        for key, pattern in patterns.items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                indices.append((key, match.start()))

        indices.sort(key=lambda x: x[1])

        for i, (key, start) in enumerate(indices):
            end = indices[i+1][1] if i+1 < len(indices) else len(text)
            sections[key] = text[start:end]

        return sections

    def _extract_field(self, text: str, key: str, limit: int = 2) -> str | List[str]:
        sentences = self._find_sentences_with_keywords(text, self.keywords[key])
        if not sentences:
            return "Not found"
        if limit == 1:
            return sentences[0]
        return sentences[:limit]

    def _extract_results(self, text: str) -> List[str]:
        sentences = self._find_sentences_with_keywords(text, self.keywords['results'])
        results = [s for s in sentences if any(c.isdigit() for c in s)]
        return results[:5] if results else ["Not found"]

    def _find_sentences_with_keywords(self, text: str, keywords: List[str]) -> List[str]:
        if not text: return []
        sentences = re.split(r'[.!?]\s+', text)
        matching = [s.strip() for s in sentences if any(k in s.lower() for k in keywords)]
        return matching

    def _regex_search(self, text: str, patterns: List[str]) -> str:
        for p in patterns:
            m = re.search(p, text)
            if m: return m.group(1).strip()
        return "Unknown"

    def _regex_extract(self, text: str, pattern: str, limit: int = 5) -> List[str]:
        return re.findall(pattern, text)[:limit]

    # --- Figure Detection Logic ---

    def detect_figures(self, output_dir: Optional[str | Path] = None) -> List[Dict[str, Any]]:
        """Detect and optionally save figure images."""
        captions = self._find_all_captions()
        figures = []

        for cap in captions:
            page_num = cap['page']
            page_plumber = self.pdf_plumber.pages[page_num]

            # Compute bbox
            bbox_pdf = self._compute_figure_bbox(cap, page_plumber)

            # Extract Image using fitz (higher quality)
            # PDF coords (x0, y0, x1, y1) -> Fitz Rect
            rect = fitz.Rect(bbox_pdf)
            page_fitz = self.doc_fitz[page_num]

            # Render to pixmap
            pix = page_fitz.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2)) # 2x zoom for clarity

            fig_data = {
                "number": cap["number"],
                "page": page_num + 1,
                "caption": cap["caption"],
                "bbox_pdf": bbox_pdf,
                "sublabels": self.SUBLABEL_PATTERN.findall(cap["caption"])
            }

            if output_dir:
                out_path = Path(output_dir) / f"fig_{cap['number']}.png"
                pix.save(str(out_path))
                fig_data["image_path"] = str(out_path)

            figures.append(fig_data)

        return figures

    def _find_all_captions(self) -> List[Dict[str, Any]]:
        captions = []
        seen = set()

        for i, page in enumerate(self.pdf_plumber.pages):
            lines = page.extract_text_lines()
            for line in lines:
                text = line['text'].strip()
                match = self._match_caption(text)
                if match and (i, match) not in seen:
                    seen.add((i, match))
                    captions.append({
                        "number": match,
                        "page": i,
                        "caption": text,
                        "x0": line["x0"], "y0": line["top"], "x1": line["x1"], "y1": line["bottom"]
                    })
        return sorted(captions, key=lambda x: x['number'])

    def _match_caption(self, text: str) -> Optional[int]:
        for pattern in self.CAPTION_PATTERNS:
            m = pattern.match(text)
            if m: return int(m.group(2))
        return None

    def _compute_figure_bbox(self, caption: Dict[str, Any], page: pdfplumber.page.Page) -> Tuple[float, float, float, float]:
        # Simple heuristic: Figure is usually ABOVE the caption
        # We look for the nearest text line above the caption to find the top boundary
        # If no text above, we use page top.

        fig_bottom = caption["y0"] - 2.0
        fig_left = 30.0
        fig_right = page.width - 30.0

        lines_above = [l for l in page.extract_text_lines() if l["bottom"] < caption["y0"] - 5]
        if not lines_above:
            fig_top = 30.0
        else:
            # Find the largest vertical gap above the caption
            lines_above.sort(key=lambda l: l["bottom"], reverse=True)
            fig_top = 30.0
            for l in lines_above:
                if (caption["y0"] - l["bottom"]) > 300: # Found a huge gap
                    fig_top = l["bottom"] + 5
                    break

        # Ensure minimum height
        if fig_bottom - fig_top < 50:
            fig_top = max(30.0, fig_bottom - 400) # Fallback to 400pt height

        return (fig_left, fig_top, fig_right, fig_bottom)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    with SciExtractor(pdf_path) as ext:
        print("--- Insights ---")
        insights = ext.extract_insights()
        print(json.dumps(insights, indent=2, ensure_ascii=False))

        print("\n--- Figures ---")
        figures = ext.detect_figures(output_dir)
        for f in figures:
            print(f"Fig {f['number']} (Page {f['page']}): {f['caption'][:100]}...")
