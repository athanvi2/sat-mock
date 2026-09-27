"""Authored Reading & Writing items (original text, not College Board material).
Every record: d (0 easy / 1 medium / 2 hard), passage, q (question stem), one correct (text, why), exactly 3 wrong (text, why).
Records are tagged by skill key from bank/skills.py. Add more records with the helpers below - the app picks them up automatically."""

RECS = {}
Q_WIC = 'Which choice completes the text with the most logical and precise word or phrase?'
Q_MAIN = 'Which choice best states the main idea of the text?'
Q_PURPOSE = 'Which choice best states the main purpose of the text?'
Q_FUNC = 'Which choice best states the function of the underlined sentence in the text as a whole?'
Q_STRUCT = 'Which choice best describes the overall structure of the text?'
Q_SUP = 'Which finding, if true, would most strongly support the hypothesis?'
Q_WEAK = 'Which finding, if true, would most weaken the claim?'
Q_INF = 'Which choice most logically completes the text?'


def rec(skill, d, passage, q, ans, *wrongs):
    assert len(wrongs) == 3, (skill, passage[:40])
    RECS.setdefault(skill, []).append(dict(d=d, passage=passage, q=q, ans=ans, wrongs=list(wrongs)))


def wic(d, sent, ans, clue, *wr):
    """sent contains ______ ; ans and wr are (word, meaning). The clue explains the logic."""
    a = (ans[0], "&ldquo;%s&rdquo; means %s. %s" % (ans[0], ans[1], clue))
    ws = [(w, "&ldquo;%s&rdquo; means %s, which does not fit the logic of the sentence." % (w, m)) for w, m in wr]
    rec('words_in_context', d, sent, Q_WIC, a, *ws)


def sense(d, passage, word, ans, why, *wr):
    """'As used in the text' items. ans / wr are (meaning_word, note)."""
    q = 'As used in the text, what does the word &ldquo;%s&rdquo; most nearly mean?' % word
    rec('words_in_context', d, passage, q, (ans[0], why), *[(w, n) for w, n in wr])


# =============================================================== WORDS IN CONTEXT
# ---- easy
wic(0, "Because the recipe was so ______, even beginners could follow it without any help.", ('straightforward', 'simple and easy to understand'),
    "The clue &ldquo;even beginners could follow it&rdquo; tells us the recipe was easy to understand.",
    ('elaborate', 'having many complicated details'), ('ambiguous', 'open to more than one meaning'), ('extravagant', 'excessively lavish'))
wic(0, "Rather than feeling ______ about moving to a new city, Lena felt excited and could hardly wait to explore it.", ('apprehensive', 'anxious about something that may happen'),
    "&ldquo;Rather than&rdquo; signals contrast with &ldquo;excited,&rdquo; so the blank must be a worried feeling.",
    ('enthusiastic', 'full of eager interest'), ('curious', 'eager to learn'), ('generous', 'willing to give freely'))
wic(0, "The scientist&rsquo;s explanation was so ______ that even young children understood it.", ('lucid', 'clearly expressed and easy to grasp'),
    "The result clause &ldquo;even young children understood it&rdquo; requires a word meaning clear.",
    ('convoluted', 'extremely complex and twisting'), ('tentative', 'uncertain or hesitant'), ('lengthy', 'taking a long time'))
wic(0, "Frogs are ______ to changes in water quality; even a small amount of pollution can make them sick.", ('sensitive', 'easily affected by something'),
    "If a small amount of pollution makes frogs sick, they are easily affected.",
    ('immune', 'protected from something'), ('resistant', 'able to withstand something'), ('indifferent', 'having no interest in something'))
wic(0, "Instead of following the trend, the designer chose a(n) ______ style that no one had seen before.", ('original', 'new and not copied from anything'),
    "&ldquo;Instead of following the trend&rdquo; and &ldquo;no one had seen before&rdquo; point to something new.",
    ('conventional', 'following accepted practice'), ('traditional', 'long established'), ('familiar', 'well known'))
wic(0, "The teacher&rsquo;s ______ comments made the nervous student feel more confident about the presentation.", ('encouraging', 'giving someone hope or confidence'),
    "The comments made the student &ldquo;more confident,&rdquo; so they must have been supportive.",
    ('sarcastic', 'meant to mock'), ('vague', 'unclear'), ('reluctant', 'unwilling'))
wic(0, "Desert plants ______ long dry periods by storing water in their thick leaves.", ('endure', 'survive through a difficult condition'),
    "Storing water lets the plants get through dry periods.",
    ('resent', 'feel bitter about'), ('prevent', 'stop from happening'), ('imitate', 'copy'))
wic(0, "Because the evidence was so ______, the jury needed only an hour to reach a verdict.", ('conclusive', 'settling a question beyond doubt'),
    "A very quick verdict suggests the evidence left no doubt.",
    ('inconclusive', 'not settling a question'), ('ambiguous', 'open to more than one meaning'), ('outdated', 'no longer current'))
