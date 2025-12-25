#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evernote ENEX to Markdown Converter
Converts .enex files to Markdown with tag-based folder organization
"""

import xml.etree.ElementTree as ET
import os
import base64
import re
from pathlib import Path
from datetime import datetime
import hashlib

class ENEXConverter:
    def __init__(self, input_dir="input_sap", output_dir="SAP_Materials"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.errors = []
        
    def convert_all(self):
        """Convert all .enex files in input directory"""
        print(f"🔍 Scanning {self.input_dir} for .enex files...")
        
        enex_files = list(self.input_dir.glob("*.enex"))
        if not enex_files:
            print("⚠️  No .enex files found")
            return
        
        print(f"📦 Found {len(enex_files)} .enex file(s)")
        
        for enex_file in enex_files:
            print(f"\n📄 Processing: {enex_file.name}")
            self.convert_enex(enex_file)
        
        if self.errors:
            print("\n" + "="*60)
            print("⚠️  ERRORS DETECTED:")
            print("="*60)
            for error in self.errors:
                print(f"❌ {error}")
        else:
            print("\n✅ All notes converted successfully!")
    
    def convert_enex(self, enex_file):
        """Convert single .enex file"""
        try:
            tree = ET.parse(enex_file)
            root = tree.getroot()
            
            for note in root.findall('note'):
                self.process_note(note)
                
        except Exception as e:
            error_msg = f"Failed to parse {enex_file.name}: {str(e)}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
    
    def process_note(self, note):
        """Process single note"""
        try:
            # Extract note data
            title = note.find('title').text or "Untitled"
            title = self.sanitize_filename(title)
            
            # Extract tags
            tags = [tag.text for tag in note.findall('tag') if tag.text]
            
            # Validate tags
            if len(tags) > 2:
                error_msg = f'ノート"{title}": タグが3つ以上あります。"# SAP"タグを含め2つまでにして下さい。（現在のタグ: {", ".join(tags)}）'
                print(f"⚠️  {error_msg}")
                self.errors.append(error_msg)
                return
            
            # Check if SAP tag exists
            if "# SAP" not in tags:
                print(f"⏭️  Skipping note '{title}': No SAP tag")
                return
            
            # Determine output folder
            output_folder = self.get_output_folder(tags)
            output_folder.mkdir(parents=True, exist_ok=True)
            
            # Extract content
            content_elem = note.find('content')
            content = content_elem.text if content_elem is not None else ""
            
            # Convert ENML to Markdown
            markdown_content = self.enml_to_markdown(content, title)
            
            # Extract metadata
            created = note.find('created').text if note.find('created') is not None else ""
            updated = note.find('updated').text if note.find('updated') is not None else ""
            
            # Add metadata to markdown
            metadata = self.create_metadata(title, tags, created, updated)
            
            # Process attachments
            attachments_md = self.process_attachments(note, output_folder, title)
            
            # Combine all content
            full_content = f"{metadata}\n\n{markdown_content}\n\n{attachments_md}"
            
            # Save markdown file
            md_file = output_folder / f"{title}.md"
            md_file.write_text(full_content, encoding='utf-8')
            
            print(f"✅ Converted: {title} → {output_folder}/{title}.md")
            
        except Exception as e:
            error_msg = f"Failed to process note: {str(e)}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
    
    def get_output_folder(self, tags):
        """Determine output folder based on tags"""
        if len(tags) == 1:  # Only "# SAP"
            return self.output_dir
        else:  # "# SAP" + another tag
            other_tag = [t for t in tags if t != "# SAP"][0]
            return self.output_dir / other_tag
    
    def enml_to_markdown(self, enml_content, title):
        """Convert ENML (Evernote Markup Language) to Markdown"""
        if not enml_content:
            return ""
        
        try:
            # Remove ENML wrapper
            content = re.sub(r'<\?xml[^>]+\?>', '', enml_content)
            content = re.sub(r'<!DOCTYPE[^>]+>', '', content)
            content = re.sub(r'<en-note[^>]*>', '', content)
            content = re.sub(r'</en-note>', '', content)
            
            # Convert common HTML tags to Markdown
            # Headers
            content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content)
            content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content)
            content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content)
            
            # Bold and italic
            content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content)
            content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content)
            content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content)
            content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content)
            
            # Links
            content = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
            
            # Lists
            content = re.sub(r'<ul[^>]*>', '\n', content)
            content = re.sub(r'</ul>', '\n', content)
            content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', content)
            
            # Line breaks
            content = re.sub(r'<br[^>]*/>', '\n', content)
            content = re.sub(r'<div[^>]*>', '\n', content)
            content = re.sub(r'</div>', '', content)
            
            # Paragraphs
            content = re.sub(r'<p[^>]*>', '\n', content)
            content = re.sub(r'</p>', '\n', content)
            
            # Remove remaining HTML tags
            content = re.sub(r'<[^>]+>', '', content)
            
            # Decode HTML entities
            content = content.replace('&lt;', '<')
            content = content.replace('&gt;', '>')
            content = content.replace('&amp;', '&')
            content = content.replace('&quot;', '"')
            content = content.replace('&nbsp;', ' ')
            
            # Clean up extra newlines
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            return content.strip()
            
        except Exception as e:
            print(f"⚠️  Warning: Failed to convert ENML to Markdown: {str(e)}")
            return enml_content
    
    def process_attachments(self, note, output_folder, note_title):
        """Process note attachments"""
        attachments = note.findall('.//resource')
        if not attachments:
            return ""
        
        attachment_folder = output_folder / f"{note_title}_attachments"
        attachment_folder.mkdir(parents=True, exist_ok=True)
        
        attachments_md = "\n## 添付ファイル\n\n"
        
        for idx, resource in enumerate(attachments, 1):
            try:
                # Get file data
                data_elem = resource.find('data')
                if data_elem is None:
                    continue
                
                file_data = base64.b64decode(data_elem.text)
                
                # Get mime type
                mime_elem = resource.find('mime')
                mime_type = mime_elem.text if mime_elem is not None else "application/octet-stream"
                
                # Get filename
                attributes = resource.find('resource-attributes')
                if attributes is not None and attributes.find('file-name') is not None:
                    filename = attributes.find('file-name').text
                else:
                    ext = self.get_extension_from_mime(mime_type)
                    filename = f"attachment_{idx}{ext}"
                
                filename = self.sanitize_filename(filename)
                
                # Save file
                file_path = attachment_folder / filename
                file_path.write_bytes(file_data)
                
                # Add to markdown
                relative_path = f"./{note_title}_attachments/{filename}"
                icon = self.get_file_icon(filename)
                attachments_md += f"- {icon} [{filename}]({relative_path})\n"
                
                print(f"  📎 Saved attachment: {filename}")
                
            except Exception as e:
                print(f"  ⚠️  Warning: Failed to save attachment: {str(e)}")
        
        return attachments_md
    
    def create_metadata(self, title, tags, created, updated):
        """Create markdown metadata header"""
        metadata = f"# {title}\n\n"
        
        if tags:
            metadata += f"**タグ:** {', '.join(tags)}\n\n"
        
        if created:
            created_date = self.format_evernote_date(created)
            metadata += f"**作成日:** {created_date}\n\n"
        
        if updated:
            updated_date = self.format_evernote_date(updated)
            metadata += f"**更新日:** {updated_date}\n\n"
        
        metadata += "---\n"
        return metadata
    
    def format_evernote_date(self, date_str):
        """Format Evernote date string"""
        try:
            # Evernote format: 20231225T120000Z
            dt = datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return date_str
    
    def sanitize_filename(self, filename):
        """Sanitize filename for filesystem"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def get_extension_from_mime(self, mime_type):
        """Get file extension from MIME type"""
        mime_map = {
            'application/pdf': '.pdf',
            'application/vnd.ms-excel': '.xls',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
            'application/vnd.ms-powerpoint': '.ppt',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'image/png': '.png',
            'image/jpeg': '.jpg',
            'image/gif': '.gif',
            'text/plain': '.txt',
        }
        return mime_map.get(mime_type, '.bin')
    
    def get_file_icon(self, filename):
        """Get emoji icon for file type"""
        ext = Path(filename).suffix.lower()
        icon_map = {
            '.pdf': '📄',
            '.xls': '📊', '.xlsx': '📊',
            '.ppt': '📽️', '.pptx': '📽️',
            '.doc': '📝', '.docx': '📝',
            '.png': '🖼️', '.jpg': '🖼️', '.gif': '🖼️',
            '.txt': '📃',
        }
        return icon_map.get(ext, '📎')

if __name__ == "__main__":
    print("=" * 60)
    print("Evernote to Markdown Converter")
    print("=" * 60)
    
    converter = ENEXConverter()
    converter.convert_all()
    
    print("\n" + "=" * 60)
    print("✨ Conversion completed!")
    print("=" * 60)
