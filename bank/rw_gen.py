"""Reading & Writing generators. Same signature as math_gen: g(rng, d, spr) -> dict.
RW dicts carry: passage (HTML, may be ''), q (stem), type='mc', choices, answer, expl, uid (for de-duplication inside one test).
Authored records live in rw_content.py / rw_content2.py; parametric skills are built here."""
import bank.rw_content as _c1  # noqa: F401  (registers records)
import bank.rw_content2 as _c2  # noqa: F401
import bank.rw_content3 as _c3  # noqa: F401  (parts 3-4 load last: authored uids are index-based)
import bank.rw_content4 as _c4  # noqa: F401
import bank.rw_content5 as _c5  # noqa: F401  (parts 5-7: append only, same reason)
import bank.rw_content6 as _c6  # noqa: F401
import bank.rw_content7 as _c7  # noqa: F401
from bank.rw_content import RECS

Q_STD = 'Which choice completes the text so that it conforms to the conventions of Standard English?'
Q_TRANS = 'Which choice completes the text with the most logical transition?'


# ------------------------------------------------------------------ builder
def build(r, passage, q, ans, wrongs, uid, figure=None):
    items = [(ans[0], ans[1], True)] + [(w, y, False) for w, y in wrongs]
    seen, uniq = set(), []
    for it in items:
        if it[0] in seen: continue
        seen.add(it[0]); uniq.append(it)
    if len(uniq) < 4: raise ValueError('duplicate choices in ' + uid)
    r.shuffle(uniq)
    letters = 'ABCD'
    ci = [i for i, it in enumerate(uniq) if it[2]][0]
    parts = ['<b>Choice %s is the best answer.</b> %s' % (letters[ci], uniq[ci][1])]
    for i, it in enumerate(uniq):
        if i != ci: parts.append('<b>Choice %s</b> is incorrect. %s' % (letters[i], it[1]))
    out = dict(type='mc', passage=passage, q=q, choices=[it[0] for it in uniq], answer=letters[ci],
               expl='<br>'.join(parts), uid=uid)
    if figure: out['figure'] = figure
    return out


def authored(skill):
    def g(r, d, spr):
        pool = [(i, x) for i, x in enumerate(RECS[skill]) if x['d'] == d]
        i, x = pool[r.randrange(len(pool))]
        return build(r, x['passage'], x['q'], x['ans'], x['wrongs'], '%s:%d' % (skill, i))
    return g


def plain(r, prefix, rest, ok, bad, why_ok, why_bad, uid, q=Q_STD):
    """Blank sits between prefix and rest. bad = list of strings (3+)."""
    sep = '' if rest[:1] in ('.', ',', ';', ':') else ' '
    passage = ('%s ______%s%s' % (prefix, sep, rest)).strip()
    return build(r, passage, q, (ok, why_ok), [(b, why_bad(b) if callable(why_bad) else why_bad) for b in bad[:3]], uid)


