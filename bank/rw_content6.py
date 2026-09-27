"""Authored Reading & Writing items, part 6 (original text; researchers and characters are fictional).
Command of evidence (textual) and inferences: 8 more per difficulty. Loaded after part 5 so older uids never shift.
Distractors are written to be as long and specific as the key (see tests/rw_quality.py)."""
from bank.rw_content import rec, Q_SUP, Q_WEAK, Q_INF
from bank.rw_content2 import Q_QUOTE

# =============================================================== COMMAND OF EVIDENCE: TEXTUAL
# ---- easy
rec('coe_textual', 0,
    "A student hypothesizes that tomato plants grow taller when they receive more hours of light each day.",
    Q_SUP, ("Plants given 14 hours of light a day grew taller than identical plants given 8 hours.", "It compares light hours and finds taller growth with more light."),
    ("Tomato plants given 14 hours of light a day needed to be watered more often than plants given 8 hours.", "Watering is not height."),
    ("Tomato plants grew taller in the student&rsquo;s garden than in her neighbor&rsquo;s garden down the street.", "Light hours are not compared."),
    ("The plants in both groups produced ripe red tomatoes by the end of July, as the student expected.", "Fruit color says nothing about light and height."))
rec('coe_textual', 0,
    "A coach claims that stretching before practice reduces the number of muscle injuries her runners suffer.",
    Q_SUP, ("During a season when the team stretched before every practice, muscle injuries fell by half.", "Fewer injuries followed the stretching."),
    ("The runners said they enjoyed stretching.", "Enjoyment does not show fewer injuries."),
    ("The team won more races during the season when the runners began stretching before every practice.", "Winning races is not the same as avoiding injuries."),
    ("Runners on other teams in the league stretched after practice rather than before it began each day.", "Other teams&rsquo; habits do not test the claim."))
rec('coe_textual', 0,
    "A town council member claims that the new crosswalk signals on Grant Avenue have made the street safer for people walking.",
    Q_WEAK, ("Accidents involving people on foot on Grant Avenue rose after the signals were installed.", "More accidents would undercut the claim of greater safety."),
    ("The signals cost less than the council had budgeted for the project, and they were installed ahead of schedule.", "Cost does not bear on safety."),
    ("Drivers on Grant Avenue said the new signals were easy to see, even at night and in the rain.", "Easy-to-see signals would tend to support the claim."),
    ("Other streets in town also have crosswalk signals, some of which were installed many years ago.", "Other streets do not test this claim."))
rec('coe_textual', 0,
    "The following text is from a 1908 novel.<br><br>In the novel, Grandfather Pell is described as a man who never wastes anything.",
    Q_QUOTE, ("&ldquo;He saved bent nails in a jar, straightening each one with a hammer when the jar was full.&rdquo;", "Saving and reusing bent nails shows he wastes nothing."),
    ("&ldquo;He rose before dawn every morning, winter and summer, and was in the fields before the sun.&rdquo;", "This shows hard work, not thrift."),
    ("&ldquo;He told the same three stories at every supper.&rdquo;", "This does not concern wasting things."),
    ("&ldquo;He was known across the county for the size of his pumpkins and the loudness of his laugh.&rdquo;", "Neither detail concerns wasting things."))
rec('coe_textual', 0,
    "A researcher claims that crows can recognize individual human faces.",
    Q_SUP, ("Crows scolded a person in a mask they had seen trap crows, but ignored people wearing other masks.", "Reacting to one face but not others shows recognition."),
    ("Crows often gather in large groups in city parks during the winter months.", "Group behavior does not show face recognition."),
    ("Crows can live for more than ten years in the wild.", "Life span does not bear on recognition."),
    ("Crows ate more peanuts from feeders placed near trees than from feeders placed in open grassy areas.", "Feeding preferences do not show face recognition."))
rec('coe_textual', 0,
    "A school principal claims that starting the school day later helps students arrive on time.",
    Q_SUP, ("After the start time moved from 7:30 to 8:30, late arrivals fell from 60 a week to 20.", "Fewer late arrivals after the later start supports the claim."),
    ("Students said they liked the later start.", "Liking the change does not show punctuality."),
    ("After the start time moved later, the school day ended an hour later as well, at 3:30 instead of 2:30.", "The end time does not show whether students arrived on time."),
    ("Teachers at the school reported that they drank less coffee in the mornings after the start time changed.", "Teachers&rsquo; habits do not test the claim."))