wic(0, "The mayor&rsquo;s speech was ______: it lasted only two minutes and made a single point.", ('concise', 'brief but complete'),
    "The colon introduces an explanation: short and to the point.",
    ('rambling', 'long and unfocused'), ('elaborate', 'detailed and complicated'), ('heated', 'angry or intense'))
wic(0, "Some birds ______ each winter, flying thousands of miles to warmer regions.", ('migrate', 'travel seasonally from one region to another'),
    "Flying thousands of miles to warmer regions is what migration means.",
    ('hibernate', 'spend the winter in a sleeplike state'), ('communicate', 'exchange information'), ('accumulate', 'gather over time'))
wic(0, "Although the two brothers look alike, their personalities are quite ______.", ('distinct', 'clearly different'),
    "&ldquo;Although&rdquo; sets up a contrast with looking alike.",
    ('similar', 'alike in many ways'), ('identical', 'exactly the same'), ('familiar', 'well known'))
wic(0, "The library&rsquo;s ______ collection includes maps, letters, and photographs from many centuries.", ('diverse', 'made up of many different kinds'),
    "Maps, letters, photographs, and many centuries all point to variety.",
    ('uniform', 'all the same'), ('limited', 'small in amount'), ('modern', 'of recent times'))
# ---- medium
wic(1, "The novelist&rsquo;s ______ prose, which conveys much in few words, has often been compared to poetry.", ('spare', 'using no more than is necessary'),
    "&ldquo;Conveys much in few words&rdquo; defines the blank.",
    ('ornate', 'heavily decorated'), ('verbose', 'using more words than needed'), ('digressive', 'wandering away from the point'))
wic(1, "Critics praised the film&rsquo;s ______ attention to historical detail; every costume and prop had been carefully researched.", ('meticulous', 'showing great care about small details'),
    "The colon explains: every costume and prop was researched.",
    ('cursory', 'hasty and superficial'), ('sporadic', 'occurring at irregular intervals'), ('detached', 'emotionally uninvolved'))
wic(1, "Many residents ______ the council&rsquo;s decision to delay the vote, since they wanted the issue settled immediately.", ('criticized', 'expressed disapproval of'),
    "Wanting the issue settled immediately explains why residents would disapprove of a delay.",
    ('endorsed', 'publicly supported'), ('anticipated', 'expected in advance'), ('overlooked', 'failed to notice'))
wic(1, "Researchers cautioned that the study&rsquo;s results, while intriguing, are only ______ and should not be treated as definitive.", ('preliminary', 'early and subject to further testing'),
    "&ldquo;Should not be treated as definitive&rdquo; requires a word meaning not final.",
    ('conclusive', 'settling a question'), ('exhaustive', 'thorough and complete'), ('irrelevant', 'not connected to the matter'))
wic(1, "Though the two theories seem ______, both can be true: one describes small-scale behavior and the other describes large-scale behavior.", ('contradictory', 'opposing each other so that both cannot be true'),
    "&ldquo;Both can be true&rdquo; after &ldquo;though&rdquo; means they only seem to conflict.",
    ('redundant', 'unnecessarily repeated'), ('obsolete', 'no longer in use'), ('identical', 'exactly the same'))
wic(1, "The tortoise&rsquo;s ______ pace should not be mistaken for laziness; it is a way of conserving energy in a harsh climate.", ('measured', 'slow, steady, and careful'),
    "The slow pace is described as an energy-saving strategy, not laziness.",
    ('frantic', 'wildly hurried'), ('erratic', 'irregular and unpredictable'), ('swift', 'fast'))
wic(1, "The band&rsquo;s early albums were ______ at first, but their later work earned widespread praise.", ('overlooked', 'not noticed or given attention'),
    "&ldquo;But&rdquo; contrasts with the later praise, so the early albums received little notice.",
    ('celebrated', 'widely praised'), ('imitated', 'copied by others'), ('revised', 'changed after review'))
wic(1, "Because the town&rsquo;s economy relied almost entirely on a single factory, its closure had a ______ effect on residents&rsquo; livelihoods.", ('profound', 'deep and far-reaching'),
    "Total reliance on one factory means its closure would deeply affect people.",
    ('negligible', 'so small as to be unimportant'), ('fleeting', 'lasting a very short time'), ('arbitrary', 'based on random choice'))
wic(1, "Historians consider the diary a(n) ______ source because its author personally witnessed the events described.", ('authoritative', 'trustworthy because of expert or direct knowledge'),
    "Direct witnessing gives the diary weight as a source.",
    ('dubious', 'doubtful'), ('speculative', 'based on guesswork'), ('peripheral', 'of minor importance'))
wic(1, "The chemist&rsquo;s ______ approach, testing one variable at a time, ensured that any change could be traced to a single cause.", ('systematic', 'done according to an organized plan'),
    "Testing one variable at a time is an orderly method.",
    ('haphazard', 'lacking order'), ('impulsive', 'acting without thinking'), ('theoretical', 'based on ideas rather than experiment'))
