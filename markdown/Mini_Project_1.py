
import re
import requests
import json
import os
from datetime import datetime


def load_config():
    
    default_config = {
        'timeout': 5,
        'max_redirects': 5,
        'validate_images': False,
        'generate_html': False,
        'exclude_extensions': [],
        'github_token': None
    }
    
    config_file = 'config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                print(f"✓ Loaded configuration from {config_file}")
        except Exception as e:
            print(f"⚠️ Error loading config: {e}. Using defaults.")
    
    return default_config

def is_markdown_file(filename):
    return filename.lower().endswith(".md")

def count_words(content):
    
    # Remove fenced code blocks
    content = re.sub(r"```[\s\S]*?```", "", content)
    # Remove inline code
    content = re.sub(r"`[^`]+`", "", content)
    # Remove links and images
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    content = re.sub(r"\[.*?\]\(.*?\)", "", content)
    # Remove markdown symbols
    content = re.sub(r"[#>*_]", " ", content)

    words = content.split()
    return len(words)

def count_headings(content):
    headings = {"h1": 0, "h2": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0}

    for match in re.finditer(r"^(#{1,6})\s+", content, re.MULTILINE):
        level = len(match.group(1))
        headings[f"h{level}"] += 1

    return headings


def extract_links(content):
    """Extract all markdown links including custom extensions."""
    links = []
    
    # Standard markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.finditer(link_pattern, content)
    
    for match in matches:
        links.append({
            'text': match.group(1),
            'url': match.group(2),
            'type': 'standard'
        })
    
    # Wiki-style links [[Page Name]]
    wiki_pattern = r'\[\[([^\]]+)\]\]'
    wiki_matches = re.finditer(wiki_pattern, content)
    
    for match in wiki_matches:
        links.append({
            'text': match.group(1),
            'url': match.group(1),
            'type': 'wiki'
        })
    
    # Reference-style links [text][ref]
    ref_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
    ref_matches = re.finditer(ref_pattern, content)
    
    for match in ref_matches:
        links.append({
            'text': match.group(1),
            'url': f"ref:{match.group(2)}",
            'type': 'reference'
        })
    
    return links


def extract_images(content):
    """Extract all markdown images ![alt](url)."""
    images = []
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.finditer(image_pattern, content)
    
    for match in matches:
        images.append({
            'alt': match.group(1),
            'url': match.group(2)
        })
    
    return images


def validate_links(links, config):
    """Validate a list of links by checking if they're accessible."""
    broken_links = []
    timeout = config.get('timeout', 5)
    
    for link in links:
        url = link['url']
        
        # Skip anchor links, relative paths, wiki links, and references
        if (url.startswith('#') or 
            url.startswith('ref:') or 
            link.get('type') == 'wiki' or
            not url.startswith(('http://', 'https://'))):
            link['status'] = 'Skipped (local/anchor/wiki)'
            continue
        
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
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


