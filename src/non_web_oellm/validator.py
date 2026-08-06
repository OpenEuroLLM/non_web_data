import iso639
import pycountry
import re
import validators
from datetime import datetime

TOPICS = ["Agriculture", "Literature", "Linguistics", "Politics", "Economics", "Law", "Science", "Technology", "Medicine", "Education", "Culture", "Journalism", "Society", "History", "Religion", "Philosophy", "Psychology", "Sports", "Entertainment", "Sociology", "Business", "Environment", "Other", "Unknown", "Public Administration"]
DATA_TYPES = ["tmx", "gz", "tar", "docx", "rar", "ppt", "pptx", "zip","vtt", "aac", "m4a", "ogg", "wav", "pdf", "rtf", "mp4", "mp3", "txt", "html", "docx", "xlsx", "csv", "json", "xml", "doc"]
LICENSES = ["Public Domain Mark 1.0", "CC-BY-NC-SA-2.5-ES", "explicit open license", "CC-BY-SA-3.0", "GPL-2.0-only", "CC-BY-NC-SA-4.0", "AGPL-3.0-only", "GFDL-1.3", "LGPL-2.0-only", "CC-BY-NC-SA-3.0", "unspecified", "LGPL-2.0-or-later", "CC-BY-4.0", "CC-BY-SA-4.0", "Apache-2.0", "CC-BY-NC-ND-4.0", "BSD-2-Clause-FreeBSD", "LGPL-3.0-only", "GPL-3.0-or-later", "CC-BY-2.5", "CC-BY-3.0", "CC-BY-NC-ND-3.0", "CC-BY-NC-4.0", "GPL-3.0-only", "CC-BY-NC-SA-2.0", "LGPL-3.0-or-later", "CC-BY-NC-3.0", "AGPL-1.0-or-later", "CC0 1.0", "CC-BY-SA-2.0", "BSD-3-Clause", "BSD-4-Clause", "GPL", "GNU General Public License v3.0 (GPL-3.0)", "GPL v3", "GPL - 2.0"]

class Validation():
    def __init__(self):
        self.topics = TOPICS
        self.data_types = DATA_TYPES
        self.licenses = LICENSES

    def validate_metadata(self, metadata):
        validated_metadata = {
            "LANGUAGE_CODE": self.validate_language_codes(metadata.get("LANGUAGE_CODE")),
            "MACRO_LANG": self.create_macro_language(metadata.get("LANGUAGE_CODE")),
            "SCRIPT_LANG": self.validate_script(metadata.get("SCRIPT_LANG")),
            "LANGUAGE": self.create_language_name(metadata.get("LANGUAGE_CODE")),
            "VARIANT": self.validate_free_text(metadata.get("VARIANT")),
            "TOPIC": self.validate_topic(metadata.get("TOPIC")),
            "DATA_TYPE": self.validate_data_type(metadata.get("DATA_TYPE")),
            "SOURCE_ORGANIZATION": self.validate_free_text(metadata.get("SOURCE_ORGANIZATION")),
            "LICENSE": self.validate_license(metadata.get("LICENSE")),
            "DOWNLOAD_SOURCE": self.validate_url(metadata.get("DOWNLOAD_SOURCE")),
            "MIXED_LANGUAGES": self.validate_mixed_languages(metadata.get("MIXED_LANGUAGES")),
            "COMMENTARY": self.validate_free_text(metadata.get("COMMENTARY")),
            "DATASET_NAME_OR_DESCRIPTION": self.validate_free_text(metadata.get("DATASET_NAME_OR_DESCRIPTION")),
            "DATE_OF_IDENTIFICATION": self.validate_date(metadata.get("DATE_OF_IDENTIFICATION")),
            "CONTACT": self.validate_free_text(metadata.get("CONTACT")),
            "SOURCE_IDENTIFICATION_URL": self.validate_url(metadata.get("SOURCE_IDENTIFICATION_URL"))
        }
        
        # Preserve NAME and PATH if they exist
        if 'NAME' in metadata: validated_metadata['NAME'] = metadata['NAME']
        if 'PATH' in metadata: validated_metadata['PATH'] = metadata['PATH']

        errors = [key for key, value in validated_metadata.items() if value is False]
        if errors:
            return "errors occured in the following fields: " + ", ".join(errors)
        return validated_metadata
    
    def validate_language_codes(self, lang_code):
        try:
            l = iso639.Lang(lang_code)
            if l.pt3 == lang_code:
                return lang_code
            return False
        except:
            return False
    
    def create_macro_language(self, lang_code):
        try:
            l = iso639.Lang(lang_code)
            macro = l.macro()
            return macro.pt3 if macro else lang_code
        except:
            return lang_code
        
    def validate_script(self, script_code):
        if not isinstance(script_code, str):
            return False
        script = pycountry.scripts.get(alpha_4=script_code)
        return script_code.lower() if script is not None else False
    
    def create_language_name(self, lang_code):
        try:
            l = iso639.Lang(lang_code)
            return l.name
        except:
            return "not found"
    
    def validate_topic(self, topic):
        return topic if topic in self.topics else False
    
    def validate_data_type(self, data_type):
        return data_type if data_type in self.data_types else False
    
    def validate_license(self, license):
        return license if license in self.licenses else False
    
    def validate_url(self, url):
        validation = validators.url(url)
        return url if validation else False
    
    def validate_mixed_languages(self, mixed_langs):
        if not isinstance(mixed_langs, list):
            return False
        for lang in mixed_langs:
            if not self.validate_language_codes(lang):
                return False
        return mixed_langs
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except (ValueError, TypeError):
            return False
    
    def validate_free_text(self, text):
        return text if isinstance(text, str) else False
