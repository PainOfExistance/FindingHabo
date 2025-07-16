import os
import sys


class AssetLoader:
    def __init__(self, terrain_path, sounds_path, textures_path):
        self.terrain_path = self._scan_directory(terrain_path)
        self.sounds_path = self._scan_directory(sounds_path)
        self.textures_path = self._scan_directory(textures_path)
    
    def _scan_directory(self, directory_path):
        """
        Scan a directory using os.walk and return a dictionary with all paths and filenames.
        
        Returns:
            dict: Dictionary containing:
                - 'files': dict mapping relative file paths to absolute file paths
                - 'directories': list of all directory paths found
                - 'by_extension': dict grouping files by their extensions
        """
        if not os.path.exists(directory_path):
            print(f"Warning: Directory '{directory_path}' does not exist.")
            return {
                'files': {},
                'directories': [],
                'by_extension': {}
            }
        
        result = {
            'files': {},
            'directories': [],
            'by_extension': {}
        }
        
        # Walk through the directory
        for root, dirs, files in os.walk(directory_path):
            # Add directories to the list
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                result['directories'].append(dir_path)
            
            # Add files to the dictionaries
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, directory_path)
                
                # Add to files dictionary
                result['files'][relative_path] = file_path
                
                # Group by extension
                _, ext = os.path.splitext(file_name)
                ext = ext.lower()
                if ext not in result['by_extension']:
                    result['by_extension'][ext] = []
                result['by_extension'][ext].append(file_path)
        
        return result
    
    def get_files_by_extension(self, path_dict, extension):
        """
        Get all files with a specific extension from a path dictionary.
        
        Args:
            path_dict: The path dictionary (terrain_path, sounds_path, or textures_path)
            extension: File extension to filter by (e.g., '.png', '.wav')
        
        Returns:
            list: List of file paths with the specified extension
        """
        extension = extension.lower()
        return path_dict['by_extension'].get(extension, [])
    
    def get_file_path(self, path_dict, relative_path):
        """
        Get the absolute path of a file using its relative path.
        
        Args:
            path_dict: The path dictionary (terrain_path, sounds_path, or textures_path)
            relative_path: Relative path of the file
        
        Returns:
            str: Absolute path of the file, or None if not found
        """
        return path_dict['files'].get(relative_path)
    
    def list_all_files(self, path_dict):
        """
        Get a list of all files in a path dictionary.
        
        Args:
            path_dict: The path dictionary (terrain_path, sounds_path, or textures_path)
        
        Returns:
            list: List of all file paths
        """
        return list(path_dict['files'].values())
    
    def print_summary(self):
        """Print a summary of all loaded assets."""
        print("=== Asset Loader Summary ===")
        
        print(f"\nTerrain Assets:")
        print(f"  Files: {len(self.terrain_path['files'])}")
        print(f"  Directories: {len(self.terrain_path['directories'])}")
        print(f"  Extensions: {list(self.terrain_path['by_extension'].keys())}")
        
        print(f"\nSound Assets:")
        print(f"  Files: {len(self.sounds_path['files'])}")
        print(f"  Directories: {len(self.sounds_path['directories'])}")
        print(f"  Extensions: {list(self.sounds_path['by_extension'].keys())}")
        
        print(f"\nTexture Assets:")
        print(f"  Files: {len(self.textures_path['files'])}")
        print(f"  Directories: {len(self.textures_path['directories'])}")
        print(f"  Extensions: {list(self.textures_path['by_extension'].keys())}")


# Example usage
if __name__ == "__main__":
    # Initialize the asset loader with your paths
    loader = AssetLoader(
        terrain_path="../terrain",
        sounds_path="../sounds", 
        textures_path="../textures"
    )
    
    # Print summary of loaded assets
    loader.print_summary()
    
    # Example: Get all PNG files from textures
    png_files = loader.get_files_by_extension(loader.textures_path, '.png')
    print(f"\nFound {len(png_files)} PNG files in textures")
    
    # Example: Get specific file path
    file_path = loader.get_file_path(loader.textures_path, 'some_texture.png')
    if file_path:
        print(f"Found texture at: {file_path}")
    
    # Example: List all sound files
    all_sounds = loader.list_all_files(loader.sounds_path)
    print(f"\nAll sound files: {len(all_sounds)} files found")