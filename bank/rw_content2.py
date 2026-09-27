"""Authored Reading & Writing items, part 2 (original text). Same record format as rw_content.py."""
from bank.rw_content import rec, Q_SUP, Q_WEAK, Q_INF

Q_QUOTE = 'Which quotation from the work most effectively illustrates the claim?'

# =============================================================== COMMAND OF EVIDENCE: TEXTUAL
rec('coe_textual', 0,
    "Botanist Mei Chen hypothesized that sunflowers turn to face the morning sun because warmer flower heads attract more pollinators. To test this, she compared pollinator visits to sunflowers whose heads were kept warm with visits to sunflowers whose heads were kept shaded.",
    Q_SUP, ("Warmed flower heads received more pollinator visits than shaded ones.", "It directly links warmth to more pollinator visits, which is Chen&rsquo;s hypothesis."),
    ("Shaded flower heads grew taller and produced more seeds than warmed flower heads did.", "Height and seed count say nothing about pollinator visits."),
    ("Sunflowers face east more often than they face west.", "This describes the behavior but not the reason for it."),
    ("Pollinators visited other species more often than sunflowers.", "It compares species, not warm and shaded heads."))
rec('coe_textual', 0,
    "Ecologist Sam Whitaker suspects that the recent decline of trout in a river is caused by warming water. He plans to compare trout counts in the warm main channel with counts in cool tributaries that feed it.",
    Q_WEAK, ("Trout counts were as low in the cool tributaries as in the warm main channel.", "If cool water shows the same decline, warmth is unlikely to be the cause."),
    ("Water temperature in the main channel of the river has risen steadily over the past twenty years.", "This is consistent with Whitaker&rsquo;s suspicion."),
    ("Trout prefer cooler water in laboratory tests.", "This supports the idea that warmth harms trout."),
    ("Trout counts fell most in the warmest stretch of the river.", "This supports the claim."))
rec('coe_textual', 0,
    "Astronomer Dana Ruiz claims that most craters on the moon were formed by impacts from space rather than by volcanoes.",
    Q_SUP, ("Many craters are surrounded by a ring of rock debris that appears to have been thrown outward from the center.", "Debris flung outward from the center fits a collision."),
    ("The moon has no atmosphere.", "This is true but does not distinguish impacts from volcanoes."),
    ("Craters on the moon vary widely in size.", "Size variation does not point to a cause."),
    ("Moon rocks are older than many rocks found on Earth.", "The age of rocks does not address how craters formed."))
rec('coe_textual', 0,
    "In the novel <i>The Lantern Year</i>, the narrator, Ila, gradually becomes more confident in making her own decisions.",
    Q_QUOTE, ("&ldquo;By spring I no longer asked anyone whether I was right; I simply chose, and walked on.&rdquo;", "It shows Ila deciding on her own without seeking approval."),
    ("&ldquo;That winter I asked everyone I met, even strangers on the road, to tell me what to do, and I obeyed each in turn.&rdquo;", "This shows Ila relying on others, the opposite of the claim."),
    ("&ldquo;The lantern swung in the wind, and I counted its shadows on the wall.&rdquo;", "It describes a scene and says nothing about decisions."),
    ("&ldquo;My sister was confident enough for both of us, and I let her lead.&rdquo;", "The confidence here belongs to Ila&rsquo;s sister, not Ila."))
rec('coe_textual', 1,
    "Historian Marta Elkins claims that the town of Riverton&rsquo;s population boom in the 1890s was driven primarily by the arrival of the railroad.",
    Q_SUP, ("Census records show that most new residents listed railroad-related jobs and arrived within two years of the line opening.", "It ties both the residents&rsquo; jobs and the timing directly to the railroad."),
    ("Newspaper advertisements for Riverton&rsquo;s farmland increased in the 1890s.", "This points to farming as a possible cause instead."),
    ("Riverton&rsquo;s population declined after 1900.", "What happened after the boom does not show what caused it."),
    ("The railroad company was one of the largest employers in the state.", "It is about the company, not about Riverton&rsquo;s growth."))
