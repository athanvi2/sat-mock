"""Authored Reading & Writing items, part 7 (original text; researchers and characters are fictional).
Rhetorical synthesis (8 more per difficulty), hard cross-text (8 more), and words in context (6 more per difficulty).
Loaded after part 6 so older index-based uids never shift. Distractors are as long and specific as the key."""
from bank.rw_content import rec, wic, sense
from bank.rw_content2 import rs, two, Q_X

Q_REL = 'Which choice best describes the relationship between the texts?'

# =============================================================== RHETORICAL SYNTHESIS
# ---- easy
rs(0, ["The Great Wall of China was built over many centuries.", "Its sections stretch for thousands of kilometers.", "Much of it was built to defend against raids from the north.", "Today it is a popular tourist site."],
   "explain why the Great Wall was built",
   ("Much of the Great Wall of China, built over many centuries, was meant to defend against raids from the north.", "It gives the wall&rsquo;s purpose."),
   ("The Great Wall of China is a popular tourist site today.", "It gives its current use, not why it was built."),
   ("The Great Wall of China, built over many centuries, has sections that stretch for thousands of kilometers across the land.", "It gives its length, not its purpose."),
   ("The Great Wall was built over many centuries, and it is now visited by many tourists each year.", "It does not say why it was built."))
rs(0, ["Maya Lin designed the Vietnam Veterans Memorial in Washington, D.C.", "She was a 21-year-old college student when her design was chosen.", "The memorial is a long black granite wall.", "It lists the names of more than 58,000 service members."],
   "emphasize how young Lin was when her design was chosen",
   ("Maya Lin was only a 21-year-old college student when her design for the Vietnam Veterans Memorial was chosen.", "It stresses her age."),
   ("The Vietnam Veterans Memorial is a long black granite wall.", "It describes the memorial, not Lin&rsquo;s age."),
   ("The memorial that Maya Lin designed lists the names of more than 58,000 service members.", "It omits her age."),
   ("Maya Lin designed the Vietnam Veterans Memorial, a long black granite wall in Washington, D.C., that lists more than 58,000 names.", "It never mentions her age."))
rs(0, ["Koalas eat eucalyptus leaves.", "Eucalyptus leaves are low in nutrients.", "Koalas sleep up to 20 hours a day.", "Sleeping saves energy."],
   "explain why koalas sleep so much",
   ("Because eucalyptus leaves are low in nutrients, koalas save energy by sleeping up to 20 hours a day.", "It links the diet to the sleep."),
   ("Koalas eat eucalyptus leaves.", "It does not mention sleep."),
   ("Koalas sleep up to 20 hours a day, and they eat eucalyptus leaves during the few hours when they are awake in the trees.", "It lists facts without giving the reason."),
   ("Sleeping saves energy for many animals.", "It does not connect sleep to koalas&rsquo; diet."))
rs(0, ["The Hope Street Garden opened in 2020.", "It has 40 garden plots.", "Neighbors can rent a plot for $10 a year.", "The garden has a waiting list of 25 people."],
   "show that the garden is popular",
   ("The Hope Street Garden has a waiting list of 25 people for its 40 plots.", "A waiting list shows demand."),
   ("The Hope Street Garden opened in 2020 and has 40 garden plots that neighbors can rent for $10 a year.", "It gives facts but no sign of popularity."),
   ("Neighbors can rent a plot at the Hope Street Garden for only $10 a year.", "Price alone does not show popularity."),
   ("The Hope Street Garden, which opened in 2020, has 40 plots.", "It does not show popularity."))
rs(0, ["The okapi lives in the rainforests of central Africa.", "It has stripes on its legs like a zebra.", "It is actually the closest living relative of the giraffe.", "Scientists did not describe it until 1901."],
   "present a surprising fact about the okapi",
   ("Although it has zebra-like stripes on its legs, the okapi is the closest living relative of the giraffe.", "It sets appearance against an unexpected relationship."),
   ("The okapi lives in the rainforests of central Africa.", "This is not presented as surprising."),
   ("The okapi, which lives in the rainforests of central Africa and was not described by scientists until 1901, has striped legs.", "It gives appearance without the surprise."),
   ("Scientists described the okapi in 1901.", "It states a date without any surprise."))
