# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///

"""Update ArcGIS Pro layer files with new Oracle credentials.
Processes all .lyrx files in a directory, updating their connection strings
with the provided Oracle username and password.
"""

import json
import os
from pathlib import Path, PureWindowsPath
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

def process_layer_file(layer_file, output_dir, username, password):
    """Process a single layer file"""
    try:
        layer_file = Path(layer_file)
        output_dir = Path(output_dir)
        
        # Read the layer file
        with open(layer_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        # Update connection string
        updated = update_connection_string(content, username, password)
        
        # Create output path preserving directory structure
        rel_path = layer_file.name  # Just use filename since input might be UNC path
        output_path = output_dir / rel_path
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

@click.command()
@click.option('--username', '-u', prompt='Oracle username',
              help='Oracle database username')
@click.option('--password', '-p', prompt='Oracle password', hide_input=True,
              help='Oracle database password')
@click.option('--input-dir', '-i', type=WindowsPath(exists=True, file_okay=False),
              prompt='Input directory containing .lyrx files',
              help='Directory containing layer files to process')
@click.option('--output-dir', '-o', type=WindowsPath(file_okay=False),
              prompt='Output directory for processed files',
              help='Directory to save processed layer files')
def main(username, password, input_dir, output_dir):
    """Update ArcGIS Pro layer files with new Oracle credentials"""
    
    # Convert to Path objects
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
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
    
    # Process files with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing layer files...", total=len(layer_files))
        
        success_count = 0
        failures = []
        
        for lyr in layer_files:
            progress.update(task, description=f"Processing {lyr.name}")
            
            success, error = process_layer_file(lyr, output_dir, username, password)
            if success:
                success_count += 1
            else:
                failures.append((lyr.name, error))
                
            progress.advance(task)
    
    # Report results
    rprint(f"\n[green]Successfully processed {success_count} files[/green]")
    
    if failures:
        rprint("\n[red]Failures:[/red]")
        for file, error in failures:
            rprint(f"[red]  {file}: {error}[/red]")

if __name__ == '__main__':
    main()
