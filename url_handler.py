"""
URL handler for generating image URLs with current date.
"""

import os
from datetime import datetime
from typing import List

class URLHandler:
    """Handle URL generation with date substitution."""
    
    def __init__(self):
        """Initialize URL handler."""
        self.url_files = {
            'estu': 'urls_estu.txt',
            'stu': 'urls_stu.txt', 
            'astu': 'urls_astu.txt',
            'cripto': 'urls_cripto.txt'
        }
    
    def get_current_date_formatted(self) -> dict:
        """Get current date in required formats."""
        now = datetime.now()
        return {
            'MM': now.strftime('%m'),
            'DD': now.strftime('%d'),
            'YY': now.strftime('%y'),
            'YYYY': now.strftime('%Y')
        }
    
    def get_custom_date_formatted(self, date_str: str) -> dict:
        """Get custom date in required formats."""
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            return {
                'MM': date_obj.strftime('%m'),
                'DD': date_obj.strftime('%d'), 
                'YY': date_obj.strftime('%y'),
                'YYYY': date_obj.strftime('%Y')
            }
        except ValueError:
            # Fallback to current date if invalid
            return self.get_current_date_formatted()
    
    def add_url_to_category(self, category: str, url: str) -> bool:
        """Add URL to specified category file."""
        try:
            if category not in self.url_files:
                return False
            
            file_path = self.url_files[category]
            
            # Check if URL already exists
            existing_urls = self.load_urls_from_file(category)
            if url in existing_urls:
                return False
            
            # Add URL to file
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"{url}\n")
            
            return True
        except Exception as e:
            print(f"Error adding URL to {category}: {e}")
            return False
    
    def remove_url_from_category(self, category: str, url: str) -> bool:
        """Remove URL from specified category file."""
        try:
            if category not in self.url_files:
                return False
            
            file_path = self.url_files[category]
            existing_urls = self.load_urls_from_file(category)
            
            if url not in existing_urls:
                return False
            
            # Remove URL and rewrite file
            updated_urls = [u for u in existing_urls if u != url]
            
            with open(file_path, 'w', encoding='utf-8') as file:
                for u in updated_urls:
                    file.write(f"{u}\n")
            
            return True
        except Exception as e:
            print(f"Error removing URL from {category}: {e}")
            return False
    
    def list_urls_for_category(self, category: str) -> List[str]:
        """List all URLs for specified category."""
        return self.load_urls_from_file(category)
    
    def load_urls_from_file(self, category: str) -> List[str]:
        """Load URLs from file for given category."""
        try:
            file_path = self.url_files.get(category)
            if not file_path or not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                urls = [line.strip() for line in file.readlines() if line.strip()]
            
            return urls
        except Exception as e:
            print(f"Error loading URLs for {category}: {e}")
            return []
    
    def generate_daily_urls(self, category: str, custom_date: str = None) -> List[str]:
        """Generate URLs with specified date for given category."""
        template_urls = self.load_urls_from_file(category)
        if not template_urls:
            return []
        
        if custom_date:
            date_parts = self.get_custom_date_formatted(custom_date)
        else:
            date_parts = self.get_current_date_formatted()
        
        daily_urls = []
        for template_url in template_urls:
            # Replace date placeholders with specified date
            url = template_url.format(**date_parts)
            daily_urls.append(url)
        
        return daily_urls
    
    def get_urls_for_button(self, button_data: str, custom_date: str = None) -> List[str]:
        """Get URLs for specific button with optional custom date."""
        return self.generate_daily_urls(button_data, custom_date)