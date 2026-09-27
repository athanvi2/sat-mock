"""Authored Reading & Writing items, part 4 (original text; researchers are fictional).
Inferences, rhetorical synthesis, and hard cross-text items. Loaded after parts 1-3 so older uids never shift.
Distractors are written to be as long and specific as the key (see tests/rw_quality.py)."""
from bank.rw_content import rec, Q_INF
from bank.rw_content2 import rs, two, Q_X

Q_REL = 'Which choice best describes the relationship between the texts?'

# =============================================================== INFERENCES
# ---- easy
rec('inferences', 0,
    "Every plant in Jamal&rsquo;s garden wilted during the hot week except the ones growing in the shade of the oak tree. Jamal concluded that ______",
    Q_INF, ("the shade helped protect those plants from the heat.", "Only the shaded plants survived the hot week."),
    ("the oak tree took water away from the plants growing farther from it.", "Water use by the oak is not mentioned, and the plants near it did best."),
    ("his plants wilted because they received too much rain during the week.", "The week was hot; rain is not mentioned."),
    ("plants growing in the shade of large trees wilt faster than plants growing in full sun.", "The shaded plants were the ones that did not wilt."))
rec('inferences', 0,
    "The school library extended its hours until 7:00 p.m. In the first month, the number of students using the library after 4:00 p.m. doubled. The librarian reasoned that ______",
    Q_INF, ("many students had wanted to use the library later in the day.", "Usage after 4:00 doubled once later hours were available."),
    ("students stopped visiting in the mornings.", "Morning use is not discussed."),
    ("the library&rsquo;s new books drew students in.", "New books are not mentioned."),
    ("most students leave school at 3:00 p.m.", "This does not explain why late use increased."))
rec('inferences', 0,
    "A bakery tried selling its bread in paper bags instead of plastic ones. Customers said the crust stayed crisp longer in the paper bags. The bakery&rsquo;s owner decided that ______",
    Q_INF, ("paper bags kept the bread&rsquo;s crust crisp longer.", "Customers reported crisper crust in paper bags."),
    ("customers preferred rye bread to white bread when it was sold in paper bags.", "Types of bread are not mentioned."),
    ("plastic bags cost the bakery more money than paper bags did each month.", "Cost is not mentioned."),
    ("bread should not be sold in bags.", "Nothing suggests this."))
rec('inferences', 0,
    "Researchers placed two bird feeders in a park: one filled with sunflower seeds and one filled with corn. Over two weeks, the sunflower feeder had to be refilled four times, while the corn feeder was refilled only once. The results suggest that ______",
    Q_INF, ("the park&rsquo;s birds preferred sunflower seeds to corn.", "The sunflower feeder emptied much faster."),
    ("corn is harmful to birds.", "Harm is not mentioned."),
    ("more birds visit parks in winter than in summer.", "Seasons are not compared."),
    ("both feeders drew equal numbers of birds.", "The refill difference points to a preference."))
rec('inferences', 0,
    "Mia&rsquo;s cat usually sleeps on the sunny windowsill in the afternoon. Today, the cat slept under the bed instead, and Mia noticed that workers were using loud machines outside the window all afternoon. Mia guessed that ______",
    Q_INF, ("the noise outside kept the cat off the windowsill.", "The only change was the loud machines by the window."),
    ("the cat was hungry and was waiting under the bed for its dinner.", "Hunger is not mentioned."),
    ("the windowsill had become too cold for the cat to sleep on comfortably.", "It is described as sunny."),
    ("the cat has come to prefer dark, enclosed places to the sunny windowsill it once liked.", "It usually sleeps on the sunny windowsill; one day does not show a new preference."))
rec('inferences', 0,
    "In a town where most roads have no sidewalks, a new sidewalk was built along Oak Street. Soon after, many more parents began walking their children to the school on Oak Street. This suggests that ______",
    Q_INF, ("the lack of sidewalks had kept parents from walking their children to school.", "Walking increased once a sidewalk was built."),
    ("the school on Oak Street has more students than any other school in town.", "School size is not mentioned."),
    ("parents in the town sold their cars.", "Car ownership is not mentioned."),
    ("parents built the sidewalk themselves.", "Who built it is not mentioned."))
rec('inferences', 0,
    "Two identical ice cubes were placed on two plates, one made of metal and one made of wood. The cube on the metal plate melted much faster. Because the room temperature was the same for both, the result suggests that ______",
    Q_INF, ("the metal plate moved heat into the ice faster than the wooden plate did.", "The plate was the only difference, and heat melts ice."),
    ("wood is heavier than metal.", "Weight is not relevant here."),
    ("the air near the metal plate was warmer than the air near the wooden plate.", "The text says the room temperature was the same."),
    ("ice melts faster when it is placed in a dark room than when it is placed in sunlight.", "Light is not mentioned."))
rec('inferences', 0,
    "A town placed recycling bins next to every trash can in its main park. Before the bins were added, park workers pulled about 50 bottles a week out of the trash. After the bins were added, they pulled out about 10. This suggests that ______",
    Q_INF, ("many visitors used the recycling bins once they were easy to reach.", "Fewer bottles ended up in the trash after bins were placed nearby."),
    ("visitors stopped bringing bottles.", "The recycling bins give a simpler explanation for fewer bottles in the trash."),
    ("workers stopped checking the trash.", "They continued to count bottles."),
    ("the town removed its trash cans.", "The bins were added next to the trash cans."))