rs(0, ["Ravi and Ben both ran for class president.", "Ravi promised longer lunch periods.", "Ben promised more after-school clubs.", "Ben won the election."],
   "contrast the two candidates&rsquo; promises",
   ("Ravi promised longer lunch periods, whereas Ben promised more after-school clubs.", "It sets the two promises side by side."),
   ("Ravi and Ben both ran for class president, and Ben won the election.", "It gives the result, not the promises."),
   ("Ben, who promised more after-school clubs, won the election for class president over Ravi.", "It covers only one candidate&rsquo;s promise."),
   ("Both candidates made promises.", "It is vague and gives no contrast."))
rs(0, ["Glass can be recycled again and again.", "Recycled glass melts at a lower temperature than new raw materials.", "Using recycled glass saves energy at factories.", "Many towns collect glass for recycling."],
   "explain one benefit of recycling glass",
   ("Because recycled glass melts at a lower temperature than new raw materials, using it saves energy at factories.", "It names a benefit and its cause."),
   ("Many towns collect glass for recycling, often in separate bins.", "It describes collection, not a benefit."),
   ("Glass can be recycled.", "It does not state a benefit."),
   ("Glass that towns collect for recycling can be recycled again and again, melted down at factories, and made into new glass.", "It does not state a benefit."))
rs(0, ["Nellie Bly was a journalist.", "In 1889, she set out to travel around the world faster than the hero of a famous novel.", "The hero took 80 days.", "Bly finished in 72 days."],
   "emphasize Bly&rsquo;s achievement",
   ("In 1889, journalist Nellie Bly traveled around the world in just 72 days, beating the 80 days of a famous novel&rsquo;s hero.", "It compares her time with the goal she beat."),
   ("Nellie Bly was a journalist who set out on a trip around the world in 1889.", "It omits the result."),
   ("A famous novel&rsquo;s hero traveled around the world in 80 days.", "It is about the novel, not Bly."),
   ("Nellie Bly was a journalist.", "It says nothing about her achievement."))
# ---- medium
rs(1, ["Octavia Butler was an American science fiction writer.", "Her novel <i>Kindred</i> was published in 1979.", "In it, a Black woman in 1976 California is pulled back in time to a Maryland plantation.", "The novel uses time travel to explore the history of slavery."],
   "describe <i>Kindred</i>&rsquo;s premise to an audience unfamiliar with the novel",
   ("In Octavia Butler&rsquo;s 1979 novel <i>Kindred</i>, a Black woman in 1976 California is pulled back in time to a Maryland plantation.", "It names the novel and states its premise."),
   ("Octavia Butler, an American science fiction writer, published the novel <i>Kindred</i> in 1979.", "It identifies the book but not its premise."),
   ("<i>Kindred</i> uses time travel to explore the history of slavery.", "It gives the theme, not the premise, and does not identify the author."),
   ("Octavia Butler was an American writer whose science fiction explored history, including the history of slavery.", "It describes the author, not the novel&rsquo;s premise."))
rs(1, ["Fireflies produce light through a chemical reaction.", "Nearly all of the energy from the reaction becomes light.", "An old-style incandescent bulb turns only about 10 percent of its energy into light.", "The rest of the bulb&rsquo;s energy becomes heat."],
   "contrast the efficiency of fireflies with that of incandescent bulbs",
   ("Fireflies turn nearly all of their reaction&rsquo;s energy into light; incandescent bulbs turn only about 10 percent.", "It contrasts the two efficiencies."),
   ("Fireflies produce light through a chemical reaction.", "It omits the bulb and any efficiency."),
   ("An incandescent bulb turns only about 10 percent of its energy into light, and the rest becomes heat.", "It covers only the bulb."),
   ("Like fireflies, incandescent bulbs produce light, although they rely on electricity rather than on a chemical reaction.", "It notes a similarity, not the contrast in efficiency."))
rs(1, ["Researchers studied 500 city trees.", "Trees in wide planting strips grew about twice as fast as trees in narrow strips.", "Wide strips give roots more room.", "Many cities plant trees in narrow strips to save space."],
   "make a recommendation to city planners based on the research",
   ("Since trees in wide planting strips grew twice as fast, planners should give street trees wider strips when they can.", "It turns the finding into advice."),
   ("Researchers who studied 500 city trees found that trees in wide strips grew about twice as fast as those in narrow strips.", "It reports the finding but makes no recommendation."),
   ("Many cities plant trees in narrow strips to save space.", "It describes current practice without advice."),
   ("Wide strips give roots more room.", "It gives a reason but no recommendation."))
