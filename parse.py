import os
import glob
import json
from datetime import datetime
from bs4 import BeautifulSoup

def parse_raw_files():
    """
    Task 2: Strip navigation, footers, and chrome.
    Task 3: Extract content into predefined sections.
    """
    raw_dir = "c:/RAG/data/raw"
    parsed_dir = "c:/RAG/data/parsed"
    os.makedirs(parsed_dir, exist_ok=True)

    # Section definitions as per architecture
    sections_template = {
        "overview": "",
        "expense_ratio": "",
        "exit_load": "",
        "minimum_investment": "",
        "min_sip_amount": "",
        "riskometer": "",
        "benchmark": "",
        "tax": "",
        "fund_management": "",
        "investment_objective": "",
        "fund_house": "HDFC Mutual Fund"
    }

    for file_path in glob.glob(os.path.join(raw_dir, "*.html")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Task 2: Strip chrome (Navigation, Footers, Scripts, Styles, etc.)
            for tag in soup(["nav", "footer", "script", "style", "header", "aside", "svg"]):
                tag.decompose()

            # Task 3: Section Extraction
            # Using text-based heuristics to identify key fund data points.
            
            extracted_sections = sections_template.copy()
            
            # Clean text for heuristic searching
            content_text = soup.get_text(separator="\n")
            lines = [line.strip() for line in content_text.split("\n") if line.strip()]
            
            fund_name = soup.title.get_text(strip=True) if soup.title else os.path.basename(file_path)

            for i, line in enumerate(lines):
                lower_line = line.lower()
                
                # Heuristic mapping: Find labels and grab the subsequent text value
                if "expense ratio" in lower_line and i + 1 < len(lines):
                    extracted_sections["expense_ratio"] = lines[i+1]
                elif "exit load" in lower_line and i + 1 < len(lines):
                    extracted_sections["exit_load"] = lines[i+1]
                elif "benchmark" in lower_line and i + 1 < len(lines):
                    extracted_sections["benchmark"] = lines[i+1]
                elif "investment objective" in lower_line and i + 1 < len(lines):
                    extracted_sections["investment_objective"] = lines[i+1]
                elif ("fund manager" in lower_line or "fund management" in lower_line) and i + 1 < len(lines):
                    extracted_sections["fund_management"] = lines[i+1]
                elif ("minimum" in lower_line and "investment" in lower_line) and i + 1 < len(lines):
                    extracted_sections["minimum_investment"] = lines[i+1]
                elif "sip" in lower_line and "minimum" in lower_line and i + 1 < len(lines):
                    extracted_sections["min_sip_amount"] = lines[i+1]
                elif "riskometer" in lower_line and i + 1 < len(lines):
                    extracted_sections["riskometer"] = lines[i+1]
                elif "tax" in lower_line and "implications" in lower_line and i + 1 < len(lines):
                    extracted_sections["tax"] = lines[i+1]
                elif "overview" in lower_line and i + 1 < len(lines):
                    extracted_sections["overview"] = lines[i+1]

            # Package results with metadata
            output_data = {
                "fund_name": fund_name,
                "source_url": f"https://groww.in/mutual-funds/{os.path.basename(file_path).split('_')[0]}",
                "sections": extracted_sections,
                "metadata": {
                    "raw_source": os.path.basename(file_path),
                    "processed_at": datetime.now().isoformat()
                }
            }

            # Save to JSON for downstream vectorization
            output_filename = os.path.basename(file_path).replace(".html", ".json")
            output_path = os.path.join(parsed_dir, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4)
            
            print(f"Successfully parsed and tagged: {output_filename}")

        except Exception as e:
            print(f"Failed to parse {file_path}: {e}")

if __name__ == "__main__":
    parse_raw_files()