# ---- medium
rec('inferences', 1,
    "Linguists have noticed that speakers of a certain language use far more words for kinds of snow than speakers of neighboring languages, but only in villages located high in the mountains. Speakers of the same language living in the lowlands use no more snow words than their neighbors. This pattern suggests that ______",
    Q_INF, ("a community&rsquo;s vocabulary may reflect the conditions it regularly deals with.", "Only the mountain speakers, who encounter much more snow, have the extra words."),
    ("the language began in the lowlands.", "Origins are not discussed."),
    ("snow words are harder to learn.", "Difficulty of learning is not discussed."),
    ("mountain villages are more populous.", "Population is not compared, and it would not explain the extra snow words."))
rec('inferences', 1,
    "A museum found that visitors spent an average of 40 seconds at each painting. When it added short audio descriptions that played automatically near several paintings, visitors stayed an average of two minutes at those paintings but still about 40 seconds at the others. The museum concluded that ______",
    Q_INF, ("the audio descriptions, not a general change in visitors&rsquo; habits, increased viewing time.", "Only paintings with audio saw longer visits."),
    ("visitors prefer brightly colored paintings.", "Colors are not discussed."),
    ("visitors began spending more time at every painting in the museum after the audio descriptions were added.", "Time at the other paintings stayed about 40 seconds."),
    ("the audio descriptions made the galleries crowded.", "Crowding is not discussed."))
rec('inferences', 1,
    "When a river dam was removed in Washington State, salmon returned to spawn in stretches of river they had not reached in nearly a century. Within a few years, researchers also found more nutrients from the ocean in the soil and plants along those stretches. Since salmon carry ocean nutrients inland when they die after spawning, the researchers inferred that ______",
    Q_INF, ("the returning salmon were likely the source of the new nutrients.", "Salmon bring ocean nutrients, and the nutrients rose where salmon returned."),
    ("the dam had been adding nutrients.", "The nutrients increased after the dam was removed."),
    ("plants no longer needed river water.", "Water needs are not discussed."),
    ("salmon avoid dams because of noise.", "The dam physically blocked them; noise is not mentioned."))
rec('inferences', 1,
    "A hospital introduced a checklist that surgical teams must complete before every operation. In the following year, complications decreased by a third. However, the hospital also hired additional nurses that same year. Before crediting the checklist, hospital administrators would most likely want to know ______",
    Q_INF, ("whether complications also fell in units that got new nurses but no checklist.", "Both changes happened at once, so their effects must be separated."),
    ("how many minutes it takes a surgical team to complete the checklist before each operation.", "Duration does not help separate the two causes."),
    ("whether surgeons liked the checklist.", "Opinions do not isolate the cause."),
    ("how many operations the hospital performed in the year before the checklist was introduced.", "Volume does not separate the two causes."))
rec('inferences', 1,
    "Historian Elena Ruiz found that letters sent between two merchant families in the 1600s became much shorter after a regular postal route was established between their cities. Earlier letters had often summarized months of news, while later letters addressed only a few recent events. Ruiz suggests that ______",
    Q_INF, ("more frequent delivery meant each letter needed less news.", "Regular service meant letters could be sent more often, so each could be shorter."),
    ("the two families had grown less friendly toward each other after the postal route was established.", "Nothing suggests a change in the relationship."),
    ("paper became more expensive after the postal route opened, so the families wrote less.", "Paper prices are not discussed."),
    ("the merchants had stopped trading with each other and wrote only to exchange family news.", "Trade is not said to stop."))
rec('inferences', 1,
    "In a study of a forest, ecologists found that trees near the edges of clearings grew more branches on the side facing the clearing. Trees deep in the forest, where light comes mostly from above, grew branches evenly on all sides. The ecologists reasoned that ______",
    Q_INF, ("the trees tend to grow branches toward where the most light comes from.", "Edge trees grow toward the brighter side; interior trees get light from above and grow evenly."),
    ("clearings form in forests when trees near the edges grow too many branches on one side.", "The cause of clearings is not discussed."),
    ("edge trees are older.", "Age is not mentioned."),
    ("trees deep in the forest grow faster than trees near clearings because they are sheltered from wind.", "Growth rates and wind are not discussed."))
rec('inferences', 1,
    "A company allowed half of its employees to choose their own work hours, while the other half kept a fixed schedule. After six months, the two groups completed a similar amount of work, but employees with flexible hours took fewer sick days. These results suggest that ______",
    Q_INF, ("flexible hours may reduce absences without lowering output.", "Output was similar and sick days were lower with flexibility."),
    ("employees with fixed schedules completed more work because they had fewer distractions at home.", "The groups completed a similar amount of work."),
    ("flexible hours caused employees to take more sick days than they had before the change.", "They took fewer sick days."),
    ("fixed schedules suit most workers.", "The results favor flexible hours on absences."))
rec('inferences', 1,
    "The novelist Clara Webb published her first three books under a man&rsquo;s name. After she began publishing under her own name, reviewers who had praised the earlier books&rsquo; &ldquo;bold&rdquo; style began describing nearly identical writing as &ldquo;harsh.&rdquo; A literary historian studying these reviews would most likely conclude that ______",
    Q_INF, ("reviewers&rsquo; views were shaped by beliefs about the author&rsquo;s gender.", "Similar writing was described differently once her identity changed."),
    ("Webb&rsquo;s writing style changed dramatically once she began publishing under her own name.", "The writing is described as nearly identical."),
    ("Webb&rsquo;s later books sold more copies than her earlier ones because of the reviews.", "Sales are not discussed."),
    ("reviewers of the period did not read the books closely and relied on the author&rsquo;s reputation instead.", "Nothing supports this."))