rec('coe_textual', 1,
    "A research team proposes that a species of frog evolved bright coloration to warn predators that it is toxic.",
    Q_WEAK, ("Predators in the frogs&rsquo; habitat readily ate the brightly colored frogs and showed no ill effects.", "If predators eat the frogs unharmed, the coloration does not warn of anything."),
    ("The brightest frogs contain the highest levels of toxin.", "This supports the warning explanation."),
    ("Predators avoided artificial models painted with the frogs&rsquo; colors.", "This suggests the colors deter predators."),
    ("In field observations, the brightly colored frogs were far easier for predators to spot than similar dull-colored frogs.", "Being visible is consistent with a warning signal."))
rec('coe_textual', 1,
    "The poem &ldquo;Harbor Light&rdquo; portrays its speaker as having mixed feelings about leaving home, feeling both eagerness for the journey and reluctance to go.",
    Q_QUOTE, ("&ldquo;I lean toward the far horizon, yet my hand keeps the door&rsquo;s cold latch.&rdquo;", "Leaning toward the horizon shows eagerness; holding the latch shows reluctance."),
    ("&ldquo;The gulls wheel over the harbor, white against the gray.&rdquo;", "It describes a scene without any feeling from the speaker."),
    ("&ldquo;I will not look back, and I will not miss the place.&rdquo;", "It shows only eagerness, not reluctance."),
    ("&ldquo;How I long to stay, and stay, and never see the sea again.&rdquo;", "It shows only reluctance, not eagerness."))
rec('coe_textual', 1,
    "Linguists have proposed that bilingual children develop stronger attention-shifting skills because they must constantly switch between languages.",
    Q_SUP, ("Bilingual children who switched frequently between languages at home outperformed bilingual children who rarely switched on a task requiring attention shifting.", "It isolates language switching as the factor that matters."),
    ("Bilingual children knew more words in total than monolingual children did.", "Vocabulary size is unrelated to attention shifting."),
    ("Monolingual children were slower at tasks conducted in a second language.", "It does not address bilingual children&rsquo;s attention."),
    ("Bilingual children preferred tasks that used both of their languages.", "Preference does not show a skill difference."))
rec('coe_textual', 2,
    "A geologist proposes that a series of parallel grooves in a bedrock surface were carved by a glacier moving in one direction rather than by flowing water.",
    Q_SUP, ("Boulders resting on the grooved surface are made of a rock type found only in mountains to the north, and the grooves run north to south.", "Boulders carried from the north plus grooves aligned north to south fit a glacier moving in one direction."),
    ("The grooves have smooth, rounded edges.", "Rounded edges are also consistent with water erosion."),
    ("The bedrock contains fossilized shells.", "The fossils say nothing about how the grooves formed."),
    ("Small streams flow through the region today.", "This would, if anything, favor the water explanation."))
rec('coe_textual', 2,
    "An economist argues that raising the minimum wage in Town A caused job losses in fast-food restaurants there, citing a 6 percent fall in fast-food employment in Town A in the year after the increase.",
    Q_WEAK, ("Fast-food employment fell by a similar 6 percent in neighboring towns that did not raise their minimum wage.", "If the same drop occurred without a wage increase, the increase is unlikely to be the cause."),
    ("Some Town A restaurants reduced employee hours after the increase.", "Reduced hours are consistent with the economist&rsquo;s view."),
    ("Menu prices at Town A restaurants rose after the increase.", "Price changes do not bear on whether jobs were lost because of the wage."),
    ("Fast-food employment in Town A had been stable for several years before the increase, with few restaurants opening or closing.", "Stability before the increase makes the later drop look more related to the increase."))