rec('coe_textual', 0,
    "A gardener claims that marigolds planted near vegetables keep insects away from the vegetables.",
    Q_WEAK, ("Beds with and without marigolds had about the same number of insects on their vegetables.", "No difference in insects undercuts the claim."),
    ("Marigolds are bright orange and yellow flowers that bloom from early summer until the first frost.", "Color and bloom time do not bear on insects."),
    ("Vegetables planted near marigolds had fewer insect holes in their leaves than vegetables planted alone.", "This would support the claim."),
    ("Marigolds grow easily from seed.", "Ease of growing does not bear on the claim."))
rec('coe_textual', 0,
    "The following text is from a 1911 story.<br><br>In the story, Nora is shown to be braver than her older brother.",
    Q_QUOTE, ("&ldquo;When the dog growled at the gate, her brother ran, but Nora walked right up and offered it her hand.&rdquo;", "She approaches the dog while her brother flees."),
    ("&ldquo;Nora and her brother walked to school together every morning along the river road.&rdquo;", "This shows no difference in bravery."),
    ("&ldquo;Her brother was two years older and a full head taller.&rdquo;", "Age and height are not bravery."),
    ("&ldquo;Nora liked arithmetic best of all her subjects, while her brother preferred reading and history.&rdquo;", "School preferences are not bravery."))
# ---- medium
rec('coe_textual', 1,
    "Ecologist Imani Waweru hypothesizes that elephants avoid farms guarded by beehive fences because they fear bee stings.",
    Q_SUP, ("Elephants retreated from speakers playing buzzing bees but not from speakers playing white noise.", "The elephants respond to bee sounds specifically, suggesting fear of bees."),
    ("Farms guarded by beehive fences produced honey that farmers sold at local markets for extra income.", "Honey sales do not explain elephant behavior."),
    ("Elephants raided farms without beehive fences mainly at night, when fewer people were in the fields.", "Timing of raids does not show fear of bees."),
    ("Some fences failed when bees left their hives during dry seasons.", "This shows fences can fail, but not why they work."))
rec('coe_textual', 1,
    "Historian Tariq Haddad claims that a nineteenth-century map of the city was drawn from firsthand surveys rather than copied from earlier maps.",
    Q_SUP, ("It records several streets built the year before it was published, which appear on no earlier map.", "Recent streets absent from older maps show new observation."),
    ("The map was printed in color, which was unusual for maps of the city made in the nineteenth century.", "Printing method does not show how the map was drawn."),
    ("The map reproduces an error in the river&rsquo;s course found on a map made fifty years earlier.", "A copied error would suggest copying, weakening the claim."),
    ("The map was sold by subscription.", "How it was sold does not bear on how it was drawn."))
rec('coe_textual', 1,
    "Nutrition researcher Hana Kim claims that eating breakfast improves students&rsquo; attention during morning classes.",
    Q_WEAK, ("When some students were randomly given breakfast, their attention matched that of students given none.", "A controlled comparison found no effect, which weakens the claim."),
    ("Students who ate breakfast reported feeling less hungry during their morning classes than those who skipped it.", "Less hunger is consistent with the claim."),
    ("Most students surveyed said that they ate breakfast at home.", "Where they ate does not test the claim."),
    ("Students who ate breakfast scored higher on attention tests, and the gap was largest among the youngest students.", "This would support the claim."))
rec('coe_textual', 1,
    "The following text is from a 1914 novel.<br><br>In the novel, the narrator suggests that Mr. Lacey is more concerned with appearing generous than with being generous.",
    Q_QUOTE, ("&ldquo;He gave to every charity that printed its donors&rsquo; names, and to none that did not.&rdquo;", "His giving depends on public credit, not on generosity itself."),
    ("&ldquo;Mr. Lacey gave large sums each year to the hospital, the library, and the orphans&rsquo; home.&rdquo;", "This shows giving but not a concern with appearances."),
    ("&ldquo;He was a tall man with a loud voice who liked to tell stories about his early years in business.&rdquo;", "This does not concern generosity."),
    ("&ldquo;Mr. Lacey&rsquo;s fortune came from the cotton mills his father had built along the river.&rdquo;", "The source of his money is not the point."))
