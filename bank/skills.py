"""Skill taxonomy mirroring the Digital SAT Assessment Framework (spec Tables 2 and 3).
Every question in the system is tagged with one of these skill keys.
The 'see / how / traps' text becomes the "How to do this" cover sheet on paper homework."""

DOMAINS = {
    'rw': {'Craft and Structure': .28, 'Information and Ideas': .26,
           'Standard English Conventions': .26, 'Expression of Ideas': .20},
    'math': {'Algebra': .35, 'Advanced Math': .35,
             'Problem-Solving and Data Analysis': .15, 'Geometry and Trigonometry': .15},
}
SECTION_NAME = {'rw': 'Reading & Writing', 'math': 'Math'}
SKILLS = {}


def add(key, name, section, domain, avg_sec, see, how, traps, formulas=''):
    SKILLS[key] = dict(key=key, name=name, section=section, domain=domain, avg_sec=avg_sec,
                       see=see, how=how, traps=traps, formulas=formulas)


# ------------------------------------------------------------------ READING & WRITING
CS, II, SE, EI = 'Craft and Structure', 'Information and Ideas', 'Standard English Conventions', 'Expression of Ideas'
add('words_in_context', 'Words in Context', 'rw', CS, 60,
    ["A blank ______ in a short passage, or a word in quotes / 'As used in the text, what does ___ most nearly mean?'",
     "Clue words elsewhere in the sentence: contrast (but, although, rather than) or support (for example, because, since)"],
    ["Cover the choices. Say your own word for the blank using only the clues.",
     "Match your word to the closest choice.",
     "Plug the winner back in and read the whole sentence. Does the tone and logic still work?"],
    ["Picking the fanciest word instead of the most precise one",
     "Common words with a second meaning (e.g. 'quality' = a trait, not 'how good')",
     "A word that fits the topic but not the logic of the sentence"])
add('text_structure_purpose', 'Text Structure and Purpose', 'rw', CS, 75,
    ["'Which choice best states the function of the underlined sentence?' or 'main purpose of the text'"],
    ["Label each sentence in ~4 words: claim, evidence, example, counterpoint, hypothesis, result.",
     "Say the job of the target in one verb phrase ('sets up', 'concedes', 'gives an example of').",
     "Pick the choice whose verbs match. Throw out any choice with details that are not in the text."],
    ["Right topic, wrong function", "Verbs that are too strong ('refutes', 'proves') when the text only 'suggests'"])
add('cross_text', 'Cross-Text Connections', 'rw', CS, 90,
    ["Two passages labelled Text 1 and Text 2; the question asks how one author would respond to, or relates to, the other"],
    ["Boil each text down to ONE sentence: what does it claim?",
     "Decide the relationship: agree, disagree, add a detail, or qualify (true only sometimes).",
     "Answer in the direction the question asks (Text 2 about Text 1, not the reverse)."],
    ["Reversing the direction", "Extreme words like 'completely' or 'never'", "Answers that only summarize one text"])
add('central_ideas', 'Central Ideas and Details', 'rw', II, 70,
    ["'Which choice best states the main idea / central claim / best summarizes the text?'"],
    ["Read the whole text and mark the pivot words (but, however, yet).",
     "Tell a friend the point in one sentence before you look at the choices.",
     "Eliminate: too narrow (one detail), too broad, not in the text, or contradicts the text."],
    ["A true detail that is not the main point", "Choices that go beyond what the text says"])
add('coe_textual', 'Command of Evidence: Textual', 'rw', II, 80,
    ["'Which finding, if true, would most strongly support (or weaken) ...' or 'Which quotation most effectively illustrates the claim?'"],
    ["Restate the claim precisely. Circle every part of it.",
     "Test EVERY choice: does it hit all the parts? A choice that hits only half is wrong.",
     "For 'support' pick what makes the claim more likely; for 'weaken' pick what makes it less likely."],
    ["Interesting but irrelevant evidence", "Choices that support the OPPOSITE claim", "Matching a topic word instead of the logic"])