rs(1, ["The Svalbard Global Seed Vault is in Norway.", "It stores seeds from nearly every country.", "It is built into a mountain in the Arctic.", "The cold helps keep the seeds viable if power fails."],
   "explain why the vault&rsquo;s location was chosen",
   ("Built into an Arctic mountain, the Svalbard vault stays cold enough to keep its seeds viable even if power fails.", "It links the location to its benefit."),
   ("The Svalbard Global Seed Vault in Norway stores seeds from nearly every country in the world.", "It gives the contents, not the reason for the location."),
   ("The Svalbard Global Seed Vault is in Norway.", "It names the country but not why."),
   ("The Svalbard Global Seed Vault, which stores seeds from nearly every country in the world, is built into a mountain in the Arctic region of Norway.", "It states the location but not the reason."))
rs(1, ["Kenji Ito and Lara Novak are both marine biologists.", "Ito studies coral reefs in the Pacific.", "Novak studies kelp forests in the Atlantic.", "Both measure how rising water temperatures affect the species they study."],
   "emphasize a similarity between the two biologists&rsquo; research",
   ("Though they study different ecosystems, Ito and Novak both measure how rising water temperatures affect their species.", "It highlights the shared focus."),
   ("Ito studies coral reefs in the Pacific, while Novak studies kelp forests in the Atlantic.", "It stresses a difference."),
   ("Kenji Ito and Lara Novak are marine biologists.", "It is a vague similarity that does not concern their research."),
   ("Lara Novak, a marine biologist, measures how rising water temperatures affect kelp forests in the Atlantic.", "It covers only one biologist."))
rs(1, ["Wilma Rudolph won three Olympic gold medals in 1960.", "As a child, she had polio and wore a leg brace.", "Doctors had said she might never walk normally.", "She became known as the fastest woman in the world."],
   "emphasize the obstacles Rudolph overcame",
   ("Although doctors said she might never walk normally after childhood polio, Wilma Rudolph became known as the fastest woman in the world.", "It sets the obstacle against the achievement."),
   ("Wilma Rudolph won three Olympic gold medals and became known as the fastest woman in the world.", "It gives achievements without the obstacles."),
   ("As a child, Rudolph wore a leg brace.", "It mentions an obstacle but not what she overcame it to do."),
   ("Wilma Rudolph, who became known as the fastest woman in the world, won three Olympic gold medals in one Games.", "It omits the obstacles."))
rs(1, ["A study compared two groups of students learning Spanish.", "One group used flashcards for 20 minutes a day.", "The other group practiced conversation for 20 minutes a day.", "After a semester, the conversation group scored higher on speaking tests; the flashcard group scored higher on vocabulary tests."],
   "present the study&rsquo;s results without favoring either method",
   ("After a semester, conversation practice led to higher speaking scores, while flashcards led to higher vocabulary scores.", "It gives each method&rsquo;s advantage evenly."),
   ("Students who practiced conversation for 20 minutes a day outperformed students who used flashcards for 20 minutes a day on speaking tests after a semester.", "It reports only the result favoring conversation."),
   ("A study compared two groups of students learning Spanish.", "It gives no results."),
   ("Flashcards are the better way to learn Spanish, since students who used them scored higher on vocabulary tests.", "It favors one method."))
rs(1, ["The city of Curitiba, Brazil, opened a bus rapid transit system in 1974.", "Buses run in dedicated lanes.", "Passengers pay before boarding at tube-shaped stations.", "The design lets buses move almost as quickly as subway trains at a fraction of the cost."],
   "explain how Curitiba&rsquo;s system achieves its speed",
   ("With dedicated lanes and fares paid before boarding, Curitiba&rsquo;s buses move almost as quickly as subway trains.", "It names the features that produce speed."),
   ("Curitiba, Brazil, opened a bus rapid transit system in 1974 that costs a fraction of a subway.", "It gives the date and cost, not how speed is achieved."),
   ("Passengers in Curitiba wait for buses at tube-shaped stations.", "It describes the stations without explaining speed."),
   ("Curitiba&rsquo;s bus system, opened in 1974, is almost as fast as a subway.", "It states the speed but not how it is achieved."))
