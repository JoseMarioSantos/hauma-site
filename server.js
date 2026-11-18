// Servidor simples (sem dependências) para o Firebase App Hosting.
// Entrega o index.html e outros arquivos estáticos da pasta do projeto.
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const PORT = process.env.PORT || 8080;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".pdf": "application/pdf",
  ".woff2": "font/woff2",
};

// Arquivos do servidor que não devem ser baixados pelo navegador.
const BLOCKED = new Set(["server.js", "package.json", "package-lock.json", "apphosting.yaml"]);

http
  .createServer((req, res) => {
    let urlPath;
    try {
      urlPath = decodeURIComponent(new URL(req.url, "http://x").pathname);
    } catch {
      res.writeHead(400).end("Bad request");
      return;
    }
    if (urlPath.endsWith("/")) urlPath += "index.html";

    const file = path.normalize(path.join(ROOT, urlPath));
    const rel = path.relative(ROOT, file);
    const hidden = rel.split(path.sep).some((p) => p.startsWith(".") || p === "node_modules");

    if (rel.startsWith("..") || path.isAbsolute(rel) || hidden || BLOCKED.has(rel)) {
      res.writeHead(404).end("Not found");
      return;
    }

    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }).end("Página não encontrada");
        return;
      }
      res.writeHead(200, {
        "Content-Type": TYPES[path.extname(file).toLowerCase()] || "application/octet-stream",
        "Cache-Control": "public, max-age=300",
      });
      res.end(data);
    });
  })
  .listen(PORT, () => console.log(`Site Hauma rodando na porta ${PORT}`));