add('coe_quant', 'Command of Evidence: Quantitative', 'rw', II, 80,
    ["A table or graph plus a sentence that ends in a blank ______ and a claim (varied widely, highest, increased ...)"],
    ["Read title, labels and units first.",
     "Say which categories or values the claim needs (e.g. 'a big high AND a big low').",
     "Check each number in each choice against the table. Cross out choices that misreport or answer a different claim."],
    ["Right number, wrong label", "Choices that support a different claim", "Ignoring units (% vs count)"])
add('inferences', 'Inferences', 'rw', II, 75,
    ["'Which choice most logically completes the text?' with a blank at the end, often after 'therefore' or 'this suggests'"],
    ["Find the strongest fact or claim right before the blank.",
     "Predict what MUST be true if that is right.",
     "Choose the answer that goes just far enough. It should add no new information."],
    ["Too extreme (all, never, always)", "True in real life but not supported by the text"])
add('boundaries', 'Boundaries (punctuation)', 'rw', SE, 50,
    ["Answer choices that differ only in punctuation ( , ; : . \u2014 ) between clauses or inside a sentence"],
    ["Split the sentence at the punctuation. Is each side a complete sentence (subject + verb, can stand alone)?",
     "Complete + complete: use a period, a semicolon, or a comma + and/but/or/so.",
     "Complete clause then a list or explanation: colon.",
     "Never put a single comma, colon or semicolon between a subject and its verb.",
     "Extra information you could delete: commas (or dashes) on BOTH sides."],
    ["A comma alone joining two full sentences (comma splice)", "Semicolon + 'and'", "Punctuation splitting subject from verb"],
    )
add('form_structure_sense', 'Form, Structure, and Sense (grammar)', 'rw', SE, 55,
    ["Answer choices that differ in verb form, pronoun, plural / possessive, or word order"],
    ["Find the real subject. Cross out prepositional phrases and interrupters (of..., along with...).",
     "Match the verb to the subject in number and to the sentence in tense.",
     "Pronoun: one clear noun it points back to, same number (a committee \u2192 its).",
     "An opening phrase must be followed by the noun it describes (no dangling modifiers)."],
    ["Agreeing the verb with the nearest noun instead of the subject", "its / it's, their / there"])
add('rhetorical_synthesis', 'Rhetorical Synthesis', 'rw', EI, 80,
    ["Bulleted student notes and 'The student wants to (introduce / emphasize / compare / explain) ...'"],
    ["Underline the goal verb and the audience.",
     "Mark only the notes that serve that goal.",
     "Pick the choice that does EXACTLY that job with those notes. True but off-goal answers are wrong."],
    ["Accurate sentences that serve a different goal", "Using too many notes"])
add('transitions', 'Transitions', 'rw', EI, 45,
    ["A blank at the start of a sentence (or after a semicolon) with choices like However, Therefore, For example, In addition"],
    ["Read the sentence before AND after the blank.",
     "Name the relationship: contrast, cause/result, addition, example, sequence, similarity.",
     "Pick the transition of that type. Do not choose by 'sounds nice'."],
    ["Assuming contrast because of a negative word", "'In fact' emphasizes; it does not add a new idea"])

# ------------------------------------------------------------------------------ MATH
AL, AM, PS, GT = 'Algebra', 'Advanced Math', 'Problem-Solving and Data Analysis', 'Geometry and Trigonometry'
add('lin_eq_1var', 'Linear equations in one variable', 'math', AL, 75,
    ["'What is the value of x?', 'for what value of k are there infinitely many / no solutions?'"],
    ["Distribute, then combine like terms on each side.", "Get x terms on one side and numbers on the other.",
     "Divide. Plug your answer back in to check.",
     "Infinitely many solutions: both sides identical. No solution: same x-coefficient, different constants."],
    ["Sign errors when distributing a negative", "Answering with x when they asked for an expression like x + 3"],
    "\\(ax + b = c \\Rightarrow x = \\dfrac{c-b}{a}\\)")
