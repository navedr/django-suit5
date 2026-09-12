#!/usr/bin/env node
/**
 * Generates scss/_icons.scss -- the compatibility layer that lets the old
 * Glyphicon class names (icon-calendar, icon-trash, ...) render as Bootstrap Icons.
 *
 *   npm run build:icons
 *
 * Why this is generated rather than hand-written: Bootstrap Icons assigns codepoints
 * in alphabetical order, so inserting a new icon SHIFTS the codepoints of everything
 * after it. A hand-maintained table of "\f1f4" literals silently rots on every
 * bootstrap-icons bump -- the class keeps working and just draws a different picture.
 * (django-suit5 0.3.8 shipped .icon-calendar pointing at bi-calendar-x-fill this way.)
 *
 * So the map below is keyed on icon NAMES, and the codepoints are looked up at build
 * time from the bootstrap-icons package itself. Bumping bootstrap-icons and re-running
 * this script is all that is needed. An unknown name is a hard error, never a wrong glyph.
 */

const fs = require('fs');
const path = require('path');

const ICONS_JSON = path.join(__dirname, '..', 'node_modules', 'bootstrap-icons', 'font', 'bootstrap-icons.json');
const OUT = path.join(__dirname, '..', 'suit5', 'static', 'suit5', 'scss', '_icons.scss');

// [[legacy icon-* suffixes], bootstrap-icons name]
// A section header is a bare string.
const MAP = [

  // Navigation & UI
  [["home"], "house"],
  [["cog", "gear"], "gear"],
  [["trash"], "trash"],
  [["pencil"], "pencil"],
  [["plus"], "plus"],
  [["search"], "search"],
  [["calendar"], "calendar"],
  [["time", "clock"], "clock"],
  [["eye-open"], "eye"],
  [["eye-close"], "eye-slash"],
  [["ok", "check"], "check"],
  [["remove", "x"], "x"],
  [["chevron-right"], "chevron-right"],
  [["chevron-left"], "chevron-left"],
  [["chevron-up"], "chevron-up"],
  [["chevron-down"], "chevron-down"],
  [["arrow-up"], "arrow-up"],
  [["arrow-down"], "arrow-down"],
  [["arrow-left"], "arrow-left"],
  [["arrow-right"], "arrow-right"],
  [["lock"], "lock"],
  [["globe"], "globe"],
  [["user"], "person"],
  [["comment"], "chat"],
  [["question-sign"], "question-circle"],
  [["upload"], "upload"],
  [["download"], "download"],
  [["picture", "image"], "image"],
  [["file"], "file-earmark"],
  [["folder-open"], "folder2-open"],
  [["folder-close"], "folder2"],
  [["list"], "list"],
  [["th"], "grid"],
  [["th-list"], "list"],
  [["star"], "star-fill"],
  [["star-empty"], "star"],
  [["heart"], "heart-fill"],
  [["heart-empty"], "heart"],
  [["signal"], "signal"],
  [["refresh"], "arrow-clockwise"],
  [["filter"], "funnel"],
  [["sort"], "sort-down"],
  [["sort-by-alphabet"], "sort-alpha-down"],
  [["sort-by-order"], "sort-numeric-down"],
  [["info-sign"], "info-circle"],
  [["warning-sign"], "exclamation-triangle"],
  [["exclamation-sign"], "exclamation-circle"],
  [["ban-circle"], "slash-circle"],
  [["share"], "share"],
  [["share-alt"], "share-fill"],
  [["link"], "link-45deg"],
  [["external-link"], "box-arrow-up-right"],
  [["tag"], "tag"],
  [["tags"], "tags"],
  [["bookmark"], "bookmark-fill"],
  [["print"], "printer"],
  [["envelope"], "envelope"],
  [["phone"], "telephone"],
  [["edit"], "pencil-square"],
  [["zoom-in"], "zoom-in"],
  [["zoom-out"], "zoom-out"],
  [["move"], "arrows-move"],
  [["resize-full"], "arrows-fullscreen"],
  [["resize-small"], "fullscreen-exit"],
  [["log-in"], "box-arrow-in-right"],
  [["log-out"], "box-arrow-right"],
  [["off", "power-off"], "power"],

  // Form/Input related
  [["ok-circle"], "check-circle"],
  [["remove-circle"], "x-circle"],
  [["plus-sign"], "plus-circle"],
  [["minus-sign"], "dash-circle"],

  // Media controls
  [["play"], "play-fill"],
  [["pause"], "pause-fill"],
  [["stop"], "stop-fill"],
  [["forward"], "skip-forward-fill"],
  [["backward"], "skip-backward-fill"],
  [["fast-forward"], "fast-forward-fill"],
  [["fast-backward"], "rewind-fill"],
  [["step-forward"], "skip-end-fill"],
  [["step-backward"], "skip-start-fill"],
  [["eject"], "eject-fill"],
  [["volume-off"], "volume-mute"],
  [["volume-down"], "volume-down"],
  [["volume-up"], "volume-up"],

  // Text formatting
  [["bold"], "type-bold"],
  [["italic"], "type-italic"],
  [["text-height"], "text-paragraph"],
  [["text-width"], "text-paragraph"],
  [["align-left"], "text-left"],
  [["align-center"], "text-center"],
  [["align-right"], "text-right"],
  [["align-justify"], "justify"],
  [["indent-left"], "text-indent-left"],
  [["indent-right"], "text-indent-right"],

  // Remaining Bootstrap 2 Glyphicons
  // The original table covered the names django-suit's own templates used. Projects
  // upgrading from 0.2.x carry the rest in their own markup, where a name missing here
  // renders nothing at all -- silently, since an unmapped .icon-* still picks up the
  // bootstrap-icons font and simply has no glyph.
  [["glass"], "cup-straw"],
  [["music"], "music-note-beamed"],
  [["film"], "film"],
  [["th-large"], "grid-fill"],
  [["road"], "signpost-split"],
  [["download-alt"], "download"],
  [["inbox"], "inbox"],
  [["play-circle"], "play-circle"],
  [["repeat"], "arrow-repeat"],
  [["retweet"], "arrow-repeat"],
  [["list-alt"], "card-list"],
  [["flag"], "flag"],
  [["headphones"], "headphones"],
  [["qrcode"], "qr-code"],
  [["barcode"], "upc-scan"],
  [["book"], "book"],
  [["camera"], "camera"],
  [["font"], "fonts"],
  [["facetime-video"], "camera-video"],
  [["map-marker"], "geo-alt"],
  [["adjust"], "circle-half"],
  [["tint"], "droplet"],
  [["screenshot"], "crosshair"],
  [["minus"], "dash"],
  [["asterisk"], "asterisk"],
  [["gift"], "gift"],
  [["leaf"], "tree"],
  [["fire"], "fire"],
  [["plane"], "airplane"],
  [["random"], "shuffle"],
  [["magnet"], "magnet"],
  [["shopping-cart"], "cart"],
  [["hdd"], "hdd"],
  [["bullhorn"], "megaphone"],
  [["bell"], "bell"],
  [["certificate"], "award"],
  [["thumbs-up"], "hand-thumbs-up"],
  [["thumbs-down"], "hand-thumbs-down"],
  [["hand-right"], "hand-index"],
  [["hand-left"], "hand-index-fill"],
  [["hand-up"], "hand-index-thumb"],
  [["hand-down"], "hand-index-thumb-fill"],
  [["circle-arrow-right"], "arrow-right-circle"],
  [["circle-arrow-left"], "arrow-left-circle"],
  [["circle-arrow-up"], "arrow-up-circle"],
  [["circle-arrow-down"], "arrow-down-circle"],
  [["wrench"], "wrench"],
  [["tasks"], "list-task"],
  [["briefcase"], "briefcase"],
  [["fullscreen"], "fullscreen"],
  [["remove-sign"], "x-circle"],
  [["ok-sign"], "check-circle"],
  [["resize-vertical"], "arrows-expand"],
  [["resize-horizontal"], "arrows"],
];

