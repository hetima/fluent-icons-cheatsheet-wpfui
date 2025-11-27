#!/usr/bin/env python3
from fontTools.ttLib import TTFont
import base64
import sys
import urllib.request
import os

def download_font(url, output_path):
    """Download font file from URL"""
    print(f"📥 Downloading font from {url}...")
    urllib.request.urlretrieve(url, output_path)
    print(f"✅ Font downloaded to {output_path}")
    return output_path

def generate_cheatsheet(font_path, output_html='fluent_icons_cheatsheet.html'):
    # Load font
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    
    # Read font file for embedding
    with open(font_path, 'rb') as f:
        font_data = base64.b64encode(f.read()).decode()
    
    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fluent Icons Cheatsheet</title>
    <style>
        @font-face {{
            font-family: 'FluentIcons';
            src: url(data:font/truetype;charset=utf-8;base64,{font_data}) format('truetype');
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #1e1e1e;
            --bg-secondary: #252526;
            --bg-tertiary: #2d2d30;
            --border-color: #3c3c3c;
            --text-primary: #d4d4d4;
            --text-secondary: #858585;
            --text-bright: #fff;
            --accent-color: #007acc;
            --code-color: #4ec9b0;
        }}
        
        [data-theme="light"] {{
            --bg-primary: #f3f3f3;
            --bg-secondary: #ffffff;
            --bg-tertiary: #f8f8f8;
            --border-color: #e0e0e0;
            --text-primary: #333333;
            --text-secondary: #666666;
            --text-bright: #000000;
            --accent-color: #0078d4;
            --code-color: #0e7c6e;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        header {{
            position: sticky;
            top: 0;
            background: var(--bg-secondary);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            z-index: 100;
        }}
        
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .header-controls {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        h1 {{
            margin: 0;
            color: var(--text-bright);
        }}
        
        .btn {{
            background: var(--bg-tertiary);
            border: 2px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }}
        
        .btn:hover {{
            border-color: var(--accent-color);
            background: var(--bg-secondary);
        }}
        
        .btn.active {{
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }}
        
        .density-group {{
            display: flex;
            gap: 0;
        }}
        
        .density-group .btn {{
            border-radius: 0;
        }}
        
        .density-group .btn:first-child {{
            border-radius: 6px 0 0 6px;
        }}
        
        .density-group .btn:last-child {{
            border-radius: 0 6px 6px 0;
            border-left: none;
        }}
        
        #search {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid var(--border-color);
            border-radius: 6px;
            background: var(--bg-tertiary);
            color: var(--text-primary);
            outline: none;
            transition: background-color 0.3s, border-color 0.3s;
        }}
        
        #search:focus {{
            border-color: var(--accent-color);
        }}
        
        #count {{
            margin-top: 10px;
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            transition: gap 0.3s;
        }}
        
        .grid.dense {{
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 8px;
        }}
        
        .grid.dense .icon-card {{
            padding: 12px;
        }}
        
        .grid.dense .icon-display {{
            font-size: 32px;
            margin-bottom: 8px;
        }}
        
        .grid.dense .icon-name {{
            font-size: 10px;
        }}
        
        .grid.dense .icon-code {{
            font-size: 11px;
        }}
        
        .icon-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .icon-card:hover {{
            background: var(--bg-tertiary);
            border-color: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,122,204,0.2);
        }}
        
        .icon-display {{
            font-family: 'FluentIcons';
            font-size: 48px;
            margin-bottom: 12px;
            color: var(--text-bright);
        }}
        
        .icon-name {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            word-break: break-word;
        }}
        
        .icon-code {{
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: var(--code-color);
            background: var(--bg-primary);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        .copied {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s, slideOut 0.3s 1.7s;
            z-index: 1000;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(400px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        @keyframes slideOut {{
            from {{ transform: translateX(0); opacity: 1; }}
            to {{ transform: translateX(400px); opacity: 0; }}
        }}
        
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-top">
            <h1>Fluent Icons Cheatsheet</h1>
            <div class="header-controls">
                <div class="density-group">
                    <button class="btn" id="density-sparse" onclick="setDensity('sparse')">Sparse</button>
                    <button class="btn active" id="density-dense" onclick="setDensity('dense')">Dense</button>
                </div>
                <button class="btn" id="theme-toggle" onclick="toggleTheme()">🌙 Dark</button>
            </div>
        </div>
        <input type="text" id="search" placeholder="Search icons by name..." autocomplete="off">
        <div id="count"></div>
    </header>
    
    <div class="grid" id="icons">
'''
    
    # Add all icons
    total = 0
    for codepoint, glyph_name in sorted(cmap.items(), key=lambda x: x[1]):
        char = chr(codepoint)
        hex_code = f"0x{codepoint:04x}"
        
        # Clean up glyph name for display
        display_name = glyph_name.replace('_', ' ').title()
        
        html += f'''
        <div class="icon-card" data-name="{glyph_name.lower()}" data-code="{hex_code}" onclick="copyCode(this)">
            <div class="icon-display">{char}</div>
            <div class="icon-name">{display_name}</div>
            <div class="icon-code">{hex_code}</div>
        </div>
'''
        total += 1
    
    html += f'''
    </div>
    
    <script>
        const searchInput = document.getElementById('search');
        const iconsGrid = document.getElementById('icons');
        const countDisplay = document.getElementById('count');
        const allCards = document.querySelectorAll('.icon-card');
        const themeToggle = document.getElementById('theme-toggle');
        const densitySparseBtn = document.getElementById('density-sparse');
        const denseDenseBtn = document.getElementById('density-dense');
        
        // Density management
        function initDensity() {{
            const savedDensity = localStorage.getItem('density') || 'dense';
            setDensity(savedDensity);
        }}
        
        function setDensity(density) {{
            if (density === 'dense') {{
                iconsGrid.classList.add('dense');
                denseDenseBtn.classList.add('active');
                densitySparseBtn.classList.remove('active');
            }} else {{
                iconsGrid.classList.remove('dense');
                densitySparseBtn.classList.add('active');
                denseDenseBtn.classList.remove('active');
            }}
            localStorage.setItem('density', density);
        }}
        
        // Theme management
        function initTheme() {{
            const savedTheme = localStorage.getItem('theme');
            const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
            setTheme(theme);
        }}
        
        function setTheme(theme) {{
            if (theme === 'light') {{
                document.documentElement.setAttribute('data-theme', 'light');
                themeToggle.textContent = '☀️ Light';
            }} else {{
                document.documentElement.removeAttribute('data-theme');
                themeToggle.textContent = '🌙 Dark';
            }}
            localStorage.setItem('theme', theme);
        }}
        
        function toggleTheme() {{
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
        }}
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {{
            if (!localStorage.getItem('theme')) {{
                setTheme(e.matches ? 'dark' : 'light');
            }}
        }});
        
        function updateCount() {{
            const visible = document.querySelectorAll('.icon-card:not(.hidden)').length;
            countDisplay.textContent = `Showing ${{visible}} of {total} icons`;
        }}
        
        function filterIcons(searchText) {{
            const search = searchText.toLowerCase();
            
            allCards.forEach(card => {{
                const name = card.dataset.name;
                const code = card.dataset.code.toLowerCase();
                
                if (name.includes(search) || code.includes(search)) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
            
            updateCount();
        }}
        
        function copyCode(card) {{
            const code = card.dataset.code;
            navigator.clipboard.writeText(code).then(() => {{
                showCopied(code);
            }});
        }}
        
        function showCopied(code) {{
            const existing = document.querySelector('.copied');
            if (existing) existing.remove();
            
            const notification = document.createElement('div');
            notification.className = 'copied';
            notification.textContent = `Copied: ${{code}}`;
            document.body.appendChild(notification);
            
            setTimeout(() => notification.remove(), 2000);
        }}
        
        searchInput.addEventListener('input', (e) => {{
            filterIcons(e.target.value);
        }});
        
        // Keyboard navigation
        searchInput.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                searchInput.value = '';
                filterIcons('');
            }}
        }});
        
        // Initialize
        initTheme();
        initDensity();
        updateCount();
    </script>
</body>
</html>
'''
    
    # Write output
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated {output_html}")
    print(f"📊 Total icons: {total}")
    print(f"🌐 Open in browser to search and copy codepoints!")

if __name__ == '__main__':
    # Font URL from Microsoft's Fluent UI System Icons repository
    FONT_URL = "https://github.com/microsoft/fluentui-system-icons/raw/main/fonts/FluentSystemIcons-Regular.ttf"
    FONT_PATH = "FluentSystemIcons-Regular.ttf"
    
    # Download the latest font if it doesn't exist or force update
    if not os.path.exists(FONT_PATH) or '--update' in sys.argv:
        try:
            download_font(FONT_URL, FONT_PATH)
        except Exception as e:
            print(f"⚠️  Failed to download font: {e}")
            if not os.path.exists(FONT_PATH):
                print("❌ No local font file found. Please download manually.")
                sys.exit(1)
            print("📦 Using existing local font file...")
    else:
        print(f"📦 Using existing font: {FONT_PATH}")
        print("💡 Run with --update flag to download the latest version")
    
    generate_cheatsheet(FONT_PATH)