# ---- hard
rs(2, ["Economist Rosa Lindqvist studied a 2015 policy that required restaurants to post calorie counts on menus.", "Average calories per order fell by about 3 percent after the policy took effect.", "The drop was largest among customers who ordered high-calorie meals.", "Lindqvist notes that the study covered only chain restaurants."],
   "present Lindqvist&rsquo;s findings while noting a limit on how widely they apply",
   ("Posting calorie counts cut calories per order by about 3 percent, though Lindqvist&rsquo;s study covered only chain restaurants.", "It gives the finding and its scope limit."),
   ("Because Lindqvist studied only chain restaurants, her research reveals nothing about how menu calorie counts affect what customers order.", "It overstates the limitation and omits the finding."),
   ("After restaurants posted calorie counts, calories per order fell by about 3 percent, with the largest drop among high-calorie orders.", "It gives findings but omits the limitation."),
   ("Lindqvist studied a 2015 policy.", "It describes the topic only."))
rs(2, ["Two translations of an ancient Greek epic appeared in 2017.", "Translator A kept the original&rsquo;s line count, producing lines of the same number as the Greek.", "Translator B used plain modern prose.", "Reviewers praised A for faithfulness to form and B for readability."],
   "contrast the two translators&rsquo; priorities",
   ("Translator A preserved the original&rsquo;s line count, while Translator B favored plain prose; reviewers praised faithfulness in one and readability in the other.", "It contrasts their choices and what each gained."),
   ("Two translations of an ancient Greek epic appeared in 2017 and were praised by reviewers.", "It gives no contrast."),
   ("Translator A kept the original&rsquo;s line count, producing lines of the same number as the Greek text.", "It covers only one translator."),
   ("Both translators of the 2017 editions tried to make the ancient Greek epic accessible to modern readers.", "It invents a shared aim instead of contrasting priorities."))
rs(2, ["Historian Amir Qadir studied grain prices in eighteenth-century France.", "Prices spiked sharply in 1788 after a poor harvest.", "Bread consumed about half of a typical worker&rsquo;s wages that year.", "Qadir argues that economic hardship helped fuel unrest in 1789."],
   "present Qadir&rsquo;s argument along with the evidence that supports it",
   ("Qadir argues that hardship fueled unrest in 1789, noting that after a poor 1788 harvest, bread took about half a worker&rsquo;s wages.", "It pairs his claim with the price evidence."),
   ("After a poor harvest in 1788, grain prices in France spiked sharply.", "It gives evidence but not the argument."),
   ("Qadir argues that economic hardship helped fuel unrest in France in 1789.", "It gives the argument without evidence."),
   ("Historian Amir Qadir, who studied grain prices in eighteenth-century France, found that prices spiked sharply in 1788 after a poor harvest.", "It gives evidence but never states his argument."))
rs(2, ["Sea stars along the North American Pacific coast began dying in large numbers in 2013.", "The die-off was linked to a wasting disease.", "Sunflower sea stars, which eat sea urchins, were nearly wiped out.", "Without them, urchin populations exploded and ate large areas of kelp forest."],
   "explain how the die-off affected kelp forests",
   ("The wasting disease nearly wiped out sunflower sea stars, which eat urchins, so urchins multiplied and ate large areas of kelp forest.", "It traces the chain from disease to kelp loss."),
   ("Beginning in 2013, sea stars along the North American Pacific coast died in large numbers from a wasting disease.", "It describes the die-off, not its effect on kelp."),
   ("Sea urchin populations exploded along the Pacific coast.", "It omits the cause and the kelp."),
   ("Sunflower sea stars, which eat sea urchins, were among the species nearly wiped out by a wasting disease after 2013.", "It stops before the effect on kelp."))
rs(2, ["Photographer Dorothea Lange took &ldquo;Migrant Mother&rdquo; in 1936.", "The photo shows a mother and her children during the Great Depression.", "It was published in newspapers and helped prompt federal aid to a camp of farmworkers.", "Some critics note that Lange posed and cropped the image."],
   "acknowledge a criticism of the photograph while emphasizing its impact",
   ("Though critics note Lange posed and cropped &ldquo;Migrant Mother,&rdquo; the 1936 photo helped prompt federal aid to farmworkers.", "It concedes the criticism and stresses the impact."),
   ("Dorothea Lange&rsquo;s &ldquo;Migrant Mother&rdquo; shows a mother and her children during the Great Depression.", "It describes the image with no criticism or impact."),
   ("Because Lange posed and cropped &ldquo;Migrant Mother,&rdquo; the photograph cannot be trusted as a record of the Great Depression.", "It stresses the criticism and omits the impact."),
   ("Published in newspapers, &ldquo;Migrant Mother&rdquo; helped prompt federal aid.", "It omits the criticism."))