// Table sort indicators, same lookup, different selector shape.
const SORTABLE = [
  ['sortable-up', 'arrow-up'],
  ['sortable-down', 'arrow-down'],
];

const icons = JSON.parse(fs.readFileSync(ICONS_JSON, 'utf8'));

const errors = [];
const seen = new Map();

function codepoint(name, where) {
  const cp = icons[name];
  if (cp === undefined) {
    errors.push(`unknown bootstrap-icons name "${name}" (used by ${where})`);
    return null;
  }
  return cp.toString(16).padStart(4, '0');
}

const body = [];
for (const entry of MAP) {
  if (typeof entry === 'string') {
    body.push('', `// ${entry}`);
    continue;
  }
  const [legacy, name] = entry;
  for (const l of legacy) {
    if (seen.has(l)) errors.push(`.icon-${l} mapped twice: bi-${seen.get(l)} and bi-${name}`);
    seen.set(l, name);
  }
  const cp = codepoint(name, legacy.map((l) => `.icon-${l}`).join(', '));
  if (cp === null) continue;
  const sel = legacy.map((l) => `.icon-${l}::before`).join(',\n');
  body.push(`${sel} { content: "\\${cp}"; } // bi-${name}`);
}

const sortable = SORTABLE.map(([cls, name]) => {
  const cp = codepoint(name, `.${cls}`);
  return cp === null ? null : `.${cls}::before { content: "\\${cp}"; } // bi-${name}`;
}).filter(Boolean);

if (errors.length) {
  console.error('Icon map is invalid:');
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

const version = JSON.parse(
  fs.readFileSync(path.join(__dirname, '..', 'node_modules', 'bootstrap-icons', 'package.json'), 'utf8')
).version;

const out = `// Icon Compatibility Layer
// Maps old Glyphicon classes to Bootstrap Icons
// Bootstrap Icons font must be loaded for this to work
//
// GENERATED FILE -- do not edit by hand.
// Edit the map in scripts/gen-icons-scss.js and run: npm run build:icons
// Generated against bootstrap-icons ${version}.

// Base icon styles - use Bootstrap Icons font
[class^="icon-"],
[class*=" icon-"] {
  font-family: "bootstrap-icons" !important;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: -0.125em;

  // Hide text for icon replacement
  &::before {
    display: inline-block;
  }
}

// Icon mappings: Glyphicons -> Bootstrap Icons
${body.join('\n').trim()}

// White icon variants (for dark backgrounds)
.icon-white {
  color: #fff;

  [data-bs-theme="dark"] & {
    color: var(--suit-text-color);
  }
}

// Sortable icons for tables
${sortable.join('\n')}

// Bootstrap Icons direct class aliases (for transition period)
// Users can also use bi-* classes directly
.bi {
  font-family: "bootstrap-icons" !important;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
`;

fs.writeFileSync(OUT, out);
console.log(`Wrote ${path.relative(process.cwd(), OUT)} (${seen.size} legacy classes, bootstrap-icons ${version})`);
