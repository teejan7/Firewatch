import net from 'node:net';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawn } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const apiPort = Number(process.env.FIREWATCH_API_PORT || 8000);
const webPort = Number(process.env.FIREWATCH_WEB_PORT || 5173);
const python = process.env.FIREWATCH_PYTHON || (existsSync(resolve(root, '.venv', 'Scripts', 'python.exe'))
  ? resolve(root, '.venv', 'Scripts', 'python.exe') : 'python');
const vite = resolve(root, 'node_modules', 'vite', 'bin', 'vite.js');
const children = new Set();
let stopping = false;

function portIsFree(port) {
  return new Promise((resolvePort, reject) => {
    const server = net.createServer();
    server.once('error', reject);
    server.listen(port, '127.0.0.1', () => server.close(() => resolvePort(true)));
  });
}

function launch(command, args, options = {}) {
  const child = spawn(command, args, { cwd: root, stdio: 'inherit', ...options });
  children.add(child);
  child.once('error', error => { console.error(`Could not start ${command}: ${error.message}`); void stop(1); });
  child.once('exit', (code, signal) => {
    children.delete(child);
    if (!stopping) { console.error(`${command} stopped (${signal || `exit ${code}`}).`); void stop(code || 1); }
  });
  return child;
}

async function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  for (const child of children) if (child.exitCode === null) child.kill('SIGTERM');
  await Promise.race([Promise.all([...children].map(child => new Promise(resolveExit => child.once('exit', resolveExit)))), delay(2500)]);
  process.exit(code);
}

async function main() {
  for (const [name, port] of [['API', apiPort], ['dashboard', webPort]]) {
    try { await portIsFree(port); }
    catch { throw new Error(`${name} port ${port} is already in use. Close the other FIREWATCH process or set FIREWATCH_${name === 'API' ? 'API' : 'WEB'}_PORT.`); }
  }
  console.log(`Starting FIREWATCH API at http://127.0.0.1:${apiPort}`);
  const apiChild = launch(python, ['-m', 'uvicorn', 'app.main:app', '--reload', '--app-dir', 'backend', '--host', '127.0.0.1', '--port', String(apiPort)]);
  const healthUrl = `http://127.0.0.1:${apiPort}/api/health`;
  const deadline = Date.now() + 30_000;
  let wait = 250;
  while (Date.now() < deadline && !stopping && apiChild.exitCode === null) {
    try {
      const response = await fetch(healthUrl, { signal: AbortSignal.timeout(1500) });
      if (response.ok) break;
    } catch { /* startup is still in progress */ }
    await delay(wait);
    wait = Math.min(Math.round(wait * 1.6), 2000);
  }
  if (stopping || apiChild.exitCode !== null) throw new Error('The FIREWATCH API exited before becoming healthy. Check the API output above.');
  try {
    const response = await fetch(healthUrl, { signal: AbortSignal.timeout(1500) });
    if (!response.ok) throw new Error();
  } catch { throw new Error('FIREWATCH API did not become healthy within 30 seconds. Check backend dependencies and API output.'); }
  console.log(`API healthy. Starting dashboard at http://127.0.0.1:${webPort}`);
  launch(process.execPath, [vite, '--host', '127.0.0.1', '--port', String(webPort), '--strictPort'], {
    cwd: resolve(root, 'frontend'), env: { ...process.env, VITE_API_URL: `http://127.0.0.1:${apiPort}` },
  });
}

process.on('SIGINT', () => void stop(0));
process.on('SIGTERM', () => void stop(0));
main().catch(error => { console.error(error.message); void stop(1); });