# ------------------------------------------------------------------ transitions
REL_POOL = {
    'contrast': ['However,', 'Nevertheless,', 'On the other hand,', 'Even so,'],
    'addition': ['Moreover,', 'Furthermore,', 'In addition,', 'Additionally,'],
    'result': ['Therefore,', 'Consequently,', 'As a result,', 'Thus,'],
    'example': ['For example,', 'For instance,'],
    'sequence': ['Then,', 'Afterward,', 'Subsequently,', 'Next,'],
    'earlier': ['Previously,', 'Before that,', 'Earlier,'],
    'similarity': ['Similarly,', 'Likewise,'],
    'emphasis': ['In fact,', 'Indeed,'],
    'meanwhile': ['Meanwhile,', 'At the same time,'],
    'instead': ['Instead,', 'Rather,'],
}
REL_DESC = {
    'contrast': 'a contrast or unexpected turn', 'addition': 'an additional, similar point', 'result': 'a result or consequence',
    'example': 'a specific example', 'sequence': 'a later step in a sequence', 'earlier': 'something that happened earlier',
    'similarity': 'a similarity between two things', 'emphasis': 'a stronger restatement of the previous point',
    'meanwhile': 'something happening at the same time', 'instead': 'a replacement for what was just rejected',
}
# (d, relation, first sentence, second sentence, relations that would also sound plausible and must not be used as distractors)
TPAIRS = [
    (0, 'contrast', "The hike was long and steep.", "the view from the summit made every step worthwhile.", ['emphasis']),
    (0, 'addition', "The school garden provides fresh vegetables for the cafeteria.", "it gives students hands-on experience with science.", ['similarity', 'emphasis']),
    (0, 'result', "Heavy snow fell all night.", "the school district canceled classes on Monday.", ['sequence']),
    (0, 'example', "Many birds have adapted to city life.", "pigeons nest on ledges and rooftops.", ['emphasis', 'addition']),
    (0, 'sequence', "Mix the flour and water into a dough.", "let it rest for an hour before baking.", ['result']),
    (0, 'contrast', "Most cacti need very little water.", "some tropical varieties thrive in humid forests.", ['instead']),
    (1, 'addition', "The new phone has a faster processor.", "its battery lasts nearly twice as long.", ['similarity', 'emphasis']),
    (1, 'result', "The lake&rsquo;s water level has dropped every year since 2010.", "several boat launches have been closed.", ['sequence', 'addition']),
    (1, 'contrast', "Critics called the film slow.", "audiences packed theaters for weeks.", ['emphasis']),
    (1, 'example', "Some materials conduct electricity extremely well.", "copper is widely used in household wiring.", ['addition', 'emphasis']),
    (1, 'similarity', "In the 1800s, railroads transformed how goods moved across continents.", "the internet has transformed how information moves in our own time.", ['addition']),
    (1, 'earlier', "The bakery now sells only online.", "it operated a storefront for thirty years.", ['contrast', 'sequence']),
    (2, 'contrast', "The study found a strong link between exercise and improved mood.", "the researchers caution that the link does not prove exercise causes the improvement.", ['addition', 'instead'], 'Even so,'),
    (2, 'emphasis', "The bridge&rsquo;s design was unconventional.", "no other bridge of its era used cables in this arrangement.", ['addition', 'example'], 'In fact,'),
    (2, 'meanwhile', "Engineers in the north worked to repair the power lines.", "crews in the south restored water service.", ['addition', 'similarity'], 'Meanwhile,'),
    (2, 'instead', "Ortiz did not use commercial dyes for the fabric.", "she extracted pigments from local plants.", ['contrast', 'emphasis'], 'Instead,'),
    (2, 'earlier', "The first draft of the treaty was signed in March.", "negotiators had spent the previous year disputing borders.", ['contrast', 'emphasis', 'addition'], 'Before that,'),
    # added 2026-09: more pairs so transitions stop repeating within a few weeks (append only; uids are index-based)
    (0, 'result', "The team practiced passing every day for a month.", "its passing improved noticeably by the end of the season.", ['sequence', 'addition', 'meanwhile']),
    (0, 'contrast', "Penguins are birds.", "they cannot fly.", ['emphasis', 'instead']),
    (0, 'example', "Some foods are high in vitamin C.", "oranges and strawberries contain large amounts of it.", ['addition', 'emphasis']),
    (0, 'addition', "The new library has a large reading room.", "it offers free classes on weekends.", ['similarity', 'emphasis', 'meanwhile']),
    (0, 'sequence', "First, the students chose a topic for their project.", "they gathered sources at the library.", ['result', 'addition', 'meanwhile']),
    (0, 'result', "The river flooded the only road into the village.", "supplies had to be delivered by boat.", ['sequence', 'meanwhile']),
    (0, 'contrast', "The movie was very long.", "the audience stayed engaged until the end.", ['emphasis']),
    (0, 'similarity', "Bats use sound to find their way in the dark.", "dolphins use sound to navigate murky water.", ['addition', 'example']),
    (1, 'contrast', "Many people assume that deserts are lifeless.", "the Sonoran Desert supports thousands of plant and animal species.", ['emphasis', 'instead', 'example']),
    (1, 'result', "The factory switched from coal to natural gas.", "its carbon emissions fell by nearly half.", ['sequence', 'addition', 'meanwhile']),
    (1, 'example', "Some architects design buildings that generate their own energy.", "one office tower in Oslo produces more electricity than it uses.", ['addition', 'emphasis']),
    (1, 'addition', "The drought reduced the region&rsquo;s wheat harvest.", "it forced ranchers to buy feed for their cattle.", ['similarity', 'emphasis', 'result', 'meanwhile']),
    (1, 'earlier', "Today the old mill is a popular art museum.", "it produced textiles for more than a century.", ['contrast', 'sequence']),
    (1, 'instead', "The author did not describe the character&rsquo;s appearance directly.", "she revealed it through other characters&rsquo; reactions.", ['contrast', 'emphasis']),
    (1, 'meanwhile', "Scientists on the ship collected water samples from the surface.", "a robotic submarine gathered samples from the ocean floor.", ['addition', 'similarity', 'contrast']),
    (1, 'similarity', "Ancient Roman cities had public baths where people gathered to talk.", "modern community centers give neighbors a shared place to meet.", ['addition']),
    (2, 'contrast', "The new vaccine produced a strong immune response in laboratory animals.", "early human trials have shown a weaker effect than researchers expected.", ['addition', 'emphasis', 'instead'], 'However,'),
    (2, 'emphasis', "The composer rarely revised her scores.", "several of her symphonies were published exactly as she first wrote them.", ['addition', 'example', 'result'], 'Indeed,'),
    (2, 'result', "The two species of finch compete for the same seeds.", "where both are present, each has evolved a different beak size that suits a different seed.", ['sequence', 'addition', 'emphasis', 'meanwhile'], 'Consequently,'),
    (2, 'instead', "Historians once treated the letters as simple personal correspondence.", "they read them as carefully crafted political arguments.", ['contrast', 'emphasis', 'sequence', 'earlier'], 'Today, however,'),
    (2, 'contrast', "Early critics dismissed the novel as a minor adventure story.", "later readers found in it a sharp critique of colonial power.", ['instead', 'emphasis', 'addition'], 'By contrast,'),
    (2, 'addition', "The policy lowered costs for patients.", "it reduced the paperwork that doctors had to complete.", ['similarity', 'emphasis', 'result', 'meanwhile'], 'Moreover,'),
    (2, 'example', "Some insects have evolved remarkable defenses against predators.", "the bombardier beetle sprays a boiling chemical mixture from its abdomen.", ['addition', 'emphasis'], 'For example,'),
    (2, 'meanwhile', "While the orchestra rehearsed in the main hall, the soloist practiced alone in a small room upstairs.", "the stage crew adjusted the lights for the evening performance.", ['addition', 'sequence', 'similarity', 'contrast'], 'Meanwhile,'),
    # added 2026-09 (second batch; append only)
    (0, 'contrast', "The puzzle looked easy at first.", "it took the family three evenings to finish.", ['emphasis', 'instead']),
    (0, 'result', "The power went out during the storm.", "the family ate dinner by candlelight.", ['sequence', 'meanwhile']),
    (0, 'example', "Many animals sleep through the winter.", "bears spend months resting in their dens.", ['addition', 'emphasis']),
    (0, 'addition', "Cycling to school is good exercise.", "it saves money on bus fare.", ['similarity', 'emphasis', 'result']),
    (0, 'sequence', "First, the chef chopped the onions.", "she cooked them slowly in butter.", ['result', 'addition']),
    (0, 'similarity', "Frogs begin life in water.", "salamanders hatch from eggs laid in ponds and streams.", ['addition', 'example']),
    (1, 'contrast', "The company&rsquo;s profits rose sharply last year.", "its workers&rsquo; wages stayed the same.", ['emphasis', 'meanwhile', 'instead']),
    (1, 'result', "The bridge was closed for repairs all summer.", "drivers had to take a detour that added twenty minutes to their trips.", ['sequence', 'meanwhile', 'addition']),
    (1, 'example', "Some plants protect themselves with chemicals.", "milkweed contains a bitter sap that makes most animals sick.", ['addition', 'emphasis']),
    (1, 'earlier', "The painter is now famous for her bold landscapes.", "she worked for a decade as an illustrator of children&rsquo;s books.", ['contrast', 'sequence']),
    (1, 'instead', "The school did not buy new laptops for every student.", "it set up a lending program so students could borrow them.", ['contrast', 'emphasis', 'result']),
    (1, 'addition', "The museum&rsquo;s new exhibit features ancient pottery.", "it includes tools that were used to make the pots.", ['similarity', 'emphasis', 'example', 'meanwhile']),
    (2, 'contrast', "Most historians credit the treaty with ending the war.", "a growing number argue that the fighting had already stopped for other reasons.", ['instead', 'emphasis', 'addition', 'meanwhile'], 'Nevertheless,'),
    (2, 'result', "The river&rsquo;s course shifted westward in the 1600s.", "the town that had grown up on its banks was left several kilometers from the water.", ['sequence', 'addition', 'emphasis', 'earlier'], 'As a result,'),
    (2, 'emphasis', "The author disliked publicity.", "she refused every interview request for the last thirty years of her life.", ['addition', 'example', 'result'], 'In fact,'),
    (2, 'similarity', "Early printing presses made books affordable to ordinary readers.", "cheap recording technology put music within reach of households that could never have hired musicians.", ['addition', 'example', 'meanwhile'], 'Likewise,'),
    (2, 'instead', "The scientists did not attempt to eliminate the invasive fish entirely.", "they focused on protecting the few streams where native trout still spawned.", ['contrast', 'emphasis', 'result', 'sequence'], 'Instead,'),
    (2, 'earlier', "The theory is now widely accepted.", "it was dismissed for decades by researchers who found its evidence too thin.", ['contrast', 'sequence', 'emphasis'], 'Previously,'),
]