# ---- hard
rec('inferences', 2,
    "In some species of cichlid fish, a dominant male develops bright colors while subordinate males stay dull. When biologists removed the dominant male from a tank, one of the dull males became brightly colored within days. When they returned the dominant male, that fish faded again. These observations suggest that ______",
    Q_INF, ("a male&rsquo;s coloring tracks his current social rank rather than being fixed.", "The same fish brightened and faded as the dominant male was removed and returned."),
    ("dull males can never become dominant.", "One dull male brightened when given the chance."),
    ("bright coloring causes males to lose rank.", "The order of events runs the other way."),
    ("the dominant male&rsquo;s colors come from his diet.", "Diet is not mentioned, and the changes followed social shifts."))
rec('inferences', 2,
    "Economic historians have observed that in several nineteenth-century port cities, the introduction of the telegraph was followed by a sharp narrowing of the gap between local grain prices and prices in distant markets. Before the telegraph, price information traveled by ship and could take weeks to arrive. Taken together, these facts imply that ______",
    Q_INF, ("faster price news let traders act on gaps between markets, pulling prices together.", "The telegraph sped up price news, and the gaps narrowed afterward."),
    ("the telegraph reduced the cost of shipping grain by sea, which lowered prices in distant markets.", "Shipping costs are not mentioned."),
    ("grain prices rose everywhere.", "The passage describes narrowing gaps, not rising levels."),
    ("traders stopped shipping grain once the telegraph let them buy and sell without moving goods.", "Grain still had to move; only information moved faster."))
rec('inferences', 2,
    "Ecologist Priya Raman compared two nearby islands. Island A has foxes, which eat seabirds and their eggs; Island B does not. Island B has dense, lush vegetation, while Island A is covered mostly in sparse grass. Raman notes that seabird droppings are rich in nutrients that fertilize soil. Raman&rsquo;s observations suggest that ______",
    Q_INF, ("foxes may limit plant growth on Island A by reducing the seabirds that fertilize it.", "Foxes reduce seabirds, and seabird droppings fertilize plants."),
    ("the foxes eat most of Island A&rsquo;s plants.", "Foxes eat seabirds and eggs, not plants."),
    ("seabirds avoid Island B&rsquo;s dense plants.", "The droppings on B suggest the birds are present there."),
    ("the islands get very different rainfall.", "Rainfall is not mentioned; the passage points to foxes and seabirds."))
rec('inferences', 2,
    "In a study, participants were shown a list of words and asked to remember them. One group was told the list would be tested the next day; the other was told there would be no test. Surprisingly, both groups recalled a similar number of words, but the group expecting a test reported feeling much more anxious. If these results hold, they would most directly suggest that ______",
    Q_INF, ("expecting a test may raise anxiety without improving recall.", "Recall was similar while anxiety differed."),
    ("anxiety about an upcoming test helps people remember more of the words they have studied.", "The anxious group did not remember more."),
    ("people cannot remember words that they do not expect to be tested on the following day.", "The no-test group remembered just as many."),
    ("word lists are a poor way to measure memory because people forget them quickly whatever they expect.", "The study does not question its measure."))
rec('inferences', 2,
    "Art historians have long dated an unsigned landscape painting to the 1640s based on its style. A recent analysis found that the painting&rsquo;s blue pigment is Prussian blue, a synthetic pigment that was first manufactured in the early 1700s. If the analysis is accurate, then ______",
    Q_INF, ("the painting, or at least its blue areas, cannot date from the 1640s.", "A pigment invented in the 1700s cannot appear in paint applied in the 1640s."),
    ("the painting was most likely made by a well-known artist of the 1640s who experimented with new pigments.", "The finding makes a 1640s date less likely, not an attribution more likely."),
    ("Prussian blue was in wide use by painters throughout the 1640s.", "It was first made in the early 1700s."),
    ("style cannot date paintings.", "The finding challenges one dating, not style as a method."))
rec('inferences', 2,
    "In one region, farmers who switched from plowing their fields to leaving crop residue on the surface found that their soil held more water. Yet their total harvests did not change during the first three years of the switch. Agronomist Chen Wei points out that the benefits of such soil changes often build up slowly, as organic matter accumulates. Chen&rsquo;s point implies that ______",
    Q_INF, ("flat yields in the first three years do not rule out later gains.", "Benefits build slowly, so early flat yields are not the final word."),
    ("leaving crop residue on fields reduces the soil&rsquo;s ability to hold water over time.", "The passage says soil held more water."),
    ("farmers should return to plowing their fields because the switch did not raise their harvests.", "Chen suggests patience, not a reversal."),
    ("organic matter in the soil does not affect crop yields, no matter how long it is allowed to accumulate.", "Chen implies it may improve them over time."))
rec('inferences', 2,
    "Researchers found that bumblebees trained to associate a particular shape with a sugar reward could later recognize that shape by touch alone in the dark, even though they had only ever seen it. Because recognizing an object across senses requires some internal representation of it, the researchers argue that ______",
    Q_INF, ("bumblebees may form mental representations of objects that are not tied to one sense.", "Cross-sense recognition implies a representation beyond sight alone."),
    ("bumblebees see better in the dark than in daylight, which let them find the shape they were trained on.", "They recognized the shape by touch, not sight."),
    ("sugar rewards are not needed to train bees.", "The bees were trained with sugar."),
    ("bumblebees rely mainly on touch rather than sight when they search for flowers in the wild.", "They learned the shape visually first, and wild foraging is not discussed."))
