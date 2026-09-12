import net from "node:net";
import { once } from "node:events";

const DEFAULT_TIMEOUT_MS = 30_000;

function withTimeout(promise, ms, label) {
  return Promise.race([
    promise,
    new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`FTP timeout: ${label}`)), ms).unref?.();
    })
  ]);
}

export class FtpClient {
  constructor({ timeoutMs = DEFAULT_TIMEOUT_MS } = {}) {
    this.timeoutMs = timeoutMs;
    this.socket = null;
    this.buffer = "";
    this.pending = [];
    this.closed = false;
  }

  async connect(host, port = 21) {
    if (!host) throw new Error("FTP host is required");
    this.socket = net.connect({ host, port });
    this.socket.setEncoding("utf8");
    this.socket.on("data", (chunk) => this.onData(chunk));
    this.socket.on("error", (error) => this.failAll(error));
    this.socket.on("close", () => {
      this.closed = true;
      this.failAll(new Error("FTP control connection closed"));
    });
    await once(this.socket, "connect");
    const greeting = await this.wait("connect");
    if (greeting.code !== 220) throw new Error(`FTP connect rejected: ${greeting.code} ${greeting.text}`);
    return greeting;
  }

  async login(username, password) {
    const user = await this.command(`USER ${username}`);
    if (user.code === 230) return user;
    if (user.code !== 331) throw new Error(`FTP USER rejected: ${user.code} ${user.text}`);
    const pass = await this.command(`PASS ${password}`);
    if (pass.code !== 230) throw new Error(`FTP authentication failed: ${pass.code}`);
    await this.command("TYPE I");
    return pass;
  }

  async cwd(remotePath) {
    const result = await this.command(`CWD ${remotePath}`);
    if (result.code !== 250 && result.code !== 200) throw new Error(`FTP CWD failed: ${result.code} ${result.text}`);
    return result;
  }

  async pwd() {
    const result = await this.command("PWD");
    const match = result.text.match(/"([^"]+)"/);
    return match ? match[1] : result.text;
  }

  async mkdir(remotePath) {
    const result = await this.command(`MKD ${remotePath}`);
    if (result.code !== 257 && result.code !== 250 && result.code !== 550) {
      throw new Error(`FTP MKD failed: ${result.code} ${result.text}`);
    }
    return result;
  }

  async rename(from, to) {
    const rnfr = await this.command(`RNFR ${from}`);
    if (rnfr.code !== 350) throw new Error(`FTP RNFR failed: ${rnfr.code} ${rnfr.text}`);
    const rnto = await this.command(`RNTO ${to}`);
    if (rnto.code !== 250) throw new Error(`FTP RNTO failed: ${rnto.code} ${rnto.text}`);
    return rnto;
  }

  async delete(remotePath) {
    const result = await this.command(`DELE ${remotePath}`);
    if (result.code !== 250) throw new Error(`FTP DELE failed: ${result.code} ${result.text}`);
    return result;
  }

  async list(remotePath = ".") {
    const { socket, finish } = await this.openData(`LIST ${remotePath}`);
    const chunks = [];
    socket.on("data", (chunk) => chunks.push(chunk));
    await withTimeout(once(socket, "end"), this.timeoutMs, "LIST data");
    socket.destroy();
    const control = await finish;
    const listing = Buffer.concat(chunks).toString("utf8");
    return { listing, control };
  }

  async retrieve(remotePath, maxBytes) {
    const { socket, finish } = await this.openData(`RETR ${remotePath}`);
    const chunks = [];
    let size = 0;
    await new Promise((resolve, reject) => {
      socket.on("data", (chunk) => {
        size += chunk.length;
        if (size > maxBytes) {
          socket.destroy();
          reject(new Error(`FTP RETR exceeded max bytes (${maxBytes})`));
          return;
        }
        chunks.push(chunk);
      });
      socket.on("end", resolve);
      socket.on("error", reject);
    });
    const control = await finish;
    return { bytes: Buffer.concat(chunks), control };
  }

  async store(remotePath, bytes) {
    const { socket, finish } = await this.openData(`STOR ${remotePath}`);
    socket.write(bytes);
    socket.end();
    await withTimeout(once(socket, "close"), this.timeoutMs, "STOR data");
    return finish;
  }

  async quit() {
    try { await this.command("QUIT"); } catch {}
    this.close();
  }

  close() {
    this.closed = true;
    try { this.socket?.destroy(); } catch {}
    this.failAll(new Error("FTP client closed"));
  }

  async openData(command) {
    const pasv = await this.command("PASV");
    const target = parsePasv(pasv.text);
    if (!target) throw new Error("FTP PASV response was not parseable");
    const socket = net.connect(target);
    await withTimeout(once(socket, "connect"), this.timeoutMs, "PASV connect");
    const pending = this.command(command);
    const preview = await pending.catch((error) => ({ error }));
    if (preview?.error) {
      socket.destroy();
      throw preview.error;
    }
    if (preview.code && preview.code >= 400) {
      socket.destroy();
      throw new Error(`FTP ${command} rejected: ${preview.code} ${preview.text}`);
    }
    const finish = preview.code && preview.code >= 200 && preview.code < 300
      ? Promise.resolve(preview)
      : this.wait(command);
    return { socket, finish };
  }

  command(line) {
    if (!this.socket || this.closed) return Promise.reject(new Error("FTP control connection is closed"));
    this.socket.write(`${line}\r\n`);
    return this.wait(line.split(" ")[0]);
  }

  wait(label) {
    return withTimeout(new Promise((resolve, reject) => {
      this.pending.push({ resolve, reject, parts: [], label });
    }), this.timeoutMs, label);
  }

  onData(chunk) {
    this.buffer += chunk;
    const lines = this.buffer.split(/\r?\n/);
    this.buffer = lines.pop() ?? "";
    for (const line of lines) {
      const match = /^(\d{3})([ -])(.*)$/.exec(line);
      if (!match) continue;
      const waiter = this.pending[0];
      if (!waiter) continue;
      waiter.parts.push(line);
      if (match[2] === "-") continue;
      this.pending.shift();
      waiter.resolve({ code: Number(match[1]), text: match[3], raw: waiter.parts.join("\n") });
    }
  }

  failAll(error) {
    while (this.pending.length) {
      this.pending.shift().reject(error);
    }
  }
}

function parsePasv(text) {
  const match = text.match(/\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)/);
  if (!match) return null;
  const host = `${match[1]}.${match[2]}.${match[3]}.${match[4]}`;
  const port = Number(match[5]) * 256 + Number(match[6]);
  return { host, port };
}
