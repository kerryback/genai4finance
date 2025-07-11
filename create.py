import sys

def main():
    # Check if a name was provided as a command line argument
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <name>")
        sys.exit(1)
    
    # Get the name from command line arguments
    name = sys.argv[1]
        
    # Import subprocess module for executing terminal commands
    import subprocess
    
    dir1 = "C:\\Users\\kerry\\repos\\blog\\posts\\_template"
    dir2 = f"C:\\Users\\kerry\\repos\\blog\\posts\\{name}"
    file1 = dir1 + "\\index.qmd"
    file2 = dir2 + "\\index.qmd"
    print(file1)
    print(file2)
    
    # Execute a terminal command
    try:
        
        command1 = f"mkdir {dir2}"
        command2 = f"copy {file1} {file2}"
        result1 = subprocess.run(command1, capture_output=True, text=True, check=True)
        result2 = subprocess.run(command2, capture_output=True, text=True, check=True)
        
        # Print the output of the command
        print("Command output:")
        print(result1.stdout)
        print(result2.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