def transitions(r, d, spr):
    pool = [(i, t) for i, t in enumerate(TPAIRS) if t[0] == d]
    i, t = pool[r.randrange(len(pool))]
    rel, s1, s2, ban = t[1], t[2], t[3], t[4]
    correct = t[5] if len(t) > 5 else r.choice(REL_POOL[rel])
    others = [k for k in REL_POOL if k != rel and k not in ban]
    r.shuffle(others)
    wrongs = []
    for k in others[:3]:
        w = r.choice(REL_POOL[k])
        wrongs.append((w, '&ldquo;%s&rdquo; signals %s, but the second sentence does not do that.' % (w.rstrip(','), REL_DESC[k])))
    ans = (correct, 'The second sentence gives %s, so &ldquo;%s&rdquo; is the logical transition.' % (REL_DESC[rel], correct.rstrip(',')))
    passage = "%s %s %s" % (s1, '______', s2)
    return build(r, passage, Q_TRANS, ans, wrongs, 'transitions:%d' % i)


# ------------------------------------------------------------------ boundaries (punctuation)
B_NONE = [  # subject-verb: no punctuation between a subject and its verb
    ("The reason the old stone bridge has survived so many", "centuries", "is its unusually deep foundation."),
    ("The scientists who spent three winters studying the glacier&rsquo;s slow", "retreat", "published their findings in March."),
    ("A flock of migrating geese that had been blown far off", "course", "landed in the town square."),
    ("Whoever first noticed that the river had begun to change its", "path", "alerted the village elders."),
    ("The gardener who planted the rows of tulips along the front", "walk", "retired last spring."),
    ("What the committee members most wanted to understand about the budget", "proposal", "was why costs had doubled."),
    ("The small wooden boxes that the museum&rsquo;s staff found stacked in the old", "attic", "contained letters from the 1800s."),
    ("Anyone who wants to join the school&rsquo;s robotics", "club", "should attend the meeting on Thursday."),
]
B_INTRO = [
    ("After the storm finally", "passed", "the crew resumed repairs on the roof."),
    ("When the museum opened its new wing in", "June", "attendance nearly doubled."),
    ("Although the trail was steep and", "rocky", "most of the hikers finished before noon."),
    ("Because the printer had run out of", "ink", "the students turned in handwritten reports."),
    ("Before the first frost arrived at the", "farm", "workers picked the last of the apples."),
    ("If the seedlings are kept in", "shade", "they will grow tall and thin."),
    ("While the paint on the walls was still", "wet", "the workers covered the floor with plastic."),
    ("To reach the summit before", "dark", "the climbers left camp at four in the morning."),
]
B_FANBOYS = [
    ("The trail was closed for", "repairs", "so", "hikers used the northern route instead."),
    ("Maria studied the map for", "hours", "but", "she still could not find the cabin."),
    ("The band rehearsed every", "evening", "and", "their performance was flawless."),
    ("The lake had frozen solid by", "December", "yet", "the ice fishermen stayed home."),
    ("The bakery sold out of bread by", "noon", "and", "the owner closed early."),
    ("The museum closed its doors at", "six", "but", "the caf&eacute; stayed open late."),
    ("The seedlings grew quickly in the", "greenhouse", "so", "the gardeners moved them outside in May."),
]
B_SPLICE = [
    ("The museum opens at", "nine", "and", "the gift shop opens at ten."),
    ("Carlos wanted to join the debate", "team", "but", "he was afraid of speaking in public."),
    ("The harvest was smaller than expected", "", "so", "prices rose across the region."),
    ("Ines had rehearsed her speech all", "week", "yet", "her hands still shook at the podium."),
    ("The wind picked up in the", "afternoon", "so", "the sailors lowered the largest sail."),
    ("Amara practiced the piano for", "hours", "but", "the final passage still gave her trouble."),
]
B_SEMI = [
    ("The experiment did not produce the expected", "result", "however", "the team learned something valuable about the equipment."),
    ("Solar panels are expensive to", "install", "nevertheless", "many homeowners consider them a good investment."),
    ("The first survey drew only a few", "responses", "therefore", "the researchers sent a second round of questionnaires."),
    ("Ella has never been to", "Japan", "still", "she speaks the language fluently."),
    ("Rainfall was well below average last", "year", "consequently", "reservoir levels dropped sharply."),
    ("The committee approved the", "plan", "moreover", "it promised additional funding for repairs."),
    ("The trail was muddy after the", "rain", "nonetheless", "dozens of runners showed up for the race."),
    ("The library extended its weekend", "hours", "as a result", "more students came to study on Sundays."),
]
B_COLON = [
    ("The recipe calls for three", "ingredients", "flour, sugar, and eggs."),
    ("The expedition faced one major", "obstacle", "the unpredictable weather."),
    ("Sofia packed only the", "essentials", "a tent, a stove, and a map."),
    ("The museum offers two free", "programs", "a guided tour and a film screening."),
    ("The garden produced a single", "crop", "tomatoes."),
    ("The coach gave the team one simple", "rule", "never stop running until the whistle blows."),
]
B_NOCOLON = [
    ("The committee is composed", "of", "engineers, teachers, and two students."),
    ("The trail passes", "through", "meadows, forests, and a narrow canyon."),
    ("Her favorite subjects", "are", "biology, chemistry, and art."),
    ("The kit for new members includes", "a", "membership card, a handbook, and a T-shirt."),
    ("The best times to see the comet", "are", "just after sunset and just before dawn."),
    ("The team&rsquo;s equipment", "included", "ropes, helmets, and two-way radios."),
]
B_APPOS = [
    ("The novelist", "Jorge Tell", "whose debut appeared in 2005", "has won several international awards."),
    ("The physicist", "Amina Rahal", "who leads the observatory", "will speak at the conference."),
    ("Our school&rsquo;s founder", "Elena Park", "a former chemistry teacher", "donated her library to the town."),
    ("The city&rsquo;s oldest bridge", "the Iron Span", "which opened in 1889", "is closing for repairs."),
    ("The chef", "Marco Diaz", "who trained in Lyon", "opened a restaurant downtown."),
    ("Our town&rsquo;s newest park", "Riverside Commons", "which opened in May", "has a skate ramp and a pond."),
]
B_DASH = [
    ("The lab&rsquo;s newest", "instrument", "a spectrometer that cost two million dollars", "arrived on Tuesday."),
    ("Her first", "album", "recorded in a single afternoon", "sold out within a week."),
    ("The village&rsquo;s only", "bakery", "which had been open for ninety years", "closed in April."),
    ("The orchestra&rsquo;s newest", "member", "a cellist from Seoul", "impressed the audience."),
    ("The team&rsquo;s star", "player", "a forward who had scored in every game", "was injured in practice."),
    ("The city&rsquo;s tallest", "building", "a glass tower finished in 2019", "sways slightly in strong winds."),
]
B_SERIES = [
    ("The tour will visit", [("Austin", "Texas"), ("Denver", "Colorado"), ("Boise", "Idaho")], "over ten days."),
    ("The panel included", [("Dr. Lena Ortiz", "a chemist"), ("Marcus Bell", "an engineer"), ("Yuki Tanaka", "a designer")], "and reviewed every proposal."),
    ("The festival will be held in", [("Lyon", "France"), ("Porto", "Portugal"), ("Ghent", "Belgium")], "this summer."),
    ("Winners came from", [("Ravi Nair", "a sophomore"), ("Grace Lin", "a senior"), ("Tomas Reyes", "a freshman")], "this year."),
    ("The conference brought together", [("Ana Silva", "a biologist"), ("Omar Aziz", "a geologist"), ("Mei Chen", "a chemist")], "for three days."),
    ("The band played in", [("Nashville", "Tennessee"), ("Tulsa", "Oklahoma"), ("Omaha", "Nebraska")], "last spring."),
]


