#!/usr/bin/env python3

import asyncio
import sys
import re
import os
import html
import shutil
from datetime import datetime
from playwright.async_api import async_playwright
import requests

# ========== RICH LIBRARY ==========
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich import box
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    os.system("pip3 install rich --break-system-packages 2>/dev/null || pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich import box
    from rich.text import Text
    RICH_AVAILABLE = True

console = Console()

# ============================================================
# FULL SCREEN ADAPTIVE FUNCTIONS
# ============================================================
def get_terminal_size():
    try:
        cols, rows = shutil.get_terminal_size()
        return cols, rows
    except:
        return 80, 24

def get_terminal_width():
    cols, _ = get_terminal_size()
    return max(40, cols)

def get_terminal_height():
    _, rows = get_terminal_size()
    return max(10, rows)

def get_panel_width():
    w = get_terminal_width()
    return max(40, w - 2)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ============================================================
# TELEGRAM CONFIGURATION
# ============================================================
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# ============================================================
# BANNER
# ============================================================
BANNER = """
[bold magenta] ███▄ ▄███▓ ▄▄▄       ██▓███    ██████      ██████  ▄████▄  
▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒▒██    ▒    ▒██    ▒ ▒██▀ ▀█  
▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒░ ▓██▄      ░ ▓██▄   ▒▓█    ▄ 
▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒  ▒   ██▒     ▒   ██▒▒▓▓▄ ▄██▒
▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░▒██████▒▒   ▒██████▒▒▒ ▓███▀ ░
░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░
░  ░      ░  ▒   ▒▒ ░░▒ ░     ░ ░▒  ░ ░   ░ ░▒  ░ ░  ░  ▒   
░      ░     ░   ▒   ░░       ░  ░  ░     ░  ░  ░  ░        
       ░         ░  ░               ░           ░  ░ ░      
                                                   ░         [/]
"""

# ============================================================
# HTML CYBERPUNK 3D TEMPLATE
# ============================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeonScrape 3D • {search_query}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0f;
            color: #e0e0ff;
            min-height: 100vh;
            overflow-x: hidden;
            cursor: default;
        }}

        .cyber-grid {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: 
                linear-gradient(rgba(10, 10, 15, 0.97), rgba(10, 10, 15, 0.97)),
                repeating-linear-gradient(0deg, transparent, transparent 49px, rgba(0, 255, 255, 0.02) 49px, rgba(0, 255, 255, 0.02) 50px),
                repeating-linear-gradient(90deg, transparent, transparent 49px, rgba(0, 255, 255, 0.02) 49px, rgba(0, 255, 255, 0.02) 50px);
            perspective: 800px;
        }}

        .cyber-grid::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotateX(45deg);
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at center, rgba(0, 255, 255, 0.02) 0%, transparent 70%);
            animation: gridPulse 8s ease-in-out infinite;
        }}

        @keyframes gridPulse {{
            0%, 100% {{ opacity: 0.5; transform: translate(-50%, -50%) rotateX(45deg) scale(1); }}
            50% {{ opacity: 1; transform: translate(-50%, -50%) rotateX(45deg) scale(1.1); }}
        }}

        .neon-orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
        }}

        .neon-orb.cyan {{
            width: 500px;
            height: 500px;
            background: rgba(0, 255, 255, 0.04);
            top: -10%;
            right: -10%;
            animation: orbDrift 20s ease-in-out infinite;
        }}

        .neon-orb.pink {{
            width: 400px;
            height: 400px;
            background: rgba(255, 0, 200, 0.04);
            bottom: -10%;
            left: -10%;
            animation: orbDrift 25s ease-in-out infinite reverse;
        }}

        .neon-orb.purple {{
            width: 300px;
            height: 300px;
            background: rgba(150, 0, 255, 0.05);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: orbPulse 10s ease-in-out infinite;
        }}

        @keyframes orbDrift {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            25% {{ transform: translate(50px, -30px) scale(1.1); }}
            50% {{ transform: translate(-20px, 40px) scale(0.9); }}
            75% {{ transform: translate(30px, 20px) scale(1.05); }}
        }}

        @keyframes orbPulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.5; }}
            50% {{ transform: translate(-50%, -50%) scale(1.5); opacity: 1; }}
        }}

        .container {{
            max-width: 1400px;
            margin: 30px auto;
            padding: 40px;
            position: relative;
            z-index: 1;
            background: rgba(10, 10, 20, 0.85);
            border: 1px solid rgba(0, 255, 255, 0.15);
            border-radius: 20px;
            backdrop-filter: blur(20px);
            box-shadow: 
                0 0 40px rgba(0, 255, 255, 0.05),
                inset 0 0 60px rgba(0, 255, 255, 0.02),
                0 20px 60px rgba(0, 0, 0, 0.5);
            transition: all 0.5s ease;
        }}

        .container::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 22px;
            background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), transparent, rgba(255, 0, 200, 0.1), transparent);
            z-index: -1;
            animation: borderGlow 4s ease-in-out infinite;
        }}

        @keyframes borderGlow {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 1; }}
        }}

        .content-grid {{
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 30px;
            align-items: start;
        }}

        .model-box {{
            position: sticky;
            top: 30px;
            background: rgba(0, 255, 255, 0.02);
            border: 2px solid rgba(0, 255, 255, 0.15);
            border-radius: 16px;
            padding: 15px;
            box-shadow: 
                0 0 40px rgba(0, 255, 255, 0.03),
                inset 0 0 60px rgba(0, 255, 255, 0.02);
            transition: all 0.4s ease;
            overflow: hidden;
        }}

        .model-box::before {{
            content: '';
            position: absolute;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), transparent 50%, rgba(255, 0, 200, 0.2));
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
            opacity: 0.5;
        }}

        .model-box:hover {{
            border-color: rgba(0, 255, 255, 0.3);
            box-shadow: 0 0 60px rgba(0, 255, 255, 0.08);
            transform: translateY(-2px);
        }}

        .model-box .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 10px 15px 10px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.05);
        }}

        .model-box .model-title {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: rgba(0, 255, 255, 0.3);
            font-weight: 400;
        }}

        .model-box .model-title span {{
            color: rgba(0, 255, 255, 0.6);
        }}

        .model-box .model-counter {{
            font-size: 9px;
            color: rgba(0, 255, 255, 0.15);
            letter-spacing: 1px;
        }}

        .model-box .model-counter strong {{
            color: rgba(0, 255, 255, 0.4);
        }}

        #three-canvas {{
            width: 100%;
            height: 300px;
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.3);
            cursor: grab;
            position: relative;
            overflow: hidden;
        }}

        #three-canvas:active {{
            cursor: grabbing;
        }}

        .model-controls {{
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 12px 10px 5px 10px;
            flex-wrap: wrap;
        }}

        .model-controls .btn-3d {{
            padding: 5px 14px;
            border: 1px solid rgba(0, 255, 255, 0.08);
            border-radius: 20px;
            background: rgba(0, 255, 255, 0.02);
            color: rgba(0, 255, 255, 0.3);
            font-size: 8px;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
        }}

        .model-controls .btn-3d:hover {{
            background: rgba(0, 255, 255, 0.05);
            border-color: rgba(0, 255, 255, 0.2);
            color: rgba(0, 255, 255, 0.6);
            transform: translateY(-1px);
        }}

        .model-controls .btn-3d.active {{
            background: rgba(0, 255, 255, 0.1);
            border-color: rgba(0, 255, 255, 0.3);
            color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.05);
        }}

        .model-controls .btn-3d .icon {{
            margin-right: 4px;
        }}

        .right-content {{
            min-width: 0;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }}

        .glitch-title {{
            font-size: 42px;
            font-weight: 900;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: #00ffff;
            text-shadow: 
                0 0 10px rgba(0, 255, 255, 0.3),
                0 0 40px rgba(0, 255, 255, 0.1);
            position: relative;
            display: inline-block;
            animation: glitchText 3s ease-in-out infinite;
        }}

        .glitch-title::before,
        .glitch-title::after {{
            content: 'NEONSCRAPE';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.8;
        }}

        .glitch-title::before {{
            color: #ff00cc;
            animation: glitch1 2s infinite;
            clip-path: inset(20% 0 60% 0);
        }}

        .glitch-title::after {{
            color: #00ffaa;
            animation: glitch2 2.5s infinite;
            clip-path: inset(60% 0 20% 0);
        }}

        @keyframes glitch1 {{
            0%, 100% {{ transform: translate(0); }}
            20% {{ transform: translate(-2px, 2px); }}
            40% {{ transform: translate(2px, -2px); }}
            60% {{ transform: translate(-1px, -1px); }}
            80% {{ transform: translate(1px, 1px); }}
        }}

        @keyframes glitch2 {{
            0%, 100% {{ transform: translate(0); }}
            30% {{ transform: translate(2px, -2px); }}
            50% {{ transform: translate(-2px, 2px); }}
            70% {{ transform: translate(1px, -1px); }}
            90% {{ transform: translate(-1px, 1px); }}
        }}

        .search-query {{
            font-size: 16px;
            color: #88ddff;
            margin-top: 8px;
            letter-spacing: 6px;
            text-transform: uppercase;
            opacity: 0.7;
        }}

        .search-query strong {{
            color: #00ffff;
            opacity: 1;
        }}

        .hud-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 30px;
        }}

        .hud-item {{
            background: rgba(0, 255, 255, 0.03);
            border: 1px solid rgba(0, 255, 255, 0.08);
            border-radius: 12px;
            padding: 15px 20px;
            text-align: center;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }}

        .hud-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), transparent 50%);
            opacity: 0;
            transition: opacity 0.4s ease;
        }}

        .hud-item:hover {{
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(0, 255, 255, 0.3);
            box-shadow: 0 10px 40px rgba(0, 255, 255, 0.05);
        }}

        .hud-item:hover::before {{
            opacity: 1;
        }}

        .hud-value {{
            font-size: 32px;
            font-weight: 900;
            background: linear-gradient(135deg, #00ffff, #00ffaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Courier New', monospace;
            letter-spacing: 2px;
            display: block;
            position: relative;
            z-index: 1;
        }}

        .hud-label {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: rgba(0, 255, 255, 0.5);
            display: block;
            margin-top: 4px;
            position: relative;
            z-index: 1;
        }}

        .hud-item .hud-icon {{
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 24px;
            opacity: 0.08;
        }}

        .table-wrap {{
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 255, 0.05);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            font-family: 'Courier New', monospace;
        }}

        thead {{
            background: rgba(0, 255, 255, 0.03);
        }}

        th {{
            padding: 14px 16px;
            text-align: left;
            text-transform: uppercase;
            font-size: 9px;
            letter-spacing: 3px;
            color: rgba(0, 255, 255, 0.5);
            border-bottom: 1px solid rgba(0, 255, 255, 0.1);
            font-weight: 400;
            position: sticky;
            top: 0;
            background: rgba(10, 10, 20, 0.95);
            backdrop-filter: blur(10px);
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.03);
            vertical-align: middle;
            transition: all 0.3s ease;
        }}

        tr {{
            transition: all 0.3s ease;
        }}

        tr:hover {{
            background: rgba(0, 255, 255, 0.03);
            box-shadow: inset 0 0 30px rgba(0, 255, 255, 0.02);
        }}

        tr:nth-child(even) {{
            background: rgba(0, 255, 255, 0.01);
        }}

        .rank {{
            font-weight: 900;
            color: rgba(0, 255, 255, 0.2);
            font-size: 14px;
            text-align: center;
        }}

        .place-name {{
            color: #88ddff;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            display: inline-block;
        }}

        .place-name::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1px;
            background: #00ffff;
            box-shadow: 0 0 20px #00ffff;
            transition: width 0.3s ease;
        }}

        .place-name:hover {{
            color: #00ffff;
            text-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
        }}

        .place-name:hover::after {{
            width: 100%;
        }}

        .rating {{
            color: #00ffaa;
            font-weight: 700;
            display: inline-block;
            font-size: 14px;
            text-shadow: 0 0 20px rgba(0, 255, 170, 0.1);
        }}

        .rating-stars {{
            display: inline-block;
            margin-left: 4px;
            font-size: 10px;
            color: rgba(0, 255, 170, 0.2);
        }}

        .phone {{
            color: rgba(136, 221, 255, 0.6);
            font-family: 'Courier New', monospace;
            font-size: 11px;
            transition: all 0.3s ease;
            letter-spacing: 1px;
        }}

        .phone:hover {{
            color: #88ddff;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
        }}

        .address {{
            color: rgba(136, 221, 255, 0.3);
            font-size: 10px;
            letter-spacing: 0.5px;
        }}

        .btn-neon {{
            display: inline-block;
            padding: 5px 14px;
            border: 1px solid rgba(0, 255, 255, 0.15);
            border-radius: 20px;
            font-size: 8px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: rgba(0, 255, 255, 0.5);
            text-decoration: none;
            transition: all 0.4s ease;
            background: transparent;
            font-family: 'Courier New', monospace;
        }}

        .btn-neon:hover {{
            background: rgba(0, 255, 255, 0.1);
            color: #00ffff;
            border-color: rgba(0, 255, 255, 0.4);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.05);
            transform: translateX(3px);
        }}

        .footer {{
            text-align: center;
            margin-top: 35px;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 255, 255, 0.05);
            font-size: 9px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: rgba(0, 255, 255, 0.12);
            font-family: 'Courier New', monospace;
        }}

        .footer span {{
            color: rgba(0, 255, 255, 0.05);
        }}

        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(10, 10, 20, 0.5);
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(0, 255, 255, 0.15);
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(0, 255, 255, 0.3);
        }}

        @media (max-width: 1024px) {{
            .content-grid {{
                grid-template-columns: 1fr;
                gap: 25px;
            }}
            .model-box {{
                position: relative;
                top: 0;
            }}
            #three-canvas {{
                height: 250px;
            }}
        }}

        @media (max-width: 768px) {{
            .container {{ padding: 20px; margin: 15px; }}
            .glitch-title {{ font-size: 28px; }}
            .glitch-title::before,
            .glitch-title::after {{ content: 'NEONSCRAPE'; font-size: 28px; }}
            .search-query {{ font-size: 13px; letter-spacing: 3px; }}
            .hud-value {{ font-size: 26px; }}
            .hud-stats {{ grid-template-columns: 1fr 1fr; }}
            th, td {{ padding: 10px 12px; font-size: 10px; }}
            .rating {{ font-size: 12px; }}
            #three-canvas {{ height: 200px; }}
            .model-box {{ padding: 10px; }}
        }}

        @media (max-width: 480px) {{
            .hud-stats {{ grid-template-columns: 1fr; }}
            .glitch-title {{ font-size: 20px; }}
            .glitch-title::before,
            .glitch-title::after {{ font-size: 20px; }}
            .container {{ padding: 15px; margin: 10px; }}
            #three-canvas {{ height: 180px; }}
            .model-controls .btn-3d {{ font-size: 7px; padding: 4px 10px; }}
        }}
    </style>
