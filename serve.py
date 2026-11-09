#!/usr/bin/env python3
# 本地打开页面，并在按下「保存」时把学习记录写入 data/store.json。
# 用法：python3 serve.py
# 然后打开 http://127.0.0.1:8000/
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORE = ROOT / 'data' / 'store.json'
MAX_BODY = 1_000_000


def clean_chars(value):
    if not isinstance(value, list):
        return []
    out = []
    for item in value:
        if not isinstance(item, str):
            continue
        text = item.strip()
        if not text or len(text) > 8 or text in out:
            continue
        out.append(text)
        if len(out) >= 80:
            break
    return out


def clean_text(value, limit):
    if not isinstance(value, str):
        return ''
    return value[:limit]


def clean_store(data):
    if not isinstance(data, dict):
        raise ValueError('not an object')
    translations = []
    raw_items = data.get('translations')
    if isinstance(raw_items, list):
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            zh = clean_text(item.get('zh'), 4000).strip()
            ko = clean_text(item.get('ko'), 4000).strip()
            if not zh or not ko:
                continue
            translations.append({
                'id': clean_text(item.get('id'), 40) or 't',
                'zh': zh,
                'ko': ko,
                'rom': clean_text(item.get('rom'), 4000),
                'ipa': clean_text(item.get('ipa'), 4000),
                'memo': clean_text(item.get('memo'), 500),
                'at': int(item.get('at') or 0),
            })
            if len(translations) >= 40:
                break
    stats = data.get('stats') if isinstance(data.get('stats'), dict) else {}
    correct = int(stats.get('correct') or 0)
    total = int(stats.get('total') or 0)
    if correct < 0:
        correct = 0
    if total < 0:
        total = 0
    if correct > total:
        correct = total
    updated = int(data.get('updatedAt') or 0)
    if updated < 0:
        updated = 0
    return {
        'updatedAt': updated,
        'learned': clean_chars(data.get('learned')),
        'reviewLetters': clean_chars(data.get('reviewLetters')),
        'reviewSyllables': clean_chars(data.get('reviewSyllables')),
        'translations': translations,
        'stats': {'correct': correct, 'total': total},
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        path = self.path.split('?', 1)[0]
        if path == '/data/store.json' or path == '/api/store':
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        if self.path.split('?', 1)[0] != '/api/store':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0') or 0)
        except ValueError:
            self.send_error(400)
            return
        if length <= 0 or length > MAX_BODY:
            self.send_error(413)
            return
        raw = self.rfile.read(length)
        try:
            payload = clean_store(json.loads(raw.decode('utf-8')))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self.send_error(400)
            return
        STORE.parent.mkdir(parents=True, exist_ok=True)
        tmp = STORE.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        tmp.replace(STORE)
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    httpd = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('http://127.0.0.1:%d/' % port, flush=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