rec('coe_textual', 1,
    "Marine biologist Sofia Reyes claims that coral reefs protected from fishing recover faster after storms than reefs where fishing is allowed.",
    Q_SUP, ("Five years after a hurricane, coral cover had regrown twice as much on protected reefs as on fished ones.", "Faster regrowth on protected reefs supports the claim."),
    ("Protected reefs attracted more divers and snorkelers than fished reefs in the years before the hurricane.", "Visitor numbers do not measure recovery."),
    ("Both protected and fished reefs lost about the same share of their coral during the hurricane.", "Equal damage says nothing about the speed of recovery."),
    ("Fishing boats stayed in port during the hurricane.", "This does not compare how reefs recovered."))
rec('coe_textual', 1,
    "Psychologist Omar Farouk hypothesizes that people are more likely to finish a task if they write down a specific time and place for doing it.",
    Q_SUP, ("People who wrote down when and where they would exercise completed more workouts than others.", "The planners followed through more often."),
    ("People who wrote down plans for their tasks said the writing took less than two minutes to complete.", "Time spent writing does not show follow-through."),
    ("People who exercised in the morning finished more workouts than people who exercised in the evening.", "Time of day was not the variable tested."),
    ("Most people forgot tasks that were not written down anywhere, whether on paper or in a phone reminder.", "This does not test specific time-and-place plans."))
rec('coe_textual', 1,
    "Urban planner Kwame Asante claims that planting street trees lowers summer air temperatures in city neighborhoods.",
    Q_WEAK, ("Neighborhoods that planted many trees stayed as hot as similar ones that planted none, even years later.", "No temperature difference weakens the claim."),
    ("Residents of neighborhoods with more street trees reported that they enjoyed walking outside more often.", "Enjoyment of walking does not measure temperature."),
    ("Street trees absorb sunlight that would otherwise heat pavement and release water vapor that cools the air.", "This explains how the claim could be true."),
    ("Some street trees were damaged in storms.", "Damage to some trees does not test the claim."))
rec('coe_textual', 1,
    "The following text is from a 1921 poem. The speaker describes an old house.<br><br>The speaker suggests that the house holds memories of the people who once lived there.",
    Q_QUOTE, ("&ldquo;The stair still creaks where the children ran, / And the doorframe keeps their heights in pen.&rdquo;", "The creaking stair and pen marks keep traces of the children."),
    ("&ldquo;The roof is slate and the walls are stone, / And the chimney leans toward the western hill.&rdquo;", "This describes the house but not memories of its people."),
    ("&ldquo;The wind comes in at the broken pane.&rdquo;", "This shows decay, not memories of people."),
    ("&ldquo;A new family moved in last May, / With a gray cat and a piano that no one plays.&rdquo;", "This concerns new residents, not memories of earlier ones."))
# ---- hard
rec('coe_textual', 2,
    "Some linguists argue that a certain ancient script recorded a spoken language rather than serving only as a set of symbols for goods and numbers. Epigrapher Lena Moreau supports this view.",
    Q_SUP, ("Some signs spell foreign personal names by sound, as a script recording speech would need.", "Spelling names by sound implies the signs stood for spoken sounds."),
    ("Most surviving examples of the script appear on clay tablets that list quantities of grain and livestock.", "This fits the view that the script recorded only goods and numbers."),
    ("The script&rsquo;s symbols changed shape gradually over several centuries as scribes began using new tools.", "Changes in shape do not show whether it recorded speech."),
    ("The script was used in several cities.", "Wide use does not show it recorded speech."))
rec('coe_textual', 2,
    "A study found that hospitals that hired more nurses per patient had lower patient death rates. The study&rsquo;s authors concluded that higher nurse staffing saves lives.",
    Q_WEAK, ("The better-staffed hospitals mostly treated less seriously ill patients than the other hospitals did.", "Differences in patients, not staffing, could explain the lower death rates."),
    ("Nurses at the better-staffed hospitals reported higher job satisfaction than nurses at the other hospitals.", "Satisfaction does not undercut the link to patient deaths."),
    ("The study included hospitals in both large cities and small towns across several different regions.", "Broad coverage, if anything, strengthens the study."),
    ("Nurse staffing levels rose at many hospitals after the study was published.", "Later changes do not bear on the study&rsquo;s reasoning."))
rec('coe_textual', 2,
    "Art historian Mei Tanaka argues that the painter Hugo Brandt deliberately left some of his late canvases unfinished, rather than being prevented by illness from completing them.",
    Q_SUP, ("Brandt signed and sold several of the unfinished late canvases.", "Signing and selling them suggests he considered them complete."),
    ("Brandt&rsquo;s illness grew worse during his final years, and he painted less often than before.", "This supports the illness explanation instead."),
    ("Brandt&rsquo;s early canvases were all highly finished, with smooth surfaces and precise detail.", "Early finish does not show intent in the late works."),
    ("Several of Brandt&rsquo;s students later painted in a similar unfinished style after his death.", "Students&rsquo; choices do not show Brandt&rsquo;s intent."))
