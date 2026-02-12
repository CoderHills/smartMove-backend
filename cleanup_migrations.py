#!/usr/bin/env python3
"""Remove old broken migrations and push to GitHub."""
import os
import subprocess

os.chdir('/Users/coderhillary/smartmovebackend')

# Remove old migration files
files_to_remove = [
    'migrations/versions/6a212cbfa96b_add_mpesa_fields_to_booking_model.py',
    'migrations/versions/abc123def456_change_user_role_to_varchar.py'
]

for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed: {f}")

# Run git commands
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Remove old broken migration files'], check=True)
subprocess.run(['git', 'push'], check=True)
print("Pushed to GitHub!")