def generate_html_report(filename, word_count, headings, links, images, broken_links):
    """Generate an HTML report with charts."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate statistics
    total_headings = sum(headings.values())
    total_links = len(links)
    total_broken = len(broken_links)
    total_images = len(images)
    
    # Prepare heading data for chart
    heading_labels = [f"H{i}" for i in range(1, 7) if headings[f'h{i}'] > 0]
    heading_values = [headings[f'h{i}'] for i in range(1, 7) if headings[f'h{i}'] > 0]
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Analysis Report - {os.path.basename(filename)}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-icon {{ font-size: 3em; margin-bottom: 10px; }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .chart-container {{
            position: relative;
            height: 300px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{ background: #f5f5f5; }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-success {{ background: #d4edda; color: #155724; }}
        .badge-danger {{ background: #f8d7da; color: #721c24; }}
        .badge-warning {{ background: #fff3cd; color: #856404; }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Markdown Analysis Report</h1>
            <p>{os.path.basename(filename)}</p>
            <p style="font-size: 0.9em; opacity: 0.8;">Generated on {timestamp}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-value">{word_count:,}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📑</div>
                <div class="stat-value">{total_headings}</div>
                <div class="stat-label">Headings</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔗</div>
                <div class="stat-value">{total_links}</div>
                <div class="stat-label">Links</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🖼️</div>
                <div class="stat-value">{total_images}</div>
                <div class="stat-label">Images</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📑 Heading Distribution</h2>
                <div class="chart-container">
                    <canvas id="headingChart"></canvas>
                </div>
            </div>
            
            <div class="section">
                <h2>🔗 Link Analysis</h2>
                <div class="chart-container" style="height: 200px;">
                    <canvas id="linkChart"></canvas>
                </div>
                {f'''
                <h3 style="margin-top: 30px; color: #dc3545;">⚠️ Broken Links ({total_broken})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{link['url']}</td><td><span class='badge badge-danger'>{link['status']}</span></td></tr>" for link in broken_links])}
                    </tbody>
                </table>
                ''' if broken_links else '<p style="color: #28a745; font-weight: 600;">✓ All links are valid!</p>'}
            </div>
            
            {f'''
            <div class="section">
                <h2>🖼️ Images</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Alt Text</th>
                            <th>URL</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{img['alt'] if img['alt'] else '<em>(no alt text)</em>'}</td><td>{img['url']}</td></tr>" for img in images])}
                    </tbody>
                </table>
            </div>
            ''' if images else ''}
        </div>
        
        <div class="footer">
            <p>Generated by Markdown File Analyzer</p>
        </div>
    </div>
    
    <script>
        // Heading Distribution Chart
        const headingCtx = document.getElementById('headingChart').getContext('2d');
        new Chart(headingCtx, {{
            type: 'bar',
            data: {{
                labels: {heading_labels},
                datasets: [{{
                    label: 'Count',
                    data: {heading_values},
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ stepSize: 1 }}
                    }}
                }}
            }}
        }});
        
        // Link Status Chart
        const linkCtx = document.getElementById('linkChart').getContext('2d');
        new Chart(linkCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Valid Links', 'Broken Links'],
                datasets: [{{
                    data: [{total_links - total_broken}, {total_broken}],
                    backgroundColor: ['rgba(40, 167, 69, 0.6)', 'rgba(220, 53, 69, 0.6)'],
                    borderColor: ['rgba(40, 167, 69, 1)', 'rgba(220, 53, 69, 1)'],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    output_file = filename.replace('.md', '_report.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ HTML report generated: {output_file}")
    return output_file


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


def analyze_github_repo(repo_url, config):
    
    try:
        # Extract owner and repo name from URL
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        # GitHub API endpoint
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
        headers = {}
        if config.get('github_token'):
            headers['Authorization'] = f"token {config['github_token']}"
        
        print(f"\n🔍 Fetching repository contents from GitHub...")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch repository: {response.status_code}")
            return None
        
        contents = response.json()
        
        # Find all markdown files
        md_files = []
        for item in contents:
            if item['name'].endswith('.md') or item['name'].endswith('.markdown'):
                md_files.append({
                    'name': item['name'],
                    'url': item['download_url']
                })
        
        if not md_files:
            print("⚠️ No markdown files found in repository root.")
            return None
        
        print(f"✓ Found {len(md_files)} markdown file(s)")
        
        # Let user choose which file to analyze
        print("\nAvailable files:")
        for i, file in enumerate(md_files, 1):
            print(f"  {i}. {file['name']}")
        
        choice = input("\nEnter file number to analyze (or 'all' for all files): ").strip()
        
        if choice.lower() == 'all':
            return md_files
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(md_files):
                    return [md_files[idx]]
                else:
                    print("❌ Invalid choice")
                    return None
            except ValueError:
                print("❌ Invalid input")
                return None
                
    except Exception as e:
        print(f"❌ Error accessing GitHub repository: {e}")
        return None


def download_github_file(file_info):
    """Download a markdown file from GitHub."""
    try:
        response = requests.get(file_info['url'], timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"❌ Failed to download {file_info['name']}")
            return None
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        return None


def main():
    """Main function with enhanced features."""
    print("=" * 60)
    print("MARKDOWN FILE ANALYZER - Enhanced Edition")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Ask for input type
    print("\nChoose input method:")
    print("  1. Local file")
    print("  2. GitHub repository")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '2':
        repo_url = input("Enter GitHub repository URL: ").strip()
        files = analyze_github_repo(repo_url, config)
        
        if not files:
            return
        
        # Process GitHub files
        for file_info in files:
            print(f"\n{'=' * 60}")
            print(f"Analyzing: {file_info['name']}")
            print('=' * 60)
            
            content = download_github_file(file_info)
            if not content:
                continue
            
            # Perform analysis
            word_count = count_words(content)
            headings = count_headings(content)
            links = extract_links(content)
            images = extract_images(content)
            
            # Validate links
            print("Validating links...")
            broken_links = validate_links(links, config)
            
            # Generate reports
            print()
            generate_report(word_count, headings, links, images, broken_links)
            
            if config.get('generate_html'):
                generate_html_report(file_info['name'], word_count, headings, 
                                   links, images, broken_links)
    
    else:
        # Local file analysis
        filename = input("Enter markdown file path: ").strip()

        if not is_markdown_file(filename):
            print("Error: Invalid file format. Only .md files are allowed.")
            return


        
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
        
        # Perform analysis
        word_count = count_words(content)
        headings = count_headings(content)
        links = extract_links(content)
        images = extract_images(content)
        
        # Validate links
        print("Validating links...")
        broken_links = validate_links(links, config)
        
        # Generate reports
        print()
        generate_report(word_count, headings, links, images, broken_links)
        
        if config.get('generate_html'):
            generate_html_report(filename, word_count, headings, links, images, broken_links)


if __name__ == "__main__":
    main()
