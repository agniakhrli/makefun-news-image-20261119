#!/usr/bin/env python3
import os
import shutil
import sys

def main():
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(output_dir, exist_ok=True)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, 'entry.png')
    dst_path = os.path.join(output_dir, 'entry.png')
    
    shutil.copyfile(src_path, dst_path)
    print(f"Copied entry.png to {dst_path}")

if __name__ == '__main__':
    main()
