import os
import re

def load_env(env_file='.env'):
    """
    Load environment variables from a .env file
    """
    if not os.path.exists(env_file):
        print(f"Warning: {env_file} file not found!")
        return
    
    print(f"Loading environment from {env_file}...")
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Parse key-value pair
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                # Set the environment variable
                os.environ[key] = value
                print(f"Set {key}")

if __name__ == "__main__":
    # Create .env file from example if it doesn't exist
    if not os.path.exists('.env') and os.path.exists('.env-example'):
        print("Creating .env file from .env-example...")
        with open('.env-example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        print("Please edit the .env file with your actual credentials")
    
    # Load environment variables
    load_env() 