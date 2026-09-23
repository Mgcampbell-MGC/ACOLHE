// Small markdown dialect -> .docx, for the founder manual.
// Usage: NODE_PATH=<dir with docx> node tools/md_to_docx.js in.md out.docx
//
// Dialect (one construct per line, blank line ends a paragraph):
//   %% Header line one | Header line two | Header line three   -> dark header card
//   # Part     ## Section     ### Subsection
//   :::LABEL  ...lines...  :::                 -> callout box (red if LABEL starts NUNCA/NEVER/PARE/STOP)
//   :::CANVAS ... @kp Title / - bullet ... :::  -> Business Model Canvas (put it in a landscape section)
//   | a | b |  (2nd row |---|)                  -> table, first row is the header
//   - item   /   - [ ] item   /   1. item       -> bullet / checkbox / numbered
//   ---pagebreak---   ---landscape---   ---portrait---
//   inline **bold** and *italic*
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,
       ShadingType,AlignmentType,BorderStyle,LevelFormat,PageBreak,PageOrientation,Footer,
       PageNumber,VerticalAlign,HeightRule} = require('docx');
const fs = require('fs');

const F = "Calibri", DK = "1F3B36", ACC = "2E7D6B", RED = "9C0006", GREY = "595959";
const PORTRAIT_W = 9900, LANDSCAPE_W = 14400;

function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({text: text.slice(last, m.index), font: F, ...base}));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({text: t.slice(2, -2), font: F, ...base, bold: true}));
    else out.push(new TextRun({text: t.slice(1, -1), font: F, ...base, italics: true}));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({text: text.slice(last), font: F, ...base}));
  return out;
}

const para = (t, o = {}) => new Paragraph({spacing: {after: o.after ?? 90, line: 259},
  alignment: o.align, indent: o.indent, keepNext: o.keepNext,
  children: runs(t, {size: o.size ?? 20, color: o.color ?? "000000", bold: o.b, italics: o.i})});

function heading(t, level, newPage = false) {
  const size = {1: 32, 2: 24, 3: 21}[level];
  const hl = {1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3}[level];
  // pageBreakBefore, not a separate PageBreak paragraph: the latter leaves a blank page
  // whenever the previous part ends exactly at the bottom of a page.
  return new Paragraph({heading: hl, keepNext: true, pageBreakBefore: newPage,
    spacing: {before: level === 1 ? 80 : 180, after: level === 1 ? 120 : 80},
    border: level === 1 ? {bottom: {style: BorderStyle.SINGLE, size: 12, color: ACC, space: 4}} : undefined,
    children: [new TextRun({text: t, font: F, bold: true, size, color: DK})]});
}

const bullet = (t, lvl = 0) => new Paragraph({numbering: {reference: "b", level: lvl},
  spacing: {after: 50, line: 252}, children: runs(t, {size: 20})});

const hanging = (label, t) => new Paragraph({spacing: {after: 50, line: 252},
  indent: {left: 420, hanging: 300},
  children: [new TextRun({text: label + "\t", font: F, size: 20, bold: true, color: DK}), ...runs(t, {size: 20})],
  tabStops: [{type: "left", position: 420}]});

// Space after a table/box. Marked so a following new-page heading can drop it: a spacer
// that spills onto its own page would otherwise leave a blank page.
const spacer = after => { const p = new Paragraph({spacing: {after}, children: []}); p._spacer = true; return p; };

const NONE = {style: BorderStyle.NONE, size: 0, color: "FFFFFF"};
const THIN = {style: BorderStyle.SINGLE, size: 4, color: "BFBFBF"};