rec('inferences', 2,
    "In a long-running survey, the share of adults who said they read a printed newspaper daily fell steadily over two decades. Over the same period, the share who said they followed the news &ldquo;closely&rdquo; stayed about the same. Assuming both measures are accurate, the data suggest that ______",
    Q_INF, ("many adults likely switched to other news sources rather than following news less.", "Interest held steady while print reading fell, implying substitution."),
    ("adults became less interested in the news over the two decades as newspapers became harder to find.", "Interest stayed about the same."),
    ("printed newspapers became more expensive over the two decades, so fewer adults bought them.", "Price is not mentioned."),
    ("most adults never read printed newspapers, even at the start of the two decades the survey covered.", "The survey describes a decline, not a permanent absence."))

# =============================================================== RHETORICAL SYNTHESIS
# ---- easy
rs(0, ["The Great Wall of China is a series of fortifications.", "Parts of it were built more than 2,000 years ago.", "Its total length, including all branches, is about 21,000 kilometers.", "It was built to protect against invasions from the north."],
   "emphasize the wall&rsquo;s length",
   ("With all its branches, the Great Wall stretches about 21,000 kilometers.", "It states the length directly."),
   ("The Great Wall of China, a series of fortifications, was built to protect against invasions from the north.", "It gives what the wall is and why it was built, not its length."),
   ("Parts of the Great Wall of China, a series of fortifications, were built more than 2,000 years ago.", "It gives the age, not the length."),
   ("The Great Wall is a series of fortifications.", "It describes what the wall is, not how long it is."))
rs(0, ["Dr. Mae Jemison is an engineer and physician.", "In 1992, she became the first African American woman to travel to space.", "She flew aboard the space shuttle Endeavour.", "She later founded a technology company."],
   "state an achievement Jemison is known for",
   ("In 1992, Mae Jemison became the first African American woman in space.", "It names a notable first."),
   ("Mae Jemison, an engineer and physician, flew aboard the space shuttle Endeavour and later founded a company.", "It lists facts but omits the achievement she is known for."),
   ("Mae Jemison is an engineer and physician.", "It describes her training but not an achievement she is known for."),
   ("The space shuttle Endeavour carried astronauts, including engineers and physicians, into space.", "It is about the shuttle, not Jemison."))
rs(0, ["Tulips originally grew wild in Central Asia.", "They were brought to the Netherlands in the 1500s.", "The Netherlands now grows billions of tulip bulbs each year."],
   "explain where tulips originally came from",
   ("Tulips first grew wild in Central Asia.", "It states their origin."),
   ("The Netherlands, where tulips were brought in the 1500s, now grows billions of tulip bulbs each year.", "It describes their later history, not their origin."),
   ("Tulips were brought to the Netherlands in the 1500s.", "This is a later move, not where they came from."),
   ("Tulips are grown in many countries today, including the Netherlands.", "It does not identify their origin."))
rs(0, ["Hummingbirds can hover in place.", "Their wings beat up to 80 times per second.", "They feed on flower nectar.", "Some species migrate thousands of kilometers."],
   "explain how hummingbirds are able to hover",
   ("Hummingbirds hover by beating their wings up to 80 times per second.", "It connects hovering to the rapid wingbeats."),
   ("Hummingbirds, which can hover in place, feed on flower nectar, and some species migrate thousands of kilometers.", "It says that they hover but not how."),
   ("Some hummingbird species migrate thousands of kilometers.", "It is about migration."),
   ("Hummingbirds can hover in place.", "It states that they hover but not how."))
rs(0, ["The Lopez Library opened in 1962.", "It has 40,000 books.", "The Park Library opened in 2015.", "It has 12,000 books."],
   "contrast the two libraries&rsquo; ages",
   ("The Lopez Library opened in 1962, the Park Library in 2015.", "It compares the opening dates."),
   ("The Lopez Library has 40,000 books, while the newer Park Library has only 12,000 books.", "It contrasts collection size, not age."),
   ("The Park Library, which opened in 2015, has a collection of 12,000 books.", "It mentions only one library."),
   ("Both the Lopez Library and the Park Library lend books to the public.", "It states a similarity."))
rs(0, ["Volcanologist Kofi Mensah studies Mount Nyiragongo.", "The volcano is in the Democratic Republic of the Congo.", "It has one of the world&rsquo;s largest lava lakes.", "Mensah uses drones to measure gases above the lake."],
   "describe the method Mensah uses in his research",
   ("Mensah uses drones to measure gases above the volcano&rsquo;s lava lake.", "It describes how he does his research."),
   ("Mount Nyiragongo, in the Democratic Republic of the Congo, has one of the world&rsquo;s largest lava lakes.", "It describes the volcano, not the method."),
   ("Volcanologist Kofi Mensah studies Mount Nyiragongo, a volcano in the Democratic Republic of the Congo.", "It says what he studies but not how."),
   ("Mensah studies volcanoes.", "It gives no method."))
