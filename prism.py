"""
P.R.I.S.M. (Probe, Re-encode, and Isolated Stream Modifier)
-----------------------------------------------------------
A professional-grade command-line utility designed for advanced
media stream manipulation, multi-track mapping, and transcoding.

Author: Chaitanya Kumar Sathivada.
"""

import os
import shutil
import signal
import sys
import subprocess
import json
import time
import platform
import tkinter as tk
from tkinter import filedialog

# --- COLOR PALETTE ---
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[96m' 
GREEN = '\033[92m'
GRAY = '\033[90m'
BOLD = '\033[1m'
RESET = '\033[0m'

# --- CONFIGURATION MAPS ---
VIDEO_CODECS = {
    "1": ("H.264 (Most Compatible)", "libx264"),
    "2": ("H.265 (High Efficiency)", "libx265"),
    "3": ("VP9 (Google/WebM)", "libvpx-vp9"),
    "4": ("Copy (No Re-encoding - Fast!)", "copy")
}

AUDIO_CODECS = {
    "1": ("AAC (Standard)", "aac"),
    "2": ("MP3", "libmp3lame"),
    "3": ("OPUS (High Quality Audio)", "libopus"),
    "4": ("Copy (No Re-encoding)", "copy")
}

def check_dependency(name):
    """Verifies if a specific system tool is installed and available in PATH."""
    return shutil.which(name) is not None

def verify_dependencies():
    """Validates presence of core FFmpeg tools; redirects to settings if missing."""
    if not check_dependency("ffmpeg") or not check_dependency("ffprobe"):
        print(f"\n{RED}{BOLD}!!{RESET} {RED}CRITICAL: Dependencies (ffmpeg/ffprobe) not found.{RESET}")
        print(f"{GRAY}Redirecting to System Configuration...{RESET}")
        time.sleep(2)
        return False
    return True

def clear_screen():
    """Clears the console output for a cleaner UI experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def render_ui(status, path):
    """Renders the P.R.I.S.M. branded UI with adaptive subsystem metrics."""
    clear_screen()
    ff_stat = f"{GREEN}READY" if check_dependency("ffmpeg") else f"{RED}MISSING"
    fp_stat = f"{GREEN}READY" if check_dependency("ffprobe") else f"{RED}MISSING"
    
    parts = status.split(" | ")
    colored_status = f"{WHITE}{parts[0]}"
    for part in parts[1:]:
        colored_status += f"{WHITE} | {GREEN}{part}"
    
    print(f"{RED}{BOLD}")
    print(" ╔══════════════════════════════════════════════════════════════════╗")
    print(" ║                                                                  ║")
    print(" ║        ██████╗ ██████╗    ██╗   ███████╗   ███╗   ███╗           ║")
    print(" ║        ██╔══██╗██╔══██╗   ██║   ██╔════╝   ████╗ ████║           ║")
    print(" ║        ██████╔╝██████╔╝   ██║   ███████╗   ██╔████╔██║           ║")
    print(" ║        ██╔═══╝ ██╔══██╗   ██║   ╚════██║   ██║╚██╔╝██║           ║")
    print(" ║        ██║██╗  ██║  ██║██╗██╗██╗███████║██╗██║ ╚═╝ ██║           ║")
    print(" ║        ╚═╝╚═╝  ╚═╝  ╚═╝╚═╝╚═╝╚═╝╚══════╝╚═╝╚═╝     ╚═╝           ║")
    print(" ║                                                                  ║")
    print(" ║       (Probe, Re-encode, and Isolated Stream Modifier)           ║")
    print(" ║                                                                  ║")
    print(f" ║{RESET}{WHITE}            Credits: Chaitanya Kumar Sathivada                    {RED}{BOLD}║")
    print(f" ║{RESET}{WHITE}      GitHub: https://github.com/chaitanyakumar-ReDSeC            {RED}{BOLD}║")
    print(" ╚══════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    print(f"{RED}" + "="*70 + f"{RESET}")
    print(f"{GRAY} PATH:    {WHITE}{path}")
    print(f"{GRAY} MODE:    {colored_status}{RESET}")
    print(f"{GRAY} MODULES: {WHITE}ffmpeg ({ff_stat}{WHITE}) | ffprobe ({fp_stat}{WHITE})\n")

def invalid_msg():
    """Handles and notifies user of invalid menu selection inputs."""
    print(f"\n {RED}>> INVALID INPUT. PRESS ENTER TO RETURN. <<{RESET}")
    input()

def run_cmd(ps_script, check=True):
    """Executes PowerShell commands as a subprocess for Windows dependency management."""
    subprocess.run(["powershell", "-Command", ps_script], check=check)

def install_dependencies():
    """Triggers elevated PowerShell to install FFmpeg package deployment via winget."""
    print(f"\n {CYAN}>> Initializing FFmpeg Architecture Deployment...{RESET}")
    script = (
        'Start-Process powershell -Verb RunAs -Wait -ArgumentList "-ExecutionPolicy", "Bypass", "-Command", '
        '\"& { winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements; }\"'
    )
    run_cmd(script)
    os.execv(sys.executable, ['python'] + sys.argv)

def update_dependencies():
    """Updates existing FFmpeg installations to their latest upstream binaries."""
    script = 'winget upgrade --id Gyan.FFmpeg'
    run_cmd(script, check=False)
    input(f"\n {CYAN}>> Update complete. Press Enter to proceed.{RESET}")

def uninstall_dependencies():
    """Removes installed deployment dependencies from the system engine."""
    script = 'winget uninstall --id Gyan.FFmpeg; winget uninstall --id yt-dlp.FFmpeg'
    run_cmd(script, check=False)
    os.execv(sys.executable, ['python'] + sys.argv)

# --- EXTENSION & FILENAME INTERACTIVE PLUG ---

def get_target_extension(source_file):
    """Asks the user for target container preference, defaulting to the source's container if left blank."""
    source_ext = os.path.splitext(source_file)[1].lower()
    print(f" {BOLD}CONTAINER FORMAT CONFIGURATION{RESET}")
    print(f" {GRAY}Specify target container format [1] MKV  [2] MP4")
    print(f" {GRAY}Leave blank / Press Enter to preserve source structure ({source_ext.upper()})")
    
    choice = input(f"\n {CYAN}>> Choice (// to back): {RESET}").strip()
    if choice == '//':
        return "BACK"
    if choice == '1':
        return '.mkv'
    elif choice == '2':
        return '.mp4'
    else:
        return source_ext

# --- ENGINE LOGIC & UTILITIES ---

def select_file(title="Select Media Source File"):
    """Invokes headless tkinter filesystem dialogs to acquire target source."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[("All Supported Files", "*.mkv *.mp4 *.avi *.mov *.mp3 *.wav *.m4a *.srt *.ass *.vtt *.sup"), ("All Files", "*.*")]
    )
    root.destroy()
    return file_path

def get_metadata(file_path):
    """Uses ffprobe analyzer mechanics to dynamically read metadata stream tables."""
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return json.loads(result.stdout) if result.returncode == 0 else {}

def get_selection(menu_dict, title):
    """Renders structured choice sub-menus matching S.A.V.E. layouts."""
    print(f" {BOLD}{title.upper()} CONFIGURATION{RESET}")
    for key, (label, _) in menu_dict.items():
        print(f" {GRAY}├─ [{key}]{WHITE} {label}")
    print(f" {GRAY}└─ [//] Back")
    
    while True:
        choice = input(f"\n {CYAN}>> Selection: {RESET}").strip()
        if choice == '//':
            return "BACK"
        if choice in menu_dict:
            return menu_dict[choice][1]
        print(f" {RED}Invalid configuration key. Try again.{RESET}")

def print_stream_table(streams):
    """Prints a terminal tracking grid of raw stream info, parsing title segments dynamically."""
    print(f" {BOLD}{'INDEX':<7} | {'STREAM TYPE':<12} | {'CODEC':<12} | {'CURRENT TITLE LABEL (VLC DISPLAY BRACKETS)'}{RESET}")
    print(f" " + "-" * 80)
    for i, s in enumerate(streams):
        codec = s.get('codec_name', 'unknown')
        lang = s.get('tags', {}).get('language', 'und')
        title = s.get('tags', {}).get('title', 'None')
        stype = s.get('codec_type', 'unknown').upper()
        print(f" {GRAY}[{i:02d}]{WHITE}    | {stype:<12} | {codec:<12} | {title} [{GRAY}{lang}{WHITE}]")

def resolve_output_path(source_file, target_dir, default_basename, extension):
    """
    Auto-resolves absolute output destination coordinates error-free.
    Appends sequence counters dynamically if source and destination paths collide.
    """
    base_name = default_basename
    final_path = os.path.join(target_dir, f"{base_name}{extension}")
    
    if os.path.dirname(os.path.abspath(source_file)) == os.path.abspath(target_dir) or os.path.exists(final_path):
        counter = 1
        while os.path.exists(os.path.join(target_dir, f"{base_name} ({counter}){extension}")):
            counter += 1
        final_path = os.path.join(target_dir, f"{base_name} ({counter}){extension}")
        
    return final_path

# --- OPERATION ENGINES ---

def run_conversion(input_file, current_path):
    """Handles full container transcode pipelines via customizable profiles."""
    render_ui("Transcode Mode | Selecting Profiling Matrix", current_path)
    v_codec = get_selection(VIDEO_CODECS, "Video Codec")
    if v_codec == "BACK": return
    
    render_ui("Transcode Mode | Selecting Audio Pipelines", current_path)
    a_codec = get_selection(AUDIO_CODECS, "Audio Codec")
    if a_codec == "BACK": return
    
    render_ui("Transcode Mode | Configuring Container Format", current_path)
    target_ext = get_target_extension(input_file)
    if target_ext == "BACK": return

    render_ui("Transcode Mode | Finalizing Target Filename", current_path)
    src_basename = os.path.splitext(os.path.basename(input_file))[0]
    print(f" {GRAY}Leave blank/Press Enter to auto-default to source name: '{src_basename}'{RESET}")
    out_name = input(f" {CYAN}Target filename (// to back):\n >> {RESET}").strip()
    if out_name == '//': return
    if not out_name: out_name = src_basename
    
    if out_name.lower().endswith(target_ext):
        out_name = out_name[:-len(target_ext)]

    final_path = resolve_output_path(input_file, current_path, out_name, target_ext)
    cmd = ['ffmpeg', '-hide_banner', '-i', input_file, '-c:v', v_codec, '-c:a', a_codec, '-y', final_path]
    
    print(f"\n {CYAN}>> Initializing Transcoding Processing Pipeline...{RESET}\n")
    res = subprocess.run(cmd)
    status = f"{GREEN}SUCCESS" if res.returncode == 0 else f"{RED}FAILURE"
    print(f"\n {status} | Processed Track Output: {final_path}{RESET}")
    input(f"\n {GRAY}Press Enter to continue...{RESET}")

def extract_tracks(input_file, metadata, current_path):
    """Extraction Engine: Dynamic codec-based native tracking format output mapping."""
    render_ui("Extraction Engine | Parsing Matrix Table", current_path)
    streams = metadata.get('streams', [])
    print_stream_table(streams)
    
    raw_choice = input(f"\n {CYAN}Enter Stream Index (or batch comma-separated eg: 1,2) (// to back): {RESET}").strip()
    if raw_choice == '//' or not raw_choice: return

    indices = []
    try:
        for val in raw_choice.split(','):
            idx = int(val.strip())
            if 0 <= idx < len(streams):
                indices.append(idx)
            else:
                raise IndexError
    except (ValueError, IndexError):
        print(f"\n {RED}!! Error: Invalid processing indices mapped.{RESET}")
        time.sleep(1.5)
        return

    render_ui("Extraction Engine | Configuring Filename Parameters", current_path)
    src_basename = os.path.splitext(os.path.basename(input_file))[0]
    print(f" {GRAY}Leave blank/Press Enter to auto-default to source name: '{src_basename}'{RESET}")
    out_name = input(f" {CYAN}Output file name base (// to back):\n >> {RESET}").strip()
    if out_name == '//': return
    if not out_name: out_name = src_basename

    print(f"\n {CYAN}>> Dispatching Extraction Sequence Pipeline...{RESET}\n")
    for idx in indices:
        stream_type = streams[idx]['codec_type']
        codec_name = streams[idx].get('codec_name', '').lower()
        
        if codec_name in ['hdmv_pgs_subtitle', 'pgssub', 'dvdsub', 'dvd_subtitle']:
            req_ext = '.sup'
        elif codec_name == 'subrip':
            req_ext = '.srt'
        elif stream_type == 'audio':
            req_ext = f".{codec_name}" if codec_name else '.mka'
        elif stream_type == 'video':
            req_ext = f".{codec_name}" if codec_name in ['mp4', 'mkv', 'mov', 'avi'] else '.mkv'
        else:
            req_ext = '.mkv'
            
        cur_base = out_name
        if len(indices) > 1:
            cur_base = f"{cur_base} stream {idx}"
            
        final_path = resolve_output_path(input_file, current_path, cur_base, req_ext)
        cmd = ['ffmpeg', '-hide_banner', '-i', input_file, '-map', f'0:{idx}', '-c', 'copy', '-y', final_path]
        
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print(f" {GREEN}[SUCCESS]{WHITE} Stream {idx} safely isolated to raw media track: {final_path}{RESET}")
        else:
            print(f" {RED}[FAILED]{WHITE} Stream {idx} processing pipeline fault occurred.{RESET}")
            
    input(f"\n {GRAY}Batch Processing completed. Press Enter to continue...{RESET}")

def advanced_track_multiplexer(video_file, source_metadata, current_path):
    """Multi-Asset Track Multiplexer System for mapping video/audio/subtitles with customized tags and MP4 safety patches."""
    staged_assets = []  
    source_streams = source_metadata.get('streams', [])
    current_destination_index = len(source_streams)

    while True:
        render_ui("Muxing Engine | Multi-Asset Track Multiplexer", current_path)
        print(f" {BOLD}SOURCE MATRIX STATE:{RESET}")
        print(f" {GRAY}├─ Primary Target Source: {WHITE}{os.path.basename(video_file)}")
        print(f" {GRAY}└─ Base Stream Count:     {WHITE}{len(source_streams)} tracks")
        
        if staged_assets:
            print(f"\n {BOLD}STAGED EXTERNAL ATTACHMENTS PAYLOAD:{RESET}")
            for a_idx, asset in enumerate(staged_assets):
                print(f" {GRAY}├─ Asset [{a_idx}] File: {CYAN}{os.path.basename(asset['file_path'])}{RESET}")
                for t in asset['tracks']:
                    print(f" {GRAY}│  └─ Track #{t['internal_idx']} [{t['type'].upper()}] ➔ Destination Map Index: {GREEN}#{t['dest_idx']}{RESET}")
                    print(f" {GRAY}│     ├── Title:    {WHITE}{t['title']}")
                    print(f" {GRAY}│     └── Lang Code:{WHITE}{t['lang']}")
        else:
            print(f"\n {GRAY}No external assets currently queued for attachment.{RESET}")
            
        print("\n" + f" {BOLD}MULTIPLEXER OPERATIONS:{RESET}")
        print(f" {GRAY}├─ [1] Choose & Stage External File Asset (Video / Audio / Subtitle)")
        print(f" {GREEN}├─ [G] DISPATCH MULTIPLEX ENGINE PIPELINE (Mux and Write Options){RESET}")
        print(f" {GRAY}└─ [//] Cancel Operations and Revert Back")
        
        choice = input(f"\n {CYAN}>> Selection: {RESET}").strip().lower()
        if choice == '//':
            break
            
        elif choice == '1':
            render_ui("Multiplexer | Selection Interception System", current_path)
            print(f" {CYAN}>> Activating file explorer dialog... Choose track asset.{RESET}")
            asset_path = select_file(title="Select Asset Track to Merge")
            if not asset_path: continue
            
            asset_path = os.path.abspath(asset_path)
            asset_meta = get_metadata(asset_path)
            asset_streams = asset_meta.get('streams', [])
            
            if not asset_streams:
                # Handle text raw files like standalone .srt files which ffprobe handles differently or has empty stream array
                ext = os.path.splitext(asset_path)[1].lower()
                if ext in ['.srt', '.ass', '.vtt']:
                    asset_streams = [{'codec_type': 'subtitle', 'codec_name': 'subrip' if ext == '.srt' else ext[1:], 'tags': {}}]
                else:
                    print(f"\n {RED}!! Error: Target asset file contains no valid parseable media tracks.{RESET}")
                    time.sleep(2)
                    continue
                
            render_ui("Multiplexer | Inspecting Track Components", current_path)
            print(f" {BOLD}Target Asset: {WHITE}{os.path.basename(asset_path)}{RESET}\n")
            print_stream_table(asset_streams)
            
            print(f"\n {GRAY}Choose stream index from this asset file to import. Leave blank / Press Enter to import ALL streams.{RESET}")
            sel_idx_input = input(f" {CYAN}>> Asset track index input: {RESET}").strip()
            
            target_indices = []
            if not sel_idx_input:
                target_indices = list(range(len(asset_streams)))
            else:
                try:
                    t_idx = int(sel_idx_input)
                    if 0 <= t_idx < len(asset_streams):
                        target_indices.append(t_idx)
                    else:
                        raise IndexError
                except (ValueError, IndexError):
                    print(f" {RED}Invalid tracking coordinate inside asset space.{RESET}")
                    time.sleep(1.5)
                    continue
                    
            asset_staged_tracks = []
            for stream_idx in target_indices:
                s = asset_streams[stream_idx]
                stype = s.get('codec_type', 'unknown')
                default_title = s.get('tags', {}).get('title', 'None')
                default_lang = s.get('tags', {}).get('language', 'eng')
                
                render_ui(f"Staging Metadata | Asset Stream index #{stream_idx}", current_path)
                print(f" {BOLD}Configuring Metadata Segment for asset track component:{RESET}")
                print(f" {GRAY}├─ Target File:     {WHITE}{os.path.basename(asset_path)}")
                print(f" {GRAY}├─ Component Type:  {CYAN}{stype.upper()}{RESET}")
                print(f" {GRAY}└─ Current Title:   {WHITE}{default_title} [{default_lang}]\n")
                
                print(f" {GRAY}Leave blank to retain original track identity details.{RESET}")
                new_title = input(f" {CYAN}Assign custom Title for this track component:\n >> {RESET}").strip()
                if not new_title: new_title = default_title if default_title != 'None' else f"External {stype.capitalize()} Track"
                
                new_lang = input(f" {CYAN}Assign 3-letter language code framework (e.g., eng, ind, jpn):\n >> {RESET}").strip().lower()
                if not new_lang: 
                    new_lang = default_lang
                elif len(new_lang) != 3:
                    print(f" {RED}Warning: Invalid language length specification. Reverting to standard code validation [eng].{RESET}")
                    new_lang = 'eng'
                    time.sleep(1)
                    
                asset_staged_tracks.append({
                    'internal_idx': stream_idx,
                    'type': stype,
                    'title': new_title,
                    'lang': new_lang,
                    'dest_idx': current_destination_index
                })
                current_destination_index += 1
                
            staged_assets.append({
                'file_path': asset_path,
                'tracks': asset_staged_tracks
            })
            
        elif choice == 'g':
            if not staged_assets:
                print(f"\n {RED}!! Error: Staging payload array is empty. Attach tracks before dispatching.{RESET}")
                time.sleep(1.5)
                continue
                
            render_ui("Muxing Engine | Formatting Container Extension", current_path)
            target_ext = get_target_extension(video_file)
            if target_ext == "BACK": continue
            
            render_ui("Muxing Engine | Resolving Output Filename Target", current_path)
            src_basename = os.path.splitext(os.path.basename(video_file))[0]
            print(f" {GRAY}Leave blank/Press Enter to auto-default to source name: '{src_basename}'{RESET}")
            out_name = input(f"\n {CYAN}Target output filename base:\n >> {RESET}").strip()
            if not out_name: out_name = src_basename
            
            if out_name.lower().endswith(target_ext):
                out_name = out_name[:-len(target_ext)]
                
            final_path = resolve_output_path(video_file, current_path, out_name, target_ext)
            
            # Assembly command architecture
            cmd = ['ffmpeg', '-y', '-hide_banner', '-i', video_file]
            for asset in staged_assets:
                cmd.extend(['-i', asset['file_path']])
                
            # Maps base target structures
            cmd.extend(['-map', '0'])
            
            # Explicitly maps independent target assets
            for a_idx, asset in enumerate(staged_assets):
                input_file_index = a_idx + 1
                for t in asset['tracks']:
                    cmd.extend(['-map', f'{input_file_index}:{t["internal_idx"]}'])
                    
            # Set default global copy command
            cmd.extend(['-c', 'copy'])
            
            # MP4 CONTAINER SAFETY PATCH: Transcode text subtitles if destination is MP4
            if target_ext.lower() == '.mp4':
                for asset in staged_assets:
                    for t in asset['tracks']:
                        if t['type'].lower() == 'subtitle':
                            cmd.extend([f'-c:s:{t["dest_idx"] - len(source_streams)}', 'mov_text'])
            
            # Direct target index injection mapping loops to deploy metadata modifications tracking
            for asset in staged_assets:
                for t in asset['tracks']:
                    cmd.extend([f'-metadata:s:{t["dest_idx"]}', f'title={t["title"]}'])
                    cmd.extend([f'-metadata:s:{t["dest_idx"]}', f'language={t["lang"]}'])
                    
            cmd.append(final_path)
            
            print(f"\n {CYAN}>> Compiling structural streams into single multi-track target payload wrapper...{RESET}\n")
            
            # Execute and capture stdout/stderr to dynamically print the error logs if it fails
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if res.returncode == 0:
                print(f"\n {GREEN}[SUCCESS] Track architecture compilation complete! Pipeline resolved at:{RESET}")
                print(f" {WHITE}{final_path}{RESET}")
            else:
                print(f"\n {RED}[FAILURE] Multiplexer pipeline execution structural failure.{RESET}")
                print(f"\n{RED}{BOLD}FFMPEG ERROR LOG:{RESET}")
                print(f"{GRAY}{res.stderr}{RESET}")
                
            input(f"\n {GRAY}Press Enter to return to main action selector menu...{RESET}")
            break

def manage_metadata_and_renaming(input_file, metadata, current_path):
    """ADVANCED STAGING ENGINE: Batch stages titles/languages modifications for multi-track processing in 1 pass."""
    staged_global_title = None
    staged_track_titles = {}  
    staged_track_langs = {}   

    while True:
        render_ui("Metadata Suite | Advanced Staging Framework", current_path)
        streams = metadata.get('streams', [])
        format_info = metadata.get('format', {})
        global_title = format_info.get('tags', {}).get('title', 'None')
        
        print(f" {BOLD}CURRENT METADATA SUMMARY:{RESET}")
        print(f" {GRAY}├─ Active Global Title: {WHITE}{global_title}")
        if staged_global_title is not None:
            print(f" {GRAY}└─ {GREEN}[STAGED GLOBAL UPDATE]: {WHITE}{staged_global_title}")
        print(f" {GRAY}└─ File Location:       {WHITE}{input_file}\n")
        
        print(f" {BOLD}INTERNAL TRACK MATRIX & STAGED OPERATIONS:{RESET}")
        print(f" {BOLD}{'INDEX':<7} | {'STREAM TYPE':<12} | {'CODEC':<12} | {'METADATA STATUS'}{RESET}")
        print(f" " + "-" * 80)
        for i, s in enumerate(streams):
            codec = s.get('codec_name', 'unknown')
            lang = s.get('tags', {}).get('language', 'und')
            title = s.get('tags', {}).get('title', 'None')
            stype = s.get('codec_type', 'unknown').upper()
            
            state_desc = f"{title} [{lang}]"
            staged_updates = []
            if i in staged_track_titles:
                staged_updates.append(f"Title ➔ '{staged_track_titles[i]}'")
            if i in staged_track_langs:
                staged_updates.append(f"Lang ➔ '{staged_track_langs[i]}'")
                
            if staged_updates:
                update_string = f" | {GREEN}[STAGED: {', '.join(staged_updates)}]{WHITE}"
            else:
                update_string = ""
                
            print(f" {GRAY}[{i:02d}]{WHITE}    | {stype:<12} | {codec:<12} | {state_desc}{update_string}")
            
        print("\n" + f" {BOLD}STAGING SYSTEM ACTIONS: {RESET}")
        print(f" {GRAY}├─ [1] Stage Global Container Title")
        print(f" {GRAY}├─ [2] Stage Track Custom Title Naming")
        print(f" {GRAY}├─ [3] Stage Track Custom Language Code [Changes VLC Brackets]")
        print(f" {GREEN}├─ [G] DISPATCH ENGINE PIPELINE (Executes All Staged Modifications){RESET}")
        print(f" {GRAY}└─ [//] Cancel Actions and Revert Back")
        
        choice = input(f"\n {CYAN}>> Select Option: {RESET}").strip().lower()
        if choice == '//':
            break
            
        elif choice == '1':
            render_ui("Staging | Global Container Title", current_path)
            t_input = input(f" {CYAN}Enter target Global Title string (// to back):\n >> {RESET}").strip()
            if t_input == '//': continue
            staged_global_title = t_input
            
        elif choice == '2':
            render_ui("Staging | Track Title Identifier", current_path)
            print_stream_table(streams)
            idx_input = input(f"\n {CYAN}Target track index (// to back): {RESET}").strip()
            if idx_input == '//' or not idx_input: continue
            try:
                idx = int(idx_input)
                if not (0 <= idx < len(streams)): raise IndexError
            except (ValueError, IndexError):
                print(f" {RED}Invalid stream tracking boundary index.{RESET}")
                time.sleep(1.2)
                continue
            
            t_title = input(f" {CYAN}Enter custom Track Title string for index {idx} (// to back):\n >> {RESET}").strip()
            if t_title == '//': continue
            staged_track_titles[idx] = t_title

        elif choice == '3':
            render_ui("Staging | Language Code Tag [VLC Bracket Property]", current_path)
            print_stream_table(streams)
            idx_input = input(f"\n {CYAN}Target track index (// to back): {RESET}").strip()
            if idx_input == '//' or not idx_input: continue
            try:
                idx = int(idx_input)
                if not (0 <= idx < len(streams)): raise IndexError
            except (ValueError, IndexError):
                print(f" {RED}Invalid stream tracking boundary index.{RESET}")
                time.sleep(1.2)
                continue
            
            print(f" {GRAY}Must use a 3-letter language code mapping specification (e.g., eng, ind, jpn, hin, fre){RESET}")
            t_lang = input(f" {CYAN}Enter language code layout for index {idx} (// to back):\n >> {RESET}").strip().lower()
            if t_lang == '//': continue
            if len(t_lang) != 3:
                print(f" {RED}Error: Language codes must be exactly 3 characters long.{RESET}")
                time.sleep(1.5)
                continue
            staged_track_langs[idx] = t_lang

        elif choice == 'g':
            if staged_global_title is None and not staged_track_titles and not staged_track_langs:
                print(f"\n {RED}!! Error: No modification arrays staged for runtime pipeline execution.{RESET}")
                time.sleep(1.5)
                continue
                
            render_ui("Metadata Suite | Constructing Dispatch Pipeline", current_path)
            target_ext = get_target_extension(input_file)
            if target_ext == "BACK": continue
            
            src_basename = os.path.splitext(os.path.basename(input_file))[0]
            print(f" {GRAY}Leave blank/Press Enter to auto-default to source name: '{src_basename}'{RESET}")
            out_name = input(f"\n {CYAN}Final output filename base:\n >> {RESET}").strip()
            if not out_name: out_name = src_basename
            
            if out_name.lower().endswith(target_ext):
                out_name = out_name[:-len(target_ext)]
            
            final_path = resolve_output_path(input_file, current_path, out_name, target_ext)
            
            cmd = ['ffmpeg', '-y', '-i', input_file, '-map', '0', '-c', 'copy']
            
            if staged_global_title is not None:
                cmd.extend(['-metadata', f'title={staged_global_title}'])
                
            for idx, title_str in staged_track_titles.items():
                cmd.extend([f'-metadata:s:{idx}', f'title={title_str}'])
                
            for idx, lang_str in staged_track_langs.items():
                cmd.extend([f'-metadata:s:{idx}', f'language={lang_str}'])
                
            cmd.append(final_path)
            
            print(f"\n {CYAN}>> Deploying unified single-pass parallel metadata mutation pass...{RESET}\n")
            res = subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
            if res.returncode == 0:
                print(f"\n {GREEN}[SUCCESS] All transformations successfully committed to pipeline payload:{RESET}")
                print(f" {WHITE}{final_path}{RESET}")
            else:
                print(f"\n {RED}[FAILURE] Processing pipeline mapping execution failure.{RESET}")
            input(f"\n {GRAY}Press Enter to return to Main Menu...{RESET}")
            break

def remove_tracks_batch(input_file, metadata, current_path):
    """Drops arbitrary arrays of elements simultaneously in one structural cycle."""
    render_ui("Track Processing Engine | Purging Streams", current_path)
    streams = metadata.get('streams', [])
    print_stream_table(streams)

    raw_choice = input(f"\n {CYAN}Enter Stream Indices to drop (Comma-separated batching eg: 1,2) (// to back): {RESET}").strip()
    if raw_choice == '//' or not raw_choice: return

    drop_indices = []
    try:
        for val in raw_choice.split(','):
            idx = int(val.strip())
            if 0 <= idx < len(streams):
                drop_indices.append(idx)
            else:
                raise IndexError
    except (ValueError, IndexError):
        print(f"\n {RED}!! Error: Entry contains invalid operational parsing indexes.{RESET}")
        time.sleep(1.5)
        return

    render_ui("Track Processing Engine | Configuring Container Format", current_path)
    target_ext = get_target_extension(input_file)
    if target_ext == "BACK": return

    render_ui("Track Processing Engine | Configuring Filename Parameters", current_path)
    src_basename = os.path.splitext(os.path.basename(input_file))[0]
    print(f" {GRAY}Leave blank/Press Enter to auto-default to source name: '{src_basename}'{RESET}")
    out_name = input(f" {CYAN}Output container label (// to back):\n >> {RESET}").strip()
    if out_name == '//': return
    if not out_name: out_name = src_basename
    
    if out_name.lower().endswith(target_ext):
        out_name = out_name[:-len(target_ext)]

    final_path = resolve_output_path(input_file, current_path, out_name, target_ext)

    cmd = ['ffmpeg', '-hide_banner', '-i', input_file, '-map', '0', '-c', 'copy']
    for idx in drop_indices:
        cmd.extend(['-map', f'-0:{idx}'])
    cmd.extend(['-y', final_path])

    print(f"\n {CYAN}>> Executing single-pass batch stream removal optimization...{RESET}\n")
    res = subprocess.run(cmd)
    status = f"{GREEN}SUCCESS" if res.returncode == 0 else f"{RED}FAILURE"
    print(f"\n {status} | Filtered structural payload array output saved: {final_path}{RESET}")
    input(f"\n {GRAY}Press Enter to continue...{RESET}")

# --- MAIN CONTROLLER ROUTER ---

def run_prism():
    """Main application runtime control cycle loop."""
    current_path = os.path.join(os.path.expanduser("~"), "Downloads", "P.R.I.S.M")
    if not os.path.exists(current_path):
        os.makedirs(current_path, exist_ok=True)

    while True:
        render_ui("IDLE | Awaiting Target File Selection", current_path)
        print(f" {BOLD}MAIN ROUTER CONTROLLER MENU{RESET}")
        print(f" {GRAY}├─ [1] Choose Target File Source\n ├─ [2] Settings and Configurations\n └─ [E] Terminate Session")
        
        main_choice = input(f"\n {CYAN}>> Choice: {RESET}").strip().lower()
        if main_choice == 'e':
            print(f"\n {GRAY}Terminating session.{RESET}")
            break
            
        elif main_choice == '2':
            while True:
                render_ui("SETTINGS AND CONFIGURATIONS", current_path)
                print(f" {BOLD}SETTINGS FRAMEWORK MENU{RESET}")
                print(f" {GRAY}├─ [1] Change Execution Directory Path\n ├─ [2] Deploy/Reinstall Tool Dependencies\n ├─ [3] Wipe/Uninstall Binary Tools\n ├─ [4] Update Upstream Binaries\n └─ [//] Back")
                s = input(f"\n {CYAN}>> Command: {RESET}").strip().lower()
                if s == '//': break
                elif s == '1': 
                    new_route = input(f" {CYAN}>> Complete path tracing coordinate: {RESET}").strip()
                    if new_route and os.path.isdir(new_route):
                        current_path = new_route
                    break
                elif s == '2': install_dependencies()
                elif s == '3': uninstall_dependencies()
                elif s == '4': update_dependencies(); break
                else: invalid_msg()
                
        elif main_choice == '1':
            if not verify_dependencies():
                while True:
                    render_ui("DEPENDENCY ERROR ENCOUNTERED", current_path)
                    print(f" {RED}Dependencies missing. Initialize winget automatic deployment system?{RESET}")
                    print(f" {GRAY}├─ [1] Proceed with Auto-Installer\n └─ [//] Cancel and Back")
                    err_choice = input(f"\n {CYAN}>> Option: {RESET}").strip()
                    if err_choice == '1': install_dependencies()
                    elif err_choice == '//': break
                    else: invalid_msg()
                continue
                
            render_ui("File Selector System Activated", current_path)
            print(f" {CYAN}>> Waiting for input from native system file explorer dialog UI...{RESET}")
            target_file = select_file(title="Select Media Source File")
            if not target_file: continue
            
            target_file = os.path.abspath(target_file)
            
            while True:
                metadata = get_metadata(target_file)
                filename_short = os.path.basename(target_file)
                render_ui(f"File Active | Track Source: {filename_short}", current_path)
                
                print(f" {BOLD}OPERATIONAL ATTACK ACTIONS MATRIX{RESET}")
                print(f" {GRAY}├─ [1] Full Container Transcode Engine (Codecs/Format Modification)")
                print(f" {GRAY}├─ [2] Stream Extraction System (Isolate Single/Multiple Tracks)")
                print(f" {GRAY}├─ [3] Multi-Asset Track Multiplexer Engine (Add Video/Audio/Subs)")
                print(f" {GRAY}├─ [4] Metadata Inspector [Multi-Pass Staging]")
                print(f" {GRAY}├─ [5] Stream Purge System (Remove Multiple Tracks Simultaneously)")
                print(f" {GRAY}└─ [//] De-select File and Go Back")
                
                op_choice = input(f"\n {CYAN}>> Action: {RESET}").strip().lower()
                if op_choice == '//': break
                elif op_choice == '1': run_conversion(target_file, current_path)
                elif op_choice == '2': extract_tracks(target_file, metadata, current_path)
                elif op_choice == '3': advanced_track_multiplexer(target_file, metadata, current_path)
                elif op_choice == '4': manage_metadata_and_renaming(target_file, metadata, current_path)
                elif op_choice == '5': remove_tracks_batch(target_file, metadata, current_path)
                else: invalid_msg()
        else:
            invalid_msg()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    run_prism()