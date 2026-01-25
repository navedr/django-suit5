# Django Suit Requirements

## Project Overview

**Django Suit** is a modern theme/skin/extension for the Django admin interface. It provides a cleaner, more user-friendly alternative to the default Django admin appearance.

- **Version**: 0.2.28
- **Author**: Naved Rangwala (navedr)
- **Website**: http://djangosuit.com
- **Repository**: https://github.com/darklow/django-suit
- **License**: Creative Commons Attribution-NonCommercial 3.0

## Dependencies

### Required

- **Django**: 1.4 - 2.2

### Python Compatibility

- Python 2.5 - 3.8

## Installation

```bash
pip install django-suit==0.2.28
```

Then add `'suit'` to `INSTALLED_APPS` **before** `'django.contrib.admin'`:

```python
INSTALLED_APPS = (
    ...
    'suit',
    'django.contrib.admin',
)
```

## Features

- Modern Bootstrap v2.3.1-based admin theme
- Custom widgets (HTML5 inputs, AutosizedTextarea, LinkedSelect, EnclosedInput)
- Sortable drag-and-drop for change lists and inlines
- Form tabs for organizing fieldsets and inlines
- Form includes for embedding custom templates
- Customizable list row/cell attributes
- WYSIWYG editor integration support

## Supported Third-Party Apps

- django-cms (v2.3.5 - v2.4.3)
- django-filer (v0.9.4+)
- django-mptt
- django-reversion
- django-import-export

## Development Dependencies

For contributing or running tests:

- Bootstrap v2.3.1 CSS/JS (included in static files)
- LESS compiler (for stylesheet modifications)

---

# Bootstrap 5 Upgrade Requirements

## Objective

Upgrade from Bootstrap 2.3.1 to Bootstrap 5.x while maintaining the same user interface and experience. The admin theme should look and behave identically to users, but use modern Bootstrap 5 components under the hood.

## Current Bootstrap 2.3.1 Usage Analysis

### CSS Classes Currently Used

#### Buttons
| Current (BS 2.3.1) | Target (BS 5) | Occurrences |
|---|---|---|
| `.btn` | `.btn` | 49 |
| `.btn-primary` | `.btn-primary` | (same) |
| `.btn-info` | `.btn-info` | 22 |
| `.btn-danger` | `.btn-danger` | 6+ |
| `.btn-success` | `.btn-success` | 4+ |
| `.btn-warning` | `.btn-warning` | (same) |
| `.btn-large` | `.btn-lg` | 3+ |
| `.btn-small` | `.btn-sm` | 6+ |

#### Forms
| Current (BS 2.3.1) | Target (BS 5) | Notes |
|---|---|---|
| `.form-horizontal` | `.form-horizontal` (custom) | Keep custom implementation |
| `.form-inline` | `.d-inline-flex` or custom | 4+ occurrences |
| `.control-group` | `.mb-3` | 7+ occurrences |
| `.control-label` | `.form-label` | 10+ occurrences |
| `.controls` | Remove wrapper or `.col-*` | 8 occurrences |
| `.help-block` | `.form-text` | Block help text |
| `.help-inline` | `.form-text.d-inline` | Inline help text |
| `.input-append` | `.input-group` | Date/time pickers |
| `.add-on` | `.input-group-text` | Input addons |

#### Alerts
| Current (BS 2.3.1) | Target (BS 5) | Occurrences |
|---|---|---|
| `.alert` | `.alert` | 47 |
| `.alert-info` | `.alert-info` | 15+ |
| `.alert-error` | `.alert-danger` | 22+ |
| `.alert-warning` | `.alert-warning` | 3+ |
| `.alert-danger` | `.alert-danger` | 4+ |
| `.alert-block` | Remove (default behavior) | 14 |
| `data-dismiss="alert"` | `data-bs-dismiss="alert"` | JS attribute |

#### Tables
| Current (BS 2.3.1) | Target (BS 5) | Notes |
|---|---|---|
| `.table` | `.table` | 9+ occurrences |
| `.table-striped` | `.table-striped` | (same) |
| `.table-bordered` | `.table-bordered` | (same) |
| `.table-hover` | `.table-hover` | (same) |
| `.table-condensed` | `.table-sm` | 9+ occurrences |
| Row `.error` | `.table-danger` | Row context |
| Row `.warning` | `.table-warning` | Row context |
| Row `.info` | `.table-info` | Row context |
| Row `.success` | `.table-success` | Row context |