rec('coe_textual', 2,
    "The narrator of a short story insists that she has forgotten a painful letter, but the story implies that she has in fact suppressed the memory, since she is unable to stop thinking about it.",
    Q_QUOTE, ("&ldquo;I told myself the letter had never come, though I could have recited every line of it.&rdquo;", "It shows denial (&ldquo;never come&rdquo;) alongside vivid memory (&ldquo;recited every line&rdquo;)."),
    ("&ldquo;The letter lay on the table for a week before I opened it.&rdquo;", "It shows delay, not denial or preoccupation."),
    ("&ldquo;I told everyone the letter had come, and I read its lines aloud to them.&rdquo;", "This shows openness about the letter, the opposite of suppression."),
    ("&ldquo;She wrote back within the hour and posted the reply herself.&rdquo;", "It describes a quick reply with no sign of suppression."))
rec('coe_textual', 2,
    "Ecologists hypothesize that a certain tree species benefits from a partnership with a soil fungus.",
    Q_SUP, ("Seedlings of the tree grown in sterilized soil with the fungus added grew larger than seedlings grown in sterilized soil without it.", "Only the fungus differs between the groups, so the growth difference points to the fungus."),
    ("The fungus is often found in soil near mature trees of the species.", "A correlation in location does not show the tree benefits."),
    ("The trees grew larger in unsterilized soil than in sterilized soil.", "Unsterilized soil contains many organisms, so the fungus cannot be singled out."),
    ("The same fungus is also found near several other tree species.", "This does not show any benefit to this tree."))

# =============================================================== INFERENCES
rec('inferences', 0,
    "Nora&rsquo;s plants near the window grew tall and green, while identical plants she kept in a dark closet stayed small and pale. Nora concluded that ______",
    Q_INF, ("light helps plants grow.", "The only difference between the plants was the light they received."),
    ("plants kept in closets need more water than plants kept near windows.", "Water is not mentioned."),
    ("plants prefer small containers.", "Container size is not mentioned."),
    ("window plants received more fertilizer.", "Nothing about fertilizer appears."))
rec('inferences', 0,
    "Every time Jamal practices a piece for at least twenty minutes, he plays it with fewer mistakes at his next lesson. When he skips practice, his mistakes increase. This pattern suggests that ______",
    Q_INF, ("regular practice helps Jamal play the piece more accurately.", "Fewer mistakes with practice and more without it point to this."),
    ("Jamal makes more mistakes when the lesson is longer.", "Lesson length is not mentioned."),
    ("Jamal&rsquo;s teacher grades his playing more strictly on some days than on others.", "Grading is not mentioned."),
    ("Jamal prefers practicing for exactly twenty minutes.", "The passage gives no preference."))
rec('inferences', 0,
    "Bakers at the Hillside Cafe begin work at 4 a.m. so that bread is ready when the cafe opens. On Sundays, the cafe opens two hours later than usual. It is likely, then, that on Sundays the bakers ______",
    Q_INF, ("start work later than on other days.", "Bread must be ready at opening, and opening is later."),
    ("start work earlier than on other days.", "This reverses the logic."),
    ("do not need to bake any bread before the cafe opens.", "The cafe is open, so bread is presumably needed."),
    ("bake more bread than on other days.", "No information about quantity is given."))
rec('inferences', 0,
    "A museum found that on days when admission is free, attendance triples. On days when admission costs twelve dollars, attendance is low. The museum director infers that ______",
    Q_INF, ("the admission price affects how many people visit.", "Attendance changes when only the price changes."),
    ("visitors prefer weekend visits.", "Days of the week are not mentioned."),
    ("the museum&rsquo;s most popular exhibits change each month, which draws repeat visitors.", "Exhibits are not mentioned."),
    ("most visitors are students.", "Visitor age is not mentioned."))