function headerCard(parts, width) {
  const [a, b, c] = parts;
  const kids = [];
  if (a) kids.push(new Paragraph({spacing: {after: 40}, children: [new TextRun({text: a.toUpperCase(), font: F, size: 17, color: "B7D8CF", bold: true, characterSpacing: 30})]}));
  if (b) kids.push(new Paragraph({spacing: {after: 40}, children: [new TextRun({text: b, font: F, size: 44, color: "FFFFFF", bold: true})]}));
  if (c) kids.push(new Paragraph({spacing: {after: 0}, children: [new TextRun({text: c, font: F, size: 24, color: "E6F2EE"})]}));
  return new Table({columnWidths: [width], width: {size: width, type: WidthType.DXA},
    rows: [new TableRow({children: [new TableCell({width: {size: width, type: WidthType.DXA},
      shading: {type: ShadingType.CLEAR, color: "auto", fill: DK},
      margins: {top: 220, bottom: 220, left: 300, right: 300},
      borders: {top: NONE, bottom: NONE, left: NONE, right: NONE}, children: kids})]})]});
}

function callout(label, lines, width) {
  const red = /^(NUNCA|NEVER|PARE|STOP|ATEN)/i.test(label);
  const col = red ? RED : ACC, fill = red ? "FBEAEA" : "EAF4F1";
  const kids = [new Paragraph({spacing: {after: 60}, children: [new TextRun({text: label.toUpperCase(), font: F, size: 17, bold: true, color: col, characterSpacing: 20})]})];
  for (const l of lines) {
    if (/^- \[ \] /.test(l)) kids.push(new Paragraph({spacing: {after: 50}, indent: {left: 300, hanging: 300}, children: [new TextRun({text: "☐\t", font: F, size: 20}), ...runs(l.slice(6), {size: 20})]}));
    else if (/^- /.test(l)) kids.push(new Paragraph({spacing: {after: 50}, indent: {left: 300, hanging: 220}, children: [new TextRun({text: "•\t", font: F, size: 20, color: col}), ...runs(l.slice(2), {size: 20})]}));
    else if (/^\d+\. /.test(l)) { const m = l.match(/^(\d+\.) (.*)$/); kids.push(new Paragraph({spacing: {after: 50}, indent: {left: 360, hanging: 360}, children: [new TextRun({text: m[1] + "\t", font: F, size: 20, bold: true, color: col}), ...runs(m[2], {size: 20})]})); }
    else if (l.trim()) kids.push(new Paragraph({spacing: {after: 50, line: 252}, children: runs(l, {size: 20})}));
  }
  return [new Table({columnWidths: [width], width: {size: width, type: WidthType.DXA},
    rows: [new TableRow({cantSplit: true, children: [new TableCell({width: {size: width, type: WidthType.DXA},
      shading: {type: ShadingType.CLEAR, color: "auto", fill},
      margins: {top: 100, bottom: 100, left: 200, right: 200},
      borders: {top: NONE, bottom: NONE, right: NONE, left: {style: BorderStyle.SINGLE, size: 36, color: col}},
      children: kids})]})]}), spacer(80)];
}

function colWidths(rows, width) {
  const n = rows[0].length;
  const len = Array(n).fill(4);
  for (const r of rows) r.forEach((c, i) => { len[i] = Math.max(len[i], Math.min(60, c.replace(/\*/g, "").length)); });
  const w = len.map(x => Math.sqrt(x));
  const s = w.reduce((a, b) => a + b, 0);
  const out = w.map(x => Math.max(900, Math.round(width * x / s)));
  const diff = width - out.reduce((a, b) => a + b, 0);
  out[out.indexOf(Math.max(...out))] += diff;
  return out;
}

