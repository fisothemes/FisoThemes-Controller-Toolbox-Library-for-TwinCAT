"""
parse_plc.py  –  Parse TwinCAT PLC source files and emit Sphinx RST.

Reads the .plcproj to determine which files belong to which folder,
then parses each .TcPOU / .TcIO / .TcTLEO and writes one .rst per
source file plus index / toctree pages for each folder.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from textwrap import indent, dedent
from collections import defaultdict

# ── Paths ───────────────────────────────────────────────────────────────────
# Script lives alongside the .plcproj. All paths are derived from its location
# so the script works on any machine without editing.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJ_DIR   = SCRIPT_DIR

_candidates = list(PROJ_DIR.glob("*.plcproj"))
if not _candidates:
    sys.exit(f"ERROR: No .plcproj file found in {PROJ_DIR}")
PLCPROJ = _candidates[0]

# RST output goes into a 'docs' subfolder next to the script.
OUT_DIR = SCRIPT_DIR / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Folders we don't want in the public docs
SKIP_FOLDERS = {"Internal", "Version", "Project Information"}


# ── Helpers ─────────────────────────────────────────────────────────────────

def heading(text, char):
    return f"{text}\n{char * len(text)}\n"


def clean_doc(raw: str) -> str:
    """Strip (* *) delimiters and leading/trailing blank lines."""
    raw = raw.strip()
    raw = re.sub(r'^\(\*\s*', '', raw)
    raw = re.sub(r'\s*\*\)$', '', raw)
    # strip attribute lines
    lines = [l for l in raw.splitlines() if not l.strip().startswith('{attribute')]
    text = "\n".join(lines).strip()
    # :itf:`Name` is a LibDoc custom role — convert to inline code
    text = re.sub(r':itf:`([^`]+)`', r'``\1``', text)
    return text


def rst_safe(name: str) -> str:
    """Make a filesystem-safe name for RST files."""
    return re.sub(r'[^A-Za-z0-9_\-]', '_', name).lower()


def parse_declaration(decl: str):
    """
    Extract the docstring and signature from a CDATA declaration block.
    Returns (docstring, signature_line, vars).
    """
    decl = decl.strip()
    docstring = ""
    # Grab leading (* ... *) comment
    m = re.match(r'^\(\*(.*?)\*\)\s*', decl, re.DOTALL)
    if m:
        raw_doc = m.group(1).strip()
        # convert :itf: role
        raw_doc = re.sub(r':itf:`([^`]+)`', r'``\1``', raw_doc)
        docstring = raw_doc
        decl = decl[m.end():]
    # Strip attribute lines
    decl_lines = [l for l in decl.splitlines() if not l.strip().startswith('{')]
    signature = "\n".join(decl_lines).strip()
    return docstring, signature


def parse_var_line(line: str):
    """Parse   name : TYPE; // comment   → (name, type, comment)"""
    line = line.strip().rstrip(';')
    comment = ""
    if '//' in line:
        line, comment = line.split('//', 1)
        comment = comment.strip()
    # handle inline assignment e.g.  bInit : BOOL := TRUE
    line = re.sub(r'\s*:=.*$', '', line).strip()
    if ':' in line:
        name, typ = line.split(':', 1)
        return name.strip(), typ.strip(), comment
    return line.strip(), '', comment