rec('coe_textual', 2,
    "The following text is adapted from a 1912 novel.<br><br>In the novel, the narrator portrays Mr. Whitcombe as someone who confuses being busy with being useful.",
    Q_QUOTE, ("&ldquo;He answered every letter the day it came and considered this his chief service to the firm, though the answers settled nothing.&rdquo;", "His prompt but useless replies show busyness taken for usefulness."),
    ("&ldquo;Mr. Whitcombe arrived at the office at eight each morning and did not leave until the lamps were lit.&rdquo;", "Long hours alone do not show confusion about usefulness."),
    ("&ldquo;The clerks respected him.&rdquo;", "This does not concern his busyness or usefulness."),
    ("&ldquo;He had been with the firm for thirty years and could recall the name of every client it had ever lost.&rdquo;", "His memory for lost clients does not show the confusion."))
rec('coe_textual', 2,
    "Ecologist Aiyana Redcloud hypothesizes that wolves returning to a valley have allowed streamside willows to recover by making elk avoid the riverbanks, where elk had browsed heavily.",
    Q_SUP, ("Willows recovered most where elk grazing fell most, at spots with poor views of wolves.", "Recovery tracks the places elk now avoid, linking willows to wolves."),
    ("Elk numbers across the valley fell by about half in the years after wolves returned to the area.", "Fewer elk could explain recovery without avoidance of riverbanks."),
    ("Willows grew faster in years with heavy snow, which raised stream levels the following spring.", "Snow gives a rival explanation for recovery."),
    ("Wolves in the valley hunted mainly at dawn.", "Hunting times do not link willows to elk avoidance."))
rec('coe_textual', 2,
    "Economist Diego Salas claims that a city&rsquo;s new minimum wage did not reduce employment at restaurants, since the number of restaurant jobs in the city grew in the year after the wage increase.",
    Q_WEAK, ("Restaurant jobs grew three times faster over the same year in similar nearby cities that kept the old wage.", "Slower growth than comparable cities suggests the wage may have held jobs back."),
    ("Several new restaurants opened in the city during the year after the minimum wage increase took effect.", "New openings fit the claim that employment did not fall."),
    ("Restaurant workers in the city reported that their pay rose after the increase.", "Higher pay is the intended effect and does not bear on employment."),
    ("Surveys found that most restaurant owners in the city opposed the new minimum wage before it took effect.", "Owners&rsquo; opinions do not show what happened to jobs."))
rec('coe_textual', 2,
    "The following text is adapted from a 1916 essay.<br><br>The essayist claims that old customs often survive long after people have forgotten their purpose.",
    Q_QUOTE, ("&ldquo;We still shake hands, though none of us now needs to prove that he carries no sword.&rdquo;", "A custom survives though its original purpose is gone."),
    ("&ldquo;Every generation believes that its own customs are more sensible than those of its grandparents.&rdquo;", "This concerns attitudes toward customs, not forgotten purposes."),
    ("&ldquo;New customs appear quickly.&rdquo;", "This concerns new customs, not surviving old ones."),
    ("&ldquo;A custom that serves no purpose will be abandoned within a generation, as a matter of course.&rdquo;", "This contradicts the claim."))
rec('coe_textual', 2,
    "Biologist Noor Rahman claims that a species of lizard on a small island evolved larger heads and stronger bites within a few decades after it was introduced there, allowing it to eat the tough plants that are common on the island.",
    Q_SUP, ("The lizards&rsquo; heads grew larger over several generations, and gut studies showed they now digested tough plants.", "Heritable head changes plus a matching diet support the claim."),
    ("The island&rsquo;s tough plants grew more abundant over the same decades because of a change in rainfall.", "A change in plants does not show the lizards evolved."),
    ("Lizards on the island ate mostly insects during their first few years there, as they had on the mainland.", "An early insect diet does not show later evolution."),
    ("Larger lizards defended bigger territories.", "Territory size does not bear on heads, bites, or diet."))

