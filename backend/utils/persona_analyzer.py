import json
import re
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from collections import defaultdict

class PersonaAnalyzer:
    def __init__(self):
        try:
            # Use a lightweight sentence transformer model
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            self.embedder = None
            print("Warning: Sentence transformer not available, using fallback methods")
    
    def analyze_documents_for_persona(self, documents_data: List[Dict], persona: str, job_to_be_done: str) -> Dict[str, Any]:
        """
        Analyze documents based on persona and job requirements
        """
        try:
            # Extract all sections from documents
            all_sections = self._extract_all_sections(documents_data)
            
            # Rank sections based on persona and job
            ranked_sections = self._rank_sections_for_persona(all_sections, persona, job_to_be_done)
            
            # Extract sub-sections
            sub_sections = self._extract_subsections(ranked_sections[:10], persona, job_to_be_done)
            
            return {
                "metadata": {
                    "documents": [doc.get("filename", "unknown.pdf") for doc in documents_data],
                    "persona": persona,
                    "job_to_be_done": job_to_be_done,
                    "processing_timestamp": "2025-07-22T12:36:00Z",
                    "total_sections_analyzed": len(all_sections)
                },
                "extracted_sections": ranked_sections[:15],  # Top 15 sections
                "sub_section_analysis": sub_sections,
                "success": True
            }
        except Exception as e:
            return {
                "metadata": {
                    "documents": [],
                    "persona": persona,
                    "job_to_be_done": job_to_be_done,
                    "processing_timestamp": "2025-07-22T12:36:00Z"
                },
                "extracted_sections": [],
                "sub_section_analysis": [],
                "success": False,
                "error": str(e)
            }
    
    def _extract_all_sections(self, documents_data: List[Dict]) -> List[Dict]:
        """Extract all sections from all documents"""
        all_sections = []
        
        for doc_data in documents_data:
            filename = doc_data.get("filename", "unknown.pdf")
            outline = doc_data.get("outline", [])
            
            for i, heading in enumerate(outline):
                section = {
                    "document": filename,
                    "page": heading.get("page", 1),
                    "section_title": heading.get("text", ""),
                    "level": heading.get("level", "H1"),
                    "importance_rank": 0,  # Will be calculated
                    "section_id": f"{filename}_{i}"
                }
                all_sections.append(section)
        
        return all_sections
    
    def _rank_sections_for_persona(self, sections: List[Dict], persona: str, job_to_be_done: str) -> List[Dict]:
        """Rank sections based on persona and job relevance"""
        if not sections:
            return []
        
        # Create persona + job context
        context = f"{persona} needs to {job_to_be_done}"
        
        if self.embedder:
            return self._semantic_ranking(sections, context)
        else:
            return self._keyword_ranking(sections, context)
    
    def _semantic_ranking(self, sections: List[Dict], context: str) -> List[Dict]:
        """Use semantic similarity for ranking"""
        try:
            # Get section texts
            section_texts = [section["section_title"] for section in sections]
            
            # Encode context and sections
            context_embedding = self.embedder.encode([context])
            section_embeddings = self.embedder.encode(section_texts)
            
            # Calculate similarities
            similarities = cosine_similarity(context_embedding, section_embeddings)[0]
            
            # Add importance ranks
            for i, section in enumerate(sections):
                section["importance_rank"] = float(similarities[i])
            
            # Sort by importance
            return sorted(sections, key=lambda x: x["importance_rank"], reverse=True)
        
        except Exception as e:
            print(f"Semantic ranking failed: {e}, falling back to keyword ranking")
            return self._keyword_ranking(sections, context)
    
    def _keyword_ranking(self, sections: List[Dict], context: str) -> List[Dict]:
        """Fallback keyword-based ranking"""
        context_keywords = set(re.findall(r'\b\w+\b', context.lower()))
        
        for section in sections:
            title = section["section_title"].lower()
            title_words = set(re.findall(r'\b\w+\b', title))
            
            # Calculate overlap score
            overlap = len(context_keywords.intersection(title_words))
            section["importance_rank"] = overlap / max(len(context_keywords), 1)
        
        return sorted(sections, key=lambda x: x["importance_rank"], reverse=True)
    
    def _extract_subsections(self, top_sections: List[Dict], persona: str, job_to_be_done: str) -> List[Dict]:
        """Extract and analyze sub-sections from top sections"""
        sub_sections = []
        
        for section in top_sections[:5]:  # Top 5 sections only
            # Simulate sub-section extraction
            refined_text = self._generate_refined_text(section, persona, job_to_be_done)
            
            sub_section = {
                "document": section["document"],
                "section_title": section["section_title"],
                "refined_text": refined_text,
                "page_number": section["page"],
                "relevance_score": section["importance_rank"],
                "persona_alignment": self._calculate_persona_alignment(section, persona)
            }
            sub_sections.append(sub_section)
        
        return sub_sections
    
    def _generate_refined_text(self, section: Dict, persona: str, job_to_be_done: str) -> str:
        """Generate refined text for a section based on persona and job"""
        title = section["section_title"]
        level = section["level"]
        
        # Create contextual summary
        if "introduction" in title.lower():
            return f"Foundational concepts relevant to {persona} working on {job_to_be_done}"
        elif "method" in title.lower() or "approach" in title.lower():
            return f"Methodology section crucial for {persona} to understand implementation strategies"
        elif "result" in title.lower() or "finding" in title.lower():
            return f"Key findings and outcomes directly applicable to {job_to_be_done}"
        elif "conclusion" in title.lower():
            return f"Summary and implications for {persona} in the context of {job_to_be_done}"
        else:
            return f"{level} section providing specialized knowledge for {persona}"
    
    def _calculate_persona_alignment(self, section: Dict, persona: str) -> float:
        """Calculate how well a section aligns with the persona"""
        title = section["section_title"].lower()
        persona_lower = persona.lower()
        
        # Simple heuristic based on persona keywords
        persona_keywords = {
            "researcher": ["method", "analysis", "study", "research", "finding"],
            "student": ["introduction", "basic", "concept", "example", "summary"],
            "analyst": ["data", "trend", "analysis", "performance", "metric"],
            "developer": ["implementation", "code", "algorithm", "system", "technical"]
        }
        
        relevant_keywords = []
        for role, keywords in persona_keywords.items():
            if role in persona_lower:
                relevant_keywords.extend(keywords)
        
        if not relevant_keywords:
            return 0.5  # Default moderate alignment
        
        matches = sum(1 for keyword in relevant_keywords if keyword in title)
        return min(matches / len(relevant_keywords), 1.0)
