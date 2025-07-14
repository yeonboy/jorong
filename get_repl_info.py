
import os

# Repl 정보 출력
print("=== Repl 정보 ===")
print(f"사용자명: {os.environ.get('REPL_OWNER', '확인불가')}")
print(f"프로젝트명: {os.environ.get('REPL_SLUG', '확인불가')}")
print(f"Repl ID: {os.environ.get('REPL_ID', '확인불가')}")

# 임베드 URL 생성
username = os.environ.get('REPL_OWNER', '[사용자명]')
project_name = os.environ.get('REPL_SLUG', '[프로젝트명]')

embed_url = f"https://replit.com/@{username}/{project_name}?embed=true&theme=dark"
print(f"\n임베드 URL: {embed_url}")
