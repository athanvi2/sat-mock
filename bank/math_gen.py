"""Math question generators. Every generator: g(rng, d, spr) -> dict(q, expl, type, choices/answer...)
d = 0/1/2 (easy/medium/hard); spr=True asks for a student-produced response when the answer is numeric.
Answers are COMPUTED, never typed by hand. Math uses \\( \\) delimiters so '$' can be a real dollar sign."""
import math
from fractions import Fraction as Fr


# ----------------------------------------------------------------------- formatting
def M(s): return '\\(' + s + '\\)'


KPI = M('k\\pi')
ELL = M('\\ell')


def tx(v):
    v = Fr(v)
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + f"\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def cx(a):
    a = Fr(a)
    return '' if a == 1 else ('-' if a == -1 else tx(a))


def sg(n): return f" + {n}" if n >= 0 else f" - {-n}"


def lin(a, b, var='x'):
    a, b = Fr(a), Fr(b)
    s = f"{cx(a)}{var}" if a != 0 else ''
    if b != 0 or a == 0:
        s = tx(b) if s == '' else s + ((' + ' + tx(b)) if b > 0 else (' - ' + tx(-b)))
    return s


def lin2(a, b): return f"{cx(a)}x" + (f" + {cx(b)}y" if b > 0 else f" - {cx(-b)}y")


def poly(*cs, var='x'):
    n, out = len(cs) - 1, ''
    for i, c in enumerate(cs):
        c, p = Fr(c), n - i
        if c == 0: continue
        body = tx(abs(c)) if (abs(c) != 1 or p == 0) else ''
        v = '' if p == 0 else (var if p == 1 else f"{var}^{{{p}}}")
        t = body + v
        out = (('-' if c < 0 else '') + t) if out == '' else out + (' - ' if c < 0 else ' + ') + t
    return out or '0'


def is_term(f):
    d = Fr(f).denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return d == 1


def dec(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else f"{float(f):.6f}".rstrip('0').rstrip('.')


def table(headers, rows, cls='dt'):
    h = ''.join(f'<th>{x}</th>' for x in headers)
    b = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


# ----------------------------------------------------------------------- answer builders
def mc(r, correct, wrongs):
    seen, opts = {correct}, []
    for w in wrongs:
        if w not in seen: seen.add(w); opts.append(w)
    if len(opts) < 3: raise ValueError('not enough distinct distractors')
    allo = [correct] + opts[:3]
    r.shuffle(allo)
    return dict(type='mc', choices=allo, answer='ABCD'[allo.index(correct)])


def numeric(r, ans, spr, wrongs=(), pre='', post='', frac=False):
    ans = Fr(ans)
    if spr:
        term = is_term(ans)
        return dict(type='spr', answer=dec(ans) if term else f"{ans.numerator}/{ans.denominator}",
                    value=float(ans), tol=1e-9 if term else 6e-4)

    def show(v):
        v = Fr(v)
        s = tx(v) if (frac or not is_term(v)) else dec(v)
        return M(pre + s + post) if (pre or post) else M(s)

    step = Fr(1) if ans.denominator == 1 else Fr(1, 2) if is_term(ans) and ans * 2 == int(ans * 2) else Fr(1)
    cand = [Fr(w) for w in wrongs] + [ans + step, ans - step, ans + 2 * step, ans - 2 * step, ans + 3 * step]
    seen, opts = {ans}, []
    for w in cand:
        if w not in seen: seen.add(w); opts.append(w)
    return mc(r, show(ans), [show(w) for w in opts])


def frac_res(r, n, d, wrongs, spr):
    """probability-style answer displayed as unreduced count fractions"""
    val = Fr(n, d)
    if spr: return numeric(r, val, True)
    ok, seen = [], {val}
    for a, b in wrongs:
        if b and Fr(a, b) not in seen: seen.add(Fr(a, b)); ok.append((a, b))
    fx = lambda a, b: M(f"\\frac{{{a}}}{{{b}}}")
    return mc(r, fx(n, d), [fx(a, b) for a, b in ok])


# ============================================================================ ALGEBRA
def lin_eq_1var(r, d, spr):
    if d == 0:
        a, x, b = r.randint(2, 9), r.randint(-9, 12), r.randint(-20, 20)
        c = a * x + b
        return dict(q=f"If {M(lin(a, b) + ' = ' + str(c))}, what is the value of {M('x')}?",
                    expl=f"Undo the constant: {a}x = {c - b}. Divide by {a}: x = {x}.",
                    **numeric(r, x, spr, [c - b, -x, Fr(c + b, a), x + 2]))
    if d == 1:
        a = r.randint(2, 6); c = r.choice([v for v in range(-4, 6) if v not in (0, a)])
        b = r.choice([v for v in range(-6, 7) if v != 0]); x = r.randint(-6, 9)
        dd = (a - c) * x + a * b
        return dict(q=f"In the equation {M(f'{a}(x{sg(b)}) = {lin(c, dd)}')}, what is the value of {M('x')}?",
                    expl=f"Distribute: {a}x + {a * b} = {lin(c, dd)}. Collect x terms: {a - c}x = {dd - a * b}, so x = {x}.",
                    **numeric(r, x, spr, [-x, x + 1, Fr(dd + a * b, a - c)]))
    if r.random() < .5:
        m, n, p = r.randint(2, 6), r.randint(2, 5), r.randint(1, 9)
        k = -m * p
        return dict(q=f"{M(f'{m}({n}x - {p}) = {m * n}x + k')}<br>In the given equation, k is a constant. If the equation has infinitely many solutions, what is the value of {M('k')}?",
                    expl=f"Distribute the left side: {m * n}x - {m * p}. The x-terms already match, so the constants must match: k = {k}.",
                    **numeric(r, k, spr, [m * p, m * n, -m * n]))
    a, b = Fr(r.choice([1, 2, 3, 5]), r.choice([2, 3, 4])), Fr(r.choice([1, 2, 3]), r.choice([2, 3, 4]))
    if a == b: b += 1
    x = r.randint(-8, 12); rr = r.randint(-6, 6); u = a * x + rr - b * x
    return dict(q=f"What is the solution to the equation {M(lin(a, rr) + ' = ' + lin(b, u))}?",
                expl=f"Collect x terms: ({tx(a - b)})x = {tx(u - rr)}. So x = {x}.",
                **numeric(r, x, spr, [-x, x + 1, x - 1]))


def lin_eq_2var(r, d, spr):
    if d == 0:
        p = r.choice([v for v in range(-8, 11) if v != 0]); a = r.randint(2, 7)
        b = r.choice([-1, 1]) * r.randint(2, 7); c = a * p
        eq = M(f"{cx(a)}x {'+' if b > 0 else '-'} {abs(b)}y = {c}")
        return dict(q=f"The graph of {eq} in the xy-plane crosses the x-axis at the point {M('(p, 0)')}. What is the value of {M('p')}?",
                    expl=f"On the x-axis y = 0, so {a}p = {c} and p = {p}.",
                    **numeric(r, p, spr, [c, -p, Fr(c, b) if b else 1]))
    if d == 1:
        who, i1, i2 = r.choice([("A school club", "posters", "banners"), ("A teacher", "notebooks", "binders"),
                                ("A caterer", "sandwich trays", "salad trays")])
        A, B = r.sample(range(3, 15), 2); x0, y0 = r.randint(2, 9), r.randint(2, 9); T = A * x0 + B * y0
        q = (f"{who} buys x {i1} at ${A} each and y {i2} at ${B} each, for a total of ${T}. The equation "
             f"{M(f'{A}x + {B}y = {T}')} represents this situation. Which is the best interpretation of {M(str(B))} in this context?")
        return dict(q=q, expl=f"{B}y is the money spent on the {i2}, and y counts {i2}, so {B} is the price of one of them.",
                    **mc(r, f"Each of the {i2} costs ${B}.", [f"Each of the {i1} costs ${B}.",
                                                              f"The number of {i2} purchased is {B}.",
                                                              f"The total cost of the {i2} is ${B}."]))
    a = r.randint(1, 4); s = r.choice([-4, -3, -2, 2, 3, 4, 5]); b = s * a
    c = r.randint(-12, 12); p, qq = r.randint(-5, 6), r.randint(-9, 9)
    ans = qq - s * p
    eq = M(f"{cx(a)}x {'+' if b > 0 else '-'} {abs(b)}y = {c}"); pt = M(f'({p}, {qq})')
    return dict(q=(f"Line {ELL} has equation {eq}. Line {M('m')} is perpendicular to line {ELL} and passes through the point {pt}. "
                   f"At what y-value does line {M('m')} cross the y-axis?"),
                expl=f"Slope of \\(\\ell\\) is {tx(Fr(-a, b))}, so the perpendicular slope is {s}. Then y = {s}x + b through ({p}, {qq}) gives b = {qq} - ({s})({p}) = {ans}.",
                **numeric(r, ans, spr, [qq + s * p, -ans, qq, Fr(-a, b)]))


CTXF = [("the total cost", "guest", lambda v: f"${v}", "the total cost, in dollars, to host a party for x guests"),
        ("the seedling's height", "week", lambda v: f"{v} centimeters", "the height, in centimeters, of a seedling x weeks after it was planted"),
        ("the amount of water in the tank", "minute", lambda v: f"{v} liters", "the amount of water, in liters, in a tank x minutes after a hose is turned on")]


def lin_functions(r, d, spr):
    if d == 0:
        m, b, n, c, t, k = r.randint(2, 9), r.randint(-9, 12), r.randint(2, 9), r.randint(-9, 12), r.randint(2, 6), r.randint(2, 5)
        ans = k * (m * t + b) - (n * t + c)
        return dict(q=f"If {M(f'f(x) = {lin(m, b)}')} and {M(f'g(x) = {lin(n, c)}')}, what is the value of {M(f'{k}f({t}) - g({t})')}?",
                    expl=f"f({t}) = {m * t + b} and g({t}) = {n * t + c}. Then {k}({m * t + b}) - {n * t + c} = {ans}.",
                    **numeric(r, ans, spr, [(m * t + b) - (n * t + c), k * m * t + b - (n * t + c), ans + k, -ans]))
    if d == 1:
        noun, unit, fm, desc = r.choice(CTXF); m, b = r.randint(3, 45), r.randint(10, 200)
        if r.random() < .5:
            good = f"Each additional {unit} increases {noun} by {fm(m)}."
            bad = [f"{noun.capitalize()} is {fm(m)} when x = 0.", f"After {m} {unit}s, {noun} is {fm(b)}.", f"Each additional {unit} decreases {noun} by {fm(m)}."]
            ask, ex = m, "The slope is the change in f(x) for each 1-unit increase in x."
        else:
            good = f"When x = 0, {noun} is {fm(b)}."
            bad = [f"Each additional {unit} increases {noun} by {fm(b)}.", f"{noun.capitalize()} is {fm(m)} when x = 0.", f"After {b} {unit}s, {noun} is {fm(m)}."]
            ask, ex = b, "The constant term is the value of f(x) when x = 0 (the starting amount)."
        return dict(q=f"The function {M(f'f(x) = {m}x + {b}')} gives {desc}. Which is the best interpretation of {M(str(ask))} in this context?",
                    expl=ex, **mc(r, good, bad))
    s = r.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6]); t = r.randint(-9, 12)
    x1 = r.randint(0, 4); x2 = x1 + r.randint(2, 5); x0 = r.randint(-5, 12)
    return dict(q=f"The function g is linear. {M(f'g({x1}) = {s * x1 + t}')} and {M(f'g({x2}) = {s * x2 + t}')}. For what value of {M('x')} does {M(f'g(x) = {s * x0 + t}')}?",
                expl=f"Slope = ({s * x2 + t} - {s * x1 + t}) / ({x2} - {x1}) = {s}. Then solve {s}x + {t} = {s * x0 + t}: x = {x0}.",
                **numeric(r, x0, spr, [-x0, s * x0 + t, x0 + 1, x0 - 1]))


