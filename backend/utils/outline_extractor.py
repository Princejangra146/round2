import pdfplumber
import json
import re
from typing import List, Dict, Any

class OutlineExtractor:
    def __init__(self):
        self.font_size_threshold = 2
        
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract structured outline from PDF using pdfplumber"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                title = self._extract_title(pdf)
                outline = self._extract_headings(pdf)
                
                return {
                    "title": title,
                    "outline": outline,
                    "total_pages": len(pdf.pages),
                    "success": True
                }
        except Exception as e:
            return {
                "title": "",
                "outline": [],
                "total_pages": 0,
                "success": False,
                "error": str(e)
            }
    
    def _extract_title(self, pdf) -> str:
        """Extract document title from first page"""
        try:
            first_page = pdf.pages[0]
            chars = first_page.chars
            
            if not chars:
                return "Untitled Document"
            
            # Find the largest font size on first page
            max_font_size = max([char.get('size', 0) for char in chars])
            
            # Get text with largest font size
            title_chars = [char for char in chars if char.get('size', 0) >= max_font_size - 1]
            
            if title_chars:
                title_text = ''.join([char.get('text', '') for char in title_chars[:100]])
                title_text = re.sub(r'\s+', ' ', title_text).strip()
                return title_text if title_text else "Untitled Document"
            
            return "Untitled Document"
        except:
            return "Untitled Document"
    
    def _extract_headings(self, pdf) -> List[Dict[str, Any]]:
        """Extract hierarchical headings from PDF"""
        headings = []
        
        for page_num, page in enumerate(pdf.pages, 1):
            try:
                chars = page.chars
                if not chars:
                    continue
                
                # Group characters by line
                lines = self._group_chars_by_line(chars)
                
                for line in lines:
                    heading = self._analyze_line_as_heading(line, page_num)
                    if heading:
                        headings.append(heading)
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                continue
        
        return self._assign_heading_levels(headings)
    
    def _group_chars_by_line(self, chars: List[Dict]) -> List[List[Dict]]:
        """Group characters by line based on y-coordinate"""
        if not chars:
            return []
        
        # Sort by y-coordinate (top to bottom)
        sorted_chars = sorted(chars, key=lambda x: (-x.get('y0', 0), x.get('x0', 0)))
        
        lines = []
        current_line = []
        current_y = None
        y_tolerance = 2
        
        for char in sorted_chars:
            char_y = char.get('y0', 0)
            
            if current_y is None or abs(char_y - current_y) <= y_tolerance:
                current_line.append(char)
                current_y = char_y
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [char]
                current_y = char_y
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _analyze_line_as_heading(self, line_chars: List[Dict], page_num: int) -> Dict[str, Any]:
        """Analyze if a line is a heading"""
        if not line_chars:
            return None
        
        # Extract text and font info
        text = ''.join([char.get('text', '') for char in line_chars]).strip()
        
        if not text or len(text) < 3:
            return None
        
        # Get font characteristics
        font_sizes = [char.get('size', 0) for char in line_chars]
        avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0
        
        # Check if it's a potential heading
        is_heading = self._is_potential_heading(text, avg_font_size, line_chars)
        
        if is_heading:
            return {
                "text": text,
                "page": page_num,
                "font_size": avg_font_size,
                "char_count": len(text),
                "level": "H1"  # Will be reassigned later
            }
        
        return None
    
    def _is_potential_heading(self, text: str, font_size: float, chars: List[Dict]) -> bool:
        """Determine if text is likely a heading"""
        # Skip very long text
        if len(text) > 200:
            return False
        
        # Check for heading patterns
        heading_patterns = [
            r'^\d+\.?\s+[A-Z]',  # Numbered headings
            r'^[A-Z][A-Z\s]{2,}$',  # All caps
            r'^[A-Z][a-z\s]+:?$',  # Title case
            r'^\d+\.\d+',  # Subsection numbers
            r'^(Chapter|Section|Part)\s+\d+',  # Chapter/Section
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text.strip()):
                return True
        
        # Check font size (relative to document)
        if font_size > 12:
            return True
        
        # Check if text is bold or different formatting
        font_names = [char.get('fontname', '') for char in chars]
        has_bold = any('bold' in name.lower() for name in font_names)
        
        return has_bold and len(text) < 100
    
    def _assign_heading_levels(self, headings: List[Dict]) -> List[Dict]:
        """Assign H1, H2, H3 levels based on font size and patterns"""
        if not headings:
            return []
        
        # Sort by font size (largest first)
        font_sizes = sorted(set([h['font_size'] for h in headings]), reverse=True)
        
        # Create level mapping
        level_mapping = {}
        for i, size in enumerate(font_sizes[:3]):  # Only H1, H2, H3
            level_mapping[size] = f"H{i+1}"
        
        # Assign levels
        result = []
        for heading in headings:
            font_size = heading['font_size']
            
            # Find closest font size
            closest_size = min(level_mapping.keys(), key=lambda x: abs(x - font_size))
            heading['level'] = level_mapping[closest_size]
            
            # Clean up the heading dict
            result.append({
                "level": heading['level'],
                "text": heading['text'],
                "page": heading['page']
            })
        
        return result
