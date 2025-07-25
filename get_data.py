import requests
import re
import time
from pathlib import Path

def download_formal_texts(target_size_mb=2.5):
    """Download formal non-fiction texts from Project Gutenberg"""
    
    print("Downloading formal/non-fiction texts...")
    
    # Formal non-fiction sources
    formal_sources = {
        'declaration_independence': 'https://www.gutenberg.org/files/1/1-0.txt', 
        'federalist_papers': 'https://www.gutenberg.org/files/1404/1404-0.txt',
        'origin_species': 'https://www.gutenberg.org/files/1228/1228-0.txt',
        'wealth_nations': 'https://www.gutenberg.org/files/3300/3300-0.txt',
    }
    
    formal_texts = []
    target_size = int(target_size_mb * 1_000_000)
    current_size = 0
    
    for source_name, url in formal_sources.items():
        if current_size >= target_size:
            break
            
        print(f"Downloading {source_name}...")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                
                # Clean up text
                text = re.sub(r'\r\n', '\n', text)
                text = re.sub(r'\n\s*\n', '\n\n', text)
                text = text.strip()
                
                if text:
                    formal_texts.append(text)
                    current_size += len(text)
                    print(f"  Added {len(text):,} characters")
        
        except Exception as e:
            print(f"Error downloading {source_name}: {e}")
            continue
        
        time.sleep(0.5)
    
    # Combine all texts
    formal_text = '\n\n'.join(formal_texts)
    
    # Truncate to target size
    if len(formal_text) > target_size:
        formal_text = formal_text[:target_size]
        # End at sentence boundary
        last_period = formal_text.rfind('.')
        if last_period > target_size * 0.9:
            formal_text = formal_text[:last_period + 1]
    
    return formal_text

def download_fiction_books(target_size_mb=2.5):
    """Download fiction books from Project Gutenberg"""
    
    print("Downloading fiction books...")
    
    # Classic fiction books
    fiction_books = {
        'pride_prejudice': 'https://www.gutenberg.org/files/1342/1342-0.txt',
        'great_gatsby': 'https://www.gutenberg.org/files/64317/64317-0.txt',
        'dracula': 'https://www.gutenberg.org/files/345/345-0.txt',
        'frankenstein': 'https://www.gutenberg.org/files/84/84-0.txt',
        'adventures_sherlock': 'https://www.gutenberg.org/files/1661/1661-0.txt',
    }
    
    fiction_texts = []
    target_size = int(target_size_mb * 1_000_000)
    current_size = 0
    
    for book_name, url in fiction_books.items():
        if current_size >= target_size:
            break
            
        print(f"Downloading {book_name}...")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                
                # Clean up text
                text = re.sub(r'\r\n', '\n', text)
                text = re.sub(r'\n\s*\n', '\n\n', text)
                text = text.strip()
                
                if text:
                    fiction_texts.append(text)
                    current_size += len(text)
                    print(f"  Added {len(text):,} characters")
        
        except Exception as e:
            print(f"Error downloading {book_name}: {e}")
            continue
        
        time.sleep(0.5)
    
    # Combine all fiction
    fiction_text = '\n\n'.join(fiction_texts)
    
    # Truncate to target size
    if len(fiction_text) > target_size:
        fiction_text = fiction_text[:target_size]
        # End at sentence boundary
        last_period = fiction_text.rfind('.')
        if last_period > target_size * 0.9:
            fiction_text = fiction_text[:last_period + 1]
    
    return fiction_text

def split_train_val(text, val_ratio=0.1):
    """Split text into training and validation sets"""
    
    # Split by sentences to maintain coherence
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Calculate split point
    val_size = int(len(sentences) * val_ratio)
    train_sentences = sentences[:-val_size] if val_size > 0 else sentences
    val_sentences = sentences[-val_size:] if val_size > 0 else []
    
    # Rejoin sentences
    train_text = '. '.join(train_sentences) + '.'
    val_text = '. '.join(val_sentences) + '.' if val_sentences else ''
    
    return train_text, val_text

def main():
    """Main function to create formal vs fiction datasets with train/val splits"""
    
    output_dir = Path("training_data")
    output_dir.mkdir(exist_ok=True)
    
    print("=== CREATING FORMAL VS FICTION DATASETS ===")
    
    # Download datasets
    print("\n1. Downloading formal texts...")
    formal_text = download_formal_texts(target_size_mb=2.5)
    print(f"Formal dataset: {len(formal_text):,} characters ({len(formal_text)/1_000_000:.2f} MB)")
    
    print("\n2. Downloading fiction texts...")
    fiction_text = download_fiction_books(target_size_mb=2.5)
    print(f"Fiction dataset: {len(fiction_text):,} characters ({len(fiction_text)/1_000_000:.2f} MB)")
    
    # Split into train/validation
    print("\n3. Creating train/validation splits...")
    
    formal_train, formal_val = split_train_val(formal_text, val_ratio=0.1)
    fiction_train, fiction_val = split_train_val(fiction_text, val_ratio=0.1)
    
    # Save all files
    files_created = []
    
    # Formal datasets
    with open(output_dir / "formal_train.txt", "w", encoding="utf-8") as f:
        f.write(formal_train)
    files_created.append(f"formal_train.txt ({len(formal_train)/1_000_000:.2f} MB)")
    
    with open(output_dir / "formal_val.txt", "w", encoding="utf-8") as f:
        f.write(formal_val)
    files_created.append(f"formal_val.txt ({len(formal_val)/1_000_000:.2f} MB)")
    
    # Fiction datasets
    with open(output_dir / "fiction_train.txt", "w", encoding="utf-8") as f:
        f.write(fiction_train)
    files_created.append(f"fiction_train.txt ({len(fiction_train)/1_000_000:.2f} MB)")
    
    with open(output_dir / "fiction_val.txt", "w", encoding="utf-8") as f:
        f.write(fiction_val)
    files_created.append(f"fiction_val.txt ({len(fiction_val)/1_000_000:.2f} MB)")
    
    print(f"\n=== FILES CREATED ===")
    for file_info in files_created:
        print(f"✓ {file_info}")
    print(f"All files saved in {output_dir}/")

if __name__ == "__main__":
    main()