rec('inferences', 1,
    "Some critics contend that a city&rsquo;s historic districts stifle housing growth because their rules make building expensive. But data from the past decade show that housing costs in cities with large historic districts rose no faster than in similar cities without them. This suggests that ______",
    Q_INF, ("historic district rules are probably not the main cause of rising housing costs.", "If cities without such rules had similar increases, the rules are unlikely to be the main cause."),
    ("cities should eliminate historic districts in order to slow the rise in housing costs.", "The data do not support a policy recommendation this strong."),
    ("housing costs are not rising in any city.", "Costs did rise; they just rose at similar rates."),
    ("historic districts are always beneficial.", "The data only address housing costs."))
rec('inferences', 1,
    "Certain deep-sea fish produce their own light, a trait that costs a great deal of energy. Biologists find it puzzling that the trait is so common, since food is scarce in the deep sea. They reason that ______",
    Q_INF, ("the trait probably provides benefits that outweigh its energy cost.", "A costly trait that is common must pay off in some way."),
    ("deep-sea fish have abundant food.", "The passage says food is scarce."),
    ("producing light requires very little energy.", "The passage says it is costly."),
    ("most deep-sea fish depend on light produced by other animals rather than making their own.", "This is not stated and does not explain why fish make their own light."))
rec('inferences', 1,
    "Researchers found that a newly described lizard species lives only on the north-facing slopes of one mountain, where temperatures are consistently cool. Nearby south-facing slopes, though otherwise similar, are warm and hold no members of the species. The researchers think it likely that ______",
    Q_INF, ("the lizards&rsquo; range is limited by the temperature of their habitat.", "Similar slopes differ mainly in warmth, and the lizards occur only where it is cool."),
    ("the lizards eat only plants that grow on north-facing slopes.", "Diet is not mentioned."),
    ("the south-facing slopes lack enough of the insects and plants that the lizards need to eat.", "The passage says they are otherwise similar."),
    ("the lizards recently migrated from another mountain.", "Origin is not discussed."))
rec('inferences', 1,
    "Although the printing press made books cheaper, historian Ravi Kapoor notes that literacy rates in a region rose substantially only after schools were built there, even in places where books had been cheap for a century. Kapoor&rsquo;s point implies that ______",
    Q_INF, ("cheap books alone were not enough to raise literacy.", "Literacy rose only once schools existed, despite cheap books."),
    ("the printing press had no effect on the price of books.", "The passage says books became cheaper."),
    ("schools were built in most regions before the printing press made books cheaper.", "The passage does not give the order."),
    ("people in the region did not want to read.", "Desire is not discussed."))
rec('inferences', 2,
    "Scientists studying a species of mold observed that it grows toward, and then stops just short of, colonies of a competing mold, leaving a narrow empty gap. The gap persists even when extra nutrients are added to it. The scientists therefore hypothesize that ______",
    Q_INF, ("one mold releases a substance that inhibits the growth of the other.", "If nutrients do not fill the gap, something other than food supply is stopping growth."),
    ("the molds are limited by a lack of nutrients in the gap.", "Adding nutrients did not change the gap."),
    ("the two molds cooperate to share space.", "A persistent gap suggests competition, not cooperation."),
    ("the competing mold grows faster than the first mold whenever extra nutrients are available.", "It does not explain the gap."))
rec('inferences', 2,
    "A philosopher argues that if a moral rule admits no exceptions, it must be simple enough to state without qualifiers. Yet most rules that people call &ldquo;absolute,&rdquo; such as &ldquo;do not lie,&rdquo; turn out on reflection to require qualifiers. If the philosopher is right, then ______",
    Q_INF, ("few, if any, commonly cited &ldquo;absolute&rdquo; moral rules actually admit no exceptions.", "Needing qualifiers means a rule is not simple, so by the philosopher&rsquo;s premise it must have exceptions."),
    ("simple moral rules are the most useful ones.", "Usefulness is not discussed."),
    ("moral rules should never be stated aloud.", "Nothing supports this."),
    ("most people break the moral rules they call absolute whenever doing so benefits them.", "The argument concerns how rules are stated, not what people do."))