def boundaries(r, d, spr):
    kinds = {0: ['none', 'intro', 'fanboys'], 1: ['semi', 'colon', 'splice', 'intro'], 2: ['appos', 'dash', 'series', 'nocolon', 'none']}[d]
    k = r.choice(kinds)
    if k == 'none':
        i = r.randrange(len(B_NONE)); p, w, rest = B_NONE[i]
        return plain(r, p, rest, w, [w + ',', w + ':', w + ';'],
                     'A subject and its verb are never separated by a single punctuation mark. Nothing is needed after &ldquo;%s.&rdquo;' % w,
                     'Adding punctuation splits the subject from its verb.', 'boundaries:none:%d' % i)
    if k == 'intro':
        i = r.randrange(len(B_INTRO)); p, w, rest = B_INTRO[i]
        return plain(r, p, rest, w + ',', [w, w + ';', w + ':'],
                     'An introductory clause or phrase is followed by a comma before the main clause begins.',
                     'The introductory element needs a comma to join it to the main clause.', 'boundaries:intro:%d' % i)
    if k == 'fanboys':
        i = r.randrange(len(B_FANBOYS)); p, w, c, rest = B_FANBOYS[i]
        return plain(r, p, rest, '%s, %s' % (w, c), ['%s %s' % (w, c), '%s; %s' % (w, c), '%s: %s' % (w, c)],
                     'Two independent clauses joined by &ldquo;%s&rdquo; need a comma before the conjunction.' % c,
                     'Two complete clauses joined by a conjunction need a comma before the conjunction; a semicolon or colon does not pair with it.', 'boundaries:fan:%d' % i)
    if k == 'splice':
        i = r.randrange(len(B_SPLICE)); p, w, c, rest = B_SPLICE[i]
        p2, w2 = (p, w) if w else (p.rsplit(' ', 1)[0], p.rsplit(' ', 1)[1])
        return plain(r, p2, rest, '%s, %s' % (w2, c), ['%s,' % w2, '%s %s' % (w2, c), '%s; %s' % (w2, c)],
                     'Join two independent clauses with a comma plus a coordinating conjunction.',
                     'A comma alone makes a comma splice, and a missing comma or a semicolon with &ldquo;%s&rdquo; is incorrect.' % c, 'boundaries:splice:%d' % i)
    if k == 'semi':
        i = r.randrange(len(B_SEMI)); p, w, adv, rest = B_SEMI[i]
        return plain(r, p, rest, '%s; %s,' % (w, adv), ['%s, %s,' % (w, adv), '%s %s,' % (w, adv), '%s; %s' % (w, adv)],
                     'A conjunctive adverb such as &ldquo;%s&rdquo; joining two independent clauses takes a semicolon before it and a comma after it.' % adv,
                     'A comma before the adverb makes a comma splice, no punctuation makes a run-on, and the adverb needs a comma after it.', 'boundaries:semi:%d' % i)
    if k == 'colon':
        i = r.randrange(len(B_COLON)); p, w, rest = B_COLON[i]
        return plain(r, p, rest, w + ':', [w + ',', w + ';', w],
                     'A colon can follow a complete sentence to introduce an explanation or list.',
                     'Only a colon correctly introduces what the complete sentence promises.', 'boundaries:colon:%d' % i)
    if k == 'nocolon':
        i = r.randrange(len(B_NOCOLON)); p, w, rest = B_NOCOLON[i]
        return plain(r, p, rest, w, [w + ':', w + ',', w + ';'],
                     'A colon must follow a complete sentence. Here the list completes the verb or preposition, so no punctuation is needed.',
                     'This mark interrupts a sentence that is not yet complete.', 'boundaries:nocolon:%d' % i)
    if k == 'appos':
        i = r.randrange(len(B_APPOS)); p, name, cl, rest = B_APPOS[i]
        return plain(r, p, rest, '%s, %s,' % (name, cl), ['%s %s,' % (name, cl), '%s, %s' % (name, cl), '%s %s' % (name, cl)],
                     'Extra information that can be removed without changing the sentence&rsquo;s core meaning is set off by a pair of commas, one before and one after.',
                     'Non-essential information needs both commas; a missing comma on either side is an error.', 'boundaries:appos:%d' % i)
    if k == 'dash':
        i = r.randrange(len(B_DASH)); p, w, ph, rest = B_DASH[i]
        return plain(r, p, rest, '%s&mdash;%s&mdash;' % (w, ph), ['%s, %s&mdash;' % (w, ph), '%s&mdash;%s,' % (w, ph), '%s; %s;' % (w, ph)],
                     'An interrupting phrase set off with dashes needs a dash on each side. Marks must match at both ends.',
                     'The opening and closing marks do not match, or a semicolon is used where a semicolon cannot set off an interrupter.', 'boundaries:dash:%d' % i)
    i = r.randrange(len(B_SERIES)); p, pairs, rest = B_SERIES[i]
    ok = ', '.join(['%s, %s' % pairs[0]]).replace('', '') + '; %s, %s; and %s, %s' % (pairs[1] + pairs[2])
    bad1 = '%s, %s, %s, %s, and %s, %s' % (pairs[0] + pairs[1] + pairs[2])
    bad2 = '%s, %s; %s, %s, and %s, %s' % (pairs[0] + pairs[1] + pairs[2])
    bad3 = '%s; %s, %s; %s, and %s; %s' % (pairs[0] + pairs[1] + pairs[2])
    return plain(r, p, rest, ok, [bad1, bad2, bad3],
                 'When items in a series already contain commas, separate the items with semicolons to keep them distinct.',
                 'Commas alone (or a mix of marks) make it impossible to tell where one item ends and the next begins.', 'boundaries:series:%d' % i)


# ------------------------------------------------------------------ form, structure, and sense
VERB_EXTRA = {('is', 'are'): ('being', 'be'), ('was', 'were'): ('been', 'being'), ('seems', 'seem'): ('seeming', 'to seem'),
              ('makes', 'make'): ('making', 'to make'), ('has', 'have'): ('having', 'to have'), ('needs', 'need'): ('needing', 'to need'),
              ('lies', 'lie'): ('lying', 'to lie'), ('suggests', 'suggest'): ('suggesting', 'to suggest')}