function table(rows, width) {
  const widths = colWidths(rows, width);
  const numeric = c => /^[-−+~≈R$\d\s.,%x×/–]+$/.test(c.replace(/\*/g, "")) && /\d/.test(c);
  // right-align a column only when every body cell in it is a number
  const numCol = rows[0].map((_, i) => rows.length > 1 && rows.slice(1).every(r => numeric(r[i] || "")));
  const mk = (c, i, head, zebra) => new TableCell({width: {size: widths[i], type: WidthType.DXA},
    shading: head ? {type: ShadingType.CLEAR, color: "auto", fill: DK} : zebra ? {type: ShadingType.CLEAR, color: "auto", fill: "F4F7F6"} : undefined,
    margins: {top: 35, bottom: 35, left: 80, right: 80}, verticalAlign: VerticalAlign.CENTER,
    borders: {top: THIN, bottom: THIN, left: THIN, right: THIN},
    children: [new Paragraph({alignment: !head && i > 0 && numCol[i] ? AlignmentType.RIGHT : undefined,
      children: runs(c, {size: 18, bold: head || undefined, color: head ? "FFFFFF" : "000000"})})]});
  return [new Table({columnWidths: widths, width: {size: width, type: WidthType.DXA},
    rows: rows.map((r, ri) => new TableRow({tableHeader: ri === 0, cantSplit: true,
      children: r.map((c, i) => mk(c, i, ri === 0, ri > 0 && ri % 2 === 0))}))}),
    spacer(100)];
}

// Business Model Canvas, classic 9 blocks: @kp @ka @kr @vp @cr @ch @cs @cost @rev
function canvas(lines, width) {
  const blocks = {}; let cur = null;
  for (const l of lines) {
    const m = l.match(/^@(\w+)\s+(.*)$/);
    if (m) { cur = m[1]; blocks[cur] = {title: m[2], items: []}; }
    else if (cur && l.trim()) blocks[cur].items.push(l.replace(/^- /, ""));
  }
  const unit = Math.floor(width / 10);
  const cell = (k, cs, rs, fill) => {
    const b = blocks[k] || {title: k, items: []};
    return new TableCell({columnSpan: cs, rowSpan: rs, width: {size: unit * cs, type: WidthType.DXA},
      shading: {type: ShadingType.CLEAR, color: "auto", fill: fill || "FFFFFF"},
      margins: {top: 80, bottom: 80, left: 100, right: 100},
      borders: {top: {style: BorderStyle.SINGLE, size: 8, color: DK}, bottom: {style: BorderStyle.SINGLE, size: 8, color: DK},
                left: {style: BorderStyle.SINGLE, size: 8, color: DK}, right: {style: BorderStyle.SINGLE, size: 8, color: DK}},
      children: [new Paragraph({spacing: {after: 60}, children: [new TextRun({text: b.title.toUpperCase(), font: F, size: 18, bold: true, color: ACC})]}),
        ...b.items.map(t => new Paragraph({spacing: {after: 30, line: 240}, indent: {left: 140, hanging: 140},
          children: [new TextRun({text: "• ", font: F, size: 18, color: ACC}), ...runs(t, {size: 18})]}))]});
  };
  return [new Table({columnWidths: Array(10).fill(unit), width: {size: unit * 10, type: WidthType.DXA},
    rows: [
      new TableRow({height: {value: 3000, rule: HeightRule.ATLEAST}, children: [cell("kp", 2, 2), cell("ka", 2, 1), cell("vp", 2, 2, "EAF4F1"), cell("cr", 2, 1), cell("cs", 2, 2)]}),
      new TableRow({height: {value: 2800, rule: HeightRule.ATLEAST}, children: [cell("kr", 2, 1), cell("ch", 2, 1)]}),
      new TableRow({height: {value: 2200, rule: HeightRule.ATLEAST}, children: [cell("cost", 5, 1, "F7F7F7"), cell("rev", 5, 1, "F7F7F7")]}),
    ]})];
}