rs(0, ["Chess originated in India around the 6th century.", "It spread to Persia and then to Europe.", "The modern rules were settled in Europe around 1500."],
   "indicate how chess spread to Europe",
   ("From India, chess spread to Persia and then to Europe.", "It traces the route."),
   ("Chess originated in India around the 6th century, and its modern rules were settled in Europe around 1500.", "It gives the start and the rules but skips how it reached Europe."),
   ("The modern rules of chess were settled in Europe around 1500.", "It is about rules, not the route."),
   ("Chess, a game that originated in India around the 6th century, is more than 1,400 years old.", "It gives the origin and age but not how chess reached Europe."))
rs(0, ["Solar panels convert sunlight into electricity.", "Wind turbines convert moving air into electricity.", "Both produce electricity without burning fuel."],
   "emphasize a similarity between solar panels and wind turbines",
   ("Like wind turbines, solar panels make electricity without burning fuel.", "It states what they share."),
   ("Solar panels convert sunlight into electricity, while wind turbines convert moving air into electricity.", "It states a difference."),
   ("Wind turbines convert moving air into electricity.", "It describes only one technology."),
   ("Solar panels use sunlight.", "It describes only one technology."))
# ---- medium
rs(1, ["Sociologist Tanvi Rao studied public libraries in 12 cities.", "She surveyed more than 3,000 library visitors.", "Visitors most often cited free internet access as their reason for visiting.", "Borrowing books was the second most common reason."],
   "present the study&rsquo;s main finding",
   ("Rao found that visitors most often came to libraries for free internet access.", "It gives the main result."),
   ("In her study of public libraries in 12 cities, sociologist Tanvi Rao surveyed more than 3,000 library visitors.", "It describes the method, not the finding."),
   ("Borrowing books was the second most common reason that visitors gave for coming to the library in Rao&rsquo;s survey.", "It gives the secondary result, not the main one."),
   ("Tanvi Rao is a sociologist who studies libraries.", "It is background."))
rs(1, ["The axolotl is a salamander native to lakes near Mexico City.", "It can regrow lost limbs.", "It can also regrow parts of its heart and brain.", "Scientists study it to learn about tissue regeneration."],
   "explain why scientists study the axolotl",
   ("Because it can regrow limbs and parts of its heart and brain, the axolotl is studied to learn about tissue regeneration.", "It links its abilities to the reason for study."),
   ("The axolotl, a salamander native to lakes near Mexico City, can regrow lost limbs and parts of its heart and brain.", "It gives abilities but not why scientists study it."),
   ("The axolotl is a salamander native to lakes near Mexico City.", "It identifies the animal but gives no reason for study."),
   ("Scientists study many salamanders.", "It is general and not about the axolotl."))
rs(1, ["Bridge A is 300 meters long and was completed in 1932.", "Bridge B is 1,200 meters long and was completed in 1998.", "Both bridges cross the same river."],
   "compare the lengths of the two bridges",
   ("At 1,200 meters, Bridge B is four times as long as 300-meter Bridge A.", "It compares the lengths directly and precisely."),
   ("Bridge A was completed in 1932, and Bridge B, which crosses the same river, was completed in 1998.", "It compares completion dates."),
   ("Both bridges cross the same river, though Bridge A was completed decades earlier.", "It states a similarity and a date difference, not length."),
   ("Bridge B, completed in 1998, is 1,200 meters long and crosses the river.", "It gives one length without comparison."))
rs(1, ["A 2021 study tested a reading program in 40 schools.", "Half the schools used the program; half did not.", "Students in program schools gained more in reading scores.", "The gains were largest for students who began with the lowest scores."],
   "emphasize which students benefited most from the program",
   ("The program helped most the students who started with the lowest scores.", "It identifies the group with the largest gains."),
   ("In a 2021 study of 40 schools, students in schools that used the reading program gained more in reading scores.", "It gives the overall result, not the group that benefited most."),
   ("A 2021 study tested a reading program in 40 schools, half of which used the program and half of which did not.", "It describes the design."),
   ("The program was tested in 40 schools.", "It describes the study, not who benefited."))
rs(1, ["Octavia Butler was an American science fiction writer.", "Her novel <i>Kindred</i> (1979) combines time travel with the history of slavery.", "Her <i>Parable</i> novels depict a future shaped by climate change and inequality.", "In 1995 she became the first science fiction writer to receive a MacArthur Fellowship."],
   "describe the range of subjects in Butler&rsquo;s fiction",
   ("Butler wrote about slavery&rsquo;s history in <i>Kindred</i> and a climate-changed future in her <i>Parable</i> novels.", "It gives two contrasting subjects to show range."),
   ("In 1995, American science fiction writer Octavia Butler became the first science fiction writer to receive a MacArthur Fellowship.", "It describes an honor, not subjects."),
   ("Octavia Butler was an American science fiction writer.", "It identifies her but does not describe subjects."),
   ("Butler&rsquo;s <i>Kindred</i>, published in 1979, combines time travel with the history of slavery.", "It gives only one subject, which does not show range."))
rs(1, ["Coral reefs cover less than 1% of the ocean floor.", "About 25% of marine species live on or near reefs.", "Warming water can cause corals to bleach and die."],
   "emphasize how important reefs are to ocean life relative to their size",
   ("Reefs cover under 1% of the ocean floor yet support about 25% of marine species.", "It sets their small area against the large share of species."),
   ("Warming water can cause corals to bleach and die, threatening the reefs that cover less than 1% of the ocean floor.", "It describes a threat, not importance relative to size."),
   ("About 25% of marine species live on or near coral reefs, which warming water can cause to bleach.", "It omits the size comparison."),
   ("Coral reefs, which warming water can cause to bleach and die, cover less than 1% of the ocean floor.", "It gives size but not importance."))