SV = {
    0: [("The box of old letters", 's', ('is', 'are'), "still in the attic."),
        ("The teachers in the science department", 'p', ('makes', 'make'), "learning fun for every student."),
        ("The stack of graded papers", 's', ('was', 'were'), "on the desk this morning."),
        ("A group of hikers from the nearby camp", 's', ('was', 'were'), "rescued after the storm.")],
    1: [("Neither the coach nor the players", 'p', ('was', 'were'), "aware of the schedule change."),
        ("Neither the players nor the coach", 's', ('was', 'were'), "aware of the schedule change."),
        ("Each of the newly planted saplings", 's', ('needs', 'need'), "daily watering."),
        ("The findings of the committee, which met for six months,", 'p', ('suggests', 'suggest'), "that funding should increase.")],
    2: [("Among the treasures recovered from the shipwreck", 'p', ('was', 'were'), "a gold compass and two silver goblets."),
        ("Beyond the mountains", 's', ('lies', 'lie'), "a valley of terraced farms."),
        ("The number of students who enrolled in evening courses", 's', ('has', 'have'), "risen steadily this decade."),
        ("A large collection of manuscripts, along with several rare maps,", 's', ('is', 'are'), "housed in the university library.")],
}
TENSE = {
    0: [("After the storm ended, the crew inspected the roof and", "replaced", ["replaces", "will replace", "replacing"], "the damaged shingles."),
        ("Yesterday, Marcus walked to the station, bought a ticket, and", "boarded", ["boards", "will board", "boarding"], "the next train to the city."),
        ("Last summer, the Ruiz family", "visited", ["visits", "will visit", "visiting"], "three national parks in two weeks."),
        ("Every morning before sunrise, the baker", "lights", ["lit", "will light", "lighting"], "the ovens and begins mixing the dough."),
        ("Next spring, the city", "will open", ["opened", "has opened", "opening"], "a new public pool beside the library.")],
    1: [("When the museum first opened in 1925, it displayed only a few paintings, but by 1950 its collection", "grew", ["grows", "will grow", "has grown"], "to more than two thousand works."),
        ("The novel follows a young sailor who leaves home and", "returns", ["returned", "had returned", "returning"], "years later as a captain.")],
    2: [("By the time the rescuers reached the summit, the climbers", "had been waiting", ["have been waiting", "are waiting", "will have waited"], "for two days without food."),
        ("If the committee had reviewed the data earlier, it", "would have caught", ["will catch", "would catch", "caught"], "the error before the report was published.")],
}
PRON = {
    0: [("The company revised", "its", ["it&rsquo;s", "their", "they&rsquo;re"], "policy after receiving hundreds of complaints.", "&ldquo;Its&rdquo; is the possessive form that agrees with the singular noun &ldquo;company.&rdquo; &ldquo;It&rsquo;s&rdquo; means &ldquo;it is.&rdquo;"),
        ("The students finished", "their", ["there", "they&rsquo;re", "its"], "science projects a day early.", "&ldquo;Their&rdquo; is the possessive pronoun for the plural &ldquo;students.&rdquo; &ldquo;There&rdquo; names a place, and &ldquo;they&rsquo;re&rdquo; means &ldquo;they are.&rdquo;"),
        ("The dog wagged", "its", ["it&rsquo;s", "its&rsquo;", "their"], "tail when the children came home.", "&ldquo;Its&rdquo; is the possessive form for the singular &ldquo;dog.&rdquo; &ldquo;It&rsquo;s&rdquo; means &ldquo;it is,&rdquo; and &ldquo;its&rsquo;&rdquo; is not a word."),
        ("The coach told Maya and", "me", ["I", "myself", "mine"], "that practice would start early.", "The pronoun is an object of &ldquo;told,&rdquo; so the object form &ldquo;me&rdquo; is correct.")],
    1: [("The company announced that", "it", ["they", "them", "those"], "would move its headquarters next year.", "&ldquo;Company&rdquo; is a singular noun, so the pronoun must be singular: &ldquo;it.&rdquo;"),
        ("The award goes to the student", "whose", ["who&rsquo;s", "who", "whom"], "essay best captures the spirit of the program.", "&ldquo;Whose&rdquo; shows possession of &ldquo;essay.&rdquo; &ldquo;Who&rsquo;s&rdquo; means &ldquo;who is.&rdquo;"),
        ("The manager thanked Priya and", "me", ["I", "myself", "my"], "for finishing the report early.", "The pronoun is the object of &ldquo;thanked,&rdquo; so the object form &ldquo;me&rdquo; is needed.")],
    2: [("The books on the top shelf are older than", "those", ["that", "them", "they"], "on the table.", "&ldquo;Those&rdquo; refers back to the plural &ldquo;books&rdquo; and completes the comparison.")],
}
POSS = [
    ("Ms. Ortiz, the club&rsquo;s treasurer, kept careful records, and the", "treasurer&rsquo;s", ["treasurers&rsquo;", "treasurers", "treasurer"], "report showed a small surplus.", "One treasurer owns the report, so use the singular possessive."),
    ("Three of the club&rsquo;s treasurers met on Monday, and the", "treasurers&rsquo;", ["treasurer&rsquo;s", "treasurers", "treasurers&rsquo;s"], "reports all showed a small surplus.", "Several treasurers share ownership, so use the plural possessive."),
    ("A pair of sparrows arrived in March, and the", "sparrows&rsquo;", ["sparrow&rsquo;s", "sparrows", "sparrows&rsquo;s"], "nest was soon finished.", "The nest belongs to two sparrows, so the plural possessive is needed."),
    ("Ana and Lucia are sisters, and the", "sisters&rsquo;", ["sister&rsquo;s", "sisters", "sisters&rsquo;s"], "bicycles were parked outside.", "The bicycles belong to both sisters, so use the plural possessive."),
]
PARA = {
    0: [("On Saturdays, Leo likes swimming, biking, and", "hiking", ["to hike", "he hikes", "a hike"], "."),
        ("The recipe calls for flour, sugar, and", "two eggs", ["cracking two eggs", "to add two eggs", "you add two eggs"], "."),
        ("The new park has a playground, a pond, and", "a walking trail", ["walking on a trail", "to walk on trails", "you can walk"], ".")],
    1: [("The volunteers spent the day sorting donations, packing boxes, and", "loading trucks", ["to load trucks", "they loaded trucks", "trucks were loaded"], "."),
        ("The new library is designed to be spacious, energy efficient, and", "easy to navigate", ["it is easy to navigate", "navigation is easy", "having easy navigation"], ".")],
    2: [("The study examined how quickly the plants grew, how much water they consumed, and", "how well they resisted disease", ["their resistance to disease was measured", "resisting disease", "the disease resistance"], "."),
        ("Candidates were asked to describe their experience, explain their goals, and", "submit", ["submitting", "a submission of", "they should submit"], "a writing sample.")],
}
DANGLE = [
    ("Walking along the shore at dawn,", "the child noticed a hermit crab half buried in the sand.", ["a hermit crab half buried in the sand caught the child&rsquo;s eye.", "the sand hid a hermit crab from view.", "the sunrise made the shoreline glitter."]),
    ("Having spent three years studying the ruins,", "the archaeologist knew every stone by heart.", ["every stone of the ruins was familiar to the archaeologist.", "the ruins were well known to the archaeologist.", "the archaeologist&rsquo;s knowledge of the ruins was complete."]),
    ("Exhausted after the long climb,", "the hikers set up camp early.", ["the tents were set up early.", "a campsite was chosen early.", "setting up camp early was the plan."]),
    ("Written in just two weeks,", "the novel became the author&rsquo;s most popular work.", ["the author found the novel her most popular work.", "the author&rsquo;s most popular work was widely praised.", "critics called the author&rsquo;s style unusually fast."]),
]
COMPLETE = {
    1: [("Although the forecast called for rain,", "the parade went ahead as planned.", ["the parade going ahead as planned.", "and the parade went ahead as planned.", "so the parade went ahead as planned."]),
        ("The old clock tower, which has stood in the town square for more than two hundred years,", "is being restored by volunteers.", ["being restored by volunteers.", "it is being restored by volunteers.", "and being restored by volunteers."]),
        ("Because the bridge was closed for repairs,", "drivers took a longer route through the valley.", ["drivers taking a longer route through the valley.", "and drivers took a longer route through the valley.", "which drivers took a longer route through the valley."])],
}