# =============================================================== INFERENCES
# ---- easy
rec('inferences', 0,
    "Leo&rsquo;s class planted bean seeds in two trays. They watered both trays the same amount, but they put one tray in a dark closet and the other on a sunny windowsill. After two weeks, the beans on the windowsill were tall and green, while the beans in the closet were short and pale. The class concluded that ______",
    Q_INF, ("the bean plants needed light to grow well.", "Light was the only difference between the trays."),
    ("the closet had been too cold for the beans, since cold air slows the growth of bean plants.", "Temperature is not mentioned."),
    ("the beans in the closet had been watered too much.", "Both trays got the same water."),
    ("bean plants grow best when they are kept in the dark for part of each day and moved into sunlight later.", "The dark tray grew worse."))
rec('inferences', 0,
    "Every morning, a line forms outside Rosa&rsquo;s coffee shop before it opens. One week, the shop across the street began offering free coffee to anyone who arrived before 7:00 a.m. That week, the line outside Rosa&rsquo;s shop was much shorter than usual. It is most likely that ______",
    Q_INF, ("some of Rosa&rsquo;s usual customers went across the street that week to get the free coffee instead.", "The offer explains the shorter line."),
    ("Rosa&rsquo;s shop opened later that week.", "Opening time is not mentioned."),
    ("Rosa&rsquo;s customers had grown tired of coffee and switched to drinking tea at home each morning.", "Nothing suggests they stopped drinking coffee."),
    ("the shop across the street charged more for its coffee than Rosa did, even before 7:00 a.m.", "It gave coffee away before 7:00."))
rec('inferences', 0,
    "Squirrels in Maple Park bury acorns in the fall and dig many of them up in winter. Park workers noticed that small oak trees often sprout in spring in places where squirrels had been digging the previous fall. This suggests that ______",
    Q_INF, ("some buried acorns the squirrels never dug up grew into new oak trees.", "Sprouts appear where acorns were buried."),
    ("squirrels plant acorns on purpose so that new oak trees will grow in the park each spring.", "Nothing suggests squirrels intend this."),
    ("oak trees grow only in parks.", "Nothing supports this."),
    ("park workers bury acorns in the fall.", "The squirrels bury them."))
rec('inferences', 0,
    "A town library started a program in which children could read aloud to trained therapy dogs. Teachers noticed that children who joined the program began volunteering to read aloud in class more often. The teachers suspected that ______",
    Q_INF, ("reading to the dogs made the children more confident about reading aloud.", "Practice with a friendly listener could explain the change in class."),
    ("the children wanted to adopt dogs.", "Adoption is not mentioned."),
    ("the dogs had learned to read.", "Dogs listen; they do not read."),
    ("the children read aloud in class more often because their teachers had begun giving them easier books to read.", "Easier books are not mentioned."))
rec('inferences', 0,
    "Sam left a glass of cold lemonade on the porch on a hot afternoon. When he came back an hour later, the outside of the glass was covered in water droplets, even though none of the lemonade had spilled. Sam figured that ______",
    Q_INF, ("water from the warm air had collected on the cold glass.", "The droplets came from outside, since nothing spilled."),
    ("the lemonade had leaked through tiny cracks in the glass and formed drops on the outside.", "Nothing suggests cracks, and nothing spilled."),
    ("someone had watered the plants on the porch and splashed the glass.", "No one watering is mentioned."),
    ("it had rained on the porch while he was away, although the sky had been clear and sunny all afternoon.", "The text gives no reason to think it rained."))
rec('inferences', 0,
    "A zoo moved its giraffes to a new enclosure with taller feeding platforms. Keepers noticed that the giraffes now spent more time eating and less time pacing along the fence. The keepers concluded that ______",
    Q_INF, ("the taller platforms suited the giraffes better than the old ones.", "The change in behavior followed the new platforms."),
    ("the giraffes had grown taller during the move to the new enclosure, so they needed higher platforms.", "The giraffes did not grow; the platforms changed."),
    ("the giraffes preferred pacing to eating.", "They paced less once they could eat comfortably."),
    ("the zoo had begun feeding the giraffes a new kind of food that they found much more appealing than their old food.", "Food is not said to have changed."))
rec('inferences', 0,
    "Ms. Park asked her students to guess how many marbles were in a jar. Most guesses were far off, some too high and some too low. But when she averaged all thirty guesses, the result was within five marbles of the true number. This suggests that ______",
    Q_INF, ("a group&rsquo;s average guess can be more accurate than most of its members&rsquo; single guesses.", "The average was close even though most guesses were far off."),
    ("most students counted the marbles carefully.", "Most guesses were far off."),
    ("students who guessed too high were better at math than students who guessed too low.", "Math skill is not discussed."),
    ("guessing games are a poor way to teach students about numbers, because most individual guesses are wrong.", "The result points the other way."))