rs(1, ["The Harvey Street community fridge opened in 2020.", "Neighbors stock it with fresh food.", "Anyone can take food at any time.", "It is cleaned daily by volunteers."],
   "explain how the fridge works to an audience unfamiliar with it",
   ("Neighbors stock the Harvey Street fridge with fresh food that anyone can take at any time.", "It explains who stocks it and who can use it."),
   ("The Harvey Street community fridge, which opened in 2020, is cleaned every day by a group of volunteers.", "It gives a date and a maintenance detail, not how the fridge works."),
   ("The Harvey Street community fridge opened in 2020.", "It gives a date, not how it works."),
   ("Community fridges have become common in many cities.", "It is general and not about how this fridge works."))
rs(1, ["Engineer Lars Holm designed a floating solar farm.", "It sits on a reservoir in Norway.", "The water cools the panels.", "Cooler panels produce more electricity than hot ones."],
   "explain an advantage of placing solar panels on water",
   ("Water cools the panels, and cooler panels produce more electricity.", "It connects the water&rsquo;s cooling to higher output."),
   ("Engineer Lars Holm designed a floating solar farm that sits on a reservoir in Norway.", "It describes the project, not an advantage."),
   ("Cooler solar panels produce more electricity than hot ones do.", "It states a general fact without connecting it to the water."),
   ("The farm floats on a reservoir.", "It gives only the location."))
# ---- hard
rs(2, ["A 2019 study tracked 2,000 adults for ten years.", "Participants who walked at least 7,000 steps a day had a lower risk of early death.", "Walking more than 10,000 steps a day brought little additional benefit.", "The study was observational, not a controlled experiment."],
   "present the study&rsquo;s findings while acknowledging a limitation",
   ("Walking 7,000 or more steps a day was linked to lower risk of early death, though the observational design limits causal claims.", "It gives the finding and notes the limitation."),
   ("Because the 2019 study of 2,000 adults was observational rather than a controlled experiment, its findings about walking and early death are meaningless.", "It overstates the limitation and omits the findings."),
   ("Walking at least 7,000 steps a day lowers the risk of early death, and walking more than 10,000 steps brings little additional benefit.", "It presents the findings as proven causes and omits the limitation."),
   ("A 2019 study tracked 2,000 adults for ten years.", "It describes the design only."))
rs(2, ["Historian Yusuf Adeyemi studied trade records from the medieval city of Timbuktu.", "The records list manuscripts among the city&rsquo;s most valuable imports.", "Scholars in the city copied and sold manuscripts.", "Some families preserved manuscripts for centuries."],
   "support the claim that manuscripts played an important role in Timbuktu&rsquo;s economy",
   ("Manuscripts ranked among Timbuktu&rsquo;s most valuable imports, and local scholars copied and sold them.", "It gives economic evidence: valuable imports and a local trade."),
   ("Historian Yusuf Adeyemi studied trade records from Timbuktu, where some families preserved manuscripts for centuries.", "Preservation shows value to families but not an economic role."),
   ("Some families in Timbuktu preserved their manuscripts for centuries.", "It does not address the economy."),
   ("Many medieval cities traded in manuscripts, and some of the most valuable passed through Timbuktu&rsquo;s markets.", "It is general, and the claim about markets is not in the notes."))
rs(2, ["Species A of fern reproduces mainly by spores.", "Species B reproduces mainly by spreading underground stems.", "In a burned forest, Species B regrew within one season.", "Species A took three seasons to reappear."],
   "suggest a possible reason for the difference in how quickly the two species recovered after the fire",
   ("Species B, spreading by underground stems that may have survived the fire, regrew in one season; spore-dependent Species A took three.", "It links each reproductive strategy to its recovery time."),
   ("After the fire, Species B regrew within one season, while Species A, a fern of the same forest, took three full seasons to reappear.", "It states the difference but offers no reason."),
   ("Species A reproduces mainly by spores, and Species B reproduces mainly by spreading underground stems.", "It states the strategies without connecting them to recovery."),
   ("Species A and Species B, which reproduce in different ways, both eventually returned to the forest after the fire.", "It notes the different strategies but does not link them to the different recovery times."))
rs(2, ["Architect Helena Voss designed the Linden Housing Cooperative.", "Its apartments share a large central kitchen and garden.", "Voss argues that shared spaces reduce isolation.", "A resident survey found that 78% knew most of their neighbors by name."],
   "present evidence that supports Voss&rsquo;s argument",
   ("At Linden, with its shared kitchen and garden, 78% of surveyed residents knew most neighbors by name.", "It pairs the shared spaces with evidence of connection among residents."),
   ("Architect Helena Voss, who designed the Linden Housing Cooperative, argues that shared spaces such as kitchens and gardens reduce isolation.", "It restates the argument without evidence."),
   ("Helena Voss designed the Linden Housing Cooperative.", "It is background."),
   ("The Linden Housing Cooperative&rsquo;s apartments share a large central kitchen and garden that residents use.", "It describes the design but gives no evidence of reduced isolation."))