</head>
<body>

    <div class="cyber-grid"></div>
    <div class="neon-orb cyan"></div>
    <div class="neon-orb pink"></div>
    <div class="neon-orb purple"></div>

    <div class="container">

        <div class="content-grid">

            <div class="model-box">
                <div class="model-header">
                    <div class="model-title">⚡ <span>3D</span> MODEL</div>
                    <div class="model-counter"><strong id="modelIndexDisplay">1</strong> / <span id="modelTotalDisplay">5</span></div>
                </div>

                <div id="three-canvas"></div>

                <div class="model-controls">
                    <button class="btn-3d active" data-index="0">
                        <span class="icon">◈</span> Icosa
                    </button>
                    <button class="btn-3d" data-index="1">
                        <span class="icon">✦</span> Knot
                    </button>
                    <button class="btn-3d" data-index="2">
                        <span class="icon">◎</span> Rings
                    </button>
                    <button class="btn-3d" data-index="3">
                        <span class="icon">✧</span> Star
                    </button>
                    <button class="btn-3d" data-index="4">
                        <span class="icon">🧬</span> DNA
                    </button>
                </div>
            </div>

            <div class="right-content">

                <div class="header">
                    <div class="glitch-title">NEONSCRAPE</div>
                    <div class="search-query">▸ <strong>{search_query}</strong> ◂</div>
                </div>

                <div class="hud-stats">
                    <div class="hud-item">
                        <span class="hud-value">{total_data}</span>
                        <span class="hud-label">📍 Locations</span>
                        <span class="hud-icon">▣</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-value">{scan_time}</span>
                        <span class="hud-label">⏱ Scanned</span>
                        <span class="hud-icon">◈</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-value">⭐ {elite_count}</span>
                        <span class="hud-label">Elite Rated</span>
                        <span class="hud-icon">✦</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-value">{contact_count}</span>
                        <span class="hud-label">📞 Contacts</span>
                        <span class="hud-icon">⌨</span>
                    </div>
                </div>

                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>NAME</th>
                                <th>RATING</th>
                                <th>CONTACT</th>
                                <th>ADDRESS</th>
                                <th>MAP</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                </div>

                <div class="footer">
                    ⚡ <span>//</span> SCRAPER <span>//</span> {timestamp} <span>//</span> 3D MODEL
                </div>

            </div>

        </div>

    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js">
    </script>
    <script>
        const container3D = document.getElementById('three-canvas');
        const rect = container3D.getBoundingClientRect();

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a14);

        const camera = new THREE.PerspectiveCamera(40, rect.width / rect.height, 0.1, 100);
        camera.position.z = 5;

        const renderer = new THREE.WebGLRenderer({{
            alpha: false,
            antialias: true,
        }});
        renderer.setSize(rect.width, rect.height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container3D.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0x004466, 0.6);
        scene.add(ambientLight);

        const light1 = new THREE.PointLight(0x00ffff, 1.2, 20);
        light1.position.set(5, 5, 5);
        scene.add(light1);

        const light2 = new THREE.PointLight(0xff00cc, 0.8, 20);
        light2.position.set(-5, -3, 5);
        scene.add(light2);

        const light3 = new THREE.PointLight(0x00ffaa, 0.6, 20);
        light3.position.set(0, -5, -5);
        scene.add(light3);

        const glowRing = new THREE.Mesh(
            new THREE.RingGeometry(2.5, 3, 64),
            new THREE.MeshBasicMaterial({{
                color: 0x00ffff,
                transparent: true,
                opacity: 0.03,
                side: THREE.DoubleSide,
            }})
        );
        glowRing.rotation.x = Math.PI / 3;
        scene.add(glowRing);

        const glowRing2 = new THREE.Mesh(
            new THREE.RingGeometry(2.0, 2.5, 64),
            new THREE.MeshBasicMaterial({{
                color: 0xff00cc,
                transparent: true,
                opacity: 0.02,
                side: THREE.DoubleSide,
            }})
        );
        glowRing2.rotation.x = -Math.PI / 4;
        glowRing2.rotation.y = 0.5;
        scene.add(glowRing2);

        const modelTypes = [
            () => {{
                const group = new THREE.Group();
                const geo = new THREE.IcosahedronGeometry(1.2, 1);
                const mat = new THREE.MeshPhongMaterial({{
                    color: 0x00ffff,
                    wireframe: true,
                    emissive: 0x004466,
                    emissiveIntensity: 0.4,
                    shininess: 100,
                }});
                const mesh = new THREE.Mesh(geo, mat);
                group.add(mesh);

                const inner = new THREE.Mesh(
                    new THREE.SphereGeometry(0.5, 32, 32),
                    new THREE.MeshBasicMaterial({{
                        color: 0x00ffff,
                        transparent: true,
                        opacity: 0.08,
                    }})
                );
                group.add(inner);

                const particleCount = 60;
                const particleGeo = new THREE.BufferGeometry();
                const positions = new Float32Array(particleCount * 3);
                for (let i = 0; i < particleCount; i++) {{
                    const theta = Math.random() * Math.PI * 2;
                    const phi = Math.acos(2 * Math.random() - 1);
                    const r = 1.8 + Math.random() * 0.3;
                    positions[i * 3] = Math.sin(phi) * Math.cos(theta) * r;
                    positions[i * 3 + 1] = Math.sin(phi) * Math.sin(theta) * r;
                    positions[i * 3 + 2] = Math.cos(phi) * r;
                }}
                particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
                const particleMat = new THREE.PointsMaterial({{
                    color: 0x00ffff,
                    size: 0.02,
                    transparent: true,
                    opacity: 0.3,
                }});
                const particles = new THREE.Points(particleGeo, particleMat);
                group.add(particles);

                return group;
            }},
            () => {{
                const geo = new THREE.TorusKnotGeometry(1, 0.35, 64, 8);
                const mat = new THREE.MeshPhongMaterial({{
                    color: 0xff00cc,
                    emissive: 0x660044,
                    emissiveIntensity: 0.5,
                    shininess: 200,
                    wireframe: false,
                }});
                return new THREE.Mesh(geo, mat);
            }},
            () => {{
                const group = new THREE.Group();
                const mat1 = new THREE.MeshPhongMaterial({{
                    color: 0x00ffaa,
                    emissive: 0x006644,
                    emissiveIntensity: 0.3,
                    shininess: 150,
                    transparent: true,
                    opacity: 0.8,
                }});
                const ring1 = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.06, 16, 64), mat1);
                ring1.rotation.x = Math.PI / 2;
                group.add(ring1);

                const mat2 = new THREE.MeshPhongMaterial({{
                    color: 0x00ffff,
                    emissive: 0x004466,
                    emissiveIntensity: 0.3,
                    shininess: 150,
                    transparent: true,
                    opacity: 0.6,
                }});
                const ring2 = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.06, 16, 64), mat2);
                ring2.rotation.y = Math.PI / 2;
                group.add(ring2);

                const ring3 = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.06, 16, 64), mat2);
                ring3.rotation.z = Math.PI / 2;
                group.add(ring3);

                const center = new THREE.Mesh(
                    new THREE.SphereGeometry(0.15, 16, 16),
                    new THREE.MeshBasicMaterial({{ color: 0x00ffff }})
                );
                group.add(center);

                return group;
            }},
            () => {{
                const group = new THREE.Group();
                const mat = new THREE.MeshPhongMaterial({{
                    color: 0xff00cc,
                    emissive: 0x880066,
                    emissiveIntensity: 0.5,
                    shininess: 200,
                }});
                for (let i = 0; i < 8; i++) {{
                    const angle = (i / 8) * Math.PI * 2;
                    const spike = new THREE.Mesh(
                        new THREE.ConeGeometry(0.06, 1.6, 8),
                        mat
                    );
                    spike.position.set(Math.cos(angle) * 0.9, Math.sin(angle) * 0.9, 0);
                    spike.rotation.z = angle;
                    spike.rotation.x = 0.3;
                    group.add(spike);

                    const spike2 = new THREE.Mesh(
                        new THREE.ConeGeometry(0.06, 1.6, 8),
                        mat
                    );
                    spike2.position.set(Math.cos(angle + Math.PI) * 0.9, Math.sin(angle + Math.PI) * 0.9, 0);
                    spike2.rotation.z = angle + Math.PI;
                    spike2.rotation.x = -0.3;
                    group.add(spike2);
                }}
                const center = new THREE.Mesh(
                    new THREE.SphereGeometry(0.2, 16, 16),
                    new THREE.MeshBasicMaterial({{ color: 0xff00cc }})
                );
                group.add(center);
                return group;
            }},
            () => {{
                const group = new THREE.Group();
                const mat1 = new THREE.MeshPhongMaterial({{
                    color: 0x00ffff,
                    emissive: 0x004466,
                    emissiveIntensity: 0.3,
                    shininess: 150,
                }});
                const mat2 = new THREE.MeshPhongMaterial({{
                    color: 0xff00cc,
                    emissive: 0x660044,
                    emissiveIntensity: 0.3,
                    shininess: 150,
                }});
                const spheres = 14;
                for (let i = 0; i < spheres; i++) {{
                    const t = i / spheres;
                    const angle = t * Math.PI * 4;
                    const radius = 1.0;
                    const y = (t - 0.5) * 2.8;

                    const sphere = new THREE.Mesh(
                        new THREE.SphereGeometry(0.1, 8, 8),
                        i % 2 === 0 ? mat1 : mat2
                    );
                    sphere.position.set(Math.cos(angle) * radius, y, Math.sin(angle) * radius);
                    group.add(sphere);

                    const sphere2 = new THREE.Mesh(
                        new THREE.SphereGeometry(0.1, 8, 8),
                        i % 2 === 0 ? mat2 : mat1
                    );
                    sphere2.position.set(Math.cos(angle + Math.PI) * radius, y, Math.sin(angle + Math.PI) * radius);
                    group.add(sphere2);

                    if (i < spheres - 1) {{
                        const rodMat = new THREE.MeshBasicMaterial({{
                            color: 0x00ffff,
                            transparent: true,
                            opacity: 0.05,
                        }});
                        const rod = new THREE.Mesh(
                            new THREE.CylinderGeometry(0.015, 0.015, 0.25, 4),
                            rodMat
                        );
                        rod.position.set(
                            (sphere.position.x + sphere2.position.x) / 2,
                            (sphere.position.y + sphere2.position.y) / 2,
                            (sphere.position.z + sphere2.position.z) / 2
                        );
                        rod.lookAt(sphere.position);
                        group.add(rod);
                    }}
                }}
                return group;
            }}
        ];

        let currentModelIndex = 0;
        let mainObject = null;

        function createModel(index) {{
            if (mainObject) {{
                scene.remove(mainObject);
                mainObject.traverse((child) => {{
                    if (child.isMesh) {{
                        child.geometry?.dispose();
                        if (Array.isArray(child.material)) {{
                            child.material.forEach(m => m.dispose());
                        }} else {{
                            child.material?.dispose();
                        }}
                    }}
                }});
                mainObject = null;
            }}
            const modelFn = modelTypes[index % modelTypes.length];
            mainObject = modelFn();
            scene.add(mainObject);

            document.getElementById('modelIndexDisplay').textContent = index + 1;
            document.getElementById('modelTotalDisplay').textContent = modelTypes.length;

            document.querySelectorAll('.model-controls .btn-3d').forEach(btn => {{
                btn.classList.toggle('active', parseInt(btn.dataset.index) === index);
            }});

            return mainObject;
        }}

        createModel(0);

        document.querySelectorAll('.model-controls .btn-3d').forEach(btn => {{
            btn.addEventListener('click', function() {{
                const index = parseInt(this.dataset.index);
                currentModelIndex = index;
                createModel(index);
            }});
        }});

        let isDragging = false;
        let previousMouseX = 0;
        let previousMouseY = 0;
        let rotX = 0.3;
        let rotY = 0.5;

        container3D.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMouseX = e.clientX;
            previousMouseY = e.clientY;
            container3D.style.cursor = 'grabbing';
        }});

        document.addEventListener('mousemove', (e) => {{
            if (!isDragging || !mainObject) return;
            const deltaX = e.clientX - previousMouseX;
            const deltaY = e.clientY - previousMouseY;
            rotY += deltaX * 0.008;
            rotX += deltaY * 0.008;
            rotX = Math.max(-1, Math.min(1, rotX));
            previousMouseX = e.clientX;
            previousMouseY = e.clientY;
        }});

        document.addEventListener('mouseup', () => {{
            isDragging = false;
            container3D.style.cursor = 'grab';
        }});

        function resizeRenderer() {{
            const rect2 = container3D.getBoundingClientRect();
            const w = rect2.width;
            const h = rect2.height;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        }}

        window.addEventListener('resize', resizeRenderer);

        let autoRotate = true;
        container3D.addEventListener('mouseenter', () => {{ autoRotate = false; }});
        container3D.addEventListener('mouseleave', () => {{ autoRotate = true; }});

        function animate() {{
            requestAnimationFrame(animate);

            if (mainObject) {{
                if (!isDragging) {{
                    if (autoRotate) {{
                        rotY += 0.005;
                    }}
                }}

                mainObject.rotation.x = rotX;
                mainObject.rotation.y = rotY;

                if (currentModelIndex === 0) {{
                    mainObject.children.forEach(child => {{
                        if (child.isPoints) {{
                            child.rotation.x += 0.003;
                            child.rotation.y += 0.005;
                        }}
                    }});
                }} else if (currentModelIndex === 2) {{
                    mainObject.children.forEach((child, i) => {{
                        if (child.isMesh && child.geometry.type === 'TorusGeometry') {{
                            child.rotation.x += 0.005 * (i % 2 === 0 ? 1 : -1);
                            child.rotation.y += 0.008;
                        }}
                    }});
                }} else if (currentModelIndex === 4) {{
                    mainObject.rotation.x = rotX + Math.sin(Date.now() * 0.0005) * 0.05;
                }}
            }}

            glowRing.rotation.z += 0.003;
            glowRing2.rotation.z -= 0.004;

            renderer.render(scene, camera);
        }}

        animate();

        document.querySelectorAll('tbody tr').forEach(row => {{
            row.addEventListener('mousemove', (e) => {{
                const rect = row.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                row.style.transform =
                    `perspective(600px) rotateX(${{-y * 3}}deg) rotateY(${{x * 3}}deg) translateZ(5px)`;
                row.style.transition = 'transform 0.15s ease';
            }});

            row.addEventListener('mouseleave', () => {{
                row.style.transform = 'perspective(600px) rotateX(0deg) rotateY(0deg) translateZ(0)';
                row.style.transition = 'transform 0.4s ease';
            }});
        }});

        document.querySelectorAll('.hud-value').forEach(el => {{
            const original = el.textContent;
            const isNumber = !isNaN(parseFloat(original)) && original.length < 10;

            if (isNumber) {{
                let current = 0;
                const target = parseInt(original);
                const duration = 800;
                const step = Math.max(1, Math.floor(target / (duration / 16)));

                const counter = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        current = target;
                        clearInterval(counter);
                    }}
                    el.textContent = current;
                }}, 16);
            }}
        }});

        document.querySelector('.glitch-title')?.addEventListener('click', function() {{
            this.style.animation = 'none';
            setTimeout(() => {{
                this.style.animation = 'glitchText 0.5s ease-in-out';
                setTimeout(() => {{
                    this.style.animation = 'glitchText 3s ease-in-out infinite';
                }}, 500);
            }}, 10);
        }});

        setTimeout(resizeRenderer, 100);
    </script>