#### Navigation
| Current (BS 2.3.1) | Target (BS 5) | Notes |
|---|---|---|
| `.nav` | `.nav` | (same) |
| `.nav-tabs` | `.nav-tabs` | (same) |
| `.breadcrumb` | `.breadcrumb` | 18+ occurrences |
| `.pagination` | `.pagination` | (same) |

#### Utilities
| Current (BS 2.3.1) | Target (BS 5) | Notes |
|---|---|---|
| `.pull-left` | `.float-start` | Float utilities |
| `.pull-right` | `.float-end` | Float utilities |
| `.hide` | `.d-none` | Display utility |
| `.show` | `.d-block` | Display utility |
| `.muted` | `.text-muted` | Text utility |
| `.text-error` | `.text-danger` | Text color |
| `.clearfix` | `.clearfix` | (same, or use flexbox) |

### JavaScript Components

| Component | Current Usage | Migration Notes |
|---|---|---|
| Alert | Dismiss buttons | Update `data-dismiss` to `data-bs-dismiss` |
| Tabs | Custom implementation in `suit.js` | Keep custom, verify compatibility |
| Modal | Not actively used | No migration needed |
| Dropdown | Not actively used | No migration needed |
| Collapse | Custom CSS implementation | Keep custom |
| Tooltip | Not used | N/A |
| Popover | Not used | N/A |

### Icon System (Critical Migration)

**Current:** Glyphicons sprite-based icons (41 icon references)

Icons to migrate:
- `icon-home`, `icon-cog`, `icon-comment`, `icon-question-sign`
- `icon-chevron-right`, `icon-time`, `icon-eye-open`, `icon-repeat`
- `icon-trash`, `icon-pencil`, `icon-plus`, `icon-plus-sign`
- `icon-ok`, `icon-ok-sign`, `icon-bookmark`, `icon-lock`
- `icon-globe`, `icon-arrow-up`, `icon-arrow-left`, `icon-arrow-right`
- `icon-search`, `icon-upload`, `icon-picture`, `icon-white`

**Target:** Bootstrap Icons (SVG) or Font Awesome 6

## Migration Tasks

### Phase 1: Infrastructure Setup

- [ ] Add Bootstrap 5.3.x CSS and JS files to static directory
- [ ] Choose icon library (Bootstrap Icons recommended for consistency)
- [ ] Set up SCSS compilation (migrate from LESS to SCSS)
- [ ] Create CSS custom properties for theme variables
- [ ] Set up parallel development environment for testing

### Phase 2: Core CSS Migration

#### 2.1 Variables Migration (LESS → SCSS/CSS Variables)

Current LESS variables to convert:

```less
// Layout
@bgcolor: #EDEFF1;
@footer-bgcolor: #D5D7D8;
@bgcolor-light: #F6F7F8;
@text-color: #333;

// Colors
@grey: #999;
@red: #b94a48;
@blue: #08c;

// Header
@header-bgcolor-1: #3f4345;
@header-bgcolor-2: #373b3d;
@header-height: 45px;

// Dimensions
@left-column-width: 200px;
@right-column-width: 180px;
@padding: 20px;
@border-radius: 4px;
@border-color: #e7e7e7;
```

Target CSS custom properties:

```css
:root {
  --suit-bg-color: #EDEFF1;
  --suit-footer-bg: #D5D7D8;
  --suit-bg-light: #F6F7F8;
  --suit-text-color: #333;
  --suit-grey: #999;
  --suit-red: #b94a48;
  --suit-blue: #08c;
  --suit-header-bg-1: #3f4345;
  --suit-header-bg-2: #373b3d;
  --suit-header-height: 45px;
  --suit-left-column-width: 200px;
  --suit-right-column-width: 180px;
  --suit-padding: 20px;
  --suit-border-radius: 4px;
  --suit-border-color: #e7e7e7;
}
```

#### 2.2 Mixins Migration