rec('inferences', 2,
    "In a reading experiment, participants recalled more details from stories they read on paper than from identical stories read on screens, but only when they were given no time limit. Under strict time limits, recall was the same in both formats. This finding suggests that ______",
    Q_INF, ("paper&rsquo;s advantage may depend on readers having time to read carefully.", "The advantage disappears when time is short."),
    ("paper is better than screens in all circumstances.", "The results contradict this under time limits."),
    ("strict time limits improve how much readers recall from stories read on screens.", "Recall under time limits was the same in both formats, not improved."),
    ("participants read faster on paper.", "Reading speed is not reported."))
rec('inferences', 2,
    "The ancient city of Tell Amar was abandoned around 1200 CE. Some researchers attribute the abandonment to a prolonged drought, citing tree-ring evidence of low rainfall. But neighboring cities in the same region, which faced the same drought, continued to thrive for centuries. This suggests that ______",
    Q_INF, ("drought alone probably does not explain the abandonment of Tell Amar.", "Other cities survived the same drought, so something else must have contributed."),
    ("the tree-ring evidence is inaccurate.", "The passage gives no reason to doubt the evidence."),
    ("Tell Amar&rsquo;s neighbors were unaffected by the drought.", "The passage says they faced the same drought."),
    ("residents of Tell Amar moved to neighboring cities because those cities had more reliable water supplies.", "Where residents went, and why, is not discussed."))

# =============================================================== RHETORICAL SYNTHESIS
Q_RS = 'Which choice most effectively uses relevant information from the notes to accomplish this goal?'


def notes(items):
    return '<div class="notes">While researching a topic, a student has taken the following notes:<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul></div>'


def rs(d, items, goal, ans, w1, w2, w3):
    rec('rhetorical_synthesis', d, notes(items), 'The student wants to %s. %s' % (goal, Q_RS), ans, w1, w2, w3)


rs(0, ["Wangari Maathai was a Kenyan environmental activist.", "She founded the Green Belt Movement in 1977.", "The movement has planted millions of trees.", "She received the Nobel Peace Prize in 2004."],
   "introduce Maathai to an audience unfamiliar with her",
   ("Wangari Maathai, a Kenyan environmental activist, founded the Green Belt Movement in 1977 and won the Nobel Peace Prize in 2004.", "It identifies who she is and gives key facts."),
   ("The Green Belt Movement, founded in 1977, has planted millions of trees.", "It never names or identifies Maathai."),
   ("In 2004, Maathai received the Nobel Peace Prize, and her movement has planted millions of trees.", "It gives facts about her but never says who she is."),
   ("Many activists have won Nobel Prizes.", "It is general and not about Maathai."))
rs(0, ["Maya&rsquo;s Bakery bakes about 200 loaves a day using a single oven.", "Ruben&rsquo;s Bakery bakes about 2,000 loaves a day using automated ovens.", "Both bakeries use the same sourdough recipe."],
   "emphasize a difference in scale between the two bakeries",
   ("Although both bakeries use the same sourdough recipe, Maya&rsquo;s bakes about 200 loaves a day while Ruben&rsquo;s bakes about 2,000.", "It contrasts the numbers directly."),
   ("Both Maya&rsquo;s Bakery and Ruben&rsquo;s Bakery bake their loaves using the very same sourdough recipe.", "This states a similarity."),
   ("Maya&rsquo;s Bakery uses a single oven, while Ruben&rsquo;s uses automated ovens, and both use the same recipe.", "It contrasts equipment, not the number of loaves."),
   ("Ruben&rsquo;s bakes more loaves than Maya&rsquo;s does.", "It is vague and gives no figures."))