</body>
</html>"""

# ============================================================
# GENERATE HTML FUNCTION
# ============================================================
def generate_cyberpunk_html(data_list, search_query, total_data):
    """Generate cyberpunk 3D HTML from data"""
    
    rows = ""
    for i, d in enumerate(data_list, 1):
        nama = html.escape(str(d.get('Nama', 'Not available')))
        rating = d.get('Rating', 0)
        rating_str = f"{rating:.1f}" if isinstance(rating, (int, float)) and rating > 0 else "—"
        telepon = html.escape(str(d.get('Telepon', 'Not available')))
        alamat = html.escape(str(d.get('Alamat', 'Not available')))
        link = html.escape(str(d.get('Link', '#')))
        stars = "★" if rating >= 4.0 else "✦" if rating >= 3.0 else "·"
        
        rows += f"""
                    <tr>
                        <td class="rank">#{i}</td>
                        <td><a href="{link}" target="_blank" class="place-name">{nama}</a></td>
                        <td><span class="rating">{stars} {rating_str}</span></td>
                        <td><span class="phone">{telepon}</span></td>
                        <td><span class="address">{alamat[:60]}{'...' if len(alamat) > 60 else ''}</span></td>
                        <td><a href="{link}" target="_blank" class="btn-neon">▶ MAP</a></td>
                    </tr>"""
    
    scan_time = datetime.now().strftime('%H:%M')
    timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    elite_count = sum(1 for d in data_list if d.get('Rating', 0) >= 4.5)
    contact_count = len(set(d.get('Telepon', '') for d in data_list if d.get('Telepon') and d.get('Telepon') != 'Not available'))
    
    html_content = HTML_TEMPLATE.format(
        search_query=html.escape(search_query),
        total_data=total_data,
        scan_time=scan_time,
        elite_count=elite_count,
        contact_count=contact_count,
        timestamp=timestamp,
        rows=rows
    )
    
    return html_content

# ============================================================
# SCRAPER FUNCTION
# ============================================================
async def run_scraper(search_query, url, max_data=200):
    """Scrape Google Maps → HTML Cyberpunk → Telegram"""
    
    panel_width = get_panel_width()
    
    console.print(Panel(
        f"[bold yellow]⏳ SCRAPING PROCESS STARTED...[/]\n"
        f"[dim]📌 Searching: {search_query}\n"
        f"[dim]📊 Target: {max_data} places\n"
        f"[dim]⏱️ This may take a while... please be patient[/]",
        border_style="yellow",
        width=panel_width
    ))
    
    console.print(Panel(
        f"[bold cyan]🗺️  GOOGLE MAPS → SCRAPER TOOLS[/]\n"
        f"[yellow]🔍 Searching:[/] {search_query}\n"
        f"[yellow]📊 Target:[/] {max_data} places\n"
        f"[yellow]📤 Output:[/] Telegram ",
        border_style="green",
        width=panel_width
    ))

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )

        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 720}
        )

        page = await context.new_page()

        try:
            console.print("[cyan]🌐 Opening Google Maps...[/]")
            await page.goto(url, wait_until="commit", timeout=60000)

            console.print("[cyan]⏳ Waiting for list to appear...[/]")
            await page.wait_for_selector('div[role="feed"]', timeout=30000)
            await page.wait_for_timeout(5000)

            panel_kiri = page.locator('div[role="feed"]')

            console.print("[cyan]📜 Auto-scrolling...[/]")
            with Progress(
                SpinnerColumn(spinner_name="dots12"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=30, style="magenta", complete_style="cyan"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
            ) as progress:
                scroll_task = progress.add_task("[yellow]Scrolling...", total=15)
                for i in range(15):
                    await panel_kiri.evaluate("el => el.scrollBy(0, 3000)")
                    progress.update(scroll_task, advance=1)
                    await asyncio.sleep(4.5)

            kartu = page.locator("a[href*='/maps/place/']")
            jumlah = await kartu.count()
            console.print(f"[green]✅ Total detected: {jumlah}[/]")

            console.print("[cyan]🔗 Filtering unique links...[/]")
            link_unik = []
            for i in range(jumlah):
                link = await kartu.nth(i).get_attribute("href")
                if link and link not in link_unik:
                    link_unik.append(link)

            console.print(f"[green]✅ {len(link_unik)} unique places[/]")

            console.print("[cyan]📥 Fetching details...[/]")
            daftar_data = []
            target = min(len(link_unik), max_data)

            with Progress(
                SpinnerColumn(spinner_name="dots12"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=30, style="green", complete_style="yellow"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
            ) as progress:
                scrape_task = progress.add_task("[yellow]Fetching data...", total=target)
                
                for i in range(target):
                    try:
                        maps_link = link_unik[i]
                        await page.goto(maps_link, wait_until="commit", timeout=60000)
                        await asyncio.sleep(3)

                        try:
                            nama = await page.locator("h1.DUwDvf").inner_text()
                        except:
                            nama = "Not available"
                        try:
                            alamat = await page.locator('button[data-item-id="address"]').inner_text()
                            alamat = alamat.replace("", "").strip()
                        except:
                            alamat = "Not available"
                        try:
                            telepon = await page.locator('button[data-item-id^="phone:tel:"]').inner_text()
                        except:
                            telepon = "Not available"
                        try:
                            rating = await page.locator("div.F7nice span").first.inner_text()
                            rating = float(rating.replace(",", ".")) if rating else 0.0
                        except:
                            rating = 0.0

                        daftar_data.append({
                            "Nama": nama,
                            "Rating": rating,
                            "Alamat": alamat,
                            "Telepon": telepon,
                            "Link": maps_link
                        })
                        
                        progress.update(scrape_task, advance=1)
                        
                    except Exception as e:
                        console.print(f"[red]❌ Failed at data {i+1}: {e}[/]")
                        continue

            if daftar_data:
                html_content = generate_cyberpunk_html(daftar_data, search_query, len(daftar_data))
                
                console.print("[cyan]📤 Sending to Telegram...[/]")
                success = send_to_telegram_direct(html_content, search_query, len(daftar_data))
                
                if success:
                    console.print(Panel(
                        f"[bold green]✅ DONE![/]\n"
                        f"[yellow]📊 Data:[/] {len(daftar_data)} places\n"
                        f"[yellow]📍 Search:[/] {search_query}\n"
                        f"[yellow]📤 Status:[/] Sent to Telegram\n"
                        f"[dim]💡 HTML Three.js[/]",
                        border_style="green",
                        width=panel_width
                    ))
                return daftar_data
            else:
                console.print("[red]❌ No data found![/]")
                return []

        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/]")
            return []
        finally:
            await browser.close()

# ============================================================
# SEND TO TELEGRAM
# ============================================================
def send_to_telegram_direct(html_content, search_query, total_data):
    """Send HTML to Telegram directly from memory — no file saved"""
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_query = re.sub(r'[^a-zA-Z0-9]', '_', search_query)[:20]
        filename = f"neon_{clean_query}_{timestamp}.html"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        
        files = {
            'document': (filename, html_content.encode('utf-8'), 'text/html')
        }
        
        caption = f"""