rs(2, ["Researchers compared two methods of teaching fractions.", "Method 1 used number lines; Method 2 used pie diagrams.", "Students taught with number lines scored higher on tests of comparing fractions.", "Both groups scored about the same on tests of adding fractions."],
   "summarize the results in a way that avoids overstating the advantage of either method",
   ("Number lines helped more with comparing fractions; for adding fractions, the methods were about equal.", "It reports the specific advantage and the area where there was none."),
   ("Because students taught with number lines scored higher on tests of comparing fractions, number lines are the better way to teach fractions.", "It overgeneralizes one result to all fraction skills."),
   ("Pie diagrams are no longer useful.", "Nothing in the notes supports this."),
   ("Students who were taught with number lines instead of pie diagrams scored higher on tests of comparing fractions.", "It reports only the advantage, which overstates it."))
rs(2, ["The 1918 influenza pandemic infected about a third of the world&rsquo;s population.", "Unusually, it caused high death rates among healthy young adults.", "Most influenza strains are deadliest for the very young and the very old.", "Scientists still debate why the 1918 strain affected young adults so severely."],
   "emphasize what made the 1918 pandemic unusual",
   ("Unlike most flu strains, deadliest for the very young and old, the 1918 strain killed many healthy young adults.", "It contrasts the 1918 pattern with the usual one."),
   ("The 1918 influenza pandemic infected about a third of the world&rsquo;s population, and scientists still debate aspects of it today.", "It shows scale but not what was unusual about the victims."),
   ("Scientists still debate why the 1918 strain, which infected about a third of the world&rsquo;s population, hit young adults so hard.", "It mentions the debate but not the contrast with typical strains."),
   ("Most influenza strains are deadliest for the very young and the very old, as many studies have shown over the past century.", "It describes typical strains only, and the added claim is not in the notes."))
rs(2, ["The poet Gwendolyn Brooks won the Pulitzer Prize in 1950.", "She was the first African American writer to win a Pulitzer.", "Her early poems portray daily life in Chicago&rsquo;s Bronzeville neighborhood.", "In later work, she wrote more directly about civil rights."],
   "describe a change in Brooks&rsquo;s work over time",
   ("Brooks moved from portraying daily life in Bronzeville to writing more directly about civil rights.", "It contrasts the early and later focus."),
   ("In 1950, Gwendolyn Brooks became the first African American writer to win a Pulitzer Prize, an honor she received for her poetry.", "It gives an honor, not a change in her work."),
   ("Brooks&rsquo;s early poems portray daily life in Chicago&rsquo;s Bronzeville neighborhood.", "It describes only the early work."),
   ("Brooks won the Pulitzer Prize in 1950.", "It gives an honor and date, not a change."))
rs(2, ["Biologist Ana Silva studied tree frogs in Costa Rica.", "Frogs in noisy areas near waterfalls call at higher pitches.", "Frogs in quiet forest areas call at lower pitches.", "Silva hypothesizes that higher calls are easier to hear over the low roar of waterfalls."],
   "present Silva&rsquo;s hypothesis along with the observation it explains",
   ("Frogs near waterfalls call higher, which Silva thinks helps them be heard over the low roar.", "It pairs the observation with the proposed explanation."),
   ("In Silva&rsquo;s study of Costa Rican tree frogs, frogs in noisy areas near waterfalls called at higher pitches than frogs in quiet forest areas.", "It gives the observation without the hypothesis."),
   ("Biologist Ana Silva studied how the calls of tree frogs in Costa Rica differ between noisy and quiet areas.", "It is background only."),
   ("Higher calls are easier to hear over the low roar of waterfalls, according to biologist Ana Silva&rsquo;s hypothesis.", "It gives the idea but not the observation it explains."))

# =============================================================== CROSS-TEXT CONNECTIONS (hard)
rec('cross_text', 2,
    two("Economist Rafael Ortiz argues that remote work lowers productivity because workers lose the informal conversations that spread ideas in an office.",
        "A study of software teams found that remote workers completed as many tasks as office workers but proposed fewer new ideas in meetings. The researchers suggest that remote work may affect innovation more than routine output."),
    Q_X, ("By suggesting that Ortiz&rsquo;s concern applies to new ideas more than to overall productivity.", "Text 2 finds equal task output but fewer new ideas."),
    ("By agreeing that remote workers complete fewer tasks than office workers because they miss informal conversations.", "Text 2 found they completed as many tasks."),
    ("By claiming that informal conversations in the office have little or no effect on how many new ideas workers propose.", "Text 2 suggests the opposite."),
    ("By recommending that software teams return to the office so that workers can share ideas in meetings again.", "Text 2 makes no recommendation."))
rec('cross_text', 2,
    two("Many museum curators hold that artifacts should be displayed in the countries where they were found, so that local communities can connect with their own history.",
        "Curator Dana Whitfield agrees that local access matters, but she notes that some artifacts require climate-controlled storage that not every museum can provide. For such objects, she proposes long-term loans and digital replicas as a temporary compromise until facilities improve."),
    Q_REL, ("Text 2 accepts Text 1&rsquo;s principle but raises a practical obstacle and a workaround.", "Whitfield agrees on local access but notes storage limits and proposes loans and replicas."),
    ("Text 2 rejects the principle in Text 1, arguing that artifacts are best kept in museums with climate-controlled storage.", "Whitfield agrees that local access matters."),
    ("Text 2 argues that digital replicas are more useful to local communities than the original artifacts would be.", "Replicas are a temporary compromise, not a superior option."),
    ("Text 2 lists several artifacts that have been returned to their countries of origin in recent years.", "No such examples are given."))
