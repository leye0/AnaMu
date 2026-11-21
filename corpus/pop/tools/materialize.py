#!/usr/bin/env python3
"""Retrieve the acquired pop corpus from pinned sources; no musical inference.

Requires mido==1.3.3 only to export existing MIDI lyric events. Payloads are
written outside the public repository. The manifest contains quality limits.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import struct
import urllib.request
import zipfile
import zlib

import mido

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def retrieve(url, start=None, end=None):
    headers = {'Range': f'bytes={start}-{end}'} if start is not None else {}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=120) as response:
        if start is not None:
            expected = f'bytes {start}-{end}/'
            if response.status != 206 or not response.headers.get('Content-Range', '').startswith(expected):
                raise ValueError('Source did not honor the requested byte range')
        return response.read()


def embedded_lyrics(data):
    midi = mido.MidiFile(file=io.BytesIO(data))
    result = 'source_track\tabsolute_tick\ttext_json\n'
    for ti, track in enumerate(midi.tracks):
        tick = 0
        for event in track:
            tick += event.time
            if event.type == 'lyrics' and event.text.strip():
                result += f'{ti}\t{tick}\t{json.dumps(event.text, ensure_ascii=False)}\n'
    return result.encode('utf-8')


def unpack_member(span, start, spec):
    offset = spec['offset'] - start
    fields = struct.unpack('<4s5H3L2H', span[offset:offset + 30])
    if fields[0] != b'PK\x03\x04':
        raise ValueError('Invalid ZIP member header')
    payload_offset = offset + 30 + fields[-2] + fields[-1]
    data = span[payload_offset:payload_offset + spec['compressed_size']]
    if fields[3] == 8:
        data = zlib.decompress(data, -15)
    elif fields[3] != 0:
        raise ValueError('Unsupported ZIP compression')
    if len(data) != spec['size'] or (zlib.crc32(data) & 0xffffffff) != spec['crc32']:
        raise ValueError('ZIP member checksum mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    args = parser.parse_args()
    destination = args.destination.resolve()
    repo = ROOT.parents[1]
    if destination == repo or repo in destination.parents:
        parser.error('Choose a destination outside the public repository')
    destination.mkdir(parents=True, exist_ok=True)
    args.cache.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    sources = json.loads((ROOT / 'sources.json').read_text())
    member_specs = {}
    for shard in manifest['source_member_shards']:
        path = PurePosixPath(shard['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Invalid source-member shard path')
        data = (ROOT / path).read_bytes()
        if digest(data) != shard['sha256']:
            raise ValueError('Source-member shard checksum mismatch')
        member_specs.update(json.loads(gzip.decompress(data)))
    entries = []
    for shard in manifest['entry_shards']:
        path = PurePosixPath(shard['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Invalid shard path')
        data = (ROOT / path).read_bytes()
        if digest(data) != shard['sha256']:
            raise ValueError('Entry shard checksum mismatch')
        entries.extend(json.loads(gzip.decompress(data)))
    if len(entries) != manifest['summary']['distinct_song_identities_acquired']:
        raise ValueError('Entry count mismatch')
    retrieved = {}
    main_members = {n for e in entries if e['source']['source'] == 'lyrics-midi-main'
                    for n in (e['source']['midi_member'], e['source']['lyrics_member'])}
    specs = sorted((member_specs[n] for n in main_members), key=lambda v: v['offset'])
    # Batch nearby archive members to avoid downloading the 7.6 GB source ZIP.
    groups = []
    for spec in specs:
        end = spec['offset'] + spec['compressed_size'] + 30 + len(spec['name'].encode('utf-8')) + 65535
        if groups and spec['offset'] <= groups[-1][1] + 131072 and end - groups[-1][0] <= 8 * 1024 * 1024:
            groups[-1][1] = max(groups[-1][1], end)
            groups[-1][2].append(spec)
        else:
            groups.append([spec['offset'], end, [spec]])
    for start, end, group in groups:
        cache_path = args.cache / f'main-{start}-{end}.bin'
        if not cache_path.exists():
            cache_path.write_bytes(retrieve(sources['main_archive']['download_url'], start, end))
        span = cache_path.read_bytes()
        for spec in group:
            retrieved[spec['name']] = unpack_member(span, start, spec)

    clean_entries = [e for e in entries if e['source']['source'] == 'lyrics-midi-genius']
    clean = None
    lyric_rows = {}
    if clean_entries:
        cache_path = args.cache / 'genius-clean.zip'
        if not cache_path.exists():
            cache_path.write_bytes(retrieve(sources['clean_archive']['download_url']))
        if digest(cache_path.read_bytes()) != sources['clean_archive']['sha256']:
            raise ValueError('Clean source archive checksum mismatch')
        clean = zipfile.ZipFile(cache_path)
        for line in clean.read('Lyrics/genius_lyrics_cleaned_matches.jsonl').splitlines():
            row = json.loads(line)
            for name in row[1]:
                lyric_rows.setdefault('MIDIs/' + name, []).extend(row[2])

    for entry in entries:
        item_id = entry['id']
        if PurePosixPath(item_id).name != item_id or item_id in ('.', '..'):
            raise ValueError('Invalid item ID')
        source = entry['source']
        if source['source'] == 'lyrics-midi-genius':
            midi = clean.read(source['midi_member'])
            matches = [m['lyrics'].encode('utf-8') for m in lyric_rows[source['midi_member']]]
            lyrics = next((v for v in matches if digest(v) == entry['files']['lyrics.txt']['sha256']), None)
            if lyrics is None:
                raise ValueError('Published lyric pairing not found in pinned source')
        else:
            midi = retrieved[source['midi_member']]
            lyrics = retrieved[source['lyrics_member']]
        payloads = {'score.mid': midi, 'lyrics.txt': lyrics}
        if 'lyrics-timed.tsv' in entry['files']:
            payloads['lyrics-timed.tsv'] = embedded_lyrics(midi)
        folder = destination / 'items' / item_id
        folder.mkdir(parents=True, exist_ok=True)
        for name, payload in payloads.items():
            expected = entry['files'][name]
            if len(payload) != expected['bytes'] or digest(payload) != expected['sha256']:
                raise ValueError('Published file checksum mismatch: ' + item_id + '/' + name)
            path = folder / name
            if path.exists() and path.read_bytes() != payload:
                raise ValueError('Refusing to replace a different local file: ' + str(path))
            path.write_bytes(payload)
        (folder / 'metadata.json').write_text(json.dumps(entry, ensure_ascii=False, indent=2) + '\n')
    expanded = {k: v for k, v in manifest.items() if k != 'entry_shards'}
    expanded['entries'] = entries
    (destination / 'manifest.json').write_text(json.dumps(expanded, ensure_ascii=False, indent=2) + '\n')
    print(f'Materialized {len(entries)} acquired song identities. Quality limits remain in manifest.json.')


if __name__ == '__main__':
    main()
