import re
import requests


def count_words(content):
    """Count words in markdown content, excluding code blocks."""
    # Removing code blocks
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
    
    # Removing markdown syntax
    content_clean = re.sub(r'[#*_\[\]()!]', ' ', content_no_code)
    
    # Counting words
    words = content_clean.split()
    return len(words)


def count_headings(content):
    headings = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}
    
    heading_pattern = r'^(#{1,6})\s+.+$'
    matches = re.finditer(heading_pattern, content, re.MULTILINE)
    
    for match in matches:
        level = len(match.group(1))
        headings[f'h{level}'] += 1
    
    return headings


def extract_links(content):
    links = []
    link_pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
    matches = re.finditer(link_pattern, content)
    
    for match in matches:
        links.append({
            'text': match.group(1),
            'url': match.group(2)
        })
    
    return links


def extract_images(content):
    images = []
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.finditer(image_pattern, content)
    
    for match in matches:
        images.append({
            'alt': match.group(1),
            'url': match.group(2)
        })
    
    return images


def validate_links(links):
    broken_links = []
    
    for link in links:
        url = link['url']
        
        # checking links
        if url.startswith('#') or not url.startswith(('http://', 'https://')):
            link['status'] = 'Skipped (local/anchor)'
            continue
        
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                link['status'] = f'OK ({response.status_code})'
            else:
                link['status'] = f'Broken ({response.status_code})'
                broken_links.append(link)
        except requests.exceptions.Timeout:
            link['status'] = 'Broken (Timeout)'
            broken_links.append(link)
        except Exception as e:
            link['status'] = f'Broken ({type(e).__name__})'
            broken_links.append(link)
    
    return broken_links


def generate_report(word_count, headings, links, images, broken_links):
    print("=" * 60)
    print("MARKDOWN ANALYSIS REPORT")
    print("=" * 60)
    print()
    
    # Words
    print(f"📊 Words: {word_count}")
    print()
    
    # Headings
    total_headings = sum(headings.values())
    print(f"📑 Headings: {total_headings}")
    for level, count in headings.items():
        if count > 0:
            print(f"   {level.upper()}: {count}")
    print()
    
    # Links
    print(f"🔗 Links: {len(links)}")
    print(f"   Broken: {len(broken_links)}")
    if broken_links:
        print("   Broken URLs:")
        for link in broken_links:
            print(f"      - {link['url']} ({link['status']})")
    print()
    
    # Images
    print(f"🖼️  Images: {len(images)}")
    if images:
        for img in images:
            alt = img['alt'] if img['alt'] else '(no alt text)'
            print(f"   - {alt}: {img['url']}")
    print()
    
    print("=" * 60)


def main():
    filename = input("Enter markdown file path: ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    if not content.strip():
        print("⚠️ The markdown file is empty. Nothing to analyze.")
        return

    print(f"\nAnalyzing '{filename}'...\n")
    
    # Perforing analysis
    word_count = count_words(content)
    headings = count_headings(content)
    links = extract_links(content)
    images = extract_images(content)
    
    # Validating links
    print("Validating links...")
    broken_links = validate_links(links)
    
    # Generating report
    print()
    generate_report(word_count, headings, links, images, broken_links)


if __name__ == "__main__":
    main()