rec('inferences', 0,
    "The Riverside bus used to arrive at Hill Street every 30 minutes. When the city added more buses to the route, the bus began arriving every 10 minutes, and the number of people riding it doubled. This suggests that ______",
    Q_INF, ("more frequent buses made riding the bus more appealing.", "Ridership rose after waits got shorter."),
    ("the bus fare was lowered.", "Fares are not mentioned."),
    ("fewer people lived near Hill Street after the new buses were added to the route.", "Ridership rose, which does not suggest fewer residents."),
    ("people on Hill Street preferred to wait a long time for the bus because it gave them a chance to read.", "Riding rose when waits got shorter."))
# ---- medium
rec('inferences', 1,
    "Archaeologists excavating a village abandoned about 3,000 years ago found that the oldest houses had small storage pits, while houses built a few centuries later had pits several times larger. Seeds found in the later pits came mostly from a single grain crop. These findings suggest that, over those centuries, the villagers ______",
    Q_INF, ("came to rely more on stored grain from farming.", "Larger pits filled with one crop point to growing reliance on farming."),
    ("abandoned farming and turned to hunting and gathering, which required less storage space.", "Storage grew larger, not smaller."),
    ("moved to a different village farther up the river valley, where the soil was richer.", "The later houses are in the same village."),
    ("built smaller houses because the population of the village declined during those centuries.", "House size and population are not discussed."))
rec('inferences', 1,
    "In a study of online reviews, researchers found that products with a few negative reviews among many positive ones sold better than products with only positive reviews. The researchers suggested that shoppers may treat a small number of complaints as a sign that ______",
    Q_INF, ("the reviews are genuine rather than written or carefully filtered by the seller to hide complaints.", "A few complaints make the reviews seem authentic."),
    ("the product is poorly made and likely to break soon after it is bought.", "That would reduce sales, not raise them."),
    ("the seller offers refunds.", "Refunds are not mentioned."),
    ("most shoppers never read reviews at all and choose products only on the basis of their prices.", "The study shows reviews affect sales."))
rec('inferences', 1,
    "Botanist Aria Chen noticed that a certain wildflower produces far more nectar on the side of the flower facing the morning sun. When she turned potted plants so the other side faced east, the extra nectar shifted to that side within a few days. Chen concluded that ______",
    Q_INF, ("the flower&rsquo;s nectar production responds to the direction of the morning sun.", "The extra nectar follows whichever side faces east."),
    ("the flowers produce nectar only at night, when no sunlight reaches them.", "Nothing suggests nectar is made only at night."),
    ("pollinators prefer the shaded side of the flower.", "Pollinators are not discussed."),
    ("the plant is fixed from birth, making nectar on the same side no matter how it is turned or where it is placed.", "The nectar shifted when the plant was turned."))
rec('inferences', 1,
    "In the 1800s, many lighthouse keepers kept detailed logs of weather and passing ships. Climate researchers have begun using these logs to reconstruct past storms. Because the keepers recorded conditions several times a day, every day, for decades, the logs can ______",
    Q_INF, ("give a nearly continuous record of weather for times and places with few other records.", "Frequent, long-term entries fill gaps in the weather record."),
    ("tell researchers exactly how many ships sank in each storm during the 1800s.", "The logs recorded passing ships; sinkings are not mentioned."),
    ("replace modern instruments.", "Nothing suggests the logs replace current tools."),
    ("show that storms in the 1800s were always weaker than the storms that occur today along the same coasts.", "No comparison of storm strength is given."))
rec('inferences', 1,
    "Ants of a certain species farm fungus inside their nests, feeding it leaves and eating the fungus. Researchers found that the ants also carry bacteria on their bodies that produce chemicals which kill a mold that attacks the fungus. When the bacteria were removed, the mold spread through the gardens. This suggests that the bacteria ______",
    Q_INF, ("help the ants protect their fungus gardens from mold.", "Without the bacteria, mold spread."),
    ("are the ants&rsquo; main source of food during the months when fresh leaves are scarce.", "The ants eat the fungus."),
    ("cause the mold to spread through the gardens, which is why the ants carry them away from the nest.", "Removing the bacteria let mold spread."),
    ("harm the ants and the fungus alike, so the ants would be better off if the bacteria were removed from their bodies.", "Removal hurt the gardens."))
