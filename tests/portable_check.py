"""Flags f-string constructs that are only legal on Python 3.12+ (backslash or same-quote reuse inside {}),
so the project also runs on Python 3.8-3.11. Run:  python tests/portable_check.py"""
import sys, tokenize, glob, os


def check(path):
    bad = []
    with open(path, 'rb') as fh:
        toks = list(tokenize.tokenize(fh.readline))
    stack = []
    for t in toks:
        inexpr = [f for f in stack if f['depth'] > 0]
        if t.type == tokenize.FSTRING_START:
            q = t.string[-1]
            if any(f['q'] == q for f in inexpr) or (inexpr and '\\' in t.string):
                bad.append((t.start[0], 'nested f-string reuses an enclosing quote'))
            stack.append({'q': q, 'depth': 0})
        elif t.type == tokenize.FSTRING_END:
            stack.pop()
        elif stack:
            top = stack[-1]
            if t.type == tokenize.OP and t.string == '{': top['depth'] += 1
            elif t.type == tokenize.OP and t.string == '}': top['depth'] -= 1
            elif t.type == tokenize.STRING and inexpr:
                if '\\' in t.string: bad.append((t.start[0], 'backslash inside f-string expression'))
                if any(f['q'] == t.string[-1] for f in inexpr): bad.append((t.start[0], 'string reuses an enclosing f-string quote'))
            elif t.type == tokenize.FSTRING_MIDDLE and '\\' in t.string and any(f['depth'] > 0 for f in stack[:-1]):
                bad.append((t.start[0], 'backslash in nested f-string inside expression'))
    return bad


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    total = 0
    for p in glob.glob(os.path.join(root, '**', '*.py'), recursive=True):
        for line, why in check(p):
            total += 1
            print(f"{os.path.relpath(p, root)}:{line}: {why}")
    print('OK: portable to Python 3.8+' if total == 0 else f'{total} problem(s)')
    sys.exit(1 if total else 0)