rs(2, ["Linguist Soo-ah Park compared how children in two countries learn color words.", "Children in Country A learned basic color words by age 3.", "Children in Country B learned them by age 5.", "Park found that parents in Country A named colors more often during play."],
   "suggest a possible explanation for the difference Park observed",
   ("Children in Country A may have learned color words two years earlier because their parents named colors more often during play.", "It links the timing difference to parents&rsquo; talk."),
   ("Children in Country A learned basic color words by age 3, while children in Country B learned them by age 5.", "It states the difference without explaining it."),
   ("Parents in Country A named colors often.", "It gives the factor without linking it to the difference."),
   ("Soo-ah Park compared how children in two countries learn basic color words, finding a difference of two years in the age of learning.", "It restates the study without offering an explanation."))
rs(2, ["Engineer Ifeoma Obi designed a water filter made from clay and sawdust.", "When fired, the sawdust burns away, leaving tiny pores.", "The pores trap bacteria while letting water through.", "The filters cost about $10 and can be made from local materials."],
   "emphasize why the filter is practical for communities with limited resources",
   ("Obi&rsquo;s filters cost about $10 and can be made from local clay and sawdust.", "It stresses low cost and local materials."),
   ("When Obi&rsquo;s clay-and-sawdust filters are fired, the sawdust burns away and leaves tiny pores that trap bacteria while letting water through.", "It explains how the filter works, not why it is practical."),
   ("Engineer Ifeoma Obi designed a water filter made from clay and sawdust that traps bacteria.", "It does not address cost or materials."),
   ("The tiny pores in Obi&rsquo;s filters trap bacteria while letting water through, which makes the water safer to drink.", "It gives a benefit but not why the filter suits limited resources."))
rs(2, ["Two cities tried different approaches to reducing homelessness.", "City X built shelters with a limited number of beds.", "City Y gave people apartments first and then offered support services.", "Two years later, City Y had a larger drop in homelessness than City X."],
   "present the results of City Y&rsquo;s approach in comparison with City X&rsquo;s",
   ("Two years later, homelessness had fallen more in City Y, which offered apartments first, than in City X, which built shelters.", "It compares outcomes and identifies each approach."),
   ("City Y gave people apartments first and then offered support services to them.", "It describes City Y&rsquo;s approach without results or comparison."),
   ("City X built shelters with a limited number of beds, while City Y gave people apartments first and then offered them support services.", "It contrasts approaches but not results."),
   ("City Y reduced homelessness.", "It gives no comparison with City X."))

# =============================================================== CROSS-TEXT (hard)
rec('cross_text', 2,
    two("Some ecologists argue that reintroducing large predators, such as wolves, restores balance to ecosystems by reducing overgrazing by deer and elk.",
        "Predators can reduce grazing, but the effect depends on local conditions. In valleys where human hunting already kept elk numbers low, researchers found that returning wolves made little difference to plant growth."),
    Q_X, ("By suggesting that the benefit depends on conditions and may be small where grazing is already controlled.", "Text 2 limits the claim to certain conditions."),
    ("By rejecting the idea that predators ever reduce grazing, since in some valleys wolves made little difference to plant growth.", "Text 2 grants that predators can reduce grazing."),
    ("By agreeing that wolves restore balance in every ecosystem.", "Text 2 describes cases where they made little difference."),
    ("By arguing that human hunting harms ecosystems more than overgrazing by deer and elk does.", "Text 2 does not compare these harms."))
rec('cross_text', 2,
    two("Literary critic Omar Haddad argues that a novel&rsquo;s ending determines its meaning: whatever came before must be reread in light of how the story concludes.",
        "Readers do not experience a novel only at its end. The suspense, sympathy, and doubt that a reader feels along the way are part of what the book means, even if the ending later resolves them. An ending can reframe what came before, but it cannot erase it."),
    Q_X, ("By granting that endings can reframe a story while denying that they alone determine its meaning.", "Text 2 concedes reframing but insists the reading experience matters too."),
    ("By agreeing that a novel&rsquo;s meaning is fixed entirely by the way its story concludes.", "Text 2 says an ending cannot erase what came before."),
    ("By arguing that endings have no effect.", "Text 2 says endings can reframe earlier parts."),
    ("By claiming that readers should skip to the end of a novel first so that they understand its meaning from the start.", "Text 2 makes no such recommendation."))
