# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///

r"""Update ArcGIS Pro layer files with new Database credentials.
Processes all .lyrx files in a directory, updating their connection strings
with the provided Database username and password. Skips layers that don't
use DBMS authentication.

Interactive Usage (will prompt for input):

    uv run save_layers_my_credentials.py

Command Line Usage:

    uv run save_layers_my_credentials.py --help

    uv run save_layers_my_credentials.py --username "[username]" --password "[password]" --input-dir "[in path]" --output-dir "[out path]" 

    uv run save_layers_my_credentials.py -u "[username]" -p "[password]" -i "[in path]" -o "[out path]"  --flatten

Inputs:
    - Path with layer files. Can be local filesystem or shared folder
        (\\portal-prd\ProLayerfiles)
    - Folder to store the result .lyr files
        (%USERPROFILE%\Documents\ArcGIS\Layers)
    - Database username
    - Database password

Options:
    - --flatten: flatten output directory structure

You can use `python ...` instead of `uv run ...` or `uv run ...` if you have the dependencies
installed in current environment.

MIT License, (c) 2025 Environment Yukon, Matt Wilkie
"""

import json
import os
from pathlib import Path
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()

def normalize_path(path_str):
    """Convert any path string to proper Windows format"""
    # Handle UNC paths specially
    if path_str.startswith('\\\\'):
        return path_str
    # Otherwise convert to absolute path
    return str(Path(path_str).absolute())

def get_relative_path(file_path, base_path):
    """Get relative path that works with UNC paths"""
    try:
        # Try standard relative_to first
        return file_path.relative_to(base_path)
    except ValueError:
        # For UNC paths, manually construct relative path
        file_parts = str(file_path).split(os.sep)
        base_parts = str(base_path).split(os.sep)
        
        # Find common prefix length
        common_len = 0
        for fp, bp in zip(file_parts, base_parts):
            if fp != bp:
                break
            common_len += 1
            
        # Build relative path
        rel_parts = file_parts[common_len:]
        return Path(*rel_parts)

def check_layer_auth_mode(content):
    """Check if layer uses DBMS authentication"""
    if isinstance(content, str):
        content = json.loads(content)
        
    for layer in content.get('layerDefinitions', []):
        if 'featureTable' in layer:
            if 'dataConnection' in layer['featureTable']:
                conn = layer['featureTable']['dataConnection']
                if conn.get('type') == 'CIMStandardDataConnection':
                    # Parse connection string
                    conn_str = conn.get('workspaceConnectionString', '')
                    parts = dict(p.split('=', 1) for p in conn_str.split(';') if '=' in p)
                    
                    # Check authentication mode
                    auth_mode = parts.get('AUTHENTICATION_MODE', '')
                    if not auth_mode:
                        return False, "We only change database connections that use DBMS authentication"
                    if auth_mode == 'DBMS':
                        return True, None
                    else:
                        return False, f"Layer uses {auth_mode} authentication (not DBMS)"
                        
    return False, "We only change database connections using DBMS authentication"

def update_connection_string(content, username, password):
    """Update the connection string in the layer file content"""
    if isinstance(content, str):
        content = json.loads(content)
        
    # Find the connection string in the layer definition
    for layer in content.get('layerDefinitions', []):
        if 'featureTable' in layer:
            if 'dataConnection' in layer['featureTable']:
                conn = layer['featureTable']['dataConnection']
                if conn.get('type') == 'CIMStandardDataConnection':
                    # Parse existing connection string
                    old_conn = conn.get('workspaceConnectionString', '')
                    parts = dict(p.split('=', 1) for p in old_conn.split(';') if '=' in p)
                    
                    # Update credentials
                    parts['USER'] = username
                    parts['PASSWORD'] = password  # Note: should be encrypted in production
                    
                    # Rebuild connection string
                    conn['workspaceConnectionString'] = ';'.join(f"{k}={v}" for k, v in parts.items())
                    
    return content

def is_same_directory(dir1, dir2):
    """Check if two directories are the same, handling UNC paths"""
    try:
        # Convert both to absolute paths
        path1 = Path(dir1).resolve()
        path2 = Path(dir2).resolve()
        
        # Handle UNC paths
        str1 = str(path1).lower().replace('/', '\\')
        str2 = str(path2).lower().replace('/', '\\')
        
        # Remove trailing slashes
        str1 = str1.rstrip('\\')
        str2 = str2.rstrip('\\')
        
        return str1 == str2
    except Exception:
        # If there's any error in resolution, compare the normalized strings
        str1 = str(dir1).lower().replace('/', '\\').rstrip('\\')
        str2 = str(dir2).lower().replace('/', '\\').rstrip('\\')
        return str1 == str2