rs(0, ["Priya Sen and Tom&aacute;s Vega are both potters.", "Sen works in Chennai; Vega works in Lima.", "Both use clay dug near their studios.", "Sen glazes her pots blue; Vega leaves his unglazed."],
   "emphasize a similarity in the two potters&rsquo; methods",
   ("Although they work in different cities, potters Priya Sen and Tom&aacute;s Vega both shape their work from clay found near their studios.", "It highlights the shared material."),
   ("Sen glazes her pots blue, whereas Vega leaves his unglazed.", "This states a difference."),
   ("Priya Sen works in Chennai.", "It covers only one potter."),
   ("Sen works in Chennai and glazes her pots blue, while Vega works in Lima and leaves his pots unglazed.", "It lists differences, not a similarity in methods."))
rs(0, ["The Ganges river dolphin lives in freshwater rivers of South Asia.", "It is nearly blind.", "It navigates using echolocation.", "It is one of very few freshwater dolphin species."],
   "introduce the animal to an audience unfamiliar with it",
   ("The Ganges river dolphin, a freshwater species of South Asia, is nearly blind and navigates by echolocation.", "It names the animal, where it lives, and its defining traits."),
   ("It is nearly blind.", "It does not identify the animal."),
   ("Like many animals that live in dark or murky places, some dolphins find their way using echolocation.", "It is general and never introduces this particular dolphin."),
   ("Dolphins are mammals.", "It is true but not about this dolphin."))
rs(1, ["Researchers at Halvorsen University studied how noise affects learning.", "120 students learned lists of words in either a quiet room or a noisy room.", "Recall was tested 24 hours later.", "Recall was 18% lower for the noisy-room group."],
   "describe the study&rsquo;s methodology",
   ("In the study, 120 students learned word lists in either a quiet or a noisy room, and their recall was tested 24 hours later.", "It describes how the study was done."),
   ("Students who learned the word lists in the noisy room recalled 18% fewer words 24 hours later.", "This is a result, not a method."),
   ("Researchers at Halvorsen University have studied the effects of noise on learning.", "This is background."),
   ("Noise affects learning.", "It is a general claim, not a method."))
rs(1, ["A fossil of a new plant species was found in Patagonia.", "It is 52 million years old.", "It is the oldest known grass-like plant in the Southern Hemisphere.", "A graduate student found it."],
   "emphasize the significance of the discovery",
   ("At 52 million years old, the Patagonian fossil is the oldest known grass-like plant in the Southern Hemisphere.", "It stresses why the find matters."),
   ("A graduate student found a fossil of a new plant species in Patagonia.", "It reports the find but not its importance."),
   ("The fossil is 52 million years old.", "It gives the age without showing significance."),
   ("A graduate student discovered the 52-million-year-old fossil of a new plant species in Patagonia.", "It reports the find and its age but not why it matters."))
rs(1, ["Kestrel Lake is in northern Minnesota.", "Fish populations there fell sharply after 2015.", "Algae blooms grew larger after 2015.", "Algae blooms lower the oxygen in water."],
   "suggest that algae blooms may explain the decline in fish",
   ("The growth of algae blooms at Kestrel Lake after 2015 may explain the drop in fish, since blooms lower the oxygen in water.", "It links blooms to the decline through oxygen."),
   ("Kestrel Lake, in northern Minnesota, has had larger algae blooms since 2015, and algae blooms lower oxygen.", "It never mentions the decline in fish."),
   ("Fish populations at Kestrel Lake fell sharply after 2015.", "It states the decline but not a cause."),
   ("Algae blooms lower oxygen levels in lakes throughout northern Minnesota.", "It overgeneralizes and ignores the fish."))
rs(1, ["The Lantern Festival is held in Taipei each year.", "It marks the end of the Lunar New Year celebrations.", "Thousands of paper lanterns are released into the sky.", "Visitors write wishes on the lanterns."],
   "describe a tradition to an audience unfamiliar with it, focusing on what visitors do",
   ("At Taipei&rsquo;s annual Lantern Festival, which ends the Lunar New Year celebrations, visitors write wishes on paper lanterns that are then released into the sky.", "It covers what the festival is and what visitors do."),
   ("The Lantern Festival, held in Taipei each year, marks the end of the Lunar New Year celebrations.", "It says nothing about what visitors do."),
   ("Thousands of paper lanterns are released into the sky.", "It omits visitors&rsquo; actions."),
   ("Visitors write wishes on lanterns.", "It gives no context on the festival."))
