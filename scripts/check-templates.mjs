// Checks that every file in templates/ is a valid artifact of its type:
// frontmatter validates against the v1alpha1 schema, and the body carries the
// required sections the chapters name, in order. The requirements are read
// from schemas/v1alpha1 and from the chapters themselves, never restated here,
// so the templates cannot drift from the normative text they exemplify.
//
// No dependencies on purpose. The YAML and JSON Schema support below covers
// exactly what the schemas and templates use, and fails loudly on anything
// else rather than guessing.
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const errors = [];
const fail = (msg) => errors.push(msg);

// --- Schemas, indexed by $id and by type name (file base). -----------------
const schemaDir = join(root, 'schemas', 'v1alpha1');
const schemasById = new Map();
const schemasByType = new Map();
for (const file of readdirSync(schemaDir)) {
  if (!file.endsWith('.schema.json')) continue;
  const schema = JSON.parse(readFileSync(join(schemaDir, file), 'utf8'));
  if (schema.$id) schemasById.set(schema.$id, schema);
  schemasByType.set(file.replace('.schema.json', ''), schema);
}

// --- YAML subset parser for template frontmatter. ---------------------------
// Supports: scalar values, inline arrays ([] and [A, B]), block lists of
// scalars, block lists of single-key or multi-key objects, and nested maps.
function parseYaml(text, file) {
  const lines = text.split('\n').filter((l) => l.trim() !== '' && !l.trim().startsWith('#'));
  let pos = 0;
  const indentOf = (l) => l.length - l.trimStart().length;

  function scalar(raw) {
    const v = raw.trim();
    if (v === '[]') return [];
    if (v.startsWith('[') && v.endsWith(']')) {
      return v.slice(1, -1).split(',').map((s) => scalar(s));
    }
    if ((v.startsWith("'") && v.endsWith("'")) || (v.startsWith('"') && v.endsWith('"'))) {
      return v.slice(1, -1);
    }
    return v;
  }

  function parseBlock(indent) {
    const isList = lines[pos] !== undefined && indentOf(lines[pos]) === indent && lines[pos].trim().startsWith('- ');
    if (isList) {
      const arr = [];
      while (pos < lines.length && indentOf(lines[pos]) === indent && lines[pos].trim().startsWith('- ')) {
        const item = lines[pos].trim().slice(2);
        const m = item.match(/^([A-Za-z0-9-]+):(?: (.*))?$/);
        if (m) {
          pos++;
          const obj = {};
          obj[m[1]] = m[2] !== undefined ? scalar(m[2]) : parseBlock(indentOf(lines[pos] ?? '') );
          // continuation keys of the same object, indented deeper than the dash
          while (pos < lines.length && indentOf(lines[pos]) > indent && !lines[pos].trim().startsWith('- ')) {
            const c = lines[pos].trim().match(/^([A-Za-z0-9-]+): (.*)$/);
            if (!c) throw new Error(`${file}: unsupported YAML at '${lines[pos]}'`);
            obj[c[1]] = scalar(c[2]);
            pos++;
          }
          arr.push(obj);
        } else {
          arr.push(scalar(item));
          pos++;
        }
      }
      return arr;
    }
    const obj = {};
    while (pos < lines.length && indentOf(lines[pos]) === indent && !lines[pos].trim().startsWith('- ')) {
      const m = lines[pos].match(/^\s*([A-Za-z0-9-]+):(?: (.*))?$/);
      if (!m) throw new Error(`${file}: unsupported YAML at '${lines[pos]}'`);
      pos++;
      if (m[2] !== undefined) {
        obj[m[1]] = scalar(m[2]);
      } else {
        if (pos >= lines.length || indentOf(lines[pos]) <= indent) {
          throw new Error(`${file}: key '${m[1]}' has no value`);
        }
        obj[m[1]] = parseBlock(indentOf(lines[pos]));
      }
    }
    return obj;
  }

  const value = parseBlock(0);
  if (pos !== lines.length) throw new Error(`${file}: unsupported YAML near '${lines[pos]}'`);
  return value;
}

// --- JSON Schema subset validator. ------------------------------------------
const ANNOTATIONS = new Set(['$schema', '$id', 'title', 'description', '$defs', '$comment']);
const KEYWORDS = new Set([
  '$ref', 'type', 'const', 'enum', 'pattern', 'minLength', 'minItems',
  'required', 'properties', 'additionalProperties', 'items', 'oneOf', 'not',
]);