rec('cross_text', 2,
    two("Many nutrition researchers have held that eating eggs raises the risk of heart disease because eggs are high in dietary cholesterol.",
        "Large studies following hundreds of thousands of adults for years have found little link between moderate egg consumption and heart disease in most people. For most people, cholesterol in food has a smaller effect on blood cholesterol than once thought, though some people are more sensitive to it than others."),
    Q_REL, ("Text 2 presents evidence that challenges Text 1&rsquo;s view for most people while noting exceptions.", "Text 2 finds little link for most but notes sensitive individuals."),
    ("Text 2 confirms Text 1&rsquo;s view that eggs raise heart disease risk.", "Text 2 finds little link for most people."),
    ("Text 2 argues that everyone should eat eggs every day, since eggs have no effect on heart disease in anyone.", "Text 2 notes some people are more sensitive."),
    ("Text 2 shows that the studies cited in Text 1 were never actually conducted by nutrition researchers.", "Text 2 does not discuss Text 1&rsquo;s sources."))
rec('cross_text', 2,
    two("Urban historian Grace Lin argues that the spread of automobiles in the 1920s was the main cause of the decline of American streetcar systems.",
        "Streetcar companies were in trouble before cars became common. Many were bound by city contracts that fixed fares at five cents even as costs rose, leaving them unable to maintain tracks or buy new cars. Automobiles hastened the decline, but they struck systems already weakened."),
    Q_X, ("By arguing that fixed fares had already weakened streetcars, so cars were not the main cause of their decline.", "Text 2 points to an earlier, underlying problem."),
    ("By agreeing that automobiles were the main cause and adding that fixed fares played no role at all.", "Text 2 emphasizes fixed fares."),
    ("By denying that automobiles had any effect.", "Text 2 says cars hastened the decline."),
    ("By claiming that streetcar companies failed because they charged fares that were too high for most riders.", "Text 2 says fares were fixed low."))
rec('cross_text', 2,
    two("Psychologist Kara Mensah contends that multitasking harms performance because the brain cannot focus on two demanding tasks at once; it must switch between them, losing time with each switch.",
        "Studies of people who frequently multitask confirm that switching carries costs. A small number of people, however, show almost no loss when combining two demanding tasks. Researchers studying these &ldquo;supertaskers&rdquo; suggest that the costs, though real for most people, may not be universal."),
    Q_X, ("By accepting that switching is costly for most people while suggesting a few may be exceptions.", "Text 2 confirms the costs but notes supertaskers."),
    ("By rejecting Mensah&rsquo;s claim entirely, since studies show that multitasking carries no costs for anyone.", "Text 2 confirms the costs for most people."),
    ("By arguing that frequent multitasking trains everyone to become a supertasker over time.", "Text 2 does not say supertasking can be learned."),
    ("By agreeing without qualification.", "Text 2 adds a qualification about exceptions."))
rec('cross_text', 2,
    two("Some art historians hold that the cave paintings at a certain site were made by a single artist, pointing to the consistent style of the animal figures.",
        "Consistency of style need not indicate a single hand; artists trained in a shared tradition can produce work that looks remarkably uniform. Moreover, radiocarbon dates from the charcoal used in the paintings span roughly five thousand years, far longer than any single lifetime."),
    Q_REL, ("Text 2 disputes Text 1&rsquo;s reasoning and offers dating evidence that undercuts its conclusion.", "Text 2 answers the style argument and adds dating evidence."),
    ("Text 2 supports Text 1 by providing dating evidence that all the paintings were made within one lifetime.", "The dates span about five thousand years."),
    ("Text 2 describes the animals in the paintings.", "Text 2 concerns authorship, not the animals."),
    ("Text 2 agrees that the style is consistent and concludes that the paintings must therefore be forgeries.", "Text 2 does not claim they are forgeries."))
rec('cross_text', 2,
    two("Economist Luis Ortega argues that raising a city&rsquo;s parking fees downtown will drive shoppers to suburban malls, hurting downtown businesses.",
        "When one city raised downtown meter prices to keep about one space per block open, sales at nearby shops rose slightly. Shoppers who had circled looking for parking now found spaces quickly, and higher turnover meant more customers could park over the course of a day."),
    Q_X, ("By presenting a case in which higher fees coincided with slightly higher downtown sales, contrary to Ortega&rsquo;s prediction.", "Text 2&rsquo;s example runs against his prediction."),
    ("By agreeing that shoppers will abandon downtown for suburban malls whenever parking fees rise.", "Text 2&rsquo;s example shows sales rising."),
    ("By arguing that cities should eliminate parking fees.", "Text 2 describes raising fees."),
    ("By claiming that downtown businesses lose customers because too many parking spaces sit empty every day.", "Text 2 does not describe empty spaces as the problem."))