rs(2, ["A 2019 survey of 1,000 commuters in Corvale found that 62% preferred trains to buses.", "The survey was conducted at the central train station.", "Corvale&rsquo;s bus ridership grew 4% in 2019."],
   "present the survey finding while acknowledging a limitation",
   ("A 2019 survey found that 62% of commuters preferred trains to buses, though because it was conducted at the central train station, its respondents may not represent all Corvale commuters.", "It states the result and the limitation."),
   ("A 2019 survey of 1,000 commuters in Corvale found that 62% preferred trains to buses.", "It states the result but no limitation."),
   ("The survey of Corvale commuters was conducted at the central train station, where 62% preferred trains.", "It distorts the finding and does not flag a limitation."),
   ("Although 62% of the 1,000 commuters surveyed in 2019 preferred trains to buses, Corvale&rsquo;s bus ridership still grew by 4% that year.", "It sets up a contrast, not a limitation."))
rs(2, ["Wolves and coyotes are both members of the dog family.", "Wolves hunt in packs of six to ten and take large prey such as elk.", "Coyotes usually hunt alone or in pairs and take small prey such as rodents and rabbits."],
   "emphasize a difference in how the two animals hunt",
   ("Whereas wolves hunt in packs of six to ten and take large prey such as elk, coyotes usually hunt alone or in pairs and pursue smaller prey such as rodents and rabbits.", "It contrasts both group size and prey."),
   ("Wolves and coyotes, both members of the dog family, hunt a range of animals, from elk to rodents and rabbits.", "It blends the two animals together instead of contrasting how they hunt."),
   ("Wolves hunt in packs of six to ten and take large prey such as elk.", "It covers only wolves."),
   ("Coyotes usually hunt alone or in pairs and eat rodents and rabbits.", "It covers only coyotes."))
rs(2, ["Biomimicry is design inspired by nature.", "Velcro was inspired by burrs sticking to a dog&rsquo;s fur.", "Engineers have modeled a high-speed train&rsquo;s nose on a kingfisher&rsquo;s beak."],
   "define a concept for an audience unfamiliar with it and give one example",
   ("Biomimicry, design inspired by nature, gave us Velcro, modeled on burrs clinging to a dog&rsquo;s fur.", "It gives both the definition and an example."),
   ("Velcro was inspired by burrs sticking to a dog&rsquo;s fur.", "It gives only an example."),
   ("Engineers modeled a high-speed train&rsquo;s nose on a kingfisher&rsquo;s beak, and Velcro was inspired by burrs on a dog&rsquo;s fur.", "It gives examples but never defines the concept."),
   ("Biomimicry is design inspired by nature.", "It gives a definition without an example."))
rs(2, ["For decades, ecologists believed that wildfires always harm spotted owl populations.", "A study of 12 forests found that owl numbers increased in areas with small, low-intensity burns.", "The study did not examine large, high-intensity fires."],
   "emphasize how the study&rsquo;s finding challenges a long-held belief",
   ("Although ecologists long believed that wildfires always harm spotted owls, a study of 12 forests found that owl numbers rose in areas with small, low-intensity burns.", "It sets the belief against the finding."),
   ("A study of 12 forests examined how fires affect spotted owls but did not look at large fires.", "It focuses on a limitation, not the challenge."),
   ("Ecologists believed for decades that wildfires always harm spotted owls.", "It gives only the old belief."),
   ("A study of 12 forests found that spotted owl numbers rose in areas with small, low-intensity burns, though it did not examine large, high-intensity fires.", "It reports a result and a limitation but never connects them to the long-held belief."))