wic(1, "The senator&rsquo;s ______ remarks avoided taking a clear position on the bill.", ('noncommittal', 'not revealing what one thinks or will do'),
    "Avoiding a clear position is the definition of noncommittal.",
    ('emphatic', 'forceful and clear'), ('candid', 'frank and open'), ('inflammatory', 'arousing anger'))
wic(1, "The restored mural is so ______ that visitors often assume it was painted only recently.", ('pristine', 'in its original, unspoiled condition'),
    "Looking recently painted implies it looks unspoiled.",
    ('faded', 'having lost brightness'), ('primitive', 'belonging to an early stage of development'), ('ambiguous', 'open to more than one meaning'))
# ---- hard
wic(2, "The economist&rsquo;s argument is ______: it appears sound on the surface but falls apart once its unstated assumptions are examined.", ('specious', 'superficially plausible but actually wrong'),
    "Seeming sound but collapsing under examination is what specious means.",
    ('cogent', 'clear, logical, and convincing'), ('incisive', 'sharply analytical'), ('candid', 'frank'))
wic(2, "Far from being ______ about the merger, the board debated it for months before voting.", ('cavalier', 'showing a lack of proper concern'),
    "&ldquo;Far from&rdquo; rejects the idea that the board was careless; months of debate show the opposite.",
    ('deliberate', 'careful and unhurried'), ('circumspect', 'cautious and watchful'), ('scrupulous', 'diligent about doing what is right'))
wic(2, "The philosopher&rsquo;s writing is often called ______ because its meaning is deliberately concealed beneath layers of metaphor.", ('opaque', 'difficult to understand'),
    "Meaning hidden under metaphor makes the writing hard to see through.",
    ('transparent', 'easily seen through or understood'), ('didactic', 'intended to teach'), ('prosaic', 'plain and ordinary'))
wic(2, "Though critics dismissed her early experiments as ______, later scholars recognized in them the seeds of a major artistic movement.", ('frivolous', 'lacking seriousness'),
    "&ldquo;Dismissed&rdquo; and the contrast with &ldquo;later scholars&rdquo; require a negative label.",
    ('seminal', 'strongly influencing later developments'), ('meticulous', 'extremely careful'), ('orthodox', 'conforming to accepted ideas'))
wic(2, "The botanist&rsquo;s findings, though modest in scope, ______ the long-held assumption that the species reproduces only in spring.", ('undermined', 'weakened the basis of'),
    "Findings that matter to an &ldquo;assumption&rdquo; and are introduced by &ldquo;though modest&rdquo; must challenge it.",
    ('corroborated', 'confirmed with evidence'), ('epitomized', 'served as a perfect example of'), ('anticipated', 'expected or acted in advance of'))
wic(2, "The company&rsquo;s ______ growth, doubling in size each year for a decade, surprised even its founders.", ('meteoric', 'rapid and spectacular'),
    "Doubling every year for a decade is very fast and dramatic.",
    ('gradual', 'happening slowly'), ('erratic', 'irregular and unpredictable'), ('nominal', 'existing in name only'))
wic(2, "The mayor sought to ______ tensions between the two neighborhoods by inviting leaders of both to a joint meeting.", ('defuse', 'reduce the danger or tension of'),
    "A joint meeting is a peacemaking step.",
    ('exacerbate', 'make worse'), ('chronicle', 'record in order'), ('rationalize', 'attempt to justify'))
wic(2, "The archaeologist urged caution, noting that the inscription&rsquo;s meaning remains ______ despite decades of study.", ('elusive', 'difficult to grasp or pin down'),
    "&ldquo;Despite decades of study&rdquo; suggests the meaning is still hard to pin down.",
    ('manifest', 'plain to see'), ('redundant', 'unnecessary'), ('dominant', 'most powerful or common'))
wic(2, "The critic&rsquo;s praise was ______: she admired the novel&rsquo;s ambition but pointed out that its characters were thinly drawn and its plot implausible.", ('qualified', 'limited by reservations'),
    "Praise paired with criticism is limited praise.",
    ('unequivocal', 'leaving no doubt'), ('gratuitous', 'uncalled for'), ('perfunctory', 'done routinely with little interest'))
wic(2, "The diplomat&rsquo;s ______ tone, neither warm nor hostile, left observers unable to gauge his true feelings.", ('impassive', 'showing no emotion'),
    "&ldquo;Neither warm nor hostile&rdquo; and &ldquo;unable to gauge&rdquo; describe a tone that shows no feeling.",
    ('effusive', 'expressing feelings without restraint'), ('vindictive', 'seeking revenge'), ('exuberant', 'full of high spirits'))
wic(2, "The new policy is ______ rather than punitive: its aim is to help struggling students improve, not to penalize them.", ('remedial', 'intended to correct or improve a problem'),
    "The colon explains the aim: help students improve.",
    ('retributive', 'aimed at punishment'), ('arbitrary', 'based on random choice'), ('nominal', 'existing in name only'))