rec('inferences', 1,
    "A publisher released the same novel with two different covers in two similar cities. In the first city, the cover showed a photograph of the main character; in the second, it showed only the title on a plain background. The novel sold twice as many copies in the first city. The publisher reasoned that ______",
    Q_INF, ("the photograph cover probably drew more buyers than the plain cover did.", "Cover was the main difference between the cities."),
    ("people in the first city read more books than people in the second city.", "The cities were chosen as similar."),
    ("the novel&rsquo;s title was confusing.", "The title was the same in both cities."),
    ("readers in the second city preferred to buy novels online rather than in bookstores, so they never saw either cover.", "Nothing suggests this."))
rec('inferences', 1,
    "Hikers on a popular mountain trail often leave the path to take shortcuts, trampling the plants beside it. When park rangers placed large rocks along the edges of the trail&rsquo;s switchbacks, the damaged areas began to regrow within two years. The rangers concluded that ______",
    Q_INF, ("the rocks discouraged hikers from leaving the trail.", "Plants regrew once rocks lined the switchbacks."),
    ("hikers had stopped visiting the trail entirely after the rangers placed large rocks along its switchbacks.", "Nothing suggests the trail lost its hikers."),
    ("the plants grew faster because the rocks kept the soil warm.", "The text gives no evidence about soil temperature."),
    ("the trail should be closed for several years so that the trampled plants can recover.", "The rocks solved the problem without closing it."))
rec('inferences', 1,
    "Historian Nadia Petrov studied letters from a nineteenth-century merchant family. The letters written by the family&rsquo;s sons, who worked abroad, grew shorter and less frequent over time, while letters from the family&rsquo;s daughters, who stayed home, grew longer and more detailed about the family business. Petrov suggests that ______",
    Q_INF, ("the daughters may have taken on a larger role in running the business than histories acknowledge.", "Their growing knowledge of the business suggests a larger role."),
    ("the sons disliked their work abroad and planned to return home to run the business.", "No plans to return are mentioned."),
    ("the family business failed because the sons stopped writing home.", "No failure is mentioned."),
    ("the daughters wrote longer letters mainly because they had more free time than their brothers, who were busy abroad.", "The detail about the business suggests involvement, not only free time."))
# ---- hard
rec('inferences', 2,
    "Astronomers searching for planets around other stars have found many &ldquo;hot Jupiters,&rdquo; giant gas planets orbiting very close to their stars. Such planets are easy to detect, because their size and short orbits cause large, frequent changes in the light or motion of their stars. Smaller planets in wider orbits produce much subtler signals. Therefore, the large share of hot Jupiters among the planets discovered so far ______",
    Q_INF, ("may reflect which planets are easiest to find more than how common each kind of planet is.", "Detection is biased toward hot Jupiters, so their share may be inflated."),
    ("proves that most planets in the galaxy are giant gas planets orbiting very close to their stars.", "The easy detection means the share may not reflect reality."),
    ("shows that small planets cannot form in wide orbits.", "They are harder to detect, not impossible."),
    ("suggests that astronomers have stopped searching for smaller planets because hot Jupiters are more interesting to study.", "Nothing suggests the search has stopped."))
rec('inferences', 2,
    "A medieval chronicle describes a comet visible in daylight in the spring of a certain year. Astronomers can calculate that a known comet would have been close to Earth at that time, but only bright enough to see at night. The chronicle&rsquo;s author was writing about fifty years after the event, relying on older accounts. A historian might reasonably conclude that ______",
    Q_INF, ("the comet was real, but the claim that it was seen in daylight may have grown in the retelling.", "The timing fits a real comet, but the daylight detail conflicts with calculation and came secondhand."),
    ("the chronicle&rsquo;s author made up the comet entirely, since no comet could have been seen that year.", "A known comet was close to Earth then."),
    ("the astronomers&rsquo; calculations must be wrong.", "Nothing suggests the calculations are faulty."),
    ("the chronicle&rsquo;s author personally watched the comet in daylight, since writing fifty years later would not affect his memory.", "He relied on older accounts."))