def systems_2lin(r, d, spr):
    if d == 0:
        while True:
            x0, y0 = r.randint(-5, 9), r.randint(-5, 9)
            a1, b1, a2, b2 = [r.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(4)]
            if a1 * b2 - a2 * b1 != 0: break
        c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
        which = r.choice(['x', 'y', 'x + y'])
        ans = {'x': x0, 'y': y0, 'x + y': x0 + y0}[which]
        return dict(q=f"{M(lin2(a1, b1) + ' = ' + str(c1))}<br>{M(lin2(a2, b2) + ' = ' + str(c2))}<br>The solution to the given system of equations is {M('(x, y)')}. What is the value of {M(which)}?",
                    expl=f"Solving by elimination or substitution gives x = {x0} and y = {y0}.",
                    **numeric(r, ans, spr, [x0, y0, x0 - y0, x0 + y0 + 1, -ans]))
    if d == 1:
        venue, things, k1, k2 = r.choice([("theater", "tickets", "adult", "student"), ("bakery", "boxes", "small", "large"), ("farm stand", "baskets", "apple", "peach")])
        p1, p2 = r.sample(range(4, 30), 2); n1, n2 = r.randint(10, 60), r.randint(10, 60)
        return dict(q=(f"A {venue} sold {n1 + n2} {things} in one day. The {k1} {things} cost ${p1} each and the {k2} {things} cost ${p2} each, "
                       f"for a total of ${p1 * n1 + p2 * n2}. How many {k2} {things} were sold?"),
                    expl=f"Let a = {k1}, s = {k2}. a + s = {n1 + n2} and {p1}a + {p2}s = {p1 * n1 + p2 * n2}. Solving gives s = {n2}.",
                    **numeric(r, n2, spr, [n1, n1 + n2, abs(n1 - n2)]))
    a, b, m, c = r.randint(2, 6), r.randint(2, 6), r.choice([2, 3, 4]), r.randint(2, 20)
    if r.random() < .5:
        dd = m * c + r.choice([-5, -3, 3, 7])
        return dict(q=f"{M(f'{a}x + {b}y = {c}')}<br>{M(f'kx + {m * b}y = {dd}')}<br>In the given system of equations, k is a constant. If the system has no solution, what is the value of {M('k')}?",
                    expl=f"The second y-coefficient is {m} times the first, so for parallel lines k must be {m}\u00b7{a} = {m * a} (and the constants are not in the same ratio).",
                    **numeric(r, m * a, spr, [a * m + 1, m, a, m * b]))
    return dict(q=f"{M(f'{a}x + {b}y = {c}')}<br>{M(f'{m * a}x + {m * b}y = k')}<br>In the given system of equations, k is a constant. If the system has infinitely many solutions, what is the value of {M('k')}?",
                expl=f"The second equation must be {m} times the first, so k = {m}\u00b7{c} = {m * c}.",
                **numeric(r, m * c, spr, [c + m, m, c, m * c + a]))