wic(2, "Because the poet&rsquo;s imagery is so ______, a single line can call up an entire landscape in the reader&rsquo;s mind.", ('evocative', 'bringing strong images or feelings to mind'),
    "Calling up a whole landscape from one line is what evocative imagery does.",
    ('pedantic', 'overly concerned with minor details'), ('redundant', 'unnecessarily repeated'), ('quotidian', 'ordinary and everyday'))
# ---- "as used in the text"
sense(0, "Although the manor&rsquo;s interior was lavishly decorated, its exterior was strikingly plain, with bare gray walls and no ornament.", 'plain',
      ('Unadorned', ''), "&ldquo;Bare gray walls and no ornament&rdquo; and the contrast with &ldquo;lavishly decorated&rdquo; show that &ldquo;plain&rdquo; means unadorned.",
      ('Obvious', 'Plain can mean obvious, but nothing here concerns how easy something is to see.'), ('Candid', 'Plain can mean frank, but it describes a building here.'), ('Level', 'Plain can mean flat land; the walls are described as bare, not flat.'))
sense(0, "Ancient bridge builders knew that a single arch could bear tremendous weight if its stones were fitted together precisely.", 'bear',
      ('Support', ''), "The arch holding up great weight is &ldquo;supporting&rdquo; it.",
      ('Tolerate', 'Bear can mean put up with, which makes no sense for a stone arch.'), ('Produce', 'Bear can mean give birth to or yield, which does not fit weight.'), ('Display', 'Bear can mean show, as in bearing a mark; the arch is not showing weight.'))
sense(0, "The mechanic used a fine wire to reach the tiny gap inside the engine.", 'fine',
      ('Thin', ''), "A wire that fits a tiny gap must be thin.",
      ('Excellent', 'Fine can mean of high quality, but the tiny gap points to size.'), ('Satisfactory', 'Fine can mean acceptable, which does not explain reaching a tiny gap.'), ('Ornate', 'Nothing suggests decoration.'))
sense(1, "In her later work, the sculptor abandoned the human figure altogether, preferring abstract shapes.", 'figure',
      ('Form', ''), "Contrasted with &ldquo;abstract shapes,&rdquo; &ldquo;human figure&rdquo; means the shape of a human body.",
      ('Amount', 'Figure can mean a number, but that does not fit &ldquo;human.&rdquo;'), ('Symbol', 'A symbol would not be abandoned in favor of abstract shapes.'), ('Celebrity', 'Figure can mean a famous person, but sculpting shapes points to bodily form.'))
sense(1, "Few readers at the time could fully grasp the novel&rsquo;s radical structure, which shifted between three narrators without warning.", 'grasp',
      ('Understand', ''), "Readers struggling with a confusing structure means they could not understand it.",
      ('Seize', 'Grasp can mean take hold of physically, but a structure is an idea here.'), ('Reach', 'Grasp can mean the ability to reach, but it does not fit readers and structure.'), ('Endure', 'Nothing suggests readers had to put up with the structure.'))
sense(1, "Though brilliant, the physicist was reserved in public, rarely speaking unless directly asked.", 'reserved',
      ('Restrained', ''), "&ldquo;Rarely speaking unless directly asked&rdquo; shows a quiet, restrained manner.",
      ('Booked', 'Reserved can mean set aside in advance, but it is used here to describe a personality.'), ('Stored', 'Reserved can mean kept for later; it does not describe a person&rsquo;s manner.'), ('Hostile', 'Being quiet is not the same as being unfriendly.'))
sense(1, "The exhibit&rsquo;s central attraction, a rare fossil, continues to draw crowds from across the region.", 'draw',
      ('Attract', ''), "A rare fossil bringing crowds to the museum means it attracts them.",
      ('Sketch', 'Draw can mean make a picture, which does not fit crowds.'), ('Extract', 'Draw can mean pull out, as in drawing water; crowds are not pulled out.'), ('Drag', 'Draw can mean pull along, but the fossil is not physically pulling people.'))
sense(2, "The playwright cast the villain as a sympathetic figure, prompting audiences to reconsider his motives.", 'cast',
      ('Portrayed', ''), "The sentence says how the playwright presented the villain to make audiences reconsider.",
      ('Hurled', 'Cast can mean throw, which makes no sense for a character.'), ('Discarded', 'Cast can mean throw away; the villain is being reinterpreted, not rejected.'), ('Calculated', 'Cast can mean add up, as in casting a sum, which does not fit.'))
sense(2, "Engineers determined that the old bridge was structurally sound and needed only minor repairs.", 'sound',
      ('Solid', ''), "&ldquo;Structurally sound&rdquo; that needs only minor repairs means solid and dependable.",
      ('Audible', 'Sound can refer to noise, which is unrelated to a bridge&rsquo;s condition.'), ('Sensible', 'Sound can mean showing good judgment, which describes reasoning rather than a structure.'), ('Healthy', 'Sound can mean free from illness; a bridge is not ill.'))