def form_structure(r, d, spr):
    kinds = {0: ['sv', 'tense', 'pron', 'para', 'poss'], 1: ['sv', 'tense', 'pron', 'poss', 'para', 'complete'], 2: ['sv', 'tense', 'pron', 'para', 'dangle']}[d]
    k = r.choice(kinds)
    if k == 'sv':
        i = r.randrange(len(SV[d])); subj, num, (sg, pl), rest = SV[d][i]
        ok, bad = (sg, pl) if num == 's' else (pl, sg)
        ex = VERB_EXTRA[(sg, pl)]
        why = 'The subject &ldquo;%s&rdquo; is %s, so the verb must be &ldquo;%s.&rdquo; Ignore intervening phrases and check what the subject really is.' % (
            subj.rstrip(','), 'singular' if num == 's' else 'plural', ok)
        return plain(r, subj, rest, ok, [bad, ex[0], ex[1]], why,
                     lambda b: 'This form does not agree with the subject or does not create a complete, correct verb.', 'form:sv:%d:%d' % (d, i))
    if k == 'tense':
        i = r.randrange(len(TENSE[d])); p, ok, bad, rest = TENSE[d][i]
        return plain(r, p, rest, ok, bad, 'The surrounding verbs set the time frame; &ldquo;%s&rdquo; keeps the sentence consistent and logical.' % ok,
                     'This verb form does not match the time frame set by the rest of the sentence.', 'form:tense:%d:%d' % (d, i))
    if k == 'pron':
        i = r.randrange(len(PRON[d])); p, ok, bad, rest, why = PRON[d][i]
        return plain(r, p, rest, ok, bad, why, 'This pronoun form does not match its role or its antecedent in the sentence.', 'form:pron:%d:%d' % (d, i))
    if k == 'poss':
        i = r.randrange(len(POSS)); p, ok, bad, rest, why = POSS[i]
        return plain(r, p, rest, ok, bad, why, 'This form is a plain plural, is not possessive, or has the apostrophe in the wrong place.', 'form:poss:%d' % i)
    if k == 'para':
        i = r.randrange(len(PARA[d])); p, ok, bad, rest = PARA[d][i]
        return plain(r, p, rest, ok, bad, 'Items in a series should have the same grammatical form. &ldquo;%s&rdquo; matches the other items.' % ok,
                     'This does not match the grammatical form of the other items in the series.', 'form:para:%d:%d' % (d, i))
    if k == 'complete':
        i = r.randrange(len(COMPLETE[1])); p, ok, bad = COMPLETE[1][i]
        return plain(r, p, '', ok, bad, 'The opening group of words cannot stand alone, so the choice must supply a subject and a finite verb to make a complete sentence without an extra connector.',
                     'This creates a fragment or adds a connector that does not belong after the introductory clause.', 'form:complete:%d' % i)
    i = r.randrange(len(DANGLE)); p, ok, bad = DANGLE[i]
    return plain(r, p, '', ok, bad, 'An opening modifier must be followed by the person or thing it describes. Only this choice names the doer of the action in the phrase.',
                 'The subject of this clause could not have done what the opening phrase describes (a dangling modifier).', 'form:dangle:%d' % i)


# ------------------------------------------------------------------ cross-text (parametric for easy / medium)
XT = [
    dict(t1="Many highland coffee farmers hold that planting shade trees among their coffee bushes protects the crop from heat and improves harvests.",
         sup="Researchers compared 30 farms and found that shaded farms had cooler leaf temperatures and produced about 15 percent more coffee than unshaded farms.",
         con="Researchers compared 30 farms and found that shaded farms had leaf temperatures no different from those of unshaded farms and produced about 10 percent less coffee.",
         qual="Researchers compared 30 farms and found that shaded farms had cooler leaf temperatures but harvests no larger than those of unshaded farms.", who='researchers'),
    dict(t1="City planners predicted that adding protected bike lanes to Elm Street would reduce traffic accidents there.",
         sup="In the six months after the lanes opened, reported accidents on Elm Street fell from 14 to 6.",
         con="In the six months after the lanes opened, reported accidents on Elm Street rose from 14 to 19.",
         qual="In the six months after the lanes opened, cyclist accidents on Elm Street fell from 9 to 3, but total accidents did not change because collisions among cars increased.", who='the author of Text 2'),
    dict(t1="Some educators argue that assigning nightly practice problems improves students&rsquo; unit-test performance.",
         sup="In a study of 400 middle school students, those assigned nightly practice scored on average 8 points higher on unit tests than those assigned none.",
         con="In a study of 400 middle school students, those assigned nightly practice scored no higher on unit tests than those assigned none.",
         qual="In a study of 400 middle school students, those assigned nightly practice scored higher on unit tests, but only in classes where teachers reviewed the problems the next day.", who='the author of Text 2'),
    dict(t1="Some bird enthusiasts believe that backyard feeders make wild birds dependent on people and less likely to forage naturally.",
         sup="Tracking of 200 chickadees showed that birds with access to feeders spent 40 percent less time foraging than birds without feeders and drew most of their food from the feeders.",
         con="Tracking of 200 chickadees showed that birds with access to feeders foraged as much as birds without feeders and drew most of their food from natural sources.",
         qual="Tracking of 200 chickadees showed that birds drew most of their food from natural sources in summer but relied heavily on feeders during winter cold snaps.", who='the author of Text 2'),
    dict(t1="A neuroscientist proposes that sleeping soon after learning improves recall of new material.",
         sup="Students who slept within two hours of studying vocabulary remembered 20 percent more words a week later than students who stayed awake for eight hours.",
         con="Students who slept within two hours of studying vocabulary remembered no more words a week later than students who stayed awake for eight hours.",
         qual="Students who slept soon after studying remembered more words a week later when they studied in the evening but showed no benefit when they studied in the morning.", who='the author of Text 2'),
    dict(t1="Homeowners in the region often assume that rooftop solar panels pay for themselves within ten years.",
         sup="An audit of 120 households found that the median payback period for rooftop solar was 8 years.",
         con="An audit of 120 households found that the median payback period for rooftop solar was 17 years.",
         qual="An audit of 120 households found that payback took about 8 years for homes with south-facing roofs but about 16 years for all other homes.", who='the author of Text 2'),
    dict(t1="Some nutritionists argue that drinking a glass of water before each meal helps people eat less at that meal.",
         sup="In a trial with 80 adults, those who drank water before meals ate about 15 percent fewer calories at those meals than those who did not.",
         con="In a trial with 80 adults, those who drank water before meals ate just as many calories at those meals as those who did not.",
         qual="In a trial with 80 adults, drinking water before meals reduced calories eaten among older participants but not among younger ones.", who='the author of Text 2'),
    dict(t1="Many teachers believe that letting students choose their own books increases how much they read outside of school.",
         sup="A study of 600 fifth graders found that students allowed to choose their own books read about twice as many pages at home as students assigned books.",
         con="A study of 600 fifth graders found that students allowed to choose their own books read no more pages at home than students assigned books.",
         qual="A study of 600 fifth graders found that choice increased reading at home for students who already enjoyed reading but not for reluctant readers.", who='the author of Text 2'),
    dict(t1="Wildlife managers have proposed that building tunnels under highways will reduce the number of animals killed by cars.",
         sup="After tunnels were built under a mountain highway, recorded deaths of deer and foxes on that stretch fell by 80 percent.",
         con="After tunnels were built under a mountain highway, recorded deaths of deer and foxes on that stretch did not change.",
         qual="After tunnels were built under a mountain highway, deaths of foxes on that stretch fell sharply, but deaths of deer, which rarely used the tunnels, did not.", who='the author of Text 2'),
]
XT_OPTS = {
    'sup': ("It is supported by the findings described in Text 2.", "Text 2&rsquo;s results point the same direction as the claim."),
    'con': ("It is contradicted by the findings described in Text 2.", "Text 2&rsquo;s results run against the claim."),
    'qual': ("It holds in some circumstances but not in others, according to Text 2.", "Text 2&rsquo;s results support the claim only under certain conditions."),
    'none': ("It cannot be evaluated because Text 2 addresses an unrelated question.", "Text 2 directly addresses the same question."),
}