function convert(md) {
  const L = md.replace(/\r/g, "").split("\n");
  const sections = []; let kids = []; let orient = "portrait"; let firstH1 = true;
  const width = () => orient === "portrait" ? PORTRAIT_W : LANDSCAPE_W;
  const flushSection = () => { if (kids.length) sections.push({orient, kids}); kids = []; };
  let paraBuf = [];
  const flushPara = () => { if (paraBuf.length) kids.push(para(paraBuf.join(" "))); paraBuf = []; };
  for (let i = 0; i < L.length; i++) {
    const l = L[i];
    if (/^---pagebreak---\s*$/.test(l)) { flushPara(); kids.push(new Paragraph({children: [new PageBreak()]})); continue; }
    if (/^---(landscape|portrait)---\s*$/.test(l)) { flushPara(); flushSection(); orient = l.includes("landscape") ? "landscape" : "portrait"; continue; }
    if (l.startsWith("%% ")) { flushPara(); kids.push(headerCard(l.slice(3).split("|").map(s => s.trim()), width()), new Paragraph({spacing: {after: 160}, children: []})); continue; }
    const h = l.match(/^(#{1,3}) (.*)$/);
    if (h) {
      flushPara();
      const newPage = h[1].length === 1 && !firstH1 && kids.length > 0;
      if (newPage) while (kids.length && kids[kids.length - 1]._spacer) kids.pop();
      if (h[1].length === 1) firstH1 = false;
      kids.push(heading(h[2], h[1].length, newPage)); continue;
    }
    if (l.startsWith(":::")) {
      flushPara();
      const label = l.slice(3).trim(); const body = [];
      while (++i < L.length && !/^:::\s*$/.test(L[i])) body.push(L[i]);
      if (label === "CANVAS") kids.push(...canvas(body, width()));
      else kids.push(...callout(label, body, width()));
      continue;
    }
    if (l.startsWith("|")) {
      flushPara();
      const rows = [];
      for (; i < L.length && L[i].startsWith("|"); i++) {
        if (/^\|[\s:|-]+\|\s*$/.test(L[i])) continue;
        rows.push(L[i].trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()));
      }
      i--; kids.push(...table(rows, width())); continue;
    }
    let m;
    if ((m = l.match(/^- \[ \] (.*)$/))) { flushPara(); kids.push(new Paragraph({spacing: {after: 50, line: 252}, indent: {left: 420, hanging: 320}, children: [new TextRun({text: "☐\t", font: F, size: 21}), ...runs(m[1], {size: 20})]})); continue; }
    if ((m = l.match(/^(\s*)- (.*)$/))) { flushPara(); kids.push(bullet(m[2], m[1].length >= 2 ? 1 : 0)); continue; }
    if ((m = l.match(/^(\d+\.) (.*)$/))) { flushPara(); kids.push(hanging(m[1], m[2])); continue; }
    if (!l.trim()) { flushPara(); continue; }
    paraBuf.push(l.trim());
  }
  flushPara(); flushSection();
  return sections;
}

function build(md, out, footerText) {
  const secs = convert(md);
  const doc = new Document({
    creator: "ACOLHE", title: "ACOLHE — Manual",
    styles: {default: {document: {run: {font: F, size: 20}}}},
    numbering: {config: [{reference: "b", levels: [
      {level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: {paragraph: {indent: {left: 380, hanging: 240}}, run: {color: ACC}}},
      {level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: {paragraph: {indent: {left: 760, hanging: 240}}}}]}]},
    sections: secs.map(s => ({
      properties: {page: {// docx swaps width/height itself when orientation is LANDSCAPE, so always pass portrait A4 here
        size: s.orient === "landscape" ? {orientation: PageOrientation.LANDSCAPE, width: 11906, height: 16838} : {width: 11906, height: 16838},
        margin: {top: 800, bottom: 760, left: s.orient === "landscape" ? 1200 : 1000, right: s.orient === "landscape" ? 1200 : 1000}}},
      footers: {default: new Footer({children: [new Paragraph({alignment: AlignmentType.RIGHT,
        children: [new TextRun({text: footerText + "   ", font: F, size: 16, color: GREY}), new TextRun({children: [PageNumber.CURRENT], font: F, size: 16, color: GREY})]})]})},
      children: s.kids})),
  });
  return Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("written", out, b.length, "bytes"); });
}

if (require.main === module) {
  const [, , inp, out, foot] = process.argv;
  build(fs.readFileSync(inp, "utf8"), out, foot || "ACOLHE");
}
module.exports = {convert, build};
