import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const python = process.env.FIREWATCH_PYTHON || (existsSync(resolve(root, '.venv', 'Scripts', 'python.exe'))
  ? resolve(root, '.venv', 'Scripts', 'python.exe')
  : 'python');
const vite = resolve(root, 'node_modules', 'vite', 'bin', 'vite.js');
const children = [];
let stopping = false;

function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  for (const child of children) {
    if (child.exitCode === null) child.kill('SIGTERM');
  }
  setTimeout(() => process.exit(code), 300);
}

function launch(command, args, options) {
  const child = spawn(command, args, { cwd: root, stdio: 'inherit', ...options });
  children.push(child);
  child.on('error', error => {
    console.error(`Could not start ${command}: ${error.message}`);
    if (command === python) console.error('Install backend dependencies with: .venv\\Scripts\\python.exe -m pip install -r backend\\requirements.txt');
    stop(1);
  });
  child.on('exit', (code, signal) => {
    if (!stopping && code !== 0) {
      console.error(`${command} stopped (${signal || `exit ${code}`}).`);
      stop(code || 1);
    }
  });
  return child;
}

process.on('SIGINT', () => stop(0));
process.on('SIGTERM', () => stop(0));

console.log('Starting FIREWATCH API at http://localhost:8000 and dashboard at http://localhost:5173');
launch(python, ['-m', 'uvicorn', 'app.main:app', '--reload', '--app-dir', 'backend', '--host', '127.0.0.1', '--port', '8000']);
launch(process.execPath, [vite, '--host', '127.0.0.1', '--port', '5173'], { cwd: resolve(root, 'frontend') });