| Current LESS Mixin | Target Approach |
|---|---|
| `.clearfix()` | Use BS5 `.clearfix` or flexbox |
| `.horizontal-gradient()` | Standard `linear-gradient()` |
| `.vertical-gradient()` | Standard `linear-gradient()` |
| `.box-sizing()` | Remove (default in BS5) |
| `.border-radius()` | Standard `border-radius` |
| `.box-shadow()` | Standard `box-shadow` |
| `.opacity()` | Standard `opacity` |

#### 2.3 Component Styling Files to Migrate

| File | Lines | Priority | Notes |
|---|---|---|---|
| `ui/form.less` | 705 | HIGH | Heavy customization |
| `ui/table.less` | 342 | HIGH | Table styling |
| `suit.less` | 207 | HIGH | Main layout |
| `header.less` | 90 | MEDIUM | Header bar |
| `ui/box.less` | 71 | MEDIUM | Box/well styling |
| `ui/breadcrumb.less` | 55 | MEDIUM | Breadcrumb nav |
| `ui/tabs.less` | 51 | MEDIUM | Tab styling |
| `ui/pagination.less` | 39 | LOW | Pagination |
| `footer.less` | 30 | LOW | Footer |
| `ui/left-nav.less` | - | MEDIUM | Left sidebar |
| `ui/login.less` | - | LOW | Login form |
| `ui/calendar.less` | - | LOW | Calendar widget |
| `ui/datepicker.less` | - | LOW | Date picker |

### Phase 3: Template Updates

#### 3.1 HTML Class Replacements

Search and replace across 64+ template files:

```
btn-large → btn-lg
btn-small → btn-sm
alert-error → alert-danger
table-condensed → table-sm
pull-left → float-start
pull-right → float-end
hide → d-none
show → d-block
data-dismiss= → data-bs-dismiss=
input-append → input-group
add-on → input-group-text
control-group → mb-3 (with restructuring)
```

#### 3.2 Form Structure Changes

**Before (BS 2.3.1):**
```html
<div class="control-group">
  <label class="control-label">Field</label>
  <div class="controls">
    <input type="text">
    <span class="help-inline">Help text</span>
  </div>
</div>
```

**After (BS 5):**
```html
<div class="mb-3">
  <label class="form-label">Field</label>
  <input type="text" class="form-control">
  <div class="form-text">Help text</div>
</div>
```

#### 3.3 Input Group Changes

**Before (BS 2.3.1):**
```html
<div class="input-append">
  <input type="text">
  <span class="add-on"><i class="icon-calendar"></i></span>
</div>
```

**After (BS 5):**
```html
<div class="input-group">
  <input type="text" class="form-control">
  <span class="input-group-text"><i class="bi bi-calendar"></i></span>
</div>
```

### Phase 4: Icon Migration

#### 4.1 Icon Mapping (Glyphicons → Bootstrap Icons)

| Glyphicon | Bootstrap Icon | Usage |
|---|---|---|
| `icon-home` | `bi-house` | Home navigation |
| `icon-cog` | `bi-gear` | Settings |
| `icon-comment` | `bi-chat` | Comments |
| `icon-question-sign` | `bi-question-circle` | Help |
| `icon-chevron-right` | `bi-chevron-right` | Navigation arrows |
| `icon-time` | `bi-clock` | Time fields |
| `icon-eye-open` | `bi-eye` | View action |
| `icon-repeat` | `bi-arrow-repeat` | Refresh/repeat |
| `icon-trash` | `bi-trash` | Delete action |
| `icon-pencil` | `bi-pencil` | Edit action |
| `icon-plus` | `bi-plus` | Add action |
| `icon-plus-sign` | `bi-plus-circle` | Add with circle |
| `icon-ok` | `bi-check` | Checkmark |
| `icon-ok-sign` | `bi-check-circle` | Checkmark with circle |
| `icon-bookmark` | `bi-bookmark` | Bookmark |
| `icon-lock` | `bi-lock` | Security/locked |
| `icon-globe` | `bi-globe` | Global/web |
| `icon-arrow-up` | `bi-arrow-up` | Up arrow |
| `icon-arrow-left` | `bi-arrow-left` | Left arrow |
| `icon-arrow-right` | `bi-arrow-right` | Right arrow |
| `icon-search` | `bi-search` | Search |
| `icon-upload` | `bi-upload` | Upload |
| `icon-picture` | `bi-image` | Image |
| `icon-calendar` | `bi-calendar` | Date picker |
| `icon-user` | `bi-person` | User |
| `icon-remove` | `bi-x` | Remove/close |