rec('cross_text', 2,
    two("Some ecologists argue that removing invasive species from islands almost always benefits native wildlife.",
        "On one Pacific island, eradicating invasive rats led to a sharp rise in an invasive plant whose seeds the rats had been eating. Native seabirds recovered, but native plants were crowded out. Ecologist Mele Tupou argues that eradication plans should account for how invasive species interact with one another."),
    Q_X, ("By suggesting that removing one invasive species can cause unexpected harm, so benefits are not automatic.", "Removing rats helped seabirds but let an invasive plant spread."),
    ("By agreeing that removing invasive species benefits every native species, as the recovery of the island&rsquo;s seabirds shows.", "Native plants were harmed in Text 2&rsquo;s example."),
    ("By arguing that invasive rats should be left on islands because they control invasive plants.", "Tupou calls for better planning, not leaving rats in place."),
    ("By calling the seabirds invasive.", "Text 2 calls them native."))
rec('cross_text', 2,
    two("Art critic Lionel Graves contends that photographs cannot be art in the fullest sense because a camera, not the photographer&rsquo;s hand, produces the image.",
        "Photographer Ruth Amani spends hours choosing a vantage point, waiting for light, and deciding what to leave out of the frame. In her view, these decisions shape the image as surely as a painter&rsquo;s brushstrokes do; the camera records, but the photographer composes."),
    Q_X, ("By arguing that a photographer&rsquo;s choices, not the camera, make a photograph art.", "Amani locates artistry in composition decisions."),
    ("By agreeing that the camera does most of the creative work, though photographers still choose what to photograph.", "Amani stresses that the photographer composes."),
    ("By claiming that painting requires less skill than photography because painters do not have to wait for the right light.", "She compares the two but does not rank them."),
    ("By conceding that photographs are not art in the fullest sense because cameras produce the images.", "Amani disputes Graves&rsquo;s view."))
rec('cross_text', 2,
    two("A number of nutrition studies have reported that people who drink coffee live longer on average than people who do not, leading some commentators to recommend coffee for its health benefits.",
        "Epidemiologist Sunil Mehra notes that people who are already seriously ill often give up coffee. If so, the non-drinker group would contain more ill people, which could make coffee drinkers appear healthier even if coffee itself has no effect."),
    Q_X, ("By suggesting the results could reflect who quits coffee rather than an effect of coffee.", "Mehra offers a reverse-causation explanation."),
    ("By providing new evidence that coffee shortens the lives of people who are already seriously ill.", "Mehra offers an alternative explanation, not new evidence of harm."),
    ("By agreeing that people should drink coffee to live longer, as long as they are not seriously ill.", "He questions that recommendation."),
    ("By arguing that the studies measured coffee drinking inaccurately because people misreport how much they drink.", "He questions the interpretation, not the measurement."))
rec('cross_text', 2,
    two("Historian Clara Novak argues that the spread of cheap printed pamphlets in seventeenth-century England played a decisive role in turning ordinary people against the king.",
        "Pamphlets certainly circulated widely, but many were read aloud in taverns and marketplaces to people who could not read. Historian Ibrahim Sule argues that the social settings in which pamphlets were shared, rather than the printed texts alone, shaped how their ideas spread."),
    Q_REL, ("Text 2 accepts that pamphlets circulated widely but stresses how they were shared.", "Sule agrees on circulation but emphasizes social reading settings."),
    ("Text 2 denies that pamphlets circulated widely, arguing that most people in the period could not read them.", "It says they certainly circulated widely."),
    ("Text 2 argues that the king supported the printing of pamphlets as a way to reach people in taverns and marketplaces.", "The king&rsquo;s view is not discussed."),
    ("Text 2 says most people could read.", "It suggests many could not."))
rec('cross_text', 2,
    two("Neuroscientist Jae Kim claims that learning to play a musical instrument in childhood improves general intelligence, citing studies in which children who took music lessons scored higher on intelligence tests than those who did not.",
        "In an experiment that randomly assigned children to music lessons, drama lessons, or no lessons, psychologist Nora Heller found only small differences in later intelligence scores. Heller notes that families who choose music lessons often differ from other families in ways that could also affect test scores."),
    Q_X, ("By suggesting Kim&rsquo;s evidence may reflect family differences rather than music lessons.", "Heller&rsquo;s randomized experiment found small effects and points to family differences."),
    ("By agreeing that music lessons greatly increase intelligence, especially when children begin them early in life.", "Heller found only small differences."),
    ("By arguing that drama lessons improve children&rsquo;s intelligence scores more than music lessons do.", "No such ranking is claimed."),
    ("By rejecting intelligence tests.", "She does not question the tests."))
rec('cross_text', 2,
    two("Some urban planners argue that building more highway lanes is the most effective way to reduce traffic congestion.",
        "Transportation researcher Amy Lindgren analyzed decades of data from U.S. metropolitan areas and found that when highway capacity grew, the total miles driven grew in nearly equal proportion, leaving congestion largely unchanged. She attributes this to &ldquo;induced demand&rdquo;: new capacity attracts new trips."),
    Q_X, ("By showing that new lanes tend to fill with new driving, so they do not reliably ease congestion.", "Driving grew in proportion to capacity."),
    ("By agreeing that more lanes reduce congestion, provided that cities build them in the most crowded metropolitan areas.", "Her data suggest added lanes do not reduce congestion."),
    ("By arguing that highways should be closed.", "She makes no such proposal."),
    ("By claiming that congestion has largely disappeared in U.S. metropolitan areas that added highway lanes.", "She says congestion was largely unchanged."))
