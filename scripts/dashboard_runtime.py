#!/usr/bin/env python3
"""Start, inspect, or stop a target handoff Dashboard without copying it."""
from __future__ import annotations
import argparse, hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

def ident(root: Path, port: int) -> str:
    return hashlib.sha256(f'{root.resolve()}:{port}'.encode()).hexdigest()[:16]
def pidfile(root: Path, port: int) -> Path:
    return Path('/tmp') / f'local-agent-dashboard-{ident(root, port)}.pid'
def monitor_pidfile(root: Path, port: int) -> Path:
    return Path('/tmp') / f'local-agent-codex-monitor-{ident(root, port)}.pid'
def live_pid(path: Path) -> int | None:
    try:
        pid=int(path.read_text())
        os.kill(pid, 0)
        return pid
    except (ValueError, OSError):
        return None
def probe(port: int) -> dict:
    base=f'http://127.0.0.1:{port}'; out={'endpoint':base,'reachable':False}
    try:
        with urlopen(base+'/api/status', timeout=2) as r:
            out['reachable']=r.status==200; out['status']=json.loads(r.read().decode())
    except (OSError, URLError, ValueError) as exc: out['error']=str(exc)
    return out
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('action', choices=('start','status','stop')); p.add_argument('--project-root',required=True,type=Path); p.add_argument('--config',type=Path); p.add_argument('--db',type=Path); p.add_argument('--port',type=int,default=8765); a=p.parse_args()
    root=a.project_root.resolve(); config=(a.config or root/'trigger'/'config.local.json').resolve(); db=(a.db or root/'trigger'/'state.sqlite3').resolve(); pf=pidfile(root,a.port); mpf=monitor_pidfile(root,a.port)
    if a.action=='status': print(json.dumps({'ok':True,'project_root':str(root),'pid_file':str(pf),'monitor_pid_file':str(mpf),'monitor_pid':live_pid(mpf),**probe(a.port)},ensure_ascii=False)); return 0
    if a.action=='stop':
        stopped=[]
        for file in (pf,mpf):
            pid=live_pid(file)
            if pid is None:
                file.unlink(missing_ok=True)
                continue
            try:
                os.kill(pid,signal.SIGTERM); file.unlink(); stopped.append(pid)
            except OSError as exc: print(json.dumps({'ok':False,'error':str(exc)})); return 1
        if not stopped: print(json.dumps({'ok':True,'action':'not_running'})); return 0
        print(json.dumps({'ok':True,'action':'stopped','pids':stopped})); return 0
    if probe(a.port).get('reachable'):
        monitor=root/'trigger'/'codex-thread-monitor.py'; monitor_pid=live_pid(mpf); monitor_log=Path('/tmp')/f'local-agent-codex-monitor-{ident(root,a.port)}.log'
        if monitor.is_file() and monitor_pid is None:
            with monitor_log.open('ab') as stream: monitor_proc=subprocess.Popen([sys.executable,str(monitor),'--repo',str(root),'--db',str(db)],cwd=root,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            mpf.write_text(str(monitor_proc.pid)); monitor_pid=monitor_proc.pid
        print(json.dumps({'ok':True,'action':'already_running','monitor_pid':monitor_pid,'monitor_log':str(monitor_log) if monitor.is_file() else None,**probe(a.port)},ensure_ascii=False)); return 0
    trigger=root/'trigger'/'trigger.py'
    if not trigger.is_file(): print(json.dumps({'ok':False,'error':f'missing runtime: {trigger}'})); return 2
    log=Path('/tmp')/f'local-agent-dashboard-{ident(root,a.port)}.log'; cmd=[sys.executable,str(trigger),'--config',str(config),'--db',str(db),'--port',str(a.port)]
    with log.open('ab') as stream: proc=subprocess.Popen(cmd,cwd=root,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
    pf.write_text(str(proc.pid)); deadline=time.time()+8
    while time.time()<deadline:
        if probe(a.port).get('reachable'):
            monitor=root/'trigger'/'codex-thread-monitor.py'; monitor_pid=live_pid(mpf); monitor_log=Path('/tmp')/f'local-agent-codex-monitor-{ident(root,a.port)}.log'
            if monitor.is_file() and monitor_pid is None:
                with monitor_log.open('ab') as stream: monitor_proc=subprocess.Popen([sys.executable,str(monitor),'--repo',str(root),'--db',str(db)],cwd=root,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
                mpf.write_text(str(monitor_proc.pid)); monitor_pid=monitor_proc.pid
            print(json.dumps({'ok':True,'action':'started','pid':proc.pid,'log':str(log),'monitor_pid':monitor_pid,'monitor_log':str(monitor_log) if monitor.is_file() else None},ensure_ascii=False)); return 0
        time.sleep(.2)
    print(json.dumps({'ok':False,'action':'start_failed','pid':proc.pid,'log':str(log),**probe(a.port)},ensure_ascii=False)); return 1
if __name__=='__main__': raise SystemExit(main())