def process_layer_file(layer_file, input_dir, output_dir, username, password, flatten=False):
    """Process a single layer file"""
    try:
        layer_file = Path(layer_file)
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        # Safety check - ensure output is not in input directory
        if is_same_directory(input_dir, output_dir):
            return False, "Output directory cannot be the same as input directory"
        if output_dir in input_dir.parents:
            return False, "Output directory cannot be a parent of input directory"
        if input_dir in output_dir.parents:
            return False, "Input directory cannot be a parent of output directory"
            
        # Read the layer file
        with open(layer_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        # Check authentication mode
        is_dbms, reason = check_layer_auth_mode(content)
        if not is_dbms:
            return False, f"Skipped: {reason}"
            
        # Update connection string
        updated = update_connection_string(content, username, password)
        
        # Determine output path
        if flatten:
            # Just use filename in output dir
            output_path = output_dir / layer_file.name
        else:
            # Preserve directory structure
            rel_path = get_relative_path(layer_file, input_dir)
            output_path = output_dir / rel_path
            
        # Additional safety check - ensure we're not overwriting source
        if is_same_directory(layer_file.parent, output_path.parent):
            return False, "Cannot write to source directory"
            
        # Create parent directories
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save updated layer file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(updated, f, indent=2)
            
        return True, None
        
    except Exception as e:
        return False, str(e)

class WindowsPath(click.Path):
    """Custom path type that handles Windows paths correctly"""
    def convert(self, value, param, ctx):
        value = normalize_path(value)
        return super().convert(value, param, ctx)

@click.command(help="""Update ArcGIS Pro layer files with new Database credentials.

This script processes .lyrx files in a directory, updating their connection strings with the provided Database username and password. It will skip any layers that don't use DBMS authentication.

Run and prompt for input (ctrl-c to abort):

    uv run save_layers_my_credentials.py

Flatten output structure, prompt for missing parameters (username and password):

    uv run save_layers_my_credentials.py --flatten -i \\\\portal-prd\\ProLayerfiles -o "d:\\my-csw-layers" 

Full command Line (no prompts):

    uv run save_layers_my_credentials.py -u "username" -p "password" -i "\\\\portal-prd\\ProLayerfiles" -o "%USERPROFILE%\\Documents\\ArcGIS\\Layers"

Note: You can use `python ...` instead of `uv run ...` or `uv run ...` if you have the dependencies installed in your current environment.
""")
@click.option('--username', '-u', prompt='Database username',
              help='Database username for connection')
@click.option('--password', '-p', prompt='Database password', hide_input=True,
              help='Database password for connection')
@click.option('--input-dir', '-i', type=WindowsPath(exists=True, file_okay=False),
              prompt='Input directory containing .lyrx files',
              help='Directory containing .lyrx files to process.')
@click.option('--output-dir', '-o', type=WindowsPath(file_okay=False),
              prompt='Output directory to save processed files',
              help='Directory to save processed .lyrx files.')
@click.option('--flatten/--no-flatten', default=False,
              help='Flatten output directory structure. \
                Default: preserve input directory structure')
def main(username, password, input_dir, output_dir, flatten):
    """Update ArcGIS Pro layer files with new Database credentials.
    
    This script will:
    1. Find all .lyrx files in the input directory
    2. Skip any layers not using DBMS authentication
    3. Update database credentials in remaining layers
    4. Save to output directory, preserving structure unless --flatten is used
    """
    
    # Convert to Path objects
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Safety check - ensure output is not in input directory
    if is_same_directory(input_path, output_path):
        rprint("[red]Error: Output directory cannot be the same as input directory[/red]")
        return
    if output_path in input_path.parents:
        rprint("[red]Error: Output directory cannot be a parent of input directory[/red]")
        return
    if input_path in output_path.parents:
        rprint("[red]Error: Input directory cannot be a parent of output directory[/red]")
        return
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all .lyrx files
    try:
        layer_files = list(input_path.rglob('*.lyrx'))
    except Exception as e:
        rprint(f"[red]Error scanning input directory: {str(e)}[/red]")
        return
    
    if not layer_files:
        rprint("[yellow]No .lyrx files found in the input directory[/yellow]")
        return
    
    rprint(f"[green]Found {len(layer_files)} layer files to process[/green]")
    if flatten:
        rprint("[yellow]Output will be flattened to a single directory[/yellow]")
    else:
        rprint("[green]Preserving directory structure in output[/green]")
    
    # Process files with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing layer files...", total=len(layer_files))
        
        success_count = 0
        skipped_count = 0
        failures = []
        
        for lyr in layer_files:
            progress.update(task, description=f"Processing {lyr.name}")
            
            success, error = process_layer_file(lyr, input_dir, output_dir, username, password, flatten)
            if success:
                success_count += 1
            elif error.startswith("Skipped:"):
                skipped_count += 1
                rprint(f"[yellow]{lyr.name}: {error}[/yellow]")
            else:
                failures.append((lyr.name, error))
                
            progress.advance(task)
    
    # Report results
    rprint(f"\n[green]Successfully processed {success_count} files[/green]")
    rprint(f"[yellow]Skipped {skipped_count} non-DBMS authentication files[/yellow]")
    
    if failures:
        rprint("\n[red]Failures:[/red]")
        for file, error in failures:
            rprint(f"[red]  {file}: {error}[/red]")

if __name__ == '__main__':
    main()
