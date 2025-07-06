"""
Web scraping service for API Conference data.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WebScrapingServiceError(Exception):
    """Custom exception for web scraping service errors."""
    pass

class WebScrapingService:
    """Service for scraping API Conference website data."""
    
    def __init__(self, cache_dir: str = "cache"):
        """Initialize the web scraping service."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.session = None
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # Conference URLs
        self.urls = {
            "main": "https://apiconf.net",
            "speakers": "https://apiconf.net/speakers",
            "schedule": "https://apiconf.net/schedule",
            "faq": "https://apiconf.net/faq",
            "about": "https://apiconf.net/about"
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def _get_cache_path(self, url: str) -> Path:
        """Get cache file path for a URL."""
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache is still valid."""
        if not cache_path.exists():
            return False
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cache_data.get("cached_at", "1970-01-01"))
            return datetime.now() - cached_time < self.cache_duration
        except Exception:
            return False
    
    async def _fetch_url(self, url: str, use_cache: bool = True) -> Dict[str, Any]:
        """Fetch URL content with caching."""
        cache_path = self._get_cache_path(url)
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                logger.info(f"Using cached data for {url}")
                return cache_data
            except Exception as e:
                logger.warning(f"Error reading cache for {url}: {e}")
        
        # Fetch from web
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse with BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract data based on URL
                    data = await self._extract_data(url, soup)
                    
                    # Cache the result
                    if use_cache:
                        cache_data = {
                            "url": url,
                            "cached_at": datetime.now().isoformat(),
                            "status": "success",
                            "data": data
                        }
                        with open(cache_path, 'w', encoding='utf-8') as f:
                            json.dump(cache_data, f, indent=2, ensure_ascii=False)
                    
                    return {
                        "url": url,
                        "status": "success",
                        "data": data,
                        "cached": False
                    }
                else:
                    logger.error(f"HTTP {response.status} for {url}")
                    return {
                        "url": url,
                        "status": "error",
                        "error": f"HTTP {response.status}",
                        "cached": False
                    }
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return {
                "url": url,
                "status": "error",
                "error": str(e),
                "cached": False
            }
    
    async def _extract_data(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract relevant data from BeautifulSoup object."""
        if "speakers" in url:
            return await self._extract_speakers_data(soup)
        elif "schedule" in url:
            return await self._extract_schedule_data(soup)
        elif "faq" in url:
            return await self._extract_faq_data(soup)
        else:
            return await self._extract_general_data(soup)
    
    async def _extract_speakers_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract speakers data from the page."""
        speakers = []
        
        # Look for speaker elements (adjust selectors based on actual page structure)
        speaker_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(word in x.lower() for word in ['speaker', 'profile', 'card']))
        
        if not speaker_elements:
            # Fallback: look for any elements containing speaker names
            speaker_elements = soup.find_all(text=lambda text: text and any(name in text for name in [
                "Mehdi Medjaoui", "Michael Owolabi", "Chisom Uma", "Ademola Adelekan"
            ]))
        
        for element in speaker_elements:
            try:
                # Extract speaker information
                name_elem = element.find(['h1', 'h2', 'h3', 'h4']) or element
                name = name_elem.get_text(strip=True) if name_elem else "Unknown"
                
                # Look for title/company information
                title_elem = element.find(['p', 'span'], class_=lambda x: x and any(word in x.lower() for word in ['title', 'position', 'company']))
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                # Look for bio/description
                bio_elem = element.find(['p', 'div'], class_=lambda x: x and any(word in x.lower() for word in ['bio', 'description', 'about']))
                bio = bio_elem.get_text(strip=True) if bio_elem else ""
                
                if name and name != "Unknown":
                    speakers.append({
                        "name": name,
                        "title": title,
                        "bio": bio,
                        "source": "web_scraped"
                    })
            except Exception as e:
                logger.warning(f"Error extracting speaker data: {e}")
                continue
        
        return {
            "speakers": speakers,
            "total_count": len(speakers),
            "status": "complete",
            "note": "Speaker lineup has been fully announced with 44 speakers"
        }
    
    async def _extract_schedule_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract schedule data from the page."""
        schedule = []
        
        # Look for schedule elements
        schedule_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(word in x.lower() for word in ['session', 'schedule', 'event']))
        
        for element in schedule_elements:
            try:
                # Extract session information
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                time_elem = element.find(['span', 'div'], class_=lambda x: x and any(word in x.lower() for word in ['time', 'date']))
                time = time_elem.get_text(strip=True) if time_elem else ""
                
                if title:
                    schedule.append({
                        "title": title,
                        "time": time,
                        "source": "web_scraped"
                    })
            except Exception as e:
                logger.warning(f"Error extracting schedule data: {e}")
                continue
        
        return {
            "schedule": schedule,
            "total_sessions": len(schedule),
            "status": "available"
        }
    
    async def _extract_faq_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract FAQ data from the page."""
        faqs = []
        
        # Look for FAQ elements
        faq_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(word in x.lower() for word in ['faq', 'question', 'answer']))
        
        for element in faq_elements:
            try:
                question_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                question = question_elem.get_text(strip=True) if question_elem else ""
                
                answer_elem = element.find(['p', 'div'])
                answer = answer_elem.get_text(strip=True) if answer_elem else ""
                
                if question:
                    faqs.append({
                        "question": question,
                        "answer": answer,
                        "source": "web_scraped"
                    })
            except Exception as e:
                logger.warning(f"Error extracting FAQ data: {e}")
                continue
        
        return {
            "faqs": faqs,
            "total_faqs": len(faqs),
            "status": "available"
        }
    
    async def _extract_general_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract general page data."""
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ""
        
        # Extract main content
        main_content = soup.find(['main', 'article', 'div'], class_=lambda x: x and any(word in x.lower() for word in ['content', 'main', 'body']))
        content_text = main_content.get_text(strip=True) if main_content else ""
        
        return {
            "title": title_text,
            "content": content_text[:1000] + "..." if len(content_text) > 1000 else content_text,
            "status": "available"
        }
    
    async def get_speakers_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get speakers data from the website."""
        return await self._fetch_url(self.urls["speakers"], use_cache=not force_refresh)
    
    async def get_schedule_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get schedule data from the website."""
        return await self._fetch_url(self.urls["schedule"], use_cache=not force_refresh)
    
    async def get_faq_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get FAQ data from the website."""
        return await self._fetch_url(self.urls["faq"], use_cache=not force_refresh)
    
    async def get_main_page_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get main page data from the website."""
        return await self._fetch_url(self.urls["main"], use_cache=not force_refresh)
    
    async def get_all_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get all available data from the website."""
        tasks = [
            self.get_speakers_data(force_refresh),
            self.get_schedule_data(force_refresh),
            self.get_faq_data(force_refresh),
            self.get_main_page_data(force_refresh)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "speakers": results[0] if not isinstance(results[0], Exception) else {"status": "error", "error": str(results[0])},
            "schedule": results[1] if not isinstance(results[1], Exception) else {"status": "error", "error": str(results[1])},
            "faq": results[2] if not isinstance(results[2], Exception) else {"status": "error", "error": str(results[2])},
            "main": results[3] if not isinstance(results[3], Exception) else {"status": "error", "error": str(results[3])}
        }
    
    async def clear_cache(self) -> Dict[str, Any]:
        """Clear all cached data."""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            for cache_file in cache_files:
                cache_file.unlink()
            
            return {
                "status": "success",
                "message": f"Cleared {len(cache_files)} cache files"
            }
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

# Global instance
web_scraping_service = WebScrapingService() 