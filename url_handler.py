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
            'YYYY': now.strftime('%Y')
        }
    
    def get_custom_date_formatted(self, date_str: str) -> dict:
        """Get custom date in required formats."""
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            return {
                'MM': date_obj.strftime('%m'),
                'DD': date_obj.strftime('%d'),
                'YYYY': date_obj.strftime('%Y')
            }
        except ValueError:
            # Fallback to current date if invalid
            return self.get_current_date_formatted()
    
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