function resolveRef(ref, currentRoot) {
  const [idPart, pointer] = ref.split('#');
  const rootSchema = idPart === '' ? currentRoot : schemasById.get(idPart);
  if (!rootSchema) throw new Error(`unresolvable $ref '${ref}'`);
  let node = rootSchema;
  for (const seg of pointer.replace(/^\//, '').split('/')) {
    node = node[seg];
    if (node === undefined) throw new Error(`unresolvable $ref '${ref}'`);
  }
  return { node, root: rootSchema };
}

function validate(value, schema, path, root, out) {
  for (const key of Object.keys(schema)) {
    if (!KEYWORDS.has(key) && !ANNOTATIONS.has(key)) {
      throw new Error(`schema keyword '${key}' at ${path} is not supported by this checker; extend it deliberately`);
    }
  }
  if (schema.$ref) {
    const { node, root: newRoot } = resolveRef(schema.$ref, root);
    validate(value, node, path, newRoot, out);
    return;
  }
  if (schema.const !== undefined && value !== schema.const) {
    out.push(`${path}: expected ${JSON.stringify(schema.const)}, got ${JSON.stringify(value)}`);
    return;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    out.push(`${path}: ${JSON.stringify(value)} is not one of ${schema.enum.join(', ')}`);
    return;
  }
  if (schema.oneOf) {
    const passing = schema.oneOf.filter((s) => {
      const attempt = [];
      try { validate(value, s, path, root, attempt); } catch (e) { throw e; }
      return attempt.length === 0;
    });
    if (passing.length !== 1) {
      out.push(`${path}: matched ${passing.length} of the oneOf branches, expected exactly 1`);
    }
    return;
  }
  if (schema.not) {
    const attempt = [];
    validate(value, schema.not, path, root, attempt);
    if (attempt.length === 0) out.push(`${path}: value matches a prohibited pattern`);
  }
  if (schema.type === 'object') {
    if (typeof value !== 'object' || value === null || Array.isArray(value)) {
      out.push(`${path}: expected an object`);
      return;
    }
    for (const req of schema.required ?? []) {
      if (!(req in value)) out.push(`${path}: missing required '${req}'`);
    }
    for (const [k, v] of Object.entries(value)) {
      const propSchema = schema.properties?.[k];
      if (!propSchema) {
        if (schema.additionalProperties === false) out.push(`${path}: unknown property '${k}'`);
        continue;
      }
      validate(v, propSchema, `${path}.${k}`, root, out);
    }
    return;
  }
  if (schema.type === 'array') {
    if (!Array.isArray(value)) {
      out.push(`${path}: expected an array`);
      return;
    }
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      out.push(`${path}: needs at least ${schema.minItems} item(s)`);
    }
    if (schema.items) value.forEach((v, i) => validate(v, schema.items, `${path}[${i}]`, root, out));
    return;
  }
  if (schema.type === 'string' || schema.pattern || schema.minLength !== undefined) {
    if (typeof value !== 'string') {
      out.push(`${path}: expected a string`);
      return;
    }
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      out.push(`${path}: shorter than minLength ${schema.minLength}`);
    }
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
      out.push(`${path}: '${value}' does not match ${schema.pattern}`);
    }
  }
}

// --- Required body sections, read from the chapters. -------------------------
function sectionRequirements() {
  const map = new Map();
  const artifacts = readFileSync(join(root, 'spec', 'artifacts.md'), 'utf8');
  for (const m of artifacts.matchAll(/^## .+\(`([a-z-]+)`, `[A-Z]+-`\)[\s\S]*?(?=^## |$(?![\s\S]))/gm)) {
    const line = m[0].match(/Required body sections: (.+?)\.\n/);
    if (line) map.set(m[1], [...line[1].matchAll(/`## ([^`]+)`/g)].map((s) => s[1]));
  }
  const changes = readFileSync(join(root, 'spec', 'product-changes.md'), 'utf8');
  const line = changes.match(/Required body sections: (.+?)\.\n/);
  if (line) map.set('product-change', [...line[1].matchAll(/`## ([^`]+)`/g)].map((s) => s[1]));
  return map;
}

// --- Check every template. ----------------------------------------------------
const required = sectionRequirements();
const templateDir = join(root, 'templates');
const templates = readdirSync(templateDir).filter((f) => f.endsWith('.md') && f !== 'README.md');
if (templates.length === 0) {
  console.error('no templates found; nothing to check is a failure, not a pass');
  process.exit(1);
}

const declaredIds = new Set();
const referencedIds = new Set();

for (const file of templates) {
  const raw = readFileSync(join(templateDir, file), 'utf8');
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n/);
  if (!fmMatch) { fail(`${file}: no frontmatter`); continue; }

  let fm;
  try { fm = parseYaml(fmMatch[1], file); } catch (e) { fail(e.message); continue; }

  const type = fm.type;
  if (file !== `${type}.md`) fail(`${file}: file name must be '${type}.md'`);
  const schema = schemasByType.get(type);
  if (!schema) { fail(`${file}: no schema for type '${type}'`); continue; }

  const out = [];
  validate(fm, schema, file, schema, out);
  errors.push(...out);

  const sections = required.get(type);
  if (!sections || sections.length === 0) {
    fail(`${file}: the chapters name no required sections for '${type}'; the parser or the chapter moved`);
  } else {
    const body = raw.slice(fmMatch[0].length).replace(/<!--[\s\S]*?-->/g, '');
    const headings = [...body.matchAll(/^## (.+)$/gm)].map((m) => m[1].trim());
    sections.forEach((want, i) => {
      if (headings[i] !== want) fail(`${file}: section ${i + 1} must be '## ${want}', found '${headings[i] ? '## ' + headings[i] : 'nothing'}'`);
    });
  }

  declaredIds.add(fm.id);
  for (const m of fmMatch[1].matchAll(/\b(?:ACT|JRN|UC|BR|TERM|BC|FR|QR|CON|SB|CHG)-EXAMPLE-\d+\b/g)) {
    referencedIds.add(m[0]);
  }
}

for (const id of referencedIds) {
  if (!declaredIds.has(id)) fail(`referenced ${id} has no template declaring it`);
}

if (errors.length) {
  for (const e of errors) console.error(`error: ${e}`);
  process.exit(1);
}
console.log(`${templates.length} templates valid against the schemas and the chapters' required sections.`);
