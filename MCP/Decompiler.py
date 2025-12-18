import subprocess
import re

def clean_output(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def decompile(bytecode):
    command = ["panoramix", "-v", "ERROR", bytecode]
    return clean_output(subprocess.run(command, capture_output=True, text=True).stdout)