add('lin_eq_2var', 'Linear equations in two variables', 'math', AL, 90,
    ["An equation like ax + by = c, intercepts, parallel / perpendicular lines, or a word problem asking what a number means"],
    ["Intercepts: set y = 0 for the x-intercept, x = 0 for the y-intercept.",
     "Convert to y = mx + b to read slope and intercept. Perpendicular slope = negative reciprocal.",
     "Meaning questions: attach units. In 5x + 3y = 60, the '3' goes with whatever y counts."],
    ["Mixing up which variable a coefficient belongs to", "Forgetting to flip the sign for perpendicular slope"],
    "\\(y = mx + b\\), \\(\\; m = \\dfrac{y_2-y_1}{x_2-x_1}\\)")
add('lin_functions', 'Linear functions', 'math', AL, 80,
    ["f(x) = mx + b notation, tables of a linear function, 'best interpretation of the slope / of 40 in this context'"],
    ["f(2) means replace every x with 2.", "Slope = change in y for each 1 change in x (rate). y-intercept = starting value.",
     "Two points give the slope; then find b."],
    ["Reading f(x) as f times x", "Slope and intercept swapped in the interpretation"],
    "\\(f(x)=mx+b\\)")
add('systems_2lin', 'Systems of two linear equations', 'math', AL, 110,
    ["Two equations with x and y, or a word problem with two totals (count and money)"],
    ["Line up the equations. Choose substitution (one variable already isolated) or elimination (matching coefficients).",
     "Solve for one variable, substitute back for the other.",
     "No solution: same slope, different intercepts. Infinitely many: the equations are multiples of each other."],
    ["Answering with x when y was asked", "Arithmetic slips when multiplying an entire equation"])
add('lin_ineq', 'Linear inequalities', 'math', AL, 90,
    ["'at most', 'at least', 'greatest / least integer', a system of inequalities, 'which point is a solution'"],
    ["'At most' is \u2264, 'at least' is \u2265, 'fewer than' is <.",
     "Solve like an equation. FLIP the sign when you multiply or divide by a negative.",
     "Points: plug the x and y into EVERY inequality."],
    ["Forgetting to flip the sign", "Strict vs non-strict (< vs \u2264)"])
add('equiv_expr', 'Equivalent expressions', 'math', AM, 90,
    ["'Which expression is equivalent to ...?' (expanding, factoring, rational expressions, exponents)"],
    ["Expand with FOIL or factor by finding two numbers that multiply to c and add to b.",
     "Rational expressions: get a common denominator first, then combine numerators (careful with the minus sign).",
     "Test a number: plug x = 2 into the original and each choice."],
    ["Dropping the middle term", "Subtracting a numerator without distributing the minus"],
    "\\((a+b)^2=a^2+2ab+b^2\\), \\(a^2-b^2=(a-b)(a+b)\\)")
add('nonlin_eq_sys', 'Nonlinear equations and systems', 'math', AM, 110,
    ["Quadratics, 'how many real solutions', 'what is a positive value of b', square-root equations, a line meeting a parabola"],
    ["Set the equation to 0, then factor or use the quadratic formula.",
     "Discriminant b\u00b2 \u2212 4ac: positive = 2 solutions, 0 = 1 solution, negative = none.",
     "Square-root equations: square both sides, solve, then CHECK for extraneous solutions.",
     "Intersection points: set the two y's equal."],
    ["Skipping the check on radical equations", "Using the wrong sign in the quadratic formula"],
    "\\(x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}\\)")
add('nonlin_functions', 'Nonlinear functions', 'math', AM, 100,
    ["Vertex form, minimum / maximum, exponential growth or decay, 'which form shows the zeros', transformations"],
    ["Vertex form a(x \u2212 h)\u00b2 + k: vertex (h, k). Factored form shows the zeros. Standard form shows y-intercept c.",
     "Growth / decay: f(x) = a\u00b7b\u02e3 with b = 1 \u00b1 rate.",
     "f(x \u2212 p) + q moves the graph right p and up q."],
    ["Sign of h in vertex form", "Using 20% as 0.2 for growth instead of 1.2"],
    "\\(a(x-h)^2+k\\), \\(\\; a\\cdot b^x\\)")