def lin_ineq(r, d, spr):
    if d == 0:
        a, b = r.randint(2, 9), r.randint(-12, 12); strict = r.random() < .5
        c = a * r.randint(2, 9) + b + r.choice([0, 0, 1, 2]); bound = Fr(c - b, a)
        ans = math.ceil(bound) - 1 if strict else math.floor(bound)
        sym = '<' if strict else '\\le'
        rel_ = '<' if strict else '\u2264'
        return dict(q=f"What is the greatest integer value of {M('x')} that satisfies {M(lin(a, b) + ' ' + sym + ' ' + str(c))}?",
                    expl=f"x {rel_} {tx(bound)}, so the greatest integer is {ans}.",
                    **numeric(r, ans, spr, [ans + 1, ans - 1, math.ceil(bound), math.floor(bound) + 1]))
    if d == 1:
        n, p, q_, B = r.randint(3, 9), r.choice([2, 3, 4, 5]), r.randint(6, 15), r.randint(60, 120)
        good = f"{q_}x + {p * n} \\le {B}"
        return dict(q=(f"Maria has ${B} to spend at a stationery store. She buys {n} notebooks that cost ${p} each and then wants to buy pens that cost ${q_} each. "
                       f"She can spend at most ${B} in total. Which inequality represents this situation, where x is the number of pens?"),
                    expl=f"Pens cost {q_}x, notebooks cost {p * n}; the total must be at most {B}.",
                    **mc(r, M(good), [M(f"{p}x + {q_ * n} \\le {B}"), M(f"{q_}x + {p * n} \\ge {B}"), M(f"{q_}x + {p * n} < {B}")]))
    for _ in range(200):
        m1, b1, m2, b2 = r.randint(-3, 3), r.randint(-6, 6), r.randint(-3, 3), r.randint(-6, 6)
        ok = lambda x, y: y > m1 * x + b1 and y <= m2 * x + b2
        pts = [(r.randint(-8, 8), r.randint(-8, 8)) for _ in range(300)]
        good = [p for p in pts if ok(*p)]; bad = []
        for p in pts:
            if not ok(*p) and p not in bad: bad.append(p)
        if good and len(bad) >= 3: break
    g = good[0]; w = bad[:3]
    f = lambda p: M(f"({p[0]}, {p[1]})")
    i1 = M(f'y > {lin(m1, b1)}'); i2 = M(f'y \\le {lin(m2, b2)}')
    return dict(q=f"{i1}<br>{i2}<br>Which point {M('(x, y)')} is a solution to the given system of inequalities in the xy-plane?",
                expl=f"Substitute each point into BOTH inequalities. Only {f(g)} makes both true.",
                **mc(r, f(g), [f(p) for p in w]))