sense(2, "Her novel approach to teaching fractions, using music instead of diagrams, raised test scores across the district.", 'novel',
      ('Original', ''), "Using music instead of diagrams is a new way to teach.",
      ('Fictional', 'A novel is a book, but here the word describes an approach.'), ('Lengthy', 'Nothing in the sentence concerns length.'), ('Complicated', 'Nothing suggests the approach was hard to understand.'))
sense(2, "The agency plans to issue new guidelines next month.", 'issue',
      ('Release', ''), "An agency planning new guidelines &ldquo;issues&rdquo; them by releasing them.",
      ('Argue', 'Issue can mean a topic of debate, but this sentence is about publishing guidelines.'), ('Result', 'Issue can mean outcome; guidelines are not results here.'), ('Complain', 'Nothing in the sentence suggests complaint.'))

# =============================================================== CENTRAL IDEAS AND DETAILS
rec('central_ideas', 0,
    "Ceramicist Ana Ortiz makes her bowls from clay she digs from the riverbank behind her studio. She fires them in a kiln she built from bricks salvaged from a demolished school. Ortiz says that using materials found near her home helps her feel connected to the place where she lives.",
    Q_MAIN, ("Ortiz creates pottery using materials she finds close to home.", "The whole passage is about materials she gathers locally: riverbank clay and salvaged bricks."),
    ("Ortiz&rsquo;s bowls are worth more than bowls made with store-bought clay.", "The passage never compares the value of her bowls with other bowls."),
    ("Ortiz taught herself to build kilns after her school closed.", "A school was demolished, but the passage does not say Ortiz learned to build kilns because of it."),
    ("Ortiz dislikes using modern equipment in her studio.", "The passage does not mention her feelings about modern equipment."))
rec('central_ideas', 0,
    "Honeybees communicate the location of food by dancing. A bee that has found nectar returns to the hive and moves in a figure-eight pattern. The angle of the dance&rsquo;s central line shows the direction of the flowers relative to the sun, and the length of the dance shows how far away they are.",
    Q_MAIN, ("Honeybees use a dance to tell hive mates where food can be found.", "Every sentence explains how the dance passes along the location of nectar."),
    ("The figure-eight dance always lasts longer when flowers are close to the hive.", "This is a misreading; the dance length shows distance and the passage does not say closer flowers lead to longer dances."),
    ("Honeybees prefer nectar from flowers that face the sun.", "The sun is used as a direction marker; the passage says nothing about flower preferences."),
    ("Honeybees are the only insects that communicate through movement.", "The passage never compares honeybees with other insects."))
rec('central_ideas', 0,
    "Last spring, the Maple Grove library began lending tools such as drills, ladders, and garden shovels along with books. Librarians report that the tool collection is checked out more often than any other non-book collection, and residents say that borrowing saves them money on items they use only once or twice a year.",
    Q_MAIN, ("Maple Grove&rsquo;s library expanded what it lends, and residents have found its tool collection useful.", "The passage describes the new tool lending and how well it has worked."),
    ("Books have become unpopular among Maple Grove residents.", "Nothing suggests books are less popular."),
    ("The library&rsquo;s tools are of higher quality than tools sold in stores.", "Quality is never discussed."),
    ("Librarians disagree about whether lending tools is appropriate.", "The passage reports no disagreement."))
rec('central_ideas', 0,
    "Many people think of cacti as plants that live only in deserts. In fact, cacti also grow in rainforests, on mountains, and even in snowy regions of South America. What these habitats share is that water is hard for the plants to absorb, so cacti have adapted by storing it in thick stems.",
    Q_MAIN, ("Cacti live in several kinds of places where water is hard to obtain, and they cope by storing water.", "This covers both the range of habitats and the shared adaptation."),
    ("Cacti grow only in deserts.", "The passage directly says the opposite."),
    ("Snowy regions are the best habitat for cacti.", "No habitat is ranked."),
    ("Cacti have thick stems because they grow on mountains.", "The passage links thick stems to storing water in every habitat, not to mountains specifically."))
rec('central_ideas', 1,
    "Sea otters eat sea urchins, which in turn graze on kelp. Where otters were hunted nearly to extinction, urchin populations exploded and stripped coastal kelp forests bare. When otters were reintroduced, the forests recovered, restoring habitat for many fish species. Ecologists cite the case as evidence that a single predator can shape an entire ecosystem.",
    Q_MAIN, ("The presence of sea otters helps sustain kelp forests and the species that depend on them.", "It captures the chain from otters to urchins to kelp to fish."),
    ("Sea urchins are the most damaging species in coastal ecosystems.", "Too broad; the passage discusses one case, not all coastal ecosystems."),
    ("Sea otters were once hunted along the coast.", "True but only a detail, not the main idea."),
    ("Kelp forests recover faster than other ecosystems do.", "No comparison to other ecosystems is made."))