#### 4.2 Icon Implementation Change

**Before (Sprite-based):**
```html
<i class="icon-search"></i>
<i class="icon-search icon-white"></i>
```

**After (SVG/Font-based):**
```html
<i class="bi bi-search"></i>
<i class="bi bi-search text-white"></i>
```

### Phase 5: JavaScript Updates

#### 5.1 Bootstrap JS Migration

- [ ] Remove Bootstrap 2.3.1 JS
- [ ] Add Bootstrap 5.3.x JS bundle
- [ ] Update alert dismiss: `data-dismiss` → `data-bs-dismiss`
- [ ] Verify custom `suit.js` compatibility with jQuery + BS5

#### 5.2 jQuery Compatibility

- Current: jQuery 1.8.3 / 2.2.4
- Target: jQuery 3.x (or consider removing jQuery dependency)
- Bootstrap 5 does not require jQuery but custom code does

#### 5.3 Custom JS Functions to Verify

| Function | File | Notes |
|---|---|---|
| `Suit.after_inline()` | suit.js | Inline form callbacks |
| `$.fn.suit_fixed()` | suit.js | Fixed positioning |
| `$.fn.suit_search_filters()` | suit.js | Filter management |
| `$.fn.suit_linked_select()` | suit.js | Linked selects |
| `$.fn.suit_form_tabs()` | suit.js | Custom tabs |
| `$.fn.suit_form_debounce()` | suit.js | Form debouncing |

### Phase 6: Testing & Validation

#### 6.1 Visual Regression Testing

- [ ] Screenshot comparison of all admin pages before/after
- [ ] Verify header appearance matches original
- [ ] Verify left sidebar navigation matches original
- [ ] Verify form layouts match original
- [ ] Verify table appearances match original
- [ ] Verify button styles match original
- [ ] Verify alert/message styles match original

#### 6.2 Functional Testing

- [ ] All form submissions work correctly
- [ ] Inline form add/remove functionality
- [ ] Sortable drag-and-drop functionality
- [ ] Form tab switching
- [ ] Alert dismissal
- [ ] Search and filtering
- [ ] Pagination
- [ ] Date/time picker widgets

#### 6.3 Browser Compatibility

Target browsers (Bootstrap 5 supported):
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Note: IE11 support dropped (Bootstrap 5 requirement)

### Phase 7: Cleanup

- [ ] Remove Bootstrap 2.3.1 files
- [ ] Remove legacy LESS files (if fully migrated to SCSS)
- [ ] Remove Glyphicons sprite images
- [ ] Remove vendor prefixes from CSS
- [ ] Update documentation

## File Structure After Migration

```
suit/static/suit/
├── bootstrap5/
│   ├── css/
│   │   └── bootstrap.min.css (v5.3.x)
│   └── js/
│       └── bootstrap.bundle.min.js (v5.3.x)
├── icons/
│   └── bootstrap-icons.css (or SVG sprites)
├── scss/
│   ├── _variables.scss
│   ├── _mixins.scss
│   ├── suit.scss
│   ├── ui/
│   │   ├── _form.scss
│   │   ├── _table.scss
│   │   ├── _tabs.scss
│   │   └── ...
│   └── ...
├── css/
│   └── suit.css (compiled)
└── js/
    ├── jquery-3.x.min.js
    └── suit.js (updated)
```

## Risk Assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Visual differences | HIGH | Extensive visual regression testing |
| Form functionality breaks | HIGH | Unit tests for all form operations |
| Third-party app compatibility | MEDIUM | Test with django-cms, django-filer, etc. |
| IE11 users affected | LOW | Document browser requirements change |
| Custom JS breaks | MEDIUM | Thorough JS testing |

## Success Criteria

1. All admin pages render identically to current version (visual comparison)
2. All existing functionality works without regression
3. All automated tests pass
4. No console errors in supported browsers
5. Third-party app integrations continue to work
6. Performance equal or better than current version