rec('cross_text', 2,
    two("Many biologists once regarded the appendix as a useless leftover of evolution with no function in modern humans.",
        "The appendix contains tissue associated with the immune system, and some researchers propose that it serves as a reservoir of helpful gut bacteria that can repopulate the intestines after illness. Supporting this idea, the appendix appears to have evolved independently many times in mammals, which would be unlikely if it served no purpose."),
    Q_REL, ("Text 2 offers a proposed function and evolutionary evidence that challenge Text 1&rsquo;s view.", "Text 2 argues the appendix may be useful."),
    ("Text 2 confirms that the appendix has no function and adds that it has disappeared in most mammals.", "Text 2 proposes a function, and says it evolved many times."),
    ("Text 2 explains how to remove the appendix.", "Surgery is not discussed."),
    ("Text 2 argues that the immune system evolved from the appendix after it lost its original digestive function.", "Text 2 makes no such claim."))

# =============================================================== WORDS IN CONTEXT
# ---- easy
wic(0, "The puppy was so ______ that it greeted every visitor with a wagging tail and tried to climb into their laps.", ('friendly', 'kind and pleasant toward others'),
    "Greeting every visitor and climbing into laps shows a friendly nature.",
    ('timid', 'shy and easily frightened'), ('sluggish', 'slow-moving and inactive'), ('stubborn', 'unwilling to change one&rsquo;s mind'))
wic(0, "After the long drought, the farmers were ______ to see dark clouds finally gathering over the fields.", ('relieved', 'freed from worry'),
    "Rain ending a long drought would ease the farmers&rsquo; worry.",
    ('disappointed', 'sad that hopes were not met'), ('indifferent', 'not caring either way'), ('confused', 'unable to understand'))
wic(0, "The museum guard asked visitors not to touch the ______ vase, which was more than two thousand years old and could break easily.", ('fragile', 'easily broken'),
    "&ldquo;Could break easily&rdquo; defines fragile.",
    ('sturdy', 'strong and hard to break'), ('ordinary', 'common and unremarkable'), ('enormous', 'extremely large'))
wic(0, "Because Lucia wanted her essay to be ______, she checked every date and name against her sources before turning it in.", ('accurate', 'free from mistakes'),
    "Checking every date and name is how one makes an essay accurate.",
    ('lengthy', 'very long'), ('humorous', 'funny'), ('vague', 'unclear or imprecise'))
sense(0, "The coach asked the players to run a few more laps before practice ended, but most of them were too tired to keep up the pace.", 'run',
      ('Complete', ''), "The players are asked to do, or complete, laps.",
      ('Manage', 'Run can mean manage, as in running a business; that does not fit laps.'), ('Flow', 'Run can mean flow, as water does; players do not flow laps.'), ('Campaign', 'Run can mean seek office; that does not fit here.'))
sense(0, "When the storm knocked out the power, the family gathered around a single candle, whose light was just bright enough to play cards by.", 'light',
      ('Glow', ''), "The candle&rsquo;s light is the glow it gives off.",
      ('Weightless', 'Light can mean not heavy, but here it is something a candle gives off.'), ('Pale', 'Light can describe a pale color, which does not fit a candle&rsquo;s brightness.'), ('Gentle', 'Light can mean gentle, as in a light touch, which does not fit here.'))
# ---- medium
wic(1, "The mayor&rsquo;s speech was ______: rather than promising specific actions, it offered only broad statements that everyone could agree with.", ('vague', 'lacking clear detail'),
    "Broad statements instead of specific actions make a speech vague.",
    ('decisive', 'showing firm resolve'), ('technical', 'full of specialized detail'), ('hostile', 'unfriendly and aggressive'))
wic(1, "The new evidence did not overturn the theory, but it did ______ it, showing that the pattern held only in warm climates.", ('refine', 'improve by making more precise'),
    "Limiting the theory to warm climates makes it more precise without overturning it.",
    ('abandon', 'give up completely'), ('celebrate', 'praise publicly'), ('conceal', 'hide from view'))