rec('central_ideas', 1,
    "In her essays, the writer Lena Marsh rejects the idea that a good sentence must be long to be beautiful. She argues that brevity forces a writer to choose each word deliberately, and she points to her own revisions, which typically cut a first draft by a third. Yet Marsh does not claim that short writing is always superior: she warns that compression can turn into obscurity when a writer strips out context that readers need.",
    Q_MAIN, ("Marsh values concise writing but recognizes that excessive compression can undermine clarity.", "It includes both her praise for brevity and her warning."),
    ("Marsh believes long sentences are always less beautiful than short ones.", "The last sentence explicitly denies that short writing is always superior."),
    ("Marsh&rsquo;s revisions have made her essays difficult for readers to understand.", "The passage warns about this risk but does not say it happened."),
    ("Marsh recommends cutting every first draft by a third.", "Cutting a third is what her drafts typically lose, not a rule she gives."))
rec('central_ideas', 1,
    "Cities are often several degrees warmer than the surrounding countryside, a phenomenon known as the urban heat island effect. Dark pavement and rooftops absorb sunlight, and a lack of vegetation reduces the cooling that plants provide. Some cities have responded by painting roofs white and planting street trees, and early measurements suggest these steps can lower local temperatures.",
    Q_MAIN, ("Cities tend to be hotter than nearby rural areas, and some are trying strategies to reduce the heat.", "It states the phenomenon and the response."),
    ("White roofs are the only effective way to cool a city.", "Too strong; trees are also mentioned and the results are described as early."),
    ("Street trees absorb more sunlight than pavement does.", "The passage does not compare trees with pavement in this way."),
    ("The countryside around cities has become warmer than the cities themselves.", "This reverses the phenomenon described."))
rec('central_ideas', 1,
    "When the city converted a vacant lot into a community garden, organizers expected mainly to grow vegetables. Instead, they found that neighbors who had never spoken began trading recipes and sharing tools, and the number of neighborhood events tripled over two years. The garden&rsquo;s greatest yield, one organizer said, turned out to be social.",
    Q_MAIN, ("A community garden produced benefits beyond food by bringing neighbors together.", "The passage centers on the unexpected social benefits."),
    ("Vacant lots in the city are quickly being turned into gardens.", "Only one lot is mentioned."),
    ("The garden failed to grow enough vegetables to be worthwhile.", "Vegetable output is never described as a failure."),
    ("Neighborhood events tripled because organizers advertised them heavily.", "The passage gives no cause like advertising."))
rec('central_ideas', 2,
    "For decades, historians portrayed medieval guilds as engines of economic stagnation that protected members&rsquo; privileges at the expense of innovation. Recent archival work complicates that picture: records from several trading cities show guilds funding apprenticeships, standardizing product quality, and sometimes sharing new techniques among members. While guilds did restrict competition, the historian Priya Nair argues, dismissing them as purely obstructive overlooks the ways they supported skilled trades.",
    Q_MAIN, ("Newer research suggests that guilds, though restrictive, also contributed positively to skilled trades, challenging the older view of them as purely obstructive.", "It captures both the old view and the revision."),
    ("Historians have now proved that guilds never limited competition.", "The passage says guilds did restrict competition."),
    ("The records from trading cities are too incomplete to draw conclusions about guilds.", "The records are used as evidence, not dismissed."),
    ("Guilds were more innovative than modern companies.", "No comparison to modern companies is made."))
rec('central_ideas', 2,
    "Because languages evolve continuously, the boundary between a &ldquo;dialect&rdquo; and a &ldquo;language&rdquo; is less a linguistic fact than a social one. Speakers of Swedish and Norwegian can largely understand each other, yet the two are counted as separate languages, whereas varieties grouped together as &ldquo;Chinese&rdquo; are often mutually unintelligible. The distinction, the passage suggests, tracks political and cultural identity more reliably than it tracks mutual comprehension.",
    Q_MAIN, ("What counts as a distinct language is often determined by social and political factors rather than by linguistic differences alone.", "This is the claim the whole passage builds toward."),
    ("Swedish and Norwegian are in fact dialects of a single language.", "The passage says they are counted as separate languages."),
    ("Varieties of Chinese cannot be understood by any speakers of other varieties.", "Too extreme; the passage says &ldquo;often,&rdquo; not always."),
    ("Linguists should stop studying dialects.", "No recommendation of this kind appears."))
rec('central_ideas', 2,
    "A common assumption holds that consumers always choose the cheapest option. But in one study, shoppers offered two nearly identical brands of olive oil often chose the pricier brand when it appeared beside a much more expensive third bottle, which made the middle option seem a bargain. The researchers concluded that people judge price relative to what surrounds it rather than in absolute terms.",
    Q_MAIN, ("Shoppers&rsquo; choices can be swayed by how prices are presented, contrary to the assumption that people simply pick the lowest price.", "It restates the assumption and the study&rsquo;s challenge to it."),
    ("Olive oil is the product most affected by pricing tricks.", "Only one product is studied; no ranking of products is given."),
    ("Consumers dislike shopping for expensive items.", "Not mentioned."),
    ("The most expensive bottle was the one shoppers bought most often.", "Shoppers often chose the middle-priced bottle."))