rec('inferences', 2,
    "The following text is adapted from a 1910 novel. Mr. Grey has invited his neighbor to dinner for the first time in twenty years.<br><br>The two old men spoke of the weather, of the price of wool, of the new road, and of nothing else. Neither mentioned the boundary fence that had stood between their farms since the lawsuit, and when Mr. Grey&rsquo;s daughter began to ask about it, her father passed her the bread with such haste that she did not finish the question. It can most reasonably be inferred that ______",
    Q_INF, ("both men avoid the old dispute, hoping to keep the peace of the evening.", "They steer clear of the fence, and Grey cuts off his daughter&rsquo;s question."),
    ("Mr. Grey has invited his neighbor in order to settle the lawsuit about the boundary fence once and for all.", "No one raises the lawsuit."),
    ("the daughter dislikes the neighbor.", "Her question shows curiosity, not dislike."),
    ("the two men have forgotten about the lawsuit, since it happened so long ago that neither remembers it clearly.", "Their careful avoidance suggests they remember."))
rec('inferences', 2,
    "Researchers tracking bumblebees found that bees from colonies exposed to a common pesticide gathered pollen as often as unexposed bees but returned with smaller loads. The exposed bees also took longer to learn which flowers held the most pollen. Taken together, these findings suggest that the pesticide may ______",
    Q_INF, ("harm colonies less by stopping foraging than by making each foraging trip less productive.", "Trips were as frequent but less effective."),
    ("cause bees to stop gathering pollen altogether within a few days of exposure.", "Exposed bees foraged as often as others."),
    ("improve bees&rsquo; memory for which flowers hold the most pollen.", "Exposed bees learned more slowly."),
    ("have no effect on bee colonies, since exposed bees foraged just as often as the bees that were never exposed to it.", "Loads were smaller and learning slower."))
rec('inferences', 2,
    "Two versions of a folk song were recorded in the 1930s, one in a mountain town and one in a coastal city. The mountain version has twelve verses and refers to local landmarks; the coastal version has five verses and mentions ships. A song collector noted that both share a nearly identical chorus and a verse about a lost ring found in no other song. The collector reasoned that ______",
    Q_INF, ("the two versions likely came from a common source and changed as they spread to different places.", "The shared chorus and unique verse suggest one origin; local details show adaptation."),
    ("the two songs were composed separately, since they contain different numbers of verses.", "The shared, unique material argues against separate composition."),
    ("the coastal version was the original.", "Nothing shows which came first."),
    ("the singers in the mountain town had copied the coastal version from a printed book of sea songs.", "Nothing suggests a printed source."))
rec('inferences', 2,
    "A city offered free home energy audits, in which an inspector shows homeowners where their houses lose heat. Homeowners who received an audit cut their energy use by an average of 8 percent. However, the homeowners who signed up for audits had already been cutting their energy use faster than their neighbors in the years before the program. This means that the 8 percent figure ______",
    Q_INF, ("may overstate the audits&rsquo; effect, since those homeowners were already cutting their energy use before the program.", "Existing trends may account for part of the drop."),
    ("proves that the audits caused homeowners to reduce their energy use by exactly 8 percent.", "Existing trends make that uncertain."),
    ("shows that homeowners who did not receive audits increased their energy use during the same period.", "Nonparticipants&rsquo; use is not reported."),
    ("understates the audits&rsquo; effect.", "The prior trend points toward overstatement."))
rec('inferences', 2,
    "Many desert plants open the pores on their leaves only at night, taking in carbon dioxide when the air is cooler and storing it for use in daylight. This lets them lose far less water than plants that open their pores during the day. Botanist Samir Aziz found that a species of cactus, when watered heavily for several weeks, began opening its pores during the day as well. Aziz concluded that the cactus&rsquo;s nighttime habit ______",
    Q_INF, ("is at least partly a response to dry conditions, not a fixed trait.", "The habit changed when water became plentiful."),
    ("is a fixed trait that cannot change, whatever conditions the plant grows in.", "The plant changed its habit when watered."),
    ("harms the plant when water is scarce, because it forces the plant to lose water through its pores at night.", "Night opening saves water."),
    ("evolved to help the plant attract pollinators.", "Pollinators are not discussed."))
rec('inferences', 2,
    "In a long-term study, children who were read to often at age three had larger vocabularies at age ten than children who were read to rarely. The researchers noted, however, that parents who read to their children often also tended to talk with them more during daily activities, such as cooking and shopping. Therefore, the study ______",
    Q_INF, ("cannot show that reading itself, rather than conversation generally, built the children&rsquo;s vocabularies.", "Reading and talking went together, so their effects are tangled."),
    ("proves that reading to children is the only way to build their vocabularies.", "The confound undercuts even the narrower claim."),
    ("shows that talking during cooking and shopping harms vocabulary growth.", "Talking was associated with larger vocabularies, if anything."),
    ("found no link.", "Children read to often did have larger vocabularies."))