add('ratios_rates', 'Ratios, rates, proportions, and units', 'math', PS, 90,
    ["'At this rate', conversions between units, density, 'per', combined work"],
    ["Write the rate as a fraction with units. Multiply by conversion factors so units cancel.",
     "Combined rates ADD (pages per minute + pages per minute).",
     "Sanity check: should the answer be bigger or smaller?"],
    ["Dividing when you should multiply", "Mixing minutes and hours"],
    "\\(\\text{rate}=\\dfrac{\\text{amount}}{\\text{time}}\\), \\(\\; \\text{density}=\\dfrac{\\text{mass}}{\\text{volume}}\\)")
add('percentages', 'Percentages', 'math', PS, 80,
    ["'increased by', 'discounted', 'markup', 'what was the original price', successive changes"],
    ["Increase p%: multiply by (1 + p/100). Decrease: multiply by (1 \u2212 p/100).",
     "Successive changes: multiply the multipliers, never add the percents.",
     "Finding the original: divide by the multiplier."],
    ["Adding +20% and \u221220% to get 0%", "Taking the percent of the wrong base"])
add('one_var_data', 'One-variable data', 'math', PS, 85,
    ["Lists, frequency tables, dot plots, mean / median / range / standard deviation, effect of adding or removing a value"],
    ["Median: sort first. Mean = sum \u00f7 count. Sum = mean \u00d7 count.",
     "Adding a constant to every value shifts mean and median but NOT the spread.",
     "Multiplying every value by k multiplies the mean and the spread by k."],
    ["Median of an unsorted list", "Thinking an outlier moves the median as much as the mean"])
add('two_var_data', 'Two-variable data', 'math', PS, 90,
    ["Scatterplots, line of best fit, 'predicted', residuals, linear vs exponential models"],
    ["Predicted value: read the LINE, not the dots.", "Residual = actual \u2212 predicted.",
     "Slope = change in predicted y per 1 unit of x; intercept = predicted y when x = 0.",
     "Constant difference \u2192 linear. Constant ratio \u2192 exponential."],
    ["Reading a dot instead of the line", "Residual sign backwards"])
add('probability', 'Probability and conditional probability', 'math', PS, 100,
    ["Two-way tables, 'if one is chosen at random', 'given that'"],
    ["Probability = favorable \u00f7 total.",
     "'GIVEN that ...' means your total shrinks to just that row or column.",
     "'A or B' = A + B \u2212 both."],
    ["Using the grand total when a 'given' shrinks the group", "Double-counting the overlap"],
    "\\(P(A|B)=\\dfrac{\\text{both}}{\\text{total in }B}\\)")
add('inference_margin', 'Inference from samples and margin of error', 'math', PS, 90,
    ["'A random sample of n...', 'estimate for the population', 'margin of error'"],
    ["Scale the sample proportion up to the population.",
     "Estimate \u00b1 margin of error gives the plausible range.",
     "Bigger sample \u2192 smaller margin of error (4\u00d7 sample \u2192 half the margin)."],
    ["Treating the margin of error as a guarantee", "Applying results to a population that was not sampled"])
add('evaluating_claims', 'Evaluating statistical claims', 'math', PS, 90,
    ["Descriptions of a survey or study: who was chosen and how, whether groups were assigned at random"],
    ["Random SAMPLE of a population \u2192 can generalize to that population.",
     "Random ASSIGNMENT to groups \u2192 can conclude cause and effect.",
     "Volunteers or convenience samples \u2192 do not generalize. No random assignment \u2192 only an association."],
    ["Confusing random sampling with random assignment", "Generalizing beyond the group sampled"])