rec('central_ideas', 2,
    "Composers of the Baroque era frequently reused their own melodies across different works. Bach, for instance, adapted movements of secular cantatas for sacred masses. Modern listeners may regard this as a lack of originality, but scholars point out that the era&rsquo;s aesthetic valued craftsmanship and the transformation of existing material over novelty for its own sake.",
    Q_MAIN, ("Baroque composers&rsquo; habit of reusing melodies reflects the values of their era rather than a shortage of creativity.", "It captures the scholars&rsquo; reinterpretation of the practice."),
    ("Bach was less original than other Baroque composers.", "No comparison among composers is made."),
    ("Secular cantatas were more highly valued than sacred masses.", "The passage does not rank the genres."),
    ("Novelty was the primary goal of Baroque composers.", "The passage says the era valued craftsmanship over novelty."))

# =============================================================== TEXT STRUCTURE AND PURPOSE
rec('text_structure_purpose', 0,
    "The city of Reykjavik heats most of its buildings with water from underground hot springs. Iceland sits on a volcanic ridge, so heat rises close to the surface. Pipes carry the hot water into homes, where it warms radiators and sinks. As a result, residents of the capital rarely burn fuel to stay warm.",
    Q_PURPOSE, ("To explain how a city uses a natural resource to heat its buildings.", "The passage traces the process from hot springs to radiators."),
    ("To compare heating methods used in several countries.", "Only one city is discussed."),
    ("To criticize the cost of heating homes in Iceland.", "Cost is never mentioned."),
    ("To describe a recent volcanic eruption in Iceland.", "No eruption is described."))
rec('text_structure_purpose', 0,
    "Marine biologist Keiko Mori spent three summers tracking sea turtles off the coast of Japan. <u>Her findings surprised her colleagues.</u> The turtles, she discovered, traveled almost twice as far each day as scientists had estimated.",
    Q_FUNC, ("It introduces the discovery that the following sentence explains.", "The underlined sentence announces a surprise, and the next sentence gives the details."),
    ("It offers a counterargument to Mori&rsquo;s discovery.", "It does not oppose the discovery; it announces it."),
    ("It describes the method Mori used to track turtles.", "Methods are not described in the underlined sentence."),
    ("It provides background about Japan&rsquo;s coastline.", "The coastline is never discussed."))
rec('text_structure_purpose', 0,
    "For years, my neighbor&rsquo;s garden was the envy of the street. Then last spring a late frost killed nearly every plant. Rather than replanting, she surprised us all by scattering wildflower seeds across the plot, and by July the garden was busier with bees and butterflies than it had ever been.",
    Q_STRUCT, ("It describes a setback and then a surprising response to it.", "The frost is the setback; the wildflowers are the response."),
    ("It presents a problem and blames the person who caused it.", "No one is blamed."),
    ("It compares two different gardening methods.", "The passage follows one garden over time."),
    ("It gives instructions for planting wildflowers.", "It tells a story rather than giving steps."))
rec('text_structure_purpose', 0,
    "Bamboo grows quickly. <u>Some species can grow nearly a meter in a single day.</u> Because it regrows so fast, builders and farmers rely on it as a renewable material.",
    Q_FUNC, ("It gives a striking detail about the growth rate mentioned in the previous sentence.", "&ldquo;Grows quickly&rdquo; is made concrete with the meter-a-day example."),
    ("It introduces an argument against using bamboo.", "The passage supports bamboo&rsquo;s usefulness."),
    ("It explains why bamboo is grown in gardens.", "Gardens are not mentioned."),
    ("It describes a disadvantage of bamboo.", "Fast growth is presented as a benefit."))
rec('text_structure_purpose', 1,
    "Many commentators have praised the electric scooter as a solution to urban congestion. <u>Certainly, scooters do take some short car trips off the road.</u> But a survey of riders in three cities found that most were using scooters instead of walking, not instead of driving, which suggests the congestion benefit is smaller than advertised.",
    Q_FUNC, ("It concedes a point in favor of the view that the passage goes on to qualify.", "&ldquo;Certainly&rdquo; grants a point, and &ldquo;But&rdquo; then limits it."),
    ("It provides the survey evidence for the passage&rsquo;s central claim.", "The survey comes in the next sentence."),
    ("It introduces a problem unrelated to scooters.", "It is about scooters."),
    ("It restates the commentators&rsquo; claim in different words.", "It makes a narrower point, not a restatement."))
rec('text_structure_purpose', 1,
    "Astronomers long assumed that planets form only around single stars. In 2011, however, a team detected a planet orbiting two stars, a discovery that forced researchers to revise their models of planetary formation. Since then, dozens of similar planets have been found.",
    Q_PURPOSE, ("To describe how a discovery challenged a long-standing assumption in astronomy.", "The passage moves from the assumption to the discovery to the revision."),
    ("To argue that single stars cannot have planets.", "The passage says planets were assumed only around single stars, not that they can&rsquo;t exist there."),
    ("To explain how astronomers detect distant planets.", "Detection methods are not discussed."),
    ("To criticize the 2011 team&rsquo;s methods.", "The team is credited, not criticized."))
