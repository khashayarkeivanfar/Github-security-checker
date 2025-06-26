import os
import tempfile
import shutil
import subprocess
from scanner import scan_text

def scan_github_repo(repo_url):
    findings = []
    temp_dir = tempfile.mkdtemp()

    try:
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, temp_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        results = scan_text(content)
                        for keyname, keyval, context in results:
                            findings.append({
                                'repo_url': repo_url,
                                'file': rel_path,
                                'key_type': keyname,
                                'key_value': keyval,
                                'context': context
                            })
                except Exception as e:
                    print(f"[WARN] Could not read file: {file_path}: {e}")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to clone {repo_url}")
    finally:
        shutil.rmtree(temp_dir)

    return findings