add('area_volume', 'Area and volume', 'math', GT, 90,
    ["Areas of shapes, volumes of solids, scaling, filling containers, unit conversion"],
    ["Write the formula, then plug in. Draw and label.", "Scale factor k: lengths \u00d7 k, area \u00d7 k\u00b2, volume \u00d7 k\u00b3.",
     "1 liter = 1000 cm\u00b3."],
    ["Using diameter as radius", "Forgetting to square or cube the scale factor"],
    "\\(V_{cyl}=\\pi r^2h\\), \\(V_{sphere}=\\tfrac43\\pi r^3\\), \\(V_{cone}=\\tfrac13\\pi r^2h\\)")
add('lines_angles_triangles', 'Lines, angles, and triangles', 'math', GT, 90,
    ["Angles in a triangle, parallel lines cut by a transversal, similar triangles, shadows"],
    ["Triangle angles sum to 180\u00b0. Straight line = 180\u00b0.",
     "Parallel lines: alternate and corresponding angles are equal; same-side interior angles add to 180\u00b0.",
     "Similar triangles: set up a proportion of matching sides."],
    ["Matching the wrong sides in a proportion", "Equal vs supplementary"])
add('right_tri_trig', 'Right triangles and trigonometry', 'math', GT, 95,
    ["Pythagorean theorem, sin / cos / tan, special right triangles, radians"],
    ["SOH-CAH-TOA: sin = opp/hyp, cos = adj/hyp, tan = opp/adj.",
     "sin of an angle = cos of its complement.",
     "\u03c0 radians = 180\u00b0. Multiply radians by 180/\u03c0."],
    ["Opposite / adjacent swapped", "Forgetting the hypotenuse is the longest side"],
    "\\(a^2+b^2=c^2\\); 45-45-90: \\(s,s,s\\sqrt2\\); 30-60-90: \\(x,x\\sqrt3,2x\\)")
add('circles', 'Circles', 'math', GT, 100,
    ["Arc length, sector area, circumference, equations like x\u00b2 + y\u00b2 + 6x \u2212 8y = 11"],
    ["Arc \u00f7 circumference = central angle \u00f7 360.",
     "Circle equation (x \u2212 h)\u00b2 + (y \u2212 k)\u00b2 = r\u00b2: complete the square in x and in y.",
     "Radius squared is the number on the right, not the radius."],
    ["Reporting r\u00b2 instead of r", "Sign of the center coordinates"],
    "\\(C=2\\pi r\\), \\(A=\\pi r^2\\), \\((x-h)^2+(y-k)^2=r^2\\)")

REFERENCE_HTML = """
<div class="ref-grid">
<div>Circle<br>\\(A=\\pi r^2\\)<br>\\(C=2\\pi r\\)</div>
<div>Rectangle<br>\\(A=\\ell w\\)</div>
<div>Triangle<br>\\(A=\\tfrac12 bh\\)</div>
<div>Pythagorean theorem<br>\\(a^2+b^2=c^2\\)</div>
<div>Special right triangles<br>45-45-90: \\(s,\\ s,\\ s\\sqrt2\\)<br>30-60-90: \\(x,\\ x\\sqrt3,\\ 2x\\)</div>
<div>Rectangular solid<br>\\(V=\\ell wh\\)</div>
<div>Cylinder<br>\\(V=\\pi r^2h\\)</div>
<div>Sphere<br>\\(V=\\tfrac43\\pi r^3\\)</div>
<div>Cone<br>\\(V=\\tfrac13\\pi r^2h\\)</div>
<div>Pyramid<br>\\(V=\\tfrac13\\ell wh\\)</div>
</div>
<ul>
<li>The number of degrees of arc in a circle is 360.</li>
<li>The number of radians of arc in a circle is \\(2\\pi\\).</li>
<li>The sum of the measures in degrees of the angles of a triangle is 180.</li>
</ul>
"""

DIFF = ['easy', 'medium', 'hard']
