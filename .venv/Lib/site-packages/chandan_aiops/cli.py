#!/usr/bin/env python3
"""
Chandan AIOps CLI - AI/ML Project Generator
Version: 1.3.0
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import Optional, List

class AIOpsGenerator:
    """Main AIOps project generator class"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.package_dir = Path(__file__).parent
        self.template_dir = self.package_dir / "templates" / "aiops_project"
        
    def validate_template(self) -> bool:
        """Validate that template files exist"""
        if not self.template_dir.exists():
            print(f"ERROR: Template directory not found: {self.template_dir}")
            return False
        
        # Check for essential files
        essential_files = [
            'src/__init__.py',
            'config.py',
            'main.py',
            'pyproject.toml',
            'README.md'
        ]
        
        missing_files = []
        for file in essential_files:
            if not (self.template_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"ERROR: Missing essential template files:")
            for file in missing_files:
                print(f"  - {file}")
            return False
        
        return True
    
    def create_project(self, project_name: str, output_dir: Optional[Path] = None) -> bool:
        """Create a new AIOps project"""
        
        # Validate project name
        if not self._validate_project_name(project_name):
            return False
        
        # Set output directory
        if output_dir:
            project_path = output_dir / project_name
        else:
            project_path = Path.cwd() / project_name
        
        # Check if project already exists
        if project_path.exists():
            print(f"ERROR: Directory '{project_name}' already exists!")
            return False
        
        # Validate template
        if not self.validate_template():
            print("Please check if template files are properly installed.")
            return False
        
        try:
            # Create project directory
            project_path.mkdir(parents=True)
            
            if self.verbose:
                print(f"Creating project: {project_name}")
                print(f"Location: {project_path}")
            
            # Copy all template files and directories
            self._copy_templates(project_path)
            
            # Display success message
            self._display_success(project_path, project_name)
            
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to create project: {str(e)}")
            # Cleanup on failure
            if project_path.exists():
                shutil.rmtree(project_path)
            return False
    
    def _validate_project_name(self, name: str) -> bool:
        """Validate project name"""
        if not name or not name.strip():
            print("ERROR: Project name cannot be empty")
            return False
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in name:
                print(f"ERROR: Project name contains invalid character: '{char}'")
                return False
        
        return True
    
    def _copy_templates(self, destination: Path):
        """Copy template files to destination"""
        for item in self.template_dir.iterdir():
            dest_item = destination / item.name
            
            if item.is_dir():
                shutil.copytree(item, dest_item)
                if self.verbose:
                    print(f"  Created directory: {item.name}/")
            else:
                shutil.copy2(item, dest_item)
                if self.verbose:
                    print(f"  Created file: {item.name}")
    
    def _display_success(self, project_path: Path, project_name: str):
        """Display success message and project structure"""
        print(f"\nSUCCESS: Project '{project_name}' created successfully!")
        print(f"Location: {project_path}")
        
        print("\nProject Structure:")
        print(f"{project_name}/")
        self._print_tree(project_path, prefix="  ")
        
        print("\nNext Steps:")
        print(f"  1. cd {project_name}")
        print(f"  2. python -m venv venv")
        print(f"  3. For Windows: venv\\Scripts\\activate")
        print(f"     For Mac/Linux: source venv/bin/activate")
        print(f"  4. pip install -e .")
        print(f"  5. Start adding your data to data/raw/")
        print(f"  6. Edit files in src/ directory")
    
    def _print_tree(self, path: Path, prefix: str = ""):
        """Print directory tree structure"""
        items = sorted(path.iterdir())
        
        for i, item in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            
            if item.is_dir():
                print(f"{prefix}{connector}{item.name}/")
                next_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                self._print_tree(item, next_prefix)
            else:
                print(f"{prefix}{connector}{item.name}")

def validate_command():
    """Validate existing project structure"""
    parser = argparse.ArgumentParser(description="Validate AIOps project structure")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to validate")
    args = parser.parse_args()
    
    project_path = Path(args.directory)
    
    required_dirs = [
        'data/raw',
        'src',
        'app',
        'models',
        'tests'
    ]
    
    required_files = [
        'src/data_ingestion.py',
        'src/model_builder.py',
        'config.py',
        'main.py',
        'pyproject.toml'
    ]
    
    print(f"Validating project structure: {project_path}")
    
    issues = []
    
    for dir_path in required_dirs:
        if (project_path / dir_path).exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/")
            issues.append(f"Missing directory: {dir_path}")
    
    for file_path in required_files:
        if (project_path / file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path}")
            issues.append(f"Missing file: {file_path}")
    
    if issues:
        print(f"\nFound {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\nAll checks passed! Project structure is valid.")
        return True

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Chandan AIOps - Create AI/ML project structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aiops-create my-project          # Create new project
  aiops-create my-project --verbose  # Create with verbose output
  aiops-create validate            # Validate current directory
  aiops-create validate ./project  # Validate specific directory
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("project_name", help="Name of the project to create")
    create_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    create_parser.add_argument("--output", "-o", help="Output directory (default: current directory)")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate project structure")
    validate_parser.add_argument("directory", nargs="?", default=".", help="Directory to validate")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show package version")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "create":
        output_dir = Path(args.output) if args.output else None
        generator = AIOpsGenerator(verbose=args.verbose)
        success = generator.create_project(args.project_name, output_dir)
        sys.exit(0 if success else 1)
    
    elif args.command == "validate":
        success = validate_command()
        sys.exit(0 if success else 1)
    
    elif args.command == "version":
        from chandan_aiops import __version__
        print(f"chandan-aiops version {__version__}")

if __name__ == "__main__":
    main()