┌─────────────────────────────┐
│  🗺️  MAPS SCRAPE COMPLETE   │
├─────────────────────────────┤
│  📍 Target   : {search_query}
│  📊 Total    : {total_data} places
│  ⚡ Generate : {datetime.now().strftime('%Y-%m-%d %H:%M')}
│  🧬 Html     : Active
│  🏷️  Dev     : PURPLE TOREN
└─────────────────────────────┘
💡 Click place name to open Maps
"""
        
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': caption
        }
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            console.print("[green]✅ HTML Cyberpunk 3D sent to Telegram![/]")
        else:
            console.print(f"[red]❌ Failed to send: {response.text}[/]")
        return response.status_code == 200
        
    except Exception as e:
        console.print(f"[red]❌ Error sending: {e}[/]")
        return False

# ============================================================
# USER INPUT FUNCTION
# ============================================================
def get_user_input():
    panel_width = get_panel_width()
    
    console.print(Panel(
        "[bold yellow]📋 HOW TO GET URL[/]\n\n"
        "1. Open [cyan]Google Maps[/] in your browser\n"
        "2. Type your search (e.g., [green]'apartement'[/])\n"
        "3. Press Enter, wait for results\n"
        "4. [bold]Copy URL[/] from address bar\n"
        "5. Paste URL below\n\n"
        "[dim]📌 Example URL:[/]\n"
        "[dim]https://www.google.com/maps/search/Apartment/@-7.6794631,110.8380282,14z?authuser=0&hl=id&utm_campaign=ml-ardl&g_ep=Eg1tbF8yMDI2MDcxNF8wIJvbDyoASAJQAQ%3D%3D[/]",
        border_style="cyan",
        width=panel_width
    ))
    
    search_query = Prompt.ask(
        "[bold cyan]🔍 What are you looking for?[/]\n[dim](cafe, hotel, restaurant, apartment, etc.)[/]",
        default="apartemen"
    )
    
    console.print("\n[bold yellow]📋 Paste Google Maps URL:[/]")
    url = Prompt.ask("[cyan]URL[/]", default="https://www.google.com/maps/search/cafe+in+semarang/@-6.9311795,110.4336253,24330m/data=!3m1!1e3!4m2!2m1!6e5?entry=ttu&g_ep=EgoyMDI2MDYxMC4wIKXMDSoASAFQAw%3D%3D")
    
    if not url.startswith("https://www.google.com/maps/"):
        console.print("[red]⚠️ Invalid URL! Must be from Google Maps.[/]")
        if not Confirm.ask("Continue anyway?"):
            return get_user_input()
    
    # ====== LIMIT DEFAULT 200 WITH OPTIONS ======
    console.print("\n[bold yellow]📊 Select maximum data limit:[/]")
    console.print("[dim]1. 50 (meldium)[/]")
    console.print("[dim]2. 100 (medium)[/]")
    console.print("[dim]3. 200 (slow, but more data) [green]← DEFAULT[/green][/]")
    console.print("[dim]4. Custom (enter your own)[/]")
    
    limit_choice = Prompt.ask("[cyan]Choose 1-4[/]", default="3")
    
    if limit_choice == "1":
        max_data = 50
    elif limit_choice == "2":
        max_data = 100
    elif limit_choice == "3":
        max_data = 200
    elif limit_choice == "4":
        try:
            max_data = int(Prompt.ask("[bold cyan]📊 Enter amount (max 200)[/]", default="200"))
            if max_data > 200:
                console.print("[yellow]⚠️ Max is 200! Set to 200.[/]")
                max_data = 200
            elif max_data < 1:
                console.print("[yellow]⚠️ Minimum is 1! Set to 1.[/]")
                max_data = 1
        except:
            console.print("[yellow]⚠️ Invalid input! Set to 200.[/]")
            max_data = 200
    else:
        max_data = 200
    
    console.print(f"[green]✅ Limit set to {max_data} data[/]")
    
    return search_query, url, max_data

# ============================================================
# MAIN
# ============================================================
async def main():
    os.system('clear')
    panel_width = get_panel_width()
    term_cols, term_rows = get_terminal_size()
    
    console.print(Panel(
        f"{BANNER}\n"
        f"[bold cyan]🗺️  GOOGLE MAPS → SCRAPER TOOLS[/]\n"
        f"[dim]Version 1.0 | FINAL EDITION[/]\n"
        f"[green]Dev PURPLE TOREN[/]\n"
        f"[dim]📺 Screen: {term_cols}x{term_rows}[/]",
        border_style="bright_magenta",
        width=panel_width
    ))
    
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        console.print("[red]⚠️ Telegram configuration is empty![/]")
        console.print("[yellow]Edit the file and change TELEGRAM_TOKEN & TELEGRAM_CHAT_ID[/]")
        console.print("[dim]How to get: @BotFather to create bot, @userinfobot to get chat_id[/]")
        return
    
    search_query, url, max_data = get_user_input()
    
    console.print("\n[green]🚀 Starting...[/]\n")
    await run_scraper(search_query, url, max_data)
    
    if Confirm.ask("[yellow]🔄 Scrape again?"):
        await main()
    else:
        console.print("[cyan]👋 Goodbye![/]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Stopped by user[/]")
    except Exception as e:
        console.print(f"[red]❌ Fatal: {e}[/]")