def cross_text(r, d, spr):
    if d == 2:
        return authored('cross_text')(r, d, spr)
    i = r.randrange(len(XT)); x = XT[i]
    rel = r.choice(['sup', 'con'] if d == 0 else ['sup', 'con', 'qual', 'qual'])
    passage = '<b>Text 1</b><br>%s<br><br><b>Text 2</b><br>%s' % (x['t1'], x[rel])
    q = 'Based on the texts, how would the author of Text 2 most likely characterize the claim in Text 1?'
    ans = (XT_OPTS[rel][0], XT_OPTS[rel][1])
    wrongs = []
    for k in ['sup', 'con', 'qual', 'none']:
        if k != rel:
            wrongs.append((XT_OPTS[k][0], 'This misdescribes how Text 2&rsquo;s results relate to Text 1&rsquo;s claim.'))
    return build(r, passage, q, ans, wrongs, 'cross_text:%d:%s' % (i, rel))


# ------------------------------------------------------------------ command of evidence: quantitative
def _tbl(title, headers, rows):
    h = ''.join('<th>%s</th>' % x for x in headers)
    b = ''.join('<tr>' + ''.join('<td>%s</td>' % c for c in row) + '</tr>' for row in rows)
    return '<table class="dt"><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (title, h, b)


QT_THEMES = [
    dict(who='students at a high school', what='their preferred study location', unit='percent of students', rows=['Library', 'Home', 'Cafe', 'Classroom', 'Outdoors']),
    dict(who='commuters in a mid-sized city', what='their main way of getting to work', unit='percent of commuters', rows=['Car', 'Bus', 'Bicycle', 'Train', 'Walking']),
    dict(who='visitors to a science museum', what='the exhibit they enjoyed most', unit='percent of visitors', rows=['Space', 'Dinosaurs', 'Robotics', 'Ocean life', 'Electricity']),
    dict(who='households in a small town', what='their main source of heat in winter', unit='percent of households', rows=['Natural gas', 'Electricity', 'Wood', 'Heating oil', 'Solar']),
]
QT_YEARS = [
    dict(who='a community garden', what='pounds of vegetables harvested', title='Annual harvest at Fernhill Community Garden', col='Pounds harvested', base=(120, 220), grow=(80, 160)),
    dict(who='a public library', what='books borrowed', title='Books borrowed per year at Cedar Street Library', col='Books borrowed', base=(4000, 6000), grow=(1200, 2000)),
    dict(who='a city bike-share program', what='rides taken', title='Rides per year in the Harbor City bike-share program', col='Rides taken', base=(9000, 14000), grow=(3000, 5000)),
]