rec('text_structure_purpose', 1,
    "Some animals use tools without being taught. <u>Crows in New Caledonia, for instance, fashion hooks from twigs to extract insects from crevices.</u> Such behavior challenges the notion that toolmaking requires human-style instruction.",
    Q_FUNC, ("It gives a specific example of the phenomenon described in the previous sentence.", "&ldquo;For instance&rdquo; introduces an example of animals using tools."),
    ("It contradicts the claim made in the previous sentence.", "It supports it."),
    ("It raises a question that later sentences cannot answer.", "No question is raised."),
    ("It summarizes the passage&rsquo;s conclusion.", "The conclusion is the final sentence."))
rec('text_structure_purpose', 1,
    "Critics of remote work argue that employees collaborate less effectively at a distance. Yet a 2020 analysis of a software firm&rsquo;s code repositories found that the number of joint contributions did not fall after the firm went remote. The finding does not prove that remote work is always as collaborative as office work, but it does undercut the criticism in its blanket form.",
    Q_PURPOSE, ("To present evidence that complicates a common criticism without claiming to settle the matter.", "The evidence &ldquo;undercuts&rdquo; the criticism but the passage admits it doesn&rsquo;t prove the opposite."),
    ("To prove that remote work is superior to office work.", "The passage explicitly says the finding does not prove this."),
    ("To explain how code repositories track employee activity.", "The repositories are only the evidence source."),
    ("To defend a software firm&rsquo;s decision to go remote.", "The firm&rsquo;s decision is not defended."))
rec('text_structure_purpose', 2,
    "In 1854, physician John Snow mapped cholera deaths in a London neighborhood and noticed that they clustered around a single water pump. <u>The prevailing theory of the day held that cholera spread through foul air, and Snow&rsquo;s map did not fit it.</u> He persuaded officials to remove the pump handle, after which the outbreak subsided.",
    Q_FUNC, ("It explains why Snow&rsquo;s finding was significant by contrasting it with the accepted explanation.", "The sentence sets Snow&rsquo;s map against the prevailing theory."),
    ("It casts doubt on the accuracy of Snow&rsquo;s map.", "The map is presented as evidence against the theory, not as unreliable."),
    ("It describes a consequence of removing the pump handle.", "The pump handle appears in the next sentence."),
    ("It offers a definition of cholera.", "Nothing defines the disease."))
rec('text_structure_purpose', 2,
    "Literary critics sometimes treat a translator&rsquo;s choices as mere technical decisions. But consider English versions of a single line from an ancient epic: one renders a warrior&rsquo;s shout as &ldquo;a roar,&rdquo; another as &ldquo;a cry,&rdquo; a third as &ldquo;a howl.&rdquo; Each portrays the hero differently, as majestic, as anguished, as bestial. Translation, then, is interpretation, and readers who ignore this may mistake one translator&rsquo;s reading for the original.",
    Q_PURPOSE, ("To argue that translation involves interpretive choices that shape how readers understand a text, using varied renderings of one line as evidence.", "It matches the claim (&ldquo;translation is interpretation&rdquo;) and the example used to prove it."),
    ("To criticize translators for producing inaccurate versions of ancient epics.", "The passage does not call the translations inaccurate."),
    ("To rank several English translations by literary quality.", "No ranking is given."),
    ("To describe the historical origins of an ancient epic.", "Origins are never discussed."))
rec('text_structure_purpose', 2,
    "When engineers designed the first suspension bridges, they worried chiefly about the downward pull of traffic. <u>Wind, by contrast, seemed a minor concern.</u> That assumption proved costly in 1940, when a bridge in Washington State twisted itself apart in a gale of only moderate strength.",
    Q_FUNC, ("It states a belief that the passage goes on to show was mistaken.", "&ldquo;That assumption proved costly&rdquo; refers back to the underlined belief."),
    ("It offers evidence that wind does not affect bridges.", "The passage shows the opposite."),
    ("It introduces a solution to an engineering problem.", "No solution is offered."),
    ("It compares two bridges built in different eras.", "Only one bridge collapse is mentioned."))
rec('text_structure_purpose', 2,
    "Consider the humble sticky note. Its adhesive was developed by a chemist attempting to make a strong glue and proved too weak to bond paper permanently, a failure by the original standard. Years passed before a colleague realized that a weak, reusable adhesive was precisely what was needed for marking pages. The episode illustrates how an apparent failure can become a success once it is matched to a different purpose.",
    Q_STRUCT, ("It introduces an everyday object, recounts how it originated, and draws a general lesson from that origin.", "The final sentence generalizes from the story."),
    ("It states a theory about adhesives and then refutes it.", "No theory is stated and refuted."),
    ("It compares two inventors and evaluates their achievements.", "The colleague and chemist are not compared or evaluated."),
    ("It lists several failed products and explains why each failed.", "Only one product is discussed."))
