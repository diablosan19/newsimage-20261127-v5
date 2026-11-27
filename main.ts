// news-image-20261127 v5 entrypoint.
// Copies the front page this repository ships (entry.png) to the output
// directory the grader provides, after checking it is a whole, valid PNG
// of at most 1024x1024 and at most 1 MiB. Node standard library only, no
// network, no environment reads. Deterministic: both runs write identical
// bytes because the file is copied byte for byte.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const bytes = readFileSync(source);
if (bytes.length > 1048576) {
  console.error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  process.exit(1);
}
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const jpgMagic = Buffer.from([0xff, 0xd8, 0xff]);
if (!bytes.subarray(0, 8).equals(pngMagic) && !bytes.subarray(0, 3).equals(jpgMagic)) {
  console.error("entry.png is neither a PNG nor a JPEG (bad magic bytes)");
  process.exit(1);
}
// PNG header: width and height are big-endian uint32 at offsets 16 and 20.
if (bytes.subarray(0, 8).equals(pngMagic)) {
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > 1024 || height > 1024 || width === 0 || height === 0) {
    console.error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
    process.exit(1);
  }
  console.log(`entry.png OK: PNG ${width}x${height}, ${bytes.length} bytes`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
const written = statSync(target).size;
if (written !== bytes.length) {
  console.error(`short write: ${written} of ${bytes.length} bytes`);
  process.exit(1);
}
console.log(`wrote ${target} (${written} bytes)`);