def coe_quant(r, d, spr):
    if d == 0 or (d == 1 and r.random() < .4):
        th = r.choice(QT_THEMES)
        vals = r.sample(range(4, 46, 2), 5)
        rows = list(zip(th['rows'], vals))
        r.shuffle(rows)
        hi = max(rows, key=lambda t: t[1]); lo = min(rows, key=lambda t: t[1])
        rest = sorted([t for t in rows if t not in (hi, lo)], key=lambda t: t[1])
        table = _tbl('Survey of %s about %s' % (th['who'], th['what']), ['Response', th['unit'].capitalize()], [[a, '%d%%' % b] for a, b in rows])
        passage = ('A researcher surveyed %s about %s. The results varied widely by response; for example, ______<br><br>%s' % (th['who'], th['what'], table))
        q = 'Which choice most effectively uses data from the table to complete the example?'
        f = lambda a, b: '%s was chosen by %d%% of respondents' % (a[0], a[1]) if False else None
        ok = 'the most common response was %s at %d%%, while the least common was %s at %d%%.' % (hi[0], hi[1], lo[0], lo[1])
        w1 = 'the two most common responses were %s at %d%% and %s at %d%%.' % (hi[0], hi[1], rest[-1][0], rest[-1][1])
        w2 = 'the most common response was %s at %d%%, while the least common was %s at %d%%.' % (lo[0], hi[1], hi[0], lo[1])
        w3 = 'the two least common responses were %s at %d%% and %s at %d%%.' % (lo[0], lo[1], rest[0][0], rest[0][1])
        return build(r, passage, q, (ok, 'Varied widely needs a very high value and a very low value, correctly matched to their labels: %s (%d%%) and %s (%d%%).' % (hi[0], hi[1], lo[0], lo[1])),
                     [(w1, 'Two high values do not show wide variation.'), (w2, 'The percentages are matched to the wrong labels.'), (w3, 'Two low values do not show wide variation.')],
                     'coe_quant:wide:%s:%s' % (th['rows'][0], hi[0]))
    if d == 1:
        th = r.choice(QT_YEARS)
        y0 = r.choice([2015, 2016, 2017]); b = r.randint(*th['base']); g = r.randint(*th['grow'])
        vals = [b, b + g, b + g + r.randint(g // 4, g // 2), b + 2 * g + r.randint(0, g // 2)]
        vals = sorted(vals)
        rows = [[y0 + i, '{:,}'.format(v)] for i, v in enumerate(vals)]
        table = _tbl(th['title'], ['Year', th['col']], rows)
        passage = ('A city official said that %s at %s grew substantially over the period shown. For example, ______<br><br>%s' % (th['what'], th['who'], table))
        q = 'Which choice most effectively uses data from the table to illustrate the official&rsquo;s claim?'
        fm = lambda v: '{:,}'.format(v)
        ok = 'the count rose from %s in %d to %s in %d.' % (fm(vals[0]), y0, fm(vals[3]), y0 + 3)
        w1 = 'the count rose from %s in %d to %s in %d.' % (fm(vals[1]), y0 + 1, fm(vals[2]), y0 + 2)
        w2 = 'the count fell from %s in %d to %s in %d.' % (fm(vals[3]), y0, fm(vals[0]), y0 + 3)
        w3 = 'the count rose from %s in %d to %s in %d.' % (fm(vals[0]), y0 + 1, fm(vals[3]), y0 + 3)
        return build(r, passage, q, (ok, 'Substantial growth is best shown by the first and last years with correct values: %s to %s.' % (fm(vals[0]), fm(vals[3])),),
                     [(w1, 'This is a real increase, but a small one that does not show substantial growth over the full period.'),
                      (w2, 'The values are reversed, so this describes a decline.'),
                      (w3, 'The starting value is matched to the wrong year.')],
                     'coe_quant:trend:%s:%d' % (th['col'], vals[0]))
    # hard: a claim that two measures need not go together; the key is the one row where the first is high and the second low
    ti = r.randrange(len(QT_TWO)); th = QT_TWO[ti]
    names = r.sample(th['names'], 4)
    a_hi, b_lo = r.randint(70, 88), r.randint(8, 22)
    rows = [(names[0], a_hi, b_lo), (names[1], r.randint(70, 88), r.randint(60, 80)), (names[2], r.randint(20, 35), r.randint(8, 22)), (names[3], r.randint(20, 35), r.randint(60, 80))]
    while rows[1][1] == a_hi: rows[1] = (rows[1][0], r.randint(70, 88), rows[1][2])
    rows.sort(key=lambda t: th['names'].index(t[0]))  # tables list rows in natural order (towns A-Z, ages youngest first)
    table = _tbl(th['title'], [th['ent'], th['a'], th['b']], [[t, '%d%%' % a, '%d%%' % b] for t, a, b in rows])
    passage = '%s For example, ______<br><br>%s' % (th['claim'], table)
    q = 'Which choice most effectively uses data from the table to illustrate the %s&rsquo;s point?' % th['who']
    d_ = {n: (a, b) for n, a, b in rows}
    say = lambda n, lead: th['say'] % dict(n=n, a=d_[n][0], b=d_[n][1], lead=lead)
    # every choice uses the same neutral connector, so the wording never hints at which row shows the gap
    ok = say(names[0], 'and')
    w1, w2, w3 = say(names[1], 'and'), say(names[2], 'and'), say(names[3], 'and')
    uid = 'coe_quant:two:%s' % names[0] if ti == 0 else 'coe_quant:two%d:%s' % (ti, names[0])
    return build(r, passage, q, (ok, 'The point needs a high first value together with a low second value; only %s has both.' % names[0]),
                 [(w1, 'Both values are high, so here the two measures do go together.'), (w2, 'Both values are low, which does not show a gap between the two measures.'),
                  (w3, 'A low first value with a high second value is the reverse of the point.')], uid)


# (claim, who makes it, table title, entity column, measure A, measure B, sentence pattern, entity names)
QT_TWO = [
    dict(claim='A transportation analyst noted that owning a bicycle does not necessarily mean people commute by bicycle.', who='analyst',
         title='Bicycle ownership and bicycle commuting by town', ent='Town', a='Households owning a bicycle', b='Workers commuting by bicycle',
         say='in %(n)s, %(a)d%% of households own a bicycle %(lead)s %(b)d%% of workers commute by bicycle.',
         names=['Ashford', 'Brenner', 'Calloway', 'Dunmore', 'Easton', 'Fairmont']),
    dict(claim='A librarian observed that having a library card does not necessarily mean a person borrows books.', who='librarian',
         title='Library cards and borrowing by county', ent='County', a='Residents with a library card', b='Residents who borrowed a book last year',
         say='in %(n)s County, %(a)d%% of residents have a library card %(lead)s %(b)d%% borrowed a book last year.',
         names=['Harlan', 'Juniper', 'Kessler', 'Linwood', 'Marlow', 'Norcross']),
    dict(claim='An education researcher argued that home internet access does not guarantee that students complete online homework.', who='researcher',
         title='Home internet access and online homework completion by school', ent='School', a='Students with home internet', b='Online assignments completed',
         say='at %(n)s, %(a)d%% of students have home internet access %(lead)s %(b)d%% of online assignments were completed.',
         names=['Oakridge High', 'Pinecrest High', 'Quarry Hill High', 'Riverside High', 'Stonebridge High', 'Twin Lakes High']),
    dict(claim='A public-health researcher noted that knowing a health recommendation does not necessarily mean people follow it.', who='researcher',
         title='Awareness of and adherence to a sleep recommendation by age group', ent='Age group', a='Aware of the recommendation', b='Report following it',
         say='among %(n)s, %(a)d%% are aware of the recommendation %(lead)s %(b)d%% report following it.',
         names=['adults aged 18&ndash;24', 'adults aged 25&ndash;34', 'adults aged 35&ndash;44', 'adults aged 45&ndash;54', 'adults aged 55&ndash;64', 'adults aged 65 and older']),
    dict(claim='An agricultural economist observed that owning irrigation equipment does not necessarily mean farmers use it regularly.', who='economist',
         title='Irrigation equipment ownership and regular use by district', ent='District', a='Farms owning irrigation equipment', b='Farms irrigating weekly',
         say='in the %(n)s district, %(a)d%% of farms own irrigation equipment %(lead)s %(b)d%% irrigate weekly.',
         names=['Alder', 'Birchwood', 'Cedar Plains', 'Dover', 'Elmstead', 'Foxglen']),
]


GEN = dict(
    words_in_context=authored('words_in_context'), text_structure_purpose=authored('text_structure_purpose'), cross_text=cross_text,
    central_ideas=authored('central_ideas'), coe_textual=authored('coe_textual'), coe_quant=coe_quant, inferences=authored('inferences'),
    boundaries=boundaries, form_structure_sense=form_structure, rhetorical_synthesis=authored('rhetorical_synthesis'), transitions=transitions,
)