wic(1, "Although the author&rsquo;s first novel sold poorly, her second was a ______ success, selling a million copies in its first year.", ('resounding', 'unmistakable and emphatic'),
    "A million copies in a year is an emphatic success, contrasting with the first novel.",
    ('modest', 'limited in size or amount'), ('doubtful', 'uncertain'), ('gradual', 'happening slowly over time'))
wic(1, "Researchers found that the medicine&rsquo;s benefits were ______: patients who stopped taking it returned to their earlier condition within weeks.", ('temporary', 'lasting only a limited time'),
    "Benefits that vanish soon after stopping are temporary.",
    ('permanent', 'lasting forever'), ('harmful', 'causing damage'), ('widespread', 'found over a large area'))
sense(1, "The committee decided to table the proposal until the next meeting, when more members would be present to vote on it.", 'table',
      ('Postpone', ''), "Putting off the proposal until the next meeting means postponing it.",
      ('Display', 'Table can suggest laying something out to show; the proposal is delayed, not displayed.'), ('Furnish', 'A table is furniture, which does not fit an action taken on a proposal.'), ('Organize', 'Tables organize data, but nothing here is being arranged.'))
sense(1, "The scientist&rsquo;s early findings were promising, but she knew they would need to be confirmed by further trials before they could carry much weight with her colleagues.", 'carry',
      ('Have', ''), "To &ldquo;carry weight&rdquo; is to have influence.",
      ('Transport', 'Carry can mean move from place to place, but findings do not move weight.'), ('Stock', 'A store carries goods, which does not fit findings.'), ('Win', 'Carry can mean win, as in carrying a vote, but that does not fit weight with colleagues.'))
# ---- hard
wic(2, "The critic&rsquo;s review was notably ______; she praised the novel&rsquo;s ambition but found fault with nearly every one of its chapters.", ('ambivalent', 'having mixed feelings'),
    "Praise for ambition alongside fault in nearly every chapter shows mixed feelings.",
    ('effusive', 'expressing unrestrained praise'), ('perfunctory', 'done with little care or interest'), ('vitriolic', 'bitterly harsh throughout'))
wic(2, "Rather than ______ the town council&rsquo;s decision, residents who disagreed with it organized a petition and gathered signatures for a new vote.", ('acquiescing to', 'accepting without protest'),
    "&ldquo;Rather than&rdquo; contrasts accepting quietly with organizing opposition.",
    ('instigating', 'causing to begin'), ('scrutinizing', 'examining closely'), ('anticipating', 'expecting in advance'))
wic(2, "The historian&rsquo;s account is ______: drawing on letters, diaries, tax records, and court documents, it reconstructs daily life in the village in extraordinary detail.", ('exhaustive', 'thorough and complete'),
    "Many kinds of sources and extraordinary detail make the account exhaustive.",
    ('speculative', 'based on guesses rather than evidence'), ('cursory', 'hasty and superficial'), ('partisan', 'strongly favoring one side'))
wic(2, "Though often described as ______, the composer in fact revised each of her pieces for months, slowly polishing even the shortest passages.", ('spontaneous', 'acting on sudden impulse'),
    "&ldquo;Though&rdquo; contrasts the reputation with months of slow revision, so the reputation is spontaneity.",
    ('painstaking', 'extremely careful and thorough'), ('derivative', 'imitating the work of others'), ('prolific', 'producing a great deal of work'))
sense(2, "The treaty did little to address the underlying dispute, but it arrested the fighting long enough for diplomats to begin serious talks.", 'arrested',
      ('Halted', ''), "The treaty stopped the fighting for a time.",
      ('Detained', 'Arrest often means take into custody, which does not fit fighting.'), ('Captivated', 'An arresting sight captures attention, which does not fit here.'), ('Accused', 'Arrest can suggest a charge, which cannot apply to fighting.'))
sense(2, "The novelist&rsquo;s spare style, with its short sentences and few adjectives, belies the emotional intensity of the scenes she describes.", 'belies',
      ('Disguises', ''), "The plain style gives a false impression of calm, disguising the intensity beneath.",
      ('Proves', 'Belie means the opposite: it contradicts or hides.'), ('Exaggerates', 'A spare style understates, rather than exaggerates, the intensity.'), ('Explains', 'The style does not explain the intensity; it masks it.'))