def extract_var_block(decl: str, block_name: str):
    """Extract variables from a named VAR_xxx block."""
    pattern = rf'VAR_{block_name}\s*(.*?)END_VAR'
    m = re.search(pattern, decl, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    lines = m.group(1).splitlines()
    vars_ = []
    for l in lines:
        l = l.strip()
        if l and not l.startswith('{') and not l.startswith('//'):
            n, t, c = parse_var_line(l)
            if n:
                vars_.append((n, t, c))
    return vars_


def var_table(vars_, caption=""):
    if not vars_:
        return ""
    lines = []
    if caption:
        lines.append(f"**{caption}**\n")
    lines.append(".. list-table::")
    lines.append("   :header-rows: 1")
    lines.append("   :widths: 25 20 55")
    lines.append("")
    lines.append("   * - Name")
    lines.append("     - Type")
    lines.append("     - Description")
    for name, typ, desc in vars_:
        lines.append(f"   * - ``{name}``")
        lines.append(f"     - ``{typ}``" if typ else "     -")
        lines.append(f"     - {desc}" if desc else "     -")
    return "\n".join(lines) + "\n"


# ── RST generators ───────────────────────────────────────────────────────────

def rst_for_pou(name: str, xml_path: Path) -> str:
    """Generate RST for a .TcPOU file (FB, Function, GVL)."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Could be POU or GVL
    pou = root.find('POU')
    if pou is None:
        # Try GVL
        gvl = root.find('GVL')
        if gvl is not None:
            return rst_for_gvl(name, gvl)
        return f"{heading(name, '=')}\n*(No content)*\n"

    decl_el = pou.find('Declaration')
    decl_raw = decl_el.text if decl_el is not None else ""
    docstring, signature = parse_declaration(decl_raw)

    # Detect type
    fb_match = re.search(r'FUNCTION_BLOCK\s+(FINAL\s+)?(\S+)', signature)
    fn_match = re.search(r'FUNCTION\s+(\S+)\s*:', signature)
    if fb_match:
        kind = "Function Block"
    elif fn_match:
        kind = "Function"
    else:
        kind = "POU"

    rst = []
    rst.append(f".. _{name.lower()}:\n")
    rst.append(heading(f"{name} ({kind})", "="))

    if docstring:
        rst.append(docstring + "\n")

    # Signature block
    if signature:
        rst.append(".. code-block:: none\n")
        rst.append(indent(signature, "   ") + "\n")

    # Methods and properties
    methods    = pou.findall('Method')
    properties = pou.findall('Property')

    if properties:
        rst.append(heading("Properties", "-"))
        for prop in properties:
            pname = prop.get('Name', '')
            pdecl = prop.find('Declaration')
            pdoc, psig = parse_declaration(pdecl.text if pdecl is not None else "")
            rst.append(f".. _{name.lower()}.{pname.lower()}:\n")
            rst.append(heading(pname, "~"))
            # type from signature
            m = re.search(r'PROPERTY\s+\S+\s*:\s*(\S+)', psig)
            if m:
                rst.append(f"Type: ``{m.group(1)}``\n")
            if pdoc:
                rst.append(pdoc + "\n")

    if methods:
        rst.append(heading("Methods", "-"))
        for meth in methods:
            mname = meth.get('Name', '')
            if mname in ('FB_init',):
                label = 'Initialisation'
            else:
                label = mname
            mdecl = meth.find('Declaration')
            mdoc, msig = parse_declaration(mdecl.text if mdecl is not None else "")
            rst.append(f".. _{name.lower()}.{mname.lower()}:\n")
            rst.append(heading(label, "~"))
            if mdoc:
                rst.append(mdoc + "\n")
            # VAR_INPUT table
            inputs = extract_var_block(msig, 'INPUT')
            if inputs:
                rst.append(var_table(inputs, "Parameters") + "\n")

    return "\n".join(rst)


def rst_for_gvl(name: str, gvl_el) -> str:
    decl_el = gvl_el.find('Declaration')
    decl_raw = decl_el.text if decl_el is not None else ""
    docstring, sig = parse_declaration(decl_raw)
    rst = []
    rst.append(heading(f"{name} (GVL)", "="))
    if docstring:
        rst.append(docstring + "\n")
    if sig:
        rst.append(".. code-block:: none\n")
        rst.append(indent(sig, "   ") + "\n")
    return "\n".join(rst)


def rst_for_itf(name: str, xml_path: Path) -> str:
    """Generate RST for a .TcIO interface file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    itf = root.find('Itf')
    if itf is None:
        return heading(name, "=") + "\n*(No content)*\n"

    decl_el = itf.find('Declaration')
    decl_raw = decl_el.text if decl_el is not None else ""
    docstring, signature = parse_declaration(decl_raw)

    rst = []
    rst.append(f".. _{name.lower()}:\n")
    rst.append(heading(f"{name} (Interface)", "="))
    if docstring:
        rst.append(docstring + "\n")
    if signature:
        rst.append(".. code-block:: none\n")
        rst.append(indent(signature, "   ") + "\n")

    properties = itf.findall('Property')
    if properties:
        rst.append(heading("Properties", "-"))
        for prop in properties:
            pname = prop.get('Name', '')
            pdecl = prop.find('Declaration')
            pdoc, psig = parse_declaration(pdecl.text if pdecl is not None else "")
            rst.append(f".. _{name.lower()}.{pname.lower()}:\n")
            rst.append(heading(pname, "~"))
            m = re.search(r'PROPERTY\s+\S+\s*:\s*(\S+)', psig)
            if m:
                rst.append(f"Type: ``{m.group(1)}``\n")
            if pdoc:
                rst.append(pdoc + "\n")

    return "\n".join(rst)


def rst_for_enum(name: str, xml_path: Path) -> str:
    """Generate RST for a .TcTLEO enum file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    el = root.find('EnumerationTextList')
    if el is None:
        return heading(name, "=") + "\n*(No content)*\n"

    decl_el = el.find('Declaration')
    decl_raw = decl_el.text if decl_el is not None else ""
    docstring, sig = parse_declaration(decl_raw)

    # Parse members from the TYPE block
    members = []
    type_block = re.search(r'TYPE\s+\S+\s*:\s*\(\s*(.*?)\s*\)\w*;', sig, re.DOTALL)
    if type_block:
        for line in type_block.group(1).splitlines():
            line = line.strip().rstrip(',')
            if not line or line.startswith('//'):
                continue
            comment = ""
            if '//' in line:
                line, comment = line.split('//', 1)
                comment = comment.strip()
            # might be multi-line comment above the member
            m = re.match(r'(\w+)\s*:=\s*(\d+)', line)
            if m:
                members.append((m.group(1), m.group(2), comment))

    rst = []
    rst.append(f".. _{name.lower()}:\n")
    rst.append(heading(f"{name} (Enum)", "="))
    if docstring:
        rst.append(docstring + "\n")

    if members:
        rst.append(heading("Members", "-"))
        rst.append(".. list-table::")
        rst.append("   :header-rows: 1")
        rst.append("   :widths: 30 10 60")
        rst.append("")
        rst.append("   * - Name")
        rst.append("     - Value")
        rst.append("     - Description")
        for mname, mval, mdesc in members:
            rst.append(f"   * - ``{mname}``")
            rst.append(f"     - {mval}")
            rst.append(f"     - {mdesc}" if mdesc else "     -")
        rst.append("")

    return "\n".join(rst)


# ── Project metadata from generated files ────────────────────────────────────

def read_project_info(proj_dir: Path) -> dict:
    """
    Extract version, title, and company from the auto-generated TwinCAT files.
    Falls back to defaults if any file is missing.
    """
    info = {"version": "0.0.0", "title": "Library", "company": ""}

    # Version from Global_Version.TcGVL
    gvl_candidates = list(proj_dir.rglob("Global_Version.TcGVL"))
    if gvl_candidates:
        try:
            tree = ET.parse(gvl_candidates[0])
            decl = tree.find('.//Declaration')
            if decl is not None and decl.text:
                m = re.search(r"sVersion\s*:=\s*'([^']+)'", decl.text)
                if m:
                    info["version"] = m.group(1)
        except Exception:
            pass

    # Company and title from F_GetCompany / F_GetTitle implementations
    for fname, key in [("F_GetCompany.TcPOU", "company"), ("F_GetTitle.TcPOU", "title")]:
        candidates = list(proj_dir.rglob(fname))
        if candidates:
            try:
                tree = ET.parse(candidates[0])
                st = tree.find('.//ST')
                if st is not None and st.text:
                    m = re.search(r':=\s*"([^"]+)"', st.text)
                    if m:
                        info[key] = m.group(1)
            except Exception:
                pass

    return info


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Parse plcproj for folder → file mapping
    tree = ET.parse(PLCPROJ)
    ns = {'ms': 'http://schemas.microsoft.com/developer/msbuild/2003'}
    root = tree.getroot()

    # folder_files[folder] = [(name, relative_path)]
    folder_files = defaultdict(list)

    for compile_el in root.iter('{http://schemas.microsoft.com/developer/msbuild/2003}Compile'):
        inc = compile_el.get('Include', '')
        parts = inc.replace('\\', '/').split('/')
        if len(parts) < 2:
            continue
        # Top-level folder only (e.g. "Conditioning", "Signals\DUTs" → "Conditioning")
        top_folder = parts[0]
        if top_folder in SKIP_FOLDERS:
            continue
        filename = parts[-1]
        name = filename.rsplit('.', 1)[0]
        # sub-folder for DUTs / ITFs
        if len(parts) == 3:
            sub = parts[1]
        else:
            sub = None

        folder_key = f"{top_folder}/{sub}" if sub else top_folder
        # Use the full relative path from the plcproj (preserves subfolders on Windows)
        xml_path = PROJ_DIR / inc.replace('\\', '/').replace('/', os.sep)
        folder_files[folder_key].append((name, xml_path))

    # Generate RST files
    # Track top-level folders and their children for index toctrees
    top_folders = defaultdict(list)   # top → [folder_key]
    all_folder_keys = list(folder_files.keys())

    for folder_key in all_folder_keys:
        parts = folder_key.split('/')
        top = parts[0]
        top_folders[top].append(folder_key)

    # Write each file's RST
    for folder_key, items in folder_files.items():
        fparts = folder_key.split('/')
        top = fparts[0]
        sub  = fparts[1] if len(fparts) > 1 else None
        folder_out = OUT_DIR / rst_safe(top)
        if sub:
            folder_out = folder_out / rst_safe(sub)
        folder_out.mkdir(parents=True, exist_ok=True)

        for name, xml_path in items:
            ext = xml_path.suffix.lower()
            try:
                if ext == '.tcpou':
                    rst = rst_for_pou(name, xml_path)
                elif ext == '.tcio':
                    rst = rst_for_itf(name, xml_path)
                elif ext == '.tctleo':
                    rst = rst_for_enum(name, xml_path)
                else:
                    continue
            except Exception as e:
                print(f"  SKIP {name}: {e}")
                continue

            out_file = folder_out / f"{rst_safe(name)}.rst"
            out_file.write_text(rst, encoding='utf-8')
            print(f"  wrote {out_file.relative_to(OUT_DIR)}")

    # Write sub-folder index files (DUTs, ITFs)
    for folder_key, items in folder_files.items():
        fparts = folder_key.split('/')
        if len(fparts) < 2:
            continue
        top, sub = fparts[0], fparts[1]
        folder_out = OUT_DIR / rst_safe(top) / rst_safe(sub)
        entries = [rst_safe(name) for name, _ in items]
        idx = heading(sub, "=")
        idx += "\n.. toctree::\n   :maxdepth: 1\n\n"
        for e in entries:
            idx += f"   {e}\n"
        (folder_out / "index.rst").write_text(idx, encoding='utf-8')

    # Write top-level folder index files
    for top, folder_keys in top_folders.items():
        top_out = OUT_DIR / rst_safe(top)
        idx = heading(top, "=")
        idx += "\n.. toctree::\n   :maxdepth: 2\n\n"
        # direct files (no sub)
        direct = folder_files.get(top, [])
        for name, _ in direct:
            idx += f"   {rst_safe(name)}\n"
        # sub-folders
        for fk in folder_keys:
            if fk != top:
                sub = fk.split('/')[1]
                idx += f"   {rst_safe(sub)}/index\n"
        (top_out / "index.rst").write_text(idx, encoding='utf-8')

    # Read project metadata from the auto-generated TwinCAT files
    meta = read_project_info(PROJ_DIR)
    lib_title   = meta["title"]
    lib_version = meta["version"]
    lib_company = meta["company"]
    print(f"  project: {lib_title} v{lib_version} ({lib_company})")

    # Write conf.py so version stays in sync with Global_Version.TcGVL
    conf_lines = [
        f'project   = "{lib_title}"',
        f'author    = "{lib_company}"',
        f'copyright = "2026, {lib_company}"',
        f'version   = "{lib_version}"',
        f'release   = "{lib_version}"',
        '',
        'extensions = ["sphinx.ext.autosectionlabel"]',
        'autosectionlabel_prefix_document = True',
        'suppress_warnings = ["autosectionlabel.*"]',
        '',
        'html_theme = "sphinx_rtd_theme"',
        'html_title = f"{project} v{release}"',
        'html_theme_options = {',
        '    "light_css_variables": {',
        '        "color-brand-primary":  "#2563eb",',
        '        "color-brand-content":  "#1d4ed8",',
        '    },',
        '    "dark_css_variables": {',
        '        "color-brand-primary":  "#60a5fa",',
        '        "color-brand-content":  "#93c5fd",',
        '    },',
        '    "footer_icons": [],',
        '}',
        'html_show_sourcelink = False',
        'html_copy_source = False',
        'highlight_language = "none"',
    ]
    (OUT_DIR / "conf.py").write_text("\n".join(conf_lines) + "\n", encoding="utf-8")

    # Write root index.rst
    title_bar = "=" * len(lib_title)
    toc_entries = "".join(f"   {rst_safe(top)}/index\n" for top in sorted(top_folders.keys()))
    root_idx = (
        f"{lib_title}\n{title_bar}\n\n"
        "A library of composable building blocks for modelling and building control systems in TwinCAT.\n\n"
        f":Company: {lib_company}\n"
        f":Version: {lib_version}\n\n"
        ".. toctree::\n"
        "   :maxdepth: 2\n"
        "   :caption: Contents\n\n"
        + toc_entries
    )
    (OUT_DIR / "index.rst").write_text(root_idx, encoding="utf-8")
    print(f"\nDone. RST written to {OUT_DIR}")


if __name__ == '__main__':
    main()