# =============================================================== CROSS-TEXT (hard, hand-authored)
Q_X = 'Based on the texts, how would the author of Text 2 most likely respond to the claim in Text 1?'


def two(t1, t2):
    return '<b>Text 1</b><br>%s<br><br><b>Text 2</b><br>%s' % (t1, t2)


rec('cross_text', 2,
    two("Literary scholar Rana Haddad contends that novels narrated in the first person are inherently less reliable than novels narrated in the third person, since a first-person narrator&rsquo;s perspective is necessarily partial.",
        "Third-person narration is often treated as objective, yet many such novels filter events through a single character&rsquo;s consciousness, so that what looks like neutral description actually reflects that character&rsquo;s biases."),
    Q_X, ("By suggesting that the contrast Haddad draws is overstated because third-person narration can also be partial.", "Text 2 says third-person narration often reflects one character&rsquo;s biases."),
    ("By agreeing with Haddad that third-person narration presents events objectively, without any character&rsquo;s bias.", "Text 2 says the opposite."),
    ("By arguing that first-person narrators are more reliable than third-person narrators in every case.", "Text 2 does not claim this."),
    ("By claiming that novels should not use narrators at all.", "Text 2 does not suggest this."))
rec('cross_text', 2,
    two("Some paleontologists have proposed that certain dinosaurs were warm-blooded because their bones show rapid growth.",
        "Rapid bone growth also occurs in some cold-blooded reptiles under favorable conditions, so it cannot by itself settle the matter. Still, oxygen-isotope analyses of some dinosaur teeth suggest body temperatures higher than their surroundings."),
    'Which choice best describes the relationship between the texts?', ("Text 2 says Text 1&rsquo;s evidence is inconclusive alone but cites other evidence pointing the same way.", "Text 2 doubts the bone-growth evidence alone but cites isotope evidence for warm-bloodedness."),
    ("Text 2 disproves the claim made in Text 1.", "Text 2 does not disprove it; it partly supports it."),
    ("Text 2 repeats the evidence in Text 1 in different words.", "It adds new evidence."),
    ("Text 2 argues that because cold-blooded reptiles can grow rapidly, dinosaurs were most likely cold-blooded too.", "Text 2 says rapid growth cannot settle the matter and then cites evidence for warm-bloodedness."))
rec('cross_text', 2,
    two("Critics have long held that mid-twentieth-century public housing projects failed because of their modernist design.",
        "A review of 150 such projects across several cities found that design style was a weaker predictor of resident outcomes than maintenance funding: well-funded modernist projects fared about as well as traditional ones."),
    'Which choice best describes the relationship between the texts?', ("Text 2 offers evidence suggesting that a factor emphasized in Text 1 matters less than another factor.", "Design style is downplayed relative to maintenance funding."),
    ("Text 2 confirms that modernist design was the main cause of failure.", "It says the reverse."),
    ("Text 2 argues that public housing projects should not have been built.", "No such argument appears."),
    ("Text 2 shows that traditional housing designs failed more often than modernist designs when both were poorly funded.", "It says well-funded modernist projects did about as well as traditional ones; poorly funded projects are not compared by design."))
rec('cross_text', 2,
    two("Linguist Omar Sidi argues that a language&rsquo;s features reflect the environment of its speakers, noting that tonal languages are more common in warm, humid regions.",
        "Skeptics point out that correlations between climate and language can arise from shared ancestry: neighboring groups often speak related languages and also share a climate, so the pattern may reflect history rather than environment."),
    'Which choice best describes the relationship between the texts?', ("Text 2 proposes an alternative explanation for a pattern that Text 1 treats as evidence.", "Shared ancestry is offered instead of environment."),
    ("Text 2 provides additional data from neighboring groups that support Sidi&rsquo;s claim about climate and language.", "Text 2 challenges the claim."),
    ("Text 2 denies that any tonal languages exist in warm regions.", "It accepts the correlation."),
    ("Text 2 describes a method for measuring humidity.", "No method is described."))