# ============================================================================ ADVANCED MATH
def equiv_expr(r, d, spr):
    if d == 0:
        p, q = r.randint(2, 5), r.randint(2, 5); a, b, c, dd = r.randint(1, 5), r.randint(-6, 6), r.randint(1, 5), r.randint(-6, 6)
        A, B = p * a + q * c, p * b + q * dd
        return dict(q=f"Which expression is equivalent to {M(f'{p}({lin(a, b)}) + {q}({lin(c, dd)})')}?",
                    expl=f"Distribute: {lin(p * a, p * b)} + {lin(q * c, q * dd)} = {lin(A, B)}.",
                    **mc(r, M(lin(A, B)), [M(lin(A, b + dd)), M(lin(A, p * b - q * dd)), M(lin(p * a - q * c, B)), M(lin(A + 1, B)), M(lin(A, B + 1)), M(lin(A, B - 1))]))
    if d == 1:
        a, c = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3)])
        b, dd = r.sample([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 2)
        ex = lambda a, b, c, d: (a * c, a * d + b * c, b * d)
        fac = lambda a, b, c, d: f"({lin(a, b)})({lin(c, d)})"
        right = ex(a, b, c, dd); cands = [(a, -b, c, -dd), (a, dd, c, b), (a, b, c, -dd), (a, -b, c, dd), (a, b + 1, c, dd), (a, b, c, dd + 1), (a, b - 1, c, dd - 1)]
        wrongs, seen = [], {right}
        for t in cands:
            if ex(*t) not in seen: seen.add(ex(*t)); wrongs.append(M(fac(*t)))
        return dict(q=f"Which expression is equivalent to {M(poly(*right))}?",
                    expl=f"Find two binomials whose product is {poly(*right)}: {fac(a, b, c, dd)}. Multiply back with FOIL to check.",
                    **mc(r, M(fac(a, b, c, dd)), wrongs))
    while True:
        p, s, qq, rr, t = r.randint(2, 7), r.randint(1, 5), r.choice([1, 2, 3, 4]), r.randint(1, 6), r.randint(1, 6)
        N1, N0 = p - s * qq, p * t + s * rr
        if N1 != 0: break
    den = f"({lin(qq, -rr)})({lin(1, t)})"; fx = lambda n: M(f"\\frac{{{n}}}{{{den}}}")
    ex_ = M(f'\\frac{{{p}}}{{{lin(qq, -rr)}}} - \\frac{{{s}}}{{{lin(1, t)}}}')
    return dict(q=f"Which expression is equivalent to {ex_}?",
                expl=f"Use the common denominator {den}. Numerator: {p}({lin(1, t)}) - {s}({lin(qq, -rr)}) = {poly(N1, N0)}.",
                **mc(r, fx(poly(N1, N0)), [fx(poly(N1, p * t - s * rr)), fx(poly(p - s * qq, -N0)), fx(poly(p + s * qq, N0)), fx(poly(p - s, N0))]))


def nonlin_eq_sys(r, d, spr):
    if d == 0:
        p, q = r.sample(range(-6, 9), 2)
        return dict(q=f"What is the greater solution of the equation {M(poly(1, -(p + q), p * q) + ' = 0')}?",
                    expl=f"Factor: (x - {p})(x - {q}) = 0, so the solutions are {p} and {q}.",
                    **numeric(r, max(p, q), spr, [min(p, q), p + q, p * q, -max(p, q)]))
    if d == 1:
        if r.random() < .5:
            p, qq = r.randint(1, 4), r.randint(1, 5)
            a, c, b = p * p, qq * qq, 2 * p * qq
            eq_ = M(f'{a}x^2 + bx + {c} = 0')
            return dict(q=f"The equation {eq_} has exactly one real solution, where b is a positive constant. What is the value of {M('b')}?",
                        expl=f"One solution means the discriminant is 0: b\u00b2 - 4({a})({c}) = 0, so b\u00b2 = {b * b} and b = {b}.",
                        **numeric(r, b, spr, [p * qq, a + c, 2 * b, b * b]))
        a, b = r.randint(1, 4), r.randint(-6, 6)
        t = r.choice([-1, 0, 1]); c = (b * b // (4 * a)) + (t * r.randint(1, 4)); disc = b * b - 4 * a * c
        ans = 'Zero' if disc < 0 else 'Exactly one' if disc == 0 else 'Exactly two'
        return dict(q=f"How many distinct real solutions does the equation {M(poly(a, b, c) + ' = 0')} have?",
                    expl=f"Discriminant = {b}\u00b2 - 4({a})({c}) = {disc}. {'Negative: no real solutions.' if disc < 0 else 'Zero: one solution.' if disc == 0 else 'Positive: two solutions.'}",
                    **mc(r, ans, [o for o in ['Zero', 'Exactly one', 'Exactly two', 'Infinitely many'] if o != ans]))
    if r.random() < .5:
        b, k = r.randint(2, 6), r.randint(2, 5); a = k * k - k - b
        eq_ = M(f'\\sqrt{{{lin(1, a)}}} = x - {b}')
        return dict(q=f"What is the solution to the equation {eq_}?",
                    expl=f"Square both sides: x{sg(a)} = (x - {b})\u00b2. Solve: x = {b + k} or x = {b + 1 - k}. Check: only x = {b + k} works; the other is extraneous.",
                    **numeric(r, b + k, spr, [b + 1 - k, b, 2 * b + 1, k]))
    p, q = r.sample(range(-5, 8), 2); b, n = r.randint(-5, 5), r.randint(-6, 6); m = b + p + q; c = n + p * q
    return dict(q=f"{M(f'y = {poly(1, b, c)}')}<br>{M(f'y = {lin(m, n)}')}<br>The graphs of the two equations intersect at two points in the xy-plane. What is the sum of the x-coordinates of these points?",
                expl=f"Set the y's equal: {poly(1, b - m, c - n)} = 0. The sum of the roots is -(b - m) = {p + q}.",
                **numeric(r, p + q, spr, [p * q, -(p + q), m, c - n]))


def nonlin_functions(r, d, spr):
    if d == 0:
        h, k = r.randint(-7, 8), r.randint(-15, 15); ask_x = r.random() < .4
        return dict(q=f"The function {M(f'f(x) = (x{sg(-h)})^2{sg(k)}')} is graphed in the xy-plane. What is the {'x-value at which f has its minimum' if ask_x else 'minimum value of f'}?",
                    expl=f"In vertex form (x - h)\u00b2 + k the vertex is (h, k) = ({h}, {k}), and the parabola opens upward.",
                    **numeric(r, h if ask_x else k, spr, [k if ask_x else h, -h, -k, h + k]))
    if d == 1:
        t = r.random()
        if t < .34:
            h, k = r.choice([v for v in range(-6, 8) if v]), r.randint(-20, 20)
            return dict(q=f"What is the minimum value of the function {M(f'f(x) = {poly(1, -2 * h, h * h + k)}')}?",
                        expl=f"Complete the square: x\u00b2 {sg(-2 * h)}x {sg(h * h + k)} = (x{sg(-h)})\u00b2 {sg(k)}. Minimum = {k}.",
                        **numeric(r, k, spr, [h, -h, h * h + k, -k]))
        if t < .67:
            grow = r.random() < .5; pct = r.choice([10, 20, 25, 50]); n = r.choice([2, 3]); a = r.choice([200, 400, 500, 1000, 2000])
            mult = Fr(100 + pct if grow else 100 - pct, 100); v = a * mult ** n
            q = (f"A social media account has {a} followers and gains {pct}% more followers each month. How many followers will it have after {n} months?" if grow
                 else f"A machine is worth ${a} and loses {pct}% of its value each year. What is the value of the machine, in dollars, after {n} years?")
            return dict(q=q, expl=f"Multiply by {dec(mult)} each period: {a} \u00d7 {dec(mult)}^{n} = {dec(v)}.",
                        **numeric(r, v, spr, [a * (1 + (pct if grow else -pct) * n / Fr(100)), a * mult ** (n - 1), a * mult ** (n + 1)]))
        p, q = r.sample(range(-8, 9), 2)
        return dict(q=f"The function {M(f'f(x) = {poly(1, -(p + q), p * q)}')} is given. Which of the following is an equivalent form of f in which the zeros of f appear as constants or coefficients?",
                    expl=f"Factored form (x - {p})(x - {q}) shows the zeros {p} and {q} directly.",
                    **mc(r, M(f"f(x) = (x{sg(-p)})(x{sg(-q)})"), [M(f"f(x) = (x{sg(p)})(x{sg(q)})"), M(f"f(x) = x(x{sg(-(p + q))}) {sg(p * q)}"),
                                                                    M(f"f(x) = (x{sg(-Fr(p + q, 2))})^2 {sg(p * q - Fr((p + q) ** 2, 4))}")]))
    if r.random() < .5:
        a, b = r.choice([2, 3, 4, 5]), r.randint(1, 12)
        return dict(q=f"The function h is defined by {M('h(x) = a^x + b')}, where a and b are positive constants. The graph of {M('y = h(x)')} passes through the points {M(f'(0, {1 + b})')} and {M(f'(2, {a * a + b})')}. What is the value of {M('ab')}?",
                    expl=f"h(0) = 1 + b = {1 + b}, so b = {b}. h(2) = a\u00b2 + {b} = {a * a + b}, so a\u00b2 = {a * a} and a = {a}. ab = {a * b}.",
                    **numeric(r, a * b, spr, [a * a * b, a + b, a * a, b]))
    h, k, p, q = r.randint(-4, 5), r.randint(-6, 6), r.choice([-4, -3, -2, 2, 3, 4]), r.choice([-5, -3, -2, 2, 3, 5])
    v = lambda a, b: M(f"({a}, {b})")
    return dict(q=f"The function f is a parabola with vertex {M(f'({h}, {k})')}. The function g is defined by {M(f'g(x) = f(x{sg(-p)}){sg(q)}')}. What is the vertex of the graph of g?",
                expl=f"f(x {'-' if p > 0 else '+'} {abs(p)}) shifts the graph {'right' if p > 0 else 'left'} {abs(p)}, and adding {q} shifts it {'up' if q > 0 else 'down'} {abs(q)}: ({h + p}, {k + q}).",
                **mc(r, v(h + p, k + q), [v(h - p, k + q), v(h + p, k - q), v(h - p, k - q)]))


# ============================================================================ PROBLEM SOLVING & DATA ANALYSIS
def ratios_rates(r, d, spr):
    if d == 0:
        what, unit = r.choice([("bottles", "minutes"), ("pages", "minutes"), ("miles", "hours")]); rate = r.randint(3, 20)
        t1, t2 = r.randint(3, 9), r.randint(10, 40)
        return dict(q=f"A machine produces {rate * t1} {what} in {t1} {unit}. At this rate, how many {what} will it produce in {t2} {unit}?",
                    expl=f"Rate = {rate} {what} per {unit[:-1]}. {rate} \u00d7 {t2} = {rate * t2}.",
                    **numeric(r, rate * t2, spr, [rate * t1 + t2, t2 // t1 * rate, rate * t2 + rate, rate * (t2 - t1)]))
    if d == 1:
        if r.random() < .5:
            k = r.randint(1, 8); v = 18 * k
            return dict(q=f"A cyclist rides at a constant speed of {v} kilometers per hour. What is the cyclist's speed, in meters per second?",
                        expl=f"{v} km/h \u00d7 1000 m/km \u00f7 3600 s/h = {5 * k} m/s.",
                        **numeric(r, 5 * k, spr, [Fr(v * 60, 1000), Fr(v, 60), 50 * k, v * 6]))
        a, b = r.sample(range(2, 8), 2)
        if math.gcd(a, b) != 1: b += 1
        tot = (a + b) * r.randint(4, 12)
        return dict(q=f"A paint mixture uses {a} parts blue paint for every {b} parts yellow paint. How many liters of blue paint are needed to make {tot} liters of the mixture?",
                    expl=f"Blue is {a} of every {a + b} parts: {tot} \u00d7 {a}/{a + b} = {tot * a // (a + b)}.",
                    **numeric(r, tot * a // (a + b), spr, [tot * b // (a + b), tot - a, tot // a, tot * a // b]))
    r1, r2, t = r.randint(10, 30), r.randint(10, 30), r.randint(4, 15); N = (r1 + r2) * t
    return dict(q=f"One printer prints {r1} pages per minute and a second printer prints {r2} pages per minute. Working together at these rates, how many minutes will they take to print {N} pages?",
                expl=f"Combined rate = {r1} + {r2} = {r1 + r2} pages per minute. {N} \u00f7 {r1 + r2} = {t} minutes.",
                **numeric(r, t, spr, [Fr(N, r1), Fr(N, r2), Fr(N, r1) + Fr(N, r2), t + 2]))


def percentages(r, d, spr):
    if d == 0:
        if r.random() < .5:
            p, N = r.choice([5, 10, 15, 20, 25, 30, 35, 40, 60, 75]), r.choice([40, 80, 120, 160, 200, 240, 400])
            return dict(q=f"What is {p}% of {N}?", expl=f"{p}/100 \u00d7 {N} = {Fr(p * N, 100)}.",
                        **numeric(r, Fr(p * N, 100), spr, [Fr(N, p), N - p, Fr(p * N, 10)]))
        w, p = r.choice([40, 60, 80, 120, 200]), r.choice([10, 20, 25, 30, 40])
        return dict(q=f"A jacket originally priced at ${w} is on sale for {p}% off. What is the sale price, in dollars?",
                    expl=f"Multiply by (1 - {p}/100): {w} \u00d7 {dec(Fr(100 - p, 100))} = {dec(w * Fr(100 - p, 100))}.",
                    **numeric(r, w * Fr(100 - p, 100), spr, [w * Fr(p, 100), w - p, w + w * Fr(p, 100)]))
    if d == 1:
        w, m, dp = r.choice([40, 60, 80, 120, 200]), r.choice([20, 25, 40, 50]), r.choice([10, 20, 25])
        v = w * Fr(100 + m, 100) * Fr(100 - dp, 100)
        return dict(q=f"A store buys a lamp for ${w} and marks up the price by {m}%. During a sale, the store discounts the marked-up price by {dp}%. What is the sale price of the lamp, in dollars?",
                    expl=f"{w} \u00d7 {dec(Fr(100 + m, 100))} \u00d7 {dec(Fr(100 - dp, 100))} = {dec(v)}.",
                    **numeric(r, v, spr, [w * Fr(100 + m - dp, 100), w * Fr(100 + m, 100), w * Fr(100 - dp, 100)]))
    if r.random() < .5:
        p, o = r.choice([10, 15, 20, 25, 40]), r.choice([400, 800, 1000, 2000, 4000]); new = o * Fr(100 + p, 100)
        return dict(q=f"After a {p}% increase, the population of a town was {dec(new)}. What was the population before the increase?",
                    expl=f"New = old \u00d7 {dec(Fr(100 + p, 100))}, so old = {dec(new)} \u00f7 {dec(Fr(100 + p, 100))} = {o}.",
                    **numeric(r, o, spr, [new * Fr(100 - p, 100), new - p, new - new * Fr(p, 100)]))
    a, b = r.choice([10, 20, 25, 50]), r.choice([20, 30, 40, 50])
    tot = (Fr(100 + a, 100) * Fr(100 + b, 100) - 1) * 100
    return dict(q=f"The price of a stock increased by {a}% in the first year and then increased by {b}% of its new value in the second year. By what percent did the price increase over the two years?",
                expl=f"{dec(Fr(100 + a, 100))} \u00d7 {dec(Fr(100 + b, 100))} = {dec(tot / 100 + 1)}, an overall increase of {dec(tot)}%.",
                **numeric(r, tot, spr, [a + b, (a + b) / Fr(2), a * b, tot + 10], post='%'))


def one_var_data(r, d, spr):
    if d == 0:
        n = r.choice([7, 9]); xs = [r.randint(2, 40) for _ in range(n)]; s = sorted(xs)
        if r.random() < .5:
            return dict(q=f"The data set {M(', '.join(map(str, xs)))} is given. What is the median of the data set?",
                        expl=f"Sorted: {', '.join(map(str, s))}. The middle value is {s[n // 2]}.",
                        **numeric(r, s[n // 2], spr, [xs[n // 2], Fr(sum(xs), n), s[n // 2 - 1], s[n // 2 + 1]]))
        xs = [r.randint(2, 30) for _ in range(5)]; xs[-1] += (5 - sum(xs) % 5) % 5
        return dict(q=f"The data set {M(', '.join(map(str, xs)))} is given. What is the mean of the data set?",
                    expl=f"Sum = {sum(xs)}, and {sum(xs)} \u00f7 5 = {sum(xs) // 5}.",
                    **numeric(r, sum(xs) // 5, spr, [sorted(xs)[2], max(xs) - min(xs), sum(xs) // 5 + 1]))
    if d == 1:
        n, m, m2 = r.randint(4, 8), r.randint(12, 40), r.randint(13, 45)
        if m2 == m: m2 += 1
        x = (n + 1) * m2 - n * m
        return dict(q=f"The mean of {n} numbers is {m}. A new number is added, and the mean of all {n + 1} numbers is {m2}. What is the value of the new number?",
                    expl=f"New sum = {n + 1} \u00d7 {m2} = {(n + 1) * m2}; old sum = {n} \u00d7 {m} = {n * m}. The new number is {x}.",
                    **numeric(r, x, spr, [m2, m2 - m, (n + 1) * m2, n * m2 - n * m]))
    A = sorted(r.sample(range(5, 40), 6))
    if r.random() < .5:
        k = r.choice([5, 10, 20]); B = [v + k for v in A]; right = 1
        why = f"Adding {k} to every value shifts the mean up by {k} but does not change how spread out the data is, so the standard deviation stays the same."
        desc = f"Data set B is created by adding {k} to each value in data set A"
    else:
        k = r.choice([2, 3]); B = [v * k for v in A]; right = 0
        why = f"Multiplying every value by {k} multiplies the mean by {k} and also stretches the spread, so the standard deviation is {k} times as large."
        desc = f"Data set B is created by multiplying each value in data set A by {k}"
    S = ["The mean and the standard deviation of B are both greater than those of A.",
         "The mean of B is greater than the mean of A, but the standard deviations of A and B are equal.",
         "The mean of B equals the mean of A, but the standard deviation of B is greater.",
         "The mean and the standard deviation of A and B are equal."]
    return dict(q=f"Data set A: {M(', '.join(map(str, A)))}<br>{desc}. Which statement about the mean and standard deviation of the two data sets is true?",
                expl=why, **mc(r, S[right], [s for i, s in enumerate(S) if i != right]))


def scatter_fig(r, m, b, xmax=10):
    pts = []
    for x in range(1, xmax):
        y = m * x + b + r.choice([-1.5, -1, -.5, 0, .5, 1, 1.5]); pts.append([x, round(y, 1)])
    ymax = int(math.ceil((m * xmax + b + 3) / 2.0) * 2)
    return dict(type='scatter', xmin=0, xmax=xmax, ymin=0, ymax=ymax, xstep=1, ystep=max(2, ymax // 8 // 2 * 2),
                points=pts, line=[[0, b], [xmax, m * xmax + b]], xlabel='x', ylabel='y')


def two_var_data(r, d, spr):
    if d == 0:
        m, b, x0 = r.choice([1, 1.5, 2, 2.5, 3]), r.choice([1, 2, 3, 4, 5]), r.choice([2, 4, 5, 6, 8])
        ans = Fr(str(m)) * x0 + b
        res = dict(q=f"The scatterplot shows the relationship between two variables, x and y. A line of best fit for the data is also shown. At {M(f'x = {x0}')}, which of the following is closest to the y-value predicted by the line of best fit?",
                   expl=f"Find x = {x0} on the horizontal axis, go up to the LINE (not to a dot), and read across: about {dec(ans)}.",
                   figure=scatter_fig(r, m, b), **numeric(r, ans, False, [ans + 2, ans - 2, ans + 4, ans - 3]))
        return res
    if d == 1:
        x, y, u1, u2 = r.choice([("hours studied", "test score", "hour", "points"), ("hours of practice", "free throws made out of 50", "hour", "free throws"),
                                 ("daily minutes of reading", "vocabulary score", "minute", "points")])
        m, b = r.randint(2, 9), r.randint(20, 60)
        eq = M(f"\\hat{{y}} = {m}x + {b}")
        which = r.random() < .5
        good = f"For each additional {u1} of {x.split(' ', 1)[1] if ' ' in x else x}, the predicted {y} increases by {m}." if which else f"The predicted {y} for a student with 0 {x.split(' ', 1)[1]} is {b}."
        bad = [f"The predicted {y} for a student with 0 {x.split(' ', 1)[1]} is {m}." if which else f"For each additional {u1}, the predicted {y} increases by {b}.",
               f"For each additional {u1}, the predicted {y} decreases by {m}." if which else f"The predicted {y} for a student with {b} {x.split(' ', 1)[1]} is {m}.",
               f"The predicted {y} is {m} times as large as the number of {x.split(' ', 1)[1]}, plus {b}." if which else f"The predicted {y} increases by {b}% each {u1}."]
        return dict(q=f"A line of best fit for a data set relates {x} (x) and {y} (y): {eq}. Which is the best interpretation of {M(str(m if which else b))} in this context?",
                    expl="The slope is the change in the predicted y for each 1-unit increase in x; the intercept is the predicted y when x = 0.",
                    **mc(r, good, bad))
    if r.random() < .5:
        m, b, x0 = r.choice([2, 2.5, 3, 3.5]), r.randint(5, 20), r.randint(3, 9); pred = Fr(str(m)) * x0 + b; act = pred + r.choice([-6, -4, -3, 3, 4, 5, 7])
        eq_ = M(f'\\hat{{y}} = {m}x + {b}'); pt_ = M(f'({x0}, {dec(act)})')
        return dict(q=f"A line of best fit for a data set is {eq_}. For the data point {pt_}, what is the residual (actual y-value minus predicted y-value)?",
                    expl=f"Predicted = {m}({x0}) + {b} = {dec(pred)}. Residual = {dec(act)} - {dec(pred)} = {dec(act - pred)}.",
                    **numeric(r, act - pred, spr, [pred - act, act, pred, act + pred]))
    a, k = r.choice([(2, 3), (3, 2), (4, 3), (5, 2), (5, 3), (6, 2), (6, 3), (4, 2)])
    ys = [a * k ** i for i in range(4)]
    return dict(q=f"{table(['x', '0', '1', '2', '3'], [['y'] + ys])}<br>The table shows four values of x and their corresponding values of y. Which equation best models the relationship between x and y?",
                expl=f"Each y is {k} times the previous y (a constant ratio), so the relationship is exponential: y = {a}({k})^x.",
                **mc(r, M(f"y = {a}({k})^x"), [M(f"y = {a} + {a * (k - 1)}x"), M(f"y = {k}({a})^x"), M(f"y = {a}x^{k}")]))


def prob_table(r, d):
    rows = r.choice([["Freshman", "Sophomore", "Junior"], ["Grade 9", "Grade 10", "Grade 11"]])
    cols = r.choice([["Pizza", "Salad"], ["Bus", "Walk"], ["Soccer", "Chess"]])
    t = [[r.randint(8, 40) for _ in cols] for _ in rows]
    return rows, cols, t


def probability(r, d, spr):
    rows, cols, t = prob_table(r, d)
    rt = [sum(x) for x in t]; ct = [sum(t[i][j] for i in range(3)) for j in range(2)]; G = sum(rt)
    hdr = ['', *cols, 'Total']
    tb = table(hdr, [[rows[i], *t[i], rt[i]] for i in range(3)] + [['Total', *ct, G]])
    i, j = r.randrange(3), r.randrange(2); cell = t[i][j]
    if d == 0:
        what = f"chose {cols[j].lower()}" if cols[j] not in ("Soccer", "Chess") else f"plays {cols[j].lower()}"
        return dict(q=f"{tb}<br>A survey asked {G} students about their preferences. If one of the students is selected at random, what is the probability that the student picked <b>{cols[j]}</b>?",
                    expl=f"{ct[j]} of the {G} students picked {cols[j]}: {ct[j]}/{G}.",
                    **frac_res(r, ct[j], G, [(cell, G), (ct[j], G - ct[j]), (rt[i], G), (cell, ct[j]), (ct[j] + 1, G), (ct[j] - 1, G)], spr))
    if d == 1:
        return dict(q=f"{tb}<br>A survey asked {G} students about their preferences. If one of the <b>{rows[i]}</b> students is selected at random, what is the probability that the student picked <b>{cols[j]}</b>?",
                    expl=f"'Given {rows[i]}' shrinks the group to the {rt[i]} students in that row; {cell} of them picked {cols[j]}: {cell}/{rt[i]}.",
                    **frac_res(r, cell, rt[i], [(cell, G), (cell, ct[j]), (ct[j], G), (rt[i], G), (cell + 1, rt[i]), (cell - 1, rt[i])], spr))
    if r.random() < .5:
        return dict(q=f"{tb}<br>Of the students who picked <b>{cols[j]}</b>, what is the probability that a randomly selected one is a <b>{rows[i]}</b> student?",
                    expl=f"The group is the {ct[j]} students who picked {cols[j]}; {cell} of them are {rows[i]}: {cell}/{ct[j]}.",
                    **frac_res(r, cell, ct[j], [(cell, rt[i]), (cell, G), (rt[i], G), (ct[j], G), (cell + 1, ct[j]), (cell - 1, ct[j])], spr))
    return dict(q=f"{tb}<br>If one student is selected at random, what is the probability that the student is a <b>{rows[i]}</b> student <b>or</b> picked <b>{cols[j]}</b>?",
                expl=f"Add the two groups and subtract the overlap so it isn't counted twice: ({rt[i]} + {ct[j]} - {cell})/{G}.",
                **frac_res(r, rt[i] + ct[j] - cell, G, [(rt[i] + ct[j], G), (cell, G), (rt[i] + ct[j] - cell, G - cell), (rt[i], G), (rt[i] + ct[j] - cell + 1, G), (rt[i] + ct[j] - cell - 1, G)], spr))


def inference_margin(r, d, spr):
    if d == 0:
        N, n = r.choice([4000, 6000, 8000, 10000]), r.choice([200, 250, 400, 500]); k = r.randint(int(n * .1), int(n * .6))
        est = Fr(N * k, n)
        return dict(q=f"A researcher selected a random sample of {n} residents from a town of {N} residents. In the sample, {k} residents said they ride a bike to work. Based on the sample, what is the best estimate of the number of residents in the town who ride a bike to work?",
                    expl=f"Sample proportion = {k}/{n}. Scale up: {N} \u00d7 {k}/{n} = {dec(est)}.",
                    **numeric(r, est, spr, [k, Fr(N * n, k), N - est, Fr(k * 100, n)]))
    if d == 1:
        mean, me = Fr(r.randint(200, 900), 10), Fr(r.randint(5, 30), 10)
        inside = mean + r.choice([-1, 1]) * me * Fr(1, 2); out = [mean + me * 2, mean - me * 2, mean + me * 3]
        f = lambda v: M(dec(v))
        return dict(q=f"A random sample of the students at a university was surveyed, and the sample mean number of hours worked per week was {dec(mean)}, with an associated margin of error of {dec(me)}. Which of the following is a plausible value for the mean number of hours worked per week for all students at the university?",
                    expl=f"The plausible range is {dec(mean)} \u00b1 {dec(me)}, that is, {dec(mean - me)} to {dec(mean + me)}. Only {dec(inside)} is inside it.",
                    **mc(r, f(inside), [f(v) for v in out]))
    me, k = r.choice([6, 8, 10, 12]), r.choice([4, 9, 16])
    ans = Fr(me, int(math.isqrt(k)))
    return dict(q=f"A poll of {r.choice([100, 150, 200])} randomly selected voters had a margin of error of {me} percentage points. If a second poll uses the same method with a random sample {k} times as large, what is the approximate margin of error for the second poll, in percentage points?",
                expl=f"Margin of error shrinks with the square root of the sample size. A sample {k} times as large divides it by \u221a{k} = {int(math.isqrt(k))}: {me}/{int(math.isqrt(k))} = {dec(ans)}.",
                **numeric(r, ans, spr, [Fr(me, k), me * 2, me - k, Fr(me * 2, 3)]))


def evaluating_claims(r, d, spr):
    subj = r.choice([("high school students", "a new study app", "quiz scores"), ("adults in a city", "a daily walking program", "resting heart rate"),
                     ("patients with mild headaches", "a magnesium supplement", "headache days per month")])
    pop, treat, out = subj
    rs, ra = r.random() < .5, r.random() < .5
    S = {(True, True): "The results can be generalized to the whole population, and the treatment caused the difference.",
         (False, True): "The treatment caused the difference among the participants, but the results cannot be generalized to the whole population.",
         (True, False): "The results can be generalized to the whole population, but the study shows only an association, not a cause.",
         (False, False): "The results apply only to the participants, and the study shows only an association, not a cause."}
    samp = f"randomly selected from all {pop} in the region" if rs else f"volunteers who responded to a flyer at one clinic or school"
    assign = f"The participants were randomly assigned to use {treat} or not." if ra else f"Each participant chose whether to use {treat}."
    if d == 2:
        extra = f" The two groups were similar in size and the {out} were measured the same way for both."
        samp += ", and the sample was large"
    else:
        extra = ''
    return dict(q=f"A study looked at the relationship between {treat} and {out} among {pop}. The participants were {samp}. {assign}{extra} Which of the following is the most appropriate conclusion?",
                expl=f"Random SAMPLE ({'yes' if rs else 'no'}) controls what you can generalize; random ASSIGNMENT ({'yes' if ra else 'no'}) controls whether you can conclude cause and effect.",
                **mc(r, S[(rs, ra)], [v for k, v in S.items() if k != (rs, ra)]))


# ============================================================================ GEOMETRY & TRIG
def area_volume(r, d, spr):
    if d == 0:
        if r.random() < .5:
            l, w, h = r.randint(3, 15), r.randint(3, 12), r.randint(2, 10)
            return dict(q=f"A rectangular prism has a volume of {l * w * h} cubic inches. Its base is {l} inches long and {w} inches wide. What is the height, in inches, of the prism?",
                        expl=f"V = lwh, so h = {l * w * h} \u00f7 ({l} \u00d7 {w}) = {h}.", **numeric(r, h, spr, [l * w * h // l, l + w, Fr(l * w * h, l + w), h + 2]))
        b1, b2, h = r.randint(4, 14), r.randint(4, 14), r.choice([2, 4, 6, 8, 10])
        return dict(q=f"A trapezoid has parallel sides of length {b1} and {b2} and a height of {h}. What is the area of the trapezoid?",
                    expl=f"A = \u00bd(b\u2081 + b\u2082)h = \u00bd({b1} + {b2})({h}) = {Fr(b1 + b2, 2) * h}.", **numeric(r, Fr(b1 + b2, 2) * h, spr, [b1 * b2 * h, (b1 + b2) * h, b1 * h]))
    if d == 1:
        rr, h = r.randint(2, 9), r.randint(3, 15); diam = r.random() < .5
        return dict(q=f"A right circular cylinder has {'a diameter' if diam else 'a radius'} of {2 * rr if diam else rr} centimeters and a height of {h} centimeters. The volume of the cylinder is {KPI} cubic centimeters. What is the value of {M('k')}?",
                    expl=f"The radius is {rr}. V = \u03c0r\u00b2h = \u03c0({rr})\u00b2({h}) = {rr * rr * h}\u03c0.",
                    **numeric(r, rr * rr * h, spr, [(2 * rr) ** 2 * h, rr * h, 2 * rr * h, Fr(rr * rr * h, 3)]))
    if r.random() < .5:
        L, W = r.choice([(40, 25), (50, 20), (20, 50), (25, 40)]); lit = r.choice([20, 30, 40, 60, 75, 90])
        dep = Fr(lit * 1000, L * W)
        return dict(q=f"A tank in the shape of a rectangular prism has a base that is {L} centimeters by {W} centimeters. The tank contains {lit} liters of water. (1 liter = 1,000 cubic centimeters.) What is the depth of the water, in centimeters?",
                    expl=f"{lit} L = {lit * 1000} cm\u00b3. Depth = {lit * 1000} \u00f7 ({L} \u00d7 {W}) = {dec(dep)}.",
                    **numeric(r, dep, spr, [Fr(lit, L * W), dep * 10, dep / 10, lit]))
    k = r.choice([2, 3, 4])
    return dict(q=f"A solid sphere has volume {M('V')}. A second sphere has a radius that is {k} times the radius of the first sphere. The volume of the second sphere is how many times the volume of the first?",
                expl=f"Volume scales with the cube of the scale factor: {k}\u00b3 = {k ** 3}.", **numeric(r, k ** 3, spr, [k * k, k, 3 * k, k ** 4]))


def lines_angles_triangles(r, d, spr):
    if d == 0:
        if r.random() < .5:
            a, b = r.randint(30, 80), r.randint(30, 80)
            return dict(q=f"In triangle ABC, angle A measures {a}\u00b0 and angle B measures {b}\u00b0. What is the measure of angle C, in degrees?",
                        expl=f"Angles sum to 180\u00b0: 180 - {a} - {b} = {180 - a - b}.", **numeric(r, 180 - a - b, spr, [a + b, 180 - a, 90 - a, 360 - a - b]))
        ap = r.choice(range(20, 130, 2))
        return dict(q=f"An isosceles triangle has a vertex angle of {ap}\u00b0. What is the measure, in degrees, of one of the base angles?",
                    expl=f"The base angles are equal and all three sum to 180\u00b0: (180 - {ap})/2 = {(180 - ap) // 2}.", **numeric(r, (180 - ap) // 2, spr, [180 - ap, ap // 2, 90 - ap, (180 - ap) // 2 + 10]))
    if d == 1:
        a, b, k = r.randint(3, 9), r.randint(4, 12), r.choice([2, 3, Fr(3, 2), Fr(5, 2)])
        if r.random() < .5:
            return dict(q=f"Triangle DEF is similar to triangle ABC, where D corresponds to A, E to B, and F to C. In triangle ABC, AB = {a} and BC = {b}. In triangle DEF, DE = {dec(a * k)}. What is the length of EF?",
                        expl=f"The scale factor is DE/AB = {dec(k)}, so EF = {dec(k)} \u00d7 {b} = {dec(b * k)}.", **numeric(r, b * k, spr, [b + (a * k - a), b * k - a, b / k, a * k]))
        h, s1 = r.randint(4, 9) * 2, r.randint(2, 5) * 2; s2 = s1 * r.choice([2, 3, 4])
        return dict(q=f"At the same time of day, a flagpole casts a shadow that is {s2} feet long, and a {h}-foot-tall post casts a shadow that is {s1} feet long. How tall, in feet, is the flagpole? (Both objects are perpendicular to flat ground.)",
                    expl=f"Similar right triangles: h/{s2} = {h}/{s1}, so h = {h * s2 // s1}.", **numeric(r, h * s2 // s1, spr, [h + s2 - s1, h * s1 // s2, h * s2, s2 - s1]))
    while True:
        m1, m2, x0, c1 = r.randint(2, 6), r.randint(2, 6), r.randint(8, 30), r.randint(-20, 20)
        eq = r.random() < .5; a1 = m1 * x0 + c1; a2 = a1 if eq else 180 - a1
        if m1 != m2 and 10 < a1 < 170 and 10 < a2 < 170: break
    c2 = a2 - m2 * x0
    rel = "are alternate interior angles" if eq else "are same-side interior angles"
    ang1 = M(f'({lin(m1, c1)})^\\circ'); ang2 = M(f'({lin(m2, c2)})^\\circ')
    why = 'Alternate interior angles are equal' if eq else 'Same-side interior angles add to 180\u00b0'
    op, tail = ('=', '') if eq else ('+', ' = 180')
    return dict(q=f"Lines {ELL} and {M('m')} are parallel and are cut by a transversal. Two angles that {rel} measure {ang1} and {ang2}. What is the value of {M('x')}?",
                expl=f"{why}: {lin(m1, c1)} {op} {lin(m2, c2)}{tail}. Solving gives x = {x0}.",
                **numeric(r, x0, spr, [a1, a2, x0 + 5, x0 - 5]))


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def right_tri_trig(r, d, spr):
    a, b, c = r.choice(TRIPLES)
    if d == 0:
        k = r.randint(1, 4) if c < 20 else 1; A, B, C = a * k, b * k, c * k
        if r.random() < .5:
            return dict(q=f"A right triangle has legs of length {A} and {B}. What is the length of its hypotenuse?", expl=f"{A}\u00b2 + {B}\u00b2 = {A * A + B * B} = {C}\u00b2.",
                        **numeric(r, C, spr, [A + B, C * C, B - A, abs(A * A - B * B)]))
        return dict(q=f"A right triangle has a hypotenuse of length {C} and one leg of length {A}. What is the length of the other leg?", expl=f"{C}\u00b2 - {A}\u00b2 = {C * C - A * A} = {B}\u00b2.",
                    **numeric(r, B, spr, [C - A, C * C - A * A, A + C, B + 2]))
    if d == 1:
        ratio = r.choice(['cos', 'tan']); ans = {'cos': (b, c), 'tan': (a, b)}[ratio]
        s_ = M(f'\\sin A = \\frac{{{a}}}{{{c}}}'); t_ = M('\\' + ratio + ' A')
        return dict(q=f"In right triangle ABC, the right angle is at C. {s_}. What is the value of {t_}?",
                    expl=f"sin A = opposite/hypotenuse = {a}/{c}, so the sides are {a}, {b}, {c}. {ratio} A = {'adjacent/hypotenuse' if ratio == 'cos' else 'opposite/adjacent'} = {ans[0]}/{ans[1]}.",
                    **frac_res(r, ans[0], ans[1], [(a, b) if ratio == 'cos' else (b, c), (c, a), (a, c), (c, b)], spr))
    t = r.choice(['comp', 'iso', 'rad'])
    if t == 'comp':
        s_ = M(f'\\sin A = \\frac{{{a}}}{{{c}}}'); c_ = M('\\cos C')
        return dict(q=f"In right triangle ABC, the right angle is at B and {s_}. What is the value of {c_}?",
                    expl="The acute angles A and C are complementary, and sin of an angle equals cos of its complement. So cos C = sin A.",
                    **frac_res(r, a, c, [(b, c), (a, b), (b, a), (c, a)], spr))
    if t == 'iso':
        L = r.randint(3, 12); f = lambda s: M(s)
        return dict(q=f"A right triangle has two legs of equal length, and its area is {dec(Fr(L * L, 2))} square units. What is the length of the hypotenuse?",
                    expl=f"Area = \u00bd\u00b7leg\u00b2 = {Fr(L * L, 2)}, so each leg is {L}. Hypotenuse = {L}\u221a2.",
                    **mc(r, f(f"{L}\\sqrt{{2}}"), [f(f"{L}"), f(f"{2 * L}"), f(f"{L}\\sqrt{{3}}")]))
    n, k = r.choice([2, 3, 4, 5, 6, 9, 10, 12]), r.randint(1, 3)
    ang_ = M(f'\\frac{{{k}\\pi}}{{{n}}}')
    return dict(q=f"An angle has a measure of {ang_} radians. What is the measure of the angle, in degrees?", expl=f"Multiply by 180/\u03c0: {k} \u00d7 180 \u00f7 {n} = {Fr(180 * k, n)}.",
                **numeric(r, Fr(180 * k, n), spr, [Fr(k * 90, n), 180 * k * n, Fr(180, n), Fr(360 * k, n)]))


def circles(r, d, spr):
    if d == 0:
        rr = r.randint(2, 12)
        c_ = M(f'{2 * rr}\\pi')
        return dict(q=f"The circumference of a circle is {c_} inches. The area of the circle is {KPI} square inches. What is the value of {M('k')}?",
                    expl=f"C = 2\u03c0r, so r = {rr}. Area = \u03c0r\u00b2 = {rr * rr}\u03c0.", **numeric(r, rr * rr, spr, [2 * rr, rr, rr * rr * 2, 4 * rr * rr]))
    if d == 1:
        th, rr = r.choice([30, 45, 60, 90, 120, 180]), r.randint(3, 12)
        arc = Fr(2 * rr * th, 360)
        if arc.denominator != 1: rr, th = 6, 60; arc = Fr(2 * rr * th, 360)
        C = 360 * arc / th
        arc_ = M(f'{dec(arc)}\\pi'); pi_ = M('\\pi')
        return dict(q=f"In a circle with center O, points A and B lie on the circle. The measure of arc AB is {th}\u00b0 and the length of arc AB is {arc_} centimeters. What is the circumference of the circle, in units of {pi_} centimeters?",
                    expl=f"{th}/360 of the circle is {dec(arc)}\u03c0, so the whole circle is {dec(arc)}\u03c0 \u00d7 360/{th} = {dec(C)}\u03c0.",
                    **numeric(r, C, spr, [arc * th / 90, arc * 2, 360 / arc, C + arc]))
    h, k, rr = r.randint(-6, 6), r.randint(-6, 6), r.randint(3, 9)
    A, B, C = -2 * h, -2 * k, rr * rr - h * h - k * k
    ask_r = r.random() < .6
    tA = '' if A == 0 else (f' + {A}x' if A > 0 else f' - {-A}x')
    tB = '' if B == 0 else (f' + {B}y' if B > 0 else f' - {-B}y')
    eq_ = M('x^2 + y^2' + tA + tB + f' = {C}')
    return dict(q=f"The equation {eq_} defines a circle in the xy-plane. What is the {'radius' if ask_r else 'x-coordinate of the center'} of the circle?",
                expl=f"Complete the square in x and y: (x{sg(-h)})\u00b2 + (y{sg(-k)})\u00b2 = {C} + {h * h} + {k * k} = {rr * rr}. The center is ({h}, {k}) and the radius is \u221a{rr * rr} = {rr}.",
                **numeric(r, rr if ask_r else h, spr, [rr * rr if ask_r else -h, C, -h if ask_r else rr, h + k]))


GEN = dict(lin_eq_1var=lin_eq_1var, lin_eq_2var=lin_eq_2var, lin_functions=lin_functions, systems_2lin=systems_2lin,
           lin_ineq=lin_ineq, equiv_expr=equiv_expr, nonlin_eq_sys=nonlin_eq_sys, nonlin_functions=nonlin_functions,
           ratios_rates=ratios_rates, percentages=percentages, one_var_data=one_var_data, two_var_data=two_var_data,
           probability=probability, inference_margin=inference_margin, evaluating_claims=evaluating_claims,
           area_volume=area_volume, lines_angles_triangles=lines_angles_triangles, right_tri_trig=right_tri_trig, circles=circles)
