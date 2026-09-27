"""Authored Reading & Writing items, part 3 (original text; researchers and characters are fictional).
Adds depth to the passage-based skills that had only 4 items per difficulty. Same record format as rw_content.py.
Loaded after parts 1 and 2 so the index-based uids of older items never shift.

Writing rule for distractors: wrong choices are about as long and specific as the right one (a misread detail, an
overreach, a true-but-off-point statement), so "pick the longest answer" never works. tests/rw_quality.py checks this."""
from bank.rw_content import rec, Q_MAIN, Q_PURPOSE, Q_FUNC, Q_STRUCT, Q_SUP, Q_WEAK

Q_QUOTE = 'Which quotation from the work most effectively illustrates the claim?'

# =============================================================== CENTRAL IDEAS AND DETAILS
# ---- easy
rec('central_ideas', 0,
    "Every autumn, volunteers in the town of Millbrook gather at the library to repair donated winter coats. They replace broken zippers, patch torn sleeves, and sew on missing buttons. The finished coats are given free of charge to families who need them before the first snow.",
    Q_MAIN, ("Volunteers repair donated coats and give them to families before winter.", "Each sentence describes the repair work and who receives the coats."),
    ("The library teaches residents to sew.", "Volunteers do the repairs; no one is taught to sew."),
    ("Most coats donated in Millbrook arrive with broken zippers that volunteers must replace before the first snow.", "Zippers are one repair among several; the passage does not say most coats have them."),
    ("Families in Millbrook buy repaired winter coats from the library at a low price each autumn.", "The coats are given free of charge."))
rec('central_ideas', 0,
    "Sea otters often wrap themselves in strands of kelp before they fall asleep. The long seaweed is anchored to the ocean floor, so an otter tangled in it will not drift away with the current while it rests. Groups of otters sometimes sleep this way side by side.",
    Q_MAIN, ("Sea otters wrap themselves in kelp so they will not drift while sleeping.", "The passage explains the habit and the reason for it."),
    ("Sea otters eat kelp before they sleep because the seaweed grows close to where they rest.", "The passage never mentions what otters eat."),
    ("Sea otters sleep in large groups because ocean currents are too strong for a single otter.", "Groups sometimes sleep together, but the passage does not give currents as the reason."),
    ("Kelp grows from the ocean floor toward the surface, where it forms thick underwater forests.", "This describes kelp, not the otters&rsquo; behavior, which is the focus."))
rec('central_ideas', 0,
    "When Dev Anand opened a bike shop in 2015, he noticed that many children in his neighborhood had no bicycles. He began fixing up old bikes that customers left behind and giving them away. So far, the shop has given away more than four hundred bicycles.",
    Q_MAIN, ("Anand fixes unwanted bikes and gives them to local children.", "The passage describes the problem he noticed and what he did about it."),
    ("Anand has sold over four hundred bikes.", "The bikes were given away, not sold."),
    ("Anand opened his bike shop in 2015 because children in his neighborhood asked him to fix their bicycles.", "The passage says many children had no bicycles; it gives no such reason for opening the shop."),
    ("Customers often leave old bikes at Anand&rsquo;s shop because repairing them costs more than buying new ones.", "Why customers leave bikes is never explained."))
rec('central_ideas', 0,
    "The Atacama Desert in Chile is one of the driest places on Earth; some weather stations there have recorded almost no rain for years at a time. Because the air is so dry and the skies are so clear, several of the world&rsquo;s largest telescopes have been built in the region.",
    Q_MAIN, ("The Atacama&rsquo;s dry, clear conditions make it well suited to large telescopes.", "The passage links the desert&rsquo;s dryness to its use for astronomy."),
    ("Weather stations in the Atacama Desert have recorded no rain at all since they were first built there.", "The passage says almost no rain for years at a time, not none ever."),
    ("Chile has built more large telescopes than any other country because of its many dry deserts.", "No country comparison is made, and only one desert is discussed."),
    ("Scientists study the Atacama Desert to learn why some regions of Earth receive almost no rain.", "The passage mentions telescopes, not studies of rainfall."))
rec('central_ideas', 0,
    "In the story, twelve-year-old Rosa practices the violin every evening after dinner. When her little brother complains about the noise, she moves her music stand to the garden shed. There, surrounded by rakes and flowerpots, she keeps practicing until it is too dark to read the notes.",
    Q_MAIN, ("Rosa is determined to keep practicing despite obstacles.", "She moves to the shed and plays until dark rather than stopping."),
    ("Rosa stops practicing the violin at home because her little brother complains about the noise every evening.", "She keeps practicing; she only moves to the shed."),
    ("Rosa prefers practicing in the garden shed because being surrounded by tools and flowerpots helps her focus.", "She moves because of her brother, not because she prefers the shed."),
    ("Rosa and her brother argue often.", "No argument over the shed is described."))
rec('central_ideas', 0,
    "Many cities are replacing ordinary streetlights with LED lights. LEDs use far less electricity than older bulbs, and they last many years longer, so cities spend less on both power and maintenance. Some cities have used the savings to fund other public services.",
    Q_MAIN, ("Switching to LED streetlights saves cities money.", "Each detail describes a cost saving from LEDs."),
    ("Cities are replacing streetlights with LEDs because older bulbs were too dim to keep streets safe at night.", "Brightness and safety are never mentioned."),
    ("Some cities have stopped funding other public services in order to pay for new LED streetlights.", "The savings are used to fund other services, not the reverse."),
    ("LEDs need more upkeep than old bulbs.", "LEDs last many years longer, which lowers maintenance."))
rec('central_ideas', 0,
    "The following text is from a 1908 novel. Mrs. Pell has just moved to a farm.<br><br>Mrs. Pell had lived in the city all her life, and at first the silence of the farm frightened her. But after a month she found she could hear things she had never noticed before: the wind in the wheat, the creak of the barn door, the owls calling after sunset. Now she could not imagine sleeping anywhere else.",
    Q_MAIN, ("Mrs. Pell comes to love the quiet farm that once frightened her.", "She changes from fearing the silence to not wanting to sleep anywhere else."),
    ("Mrs. Pell misses the noise of the city and plans to return there once the harvest is finished.", "The last sentence says the opposite."),
    ("Mrs. Pell is kept awake at night by the owls, the wind, and the creaking of the barn door.", "These are sounds she comes to enjoy, not ones that keep her awake."),
    ("Mrs. Pell finds that the farm is much noisier than the city she lived in for most of her life.", "She notices quiet sounds; the farm is described as silent."))
rec('central_ideas', 0,
    "Before the invention of refrigerators, many families kept food cold in an icebox, a wooden cabinet lined with tin or zinc. A large block of ice sat in the top compartment, and cold air sank down over the food below. Ice delivery workers brought new blocks to homes several times a week.",
    Q_MAIN, ("Before refrigerators, iceboxes cooled by blocks of ice kept food cold.", "The passage explains what an icebox was and how it worked."),
    ("Iceboxes kept food colder than modern refrigerators because cold air sank down from the ice above.", "No comparison with modern refrigerators is made."),
    ("Ice delivery was one of the most common jobs before refrigerators, with workers visiting homes daily.", "The passage says several times a week and does not say how common the job was."),
    ("Families preferred zinc iceboxes to tin ones.", "Tin and zinc are both mentioned as linings; neither is preferred."))
# ---- medium
rec('central_ideas', 1,
    "Urban planner Keiko Tanaka studied neighborhoods where streets had been narrowed and trees planted along the curbs. Drivers in those neighborhoods slowed down even though speed limits had not changed. Tanaka argues that the way a street looks can influence driver behavior as much as posted rules can.",
    Q_MAIN, ("Tanaka argues that street design can shape how fast people drive.", "Her finding and her argument both concern design changing driving behavior."),
    ("Tanaka found that drivers slowed down in neighborhoods where city officials lowered posted speed limits.", "The passage says the speed limits had not changed."),
    ("Tanaka recommends replacing speed limit signs with trees because drivers tend to ignore posted rules.", "She compares design with rules but does not recommend removing signs."),
    ("Tanaka studied whether planting trees along curbs improves air quality in narrow city streets.", "Air quality is not discussed."))
rec('central_ideas', 1,
    "The Voyager 1 spacecraft, launched in 1977, is now more than 20 billion kilometers from Earth. Its radio signals take nearly a full day to reach us, and its power supply weakens every year, forcing engineers to shut down instruments one at a time. Even so, the spacecraft continues to send back measurements from interstellar space.",
    Q_MAIN, ("Despite distance and fading power, Voyager 1 still sends back data.", "The passage lists difficulties and then says the craft continues to send data."),
    ("Engineers have shut down all of Voyager 1&rsquo;s instruments because its signals take too long to reach Earth.", "Instruments are shut down one at a time because of power, and data still arrive."),
    ("Voyager 1 was designed in 1977 to travel more than 20 billion kilometers and reach interstellar space.", "The passage gives its launch year and distance, not its design goals."),
    ("Voyager 1&rsquo;s signals slow as its power fades.", "The delay comes from distance, and signals do not slow with power."))
rec('central_ideas', 1,
    "The following text is adapted from a 1913 short story. Tom has just been offered a job in a distant city.<br><br>Tom read the letter twice and then folded it into his pocket without a word. All through supper he answered his mother&rsquo;s questions about the harvest, praised the bread, and laughed at his sister&rsquo;s jokes. Only when the lamp was out did he take the letter out again and hold it, unopened, against his chest.",
    Q_MAIN, ("Tom hides his strong feelings about the offer from his family.", "He acts normally at supper but privately holds the letter close afterward."),
    ("Tom decides to turn down the job so that he can stay home and help his family with the harvest.", "The text never shows a decision."),
    ("Tom&rsquo;s mother and sister are upset at supper because they have learned he may move away.", "The family does not know about the letter."),
    ("Tom is so worried about the harvest that he cannot bring himself to read the letter a second time.", "He reads the letter twice; the harvest is only a supper topic."))
rec('central_ideas', 1,
    "For years, scientists assumed that the tiny hairs on a gecko&rsquo;s toes stuck to walls by suction. Experiments by physicist Arjun Mehta&rsquo;s team showed that geckos cling just as well in a vacuum, where suction is impossible. The team concluded that the hairs instead rely on weak attractive forces between molecules, which add up across millions of hairs.",
    Q_MAIN, ("Geckos cling through molecular attraction, not suction.", "The passage presents the old assumption, the test that ruled it out, and the new explanation."),
    ("Mehta&rsquo;s team found that geckos lose their grip in a vacuum, which shows that their toes rely on suction.", "Geckos cling just as well in a vacuum, which rules out suction."),
    ("One toe hair can hold a gecko&rsquo;s weight.", "The forces are weak and add up across millions of hairs."),
    ("Scientists have long disagreed about whether geckos can climb smooth walls in a vacuum or only in air.", "The disagreement described is about how the hairs stick, not where geckos climb."))
rec('central_ideas', 1,
    "Many early twentieth-century quilts made by women in rural Alabama were long dismissed as crude because their patterns were irregular. Art historian Lena Brooks argues that the irregularity was deliberate: quilters improvised, varying block sizes and colors to create rhythm and surprise. Brooks compares these quilts to jazz, in which departures from a pattern are the point rather than a mistake.",
    Q_MAIN, ("Brooks argues that the quilts&rsquo; irregularity was intentional.", "She reinterprets the irregularity as deliberate improvisation."),
    ("Brooks argues that the Alabama quilters learned to improvise patterns by listening to jazz musicians of the period.", "The jazz comparison is an analogy, not a claim about influence."),
    ("Brooks concedes the quilts are crude.", "She argues the quilts are not crude but deliberately irregular."),
    ("Most art historians today agree that the Alabama quilts were made carelessly because their makers lacked training.", "The passage describes an older dismissal and Brooks&rsquo;s challenge to it."))
rec('central_ideas', 1,
    "Some farmers in Kenya have begun planting a grass called desmodium between rows of corn. The grass releases a chemical that drives away moths whose larvae damage corn, while a second grass planted around the field&rsquo;s edges attracts the moths away from the crop. Farmers using the method have reported higher yields without buying pesticides.",
    Q_MAIN, ("Companion grasses help Kenyan farmers protect corn from pests without pesticides.", "The passage explains how the two grasses control moths and the resulting yields."),
    ("Kenyan farmers have begun replacing corn with desmodium because the grass sells for more and needs no pesticides.", "Desmodium is planted between the corn rows, not instead of the corn."),
    ("Moths that damage corn prefer to lay their eggs in grasses, so farmers plant desmodium to attract them.", "Desmodium drives moths away; a different grass at the edges attracts them."),
    ("Pesticides are unavailable to many Kenyan farmers, so yields have fallen in regions where moths are common.", "The passage says farmers avoid buying pesticides and reports higher yields."))
rec('central_ideas', 1,
    "When the city of Rivera cut bus fares to zero for one year, ridership rose by nearly forty percent. However, a survey found that most new riders had previously walked or biked rather than driven. Transportation analyst Marcus Hale concludes that free fares alone may do little to reduce car traffic.",
    Q_MAIN, ("Free fares raised ridership but may not cut car traffic much.", "This captures both the ridership rise and Hale&rsquo;s conclusion about traffic."),
    ("Hale concludes that Rivera&rsquo;s free-fare year reduced car traffic because bus ridership rose by nearly forty percent.", "Hale concludes the opposite: new riders mostly had not been driving."),
    ("A survey found that most new bus riders in Rivera had stopped driving their cars during the free-fare year.", "Most new riders had previously walked or biked."),
    ("Rivera ended free fares after a year.", "Why the program lasted one year is not explained."))
rec('central_ideas', 1,
    "Historians once believed that the ancient city of Great Zimbabwe was built by outsiders, because colonial-era writers refused to credit local people with such large stone structures. Archaeological evidence, including pottery and tools matching those of the surrounding Shona communities, has since shown that the city was built by the ancestors of the Shona.",
    Q_MAIN, ("Evidence shows that Great Zimbabwe was built by ancestors of the Shona.", "The passage contrasts the old claim with the evidence that overturned it."),
    ("Colonial-era writers discovered pottery and tools at Great Zimbabwe that matched those of distant civilizations.", "The pottery and tools match local Shona communities."),
    ("Archaeologists now think that outsiders built Great Zimbabwe and later taught the Shona to make pottery and tools.", "The evidence shows the ancestors of the Shona built the city."),
    ("Historians have struggled to date Great Zimbabwe because its stone structures contain no pottery or tools.", "Pottery and tools are the evidence used, and dating is not discussed."))
# ---- hard
rec('central_ideas', 2,
    "Economists have long assumed that people value a good more once they own it, a pattern called the endowment effect. Yet in a series of trials, behavioral economist Hana Sato found that experienced traders&mdash;people who regularly buy and sell items like the ones tested&mdash;showed little or no endowment effect, while novices showed a strong one. Sato suggests that the effect may be less a fixed feature of human psychology than a habit that experience can wear away.",
    Q_MAIN, ("Sato&rsquo;s results suggest the endowment effect may fade with experience rather than being universal.", "Experienced traders lacked the effect, so Sato questions whether it is fixed."),
    ("Sato found that novices showed no endowment effect, which suggests the pattern appears only after people gain trading experience.", "It reverses the finding: novices showed a strong effect."),
    ("Sato&rsquo;s trials show that experienced traders value the goods they own more highly than novices value theirs.", "The trials concern the endowment effect, which experienced traders largely lacked."),
    ("Because experienced traders showed little endowment effect, economists have abandoned the idea that ownership changes how people value goods.", "Sato only suggests a revision; the field&rsquo;s response is not described."))
rec('central_ideas', 2,
    "The following text is adapted from a 1920 novel. Lydia, a painter, has returned to her childhood home.<br><br>She had expected the house to look smaller, as houses are said to do when one returns to them grown. Instead it seemed to have kept its size and shed its meaning: the stairs were only stairs, the window only a window, and the garden, which had once held whole kingdoms, was merely a garden that needed weeding. She found that she missed not the house but the eyes with which she had first seen it.",
    Q_MAIN, ("Lydia realizes she misses her childhood way of seeing the house, not the house.", "The final sentence states this directly, and the details build to it."),
    ("Lydia is disappointed to find that the house seems much smaller now than it did when she was a child.", "She expected that, but the house kept its size."),
    ("Lydia decides to restore the garden.", "The garden needs weeding, but she makes no plans."),
    ("Lydia regrets leaving her childhood home to become a painter because the house has lost its meaning without her.", "Her career is not presented as a regret."))
rec('central_ideas', 2,
    "Conservation biologists often measure a habitat&rsquo;s health by counting species. Ecologist Tomas Varga argues that such counts can mislead: a restored wetland may quickly regain the number of species it once had while lacking the interactions among them&mdash;pollination, predation, decomposition&mdash;that sustain the system. In Varga&rsquo;s view, a wetland with the right species list but few of these relationships is closer to a collection than to an ecosystem.",
    Q_MAIN, ("Varga argues species counts can overstate a habitat&rsquo;s health by ignoring species interactions.", "The passage contrasts counting species with measuring the relationships that sustain an ecosystem."),
    ("Varga argues that restored wetlands rarely regain the number of species they had before being damaged.", "Varga says they may regain the number quickly."),
    ("Varga argues that pollination matters more than predation or decomposition in determining whether a wetland is healthy.", "The three interactions are examples; none is ranked."),
    ("Varga argues that conservation biologists should stop restoring wetlands until better ways of counting species are developed.", "He criticizes a measurement, not restoration, and wants more than counts."))
rec('central_ideas', 2,
    "In the eighteenth century, Chinese porcelain was so prized in Europe that rulers built entire rooms to display it. European manufacturers spent decades trying to copy it, and when a German workshop finally produced true porcelain around 1710, the recipe was guarded as a state secret. Historian Mira Vasquez argues that the chase for porcelain helped push European chemistry forward, since the effort required systematic testing of clays and firing temperatures.",
    Q_MAIN, ("Vasquez argues that copying porcelain helped advance European chemistry.", "The passage builds to her claim that the effort pushed chemistry forward."),
    ("Vasquez argues that German porcelain surpassed Chinese porcelain in quality because it was developed through systematic testing.", "Quality is never compared."),
    ("European rulers lost interest in porcelain.", "Nothing says rulers lost interest."),
    ("Vasquez argues that Chinese manufacturers kept their recipe secret, which forced Europeans to test clays and firing temperatures.", "The passage says the German recipe was kept secret, not the Chinese one."))
rec('central_ideas', 2,
    "Many studies report that people who sleep poorly also tend to have weaker memories, and the finding is often summarized as &ldquo;poor sleep harms memory.&rdquo; Neuroscientist Adaeze Okafor cautions that most such studies are correlational. Stress, she notes, disrupts both sleep and memory, so it could produce the pattern even if sleep had no direct effect on memory. Okafor does not dispute that sleep matters; she argues that the evidence usually cited cannot by itself show how much.",
    Q_MAIN, ("Okafor says the usual evidence cannot by itself show how much sleep affects memory.", "She points to correlation and a possible third factor without denying sleep matters."),
    ("Okafor argues that studies linking sleep and memory are wrong because stress, not sleep, is what weakens people&rsquo;s memories.", "She offers stress as a possibility and does not dispute that sleep matters."),
    ("Okafor argues that poor sleep causes stress, which in turn weakens memory, so sleep harms memory only indirectly.", "She says stress disrupts sleep, not that sleep causes stress."),
    ("Okafor argues that correlational studies of sleep and memory should be replaced by studies of how stress affects the brain.", "She questions what the evidence shows, not which studies should be done."))
rec('central_ideas', 2,
    "Traditional accounts of the Industrial Revolution emphasize inventions such as the steam engine. Economic historian Farid Khalil contends that these accounts overlook a quieter change: the spread of standardized parts and measurements, which let workshops in different towns produce components that fit together. Without that shared system, Khalil argues, many celebrated machines could not have been built or repaired at scale.",
    Q_MAIN, ("Khalil argues that standardization was an overlooked but essential part of the Industrial Revolution.", "He adds standardization to the story and says famous machines depended on it."),
    ("Khalil argues that the steam engine mattered less to the Industrial Revolution than historians have claimed.", "He says accounts overlook something else, not that the steam engine was unimportant."),
    ("Khalil argues that workshops in different towns competed to produce the best parts for steam engines.", "Competition is not discussed; the workshops made parts that fit together."),
    ("Khalil argues that standardized measurements spread only after the celebrated machines of the period had been built.", "He says the machines depended on standardization to be built at scale."))
rec('central_ideas', 2,
    "Poet Alma Reyes&rsquo;s early collections were praised for their vivid images of her hometown&rsquo;s harbor. Her later work, written after she had lived abroad for two decades, returns to the same harbor but treats it differently: boats and gulls still appear, but each poem also questions whether memory can be trusted. Critic Jon Park suggests that the later poems are less about the harbor than about the act of remembering it.",
    Q_MAIN, ("Park suggests the later poems are more about memory than about the harbor itself.", "The passage contrasts the early images with later poems that question memory."),
    ("After living abroad for two decades, Reyes stopped writing about her hometown&rsquo;s harbor and turned to new subjects.", "Her later work returns to the harbor."),
    ("Park finds the later poems weaker.", "Park describes a change in focus, not a decline."),
    ("Reyes&rsquo;s later poems replace the boats and gulls of her early work with images from the places she lived abroad.", "Boats and gulls still appear in the later poems."))
rec('central_ideas', 2,
    "Wind farms are often opposed by nearby residents, and developers have tried to win support by offering cash payments. Political scientist Rhea Gupta studied communities that had been offered either payments or a share of ownership in the project. Although the payments were often larger in total, communities offered ownership shares were substantially more likely to approve the projects. Gupta concludes that a sense of control may matter to residents more than money does.",
    Q_MAIN, ("Ownership shares won more support than larger cash payments, possibly because they offer control.", "The finding and Gupta&rsquo;s explanation are both included."),
    ("Gupta found that communities offered cash payments rejected wind farms because the payments were too small.", "The payments were often larger in total than the ownership shares."),
    ("Gupta found that ownership shares were worth more in total than cash payments, which explains why they won more approvals.", "The passage says the payments were often larger."),
    ("Gupta concludes that most residents oppose wind energy and cannot be persuaded by either payments or ownership.", "Ownership offers substantially raised approval."))

# =============================================================== TEXT STRUCTURE AND PURPOSE
# ---- easy
rec('text_structure_purpose', 0,
    "Squirrels bury thousands of nuts each fall, and they do not find all of them. <u>Many of the forgotten nuts sprout into new trees the following spring.</u> In this way, squirrels help forests spread.",
    Q_FUNC, ("It shows how forgotten nuts lead to new trees.", "It connects the unfound nuts to the forest-spreading point in the last sentence."),
    ("It explains how squirrels use their memory to find most of the nuts they buried in the fall.", "It is about nuts squirrels do not find."),
    ("It argues that squirrels waste food.", "No judgment about waste is made."),
    ("It describes why trees drop so many nuts each fall, before squirrels have a chance to bury them.", "Why trees drop nuts is not discussed."))
rec('text_structure_purpose', 0,
    "Sofia wanted to learn to juggle. On the first day, she dropped the balls again and again. She practiced for ten minutes every morning, and after three weeks she could keep three balls in the air for a full minute.",
    Q_STRUCT, ("It shows a difficulty and how practice overcame it.", "Sofia struggles at first and succeeds after weeks of practice."),
    ("It compares Sofia&rsquo;s way of learning to juggle with the way her friends learned in less time.", "Only Sofia&rsquo;s learning is described."),
    ("It explains why juggling three balls is harder than learning most other hobbies for beginners.", "No other hobbies are mentioned."),
    ("It describes a goal Sofia set and then explains why she gave it up after three weeks.", "She reaches her goal after three weeks."))
rec('text_structure_purpose', 0,
    "Most people think of deserts as hot, but Antarctica is also a desert. A desert is any place that receives very little precipitation, and Antarctica&rsquo;s interior gets less snow each year than many sandy deserts get rain.",
    Q_PURPOSE, ("To explain why Antarctica counts as a desert.", "The text corrects a common idea by giving the definition of a desert."),
    ("To describe Antarctic wildlife.", "Animals are not mentioned."),
    ("To argue that sandy deserts receive less precipitation each year than Antarctica&rsquo;s interior does.", "It says the opposite."),
    ("To explain how snow forms in Antarctica even though the continent receives very little rain.", "Snow formation is not explained."))
rec('text_structure_purpose', 0,
    "The following text is from a 1905 story.<br><br>The old clock in the hall had stopped years ago at a quarter past four. <u>No one in the family could remember exactly when, and no one had ever tried to fix it.</u> Visitors found it strange, but to the Hartleys it was simply part of the house.",
    Q_FUNC, ("It shows the family has long accepted the stopped clock.", "Not remembering when it stopped and never fixing it shows long acceptance."),
    ("It explains that the clock stopped because no one in the family remembered to wind it.", "No cause for the stopping is given."),
    ("It shows that visitors to the house often offered to repair the old clock for the Hartleys.", "Visitors only found it strange."),
    ("It describes the clock&rsquo;s appearance and explains where in the hall it was placed.", "The sentence gives no physical details."))
rec('text_structure_purpose', 0,
    "Maple syrup is made from the sap of maple trees. Farmers collect the sap in early spring, when cold nights and warm days make it flow. Then they boil the sap for hours until most of the water evaporates and a thick, sweet syrup is left.",
    Q_STRUCT, ("It gives the steps of making maple syrup in order.", "Collecting comes first, then boiling."),
    ("It compares maple syrup with other sweeteners and explains why syrup takes longer to make.", "No other sweeteners are mentioned."),
    ("It argues syrup is healthier than sugar.", "Health is not discussed."),
    ("It explains why maple trees grow only in places where nights are cold and days are warm.", "Where maples grow is not discussed."))
rec('text_structure_purpose', 0,
    "Some people believe that goldfish can remember things for only a few seconds. <u>In one experiment, however, goldfish learned to push a lever for food and still remembered how to do it months later.</u>",
    Q_FUNC, ("It gives evidence against a common belief.", "The experiment contradicts the idea of a few-second memory."),
    ("It explains why goldfish are popular.", "Popularity is not discussed."),
    ("It supports the belief that goldfish forget what they learn after only a few seconds.", "It contradicts that belief."),
    ("It describes how goldfish in the wild learn to find food by pushing on objects.", "The experiment was not in the wild."))
rec('text_structure_purpose', 0,
    "Libraries lend more than books. Many now lend tools, musical instruments, cake pans, and even fishing rods. Borrowers can try a hobby without buying expensive equipment, and the items are shared by many people instead of sitting unused in one home.",
    Q_PURPOSE, ("To describe unusual items libraries lend and why that helps.", "The text lists the items and then explains the benefits."),
    ("To argue that people should borrow books from libraries instead of buying them from stores.", "Buying books is not discussed."),
    ("To explain how libraries decide which tools and instruments are worth buying for borrowers.", "How libraries choose items is not discussed."),
    ("To compare the items that libraries lend today with the items they lent in the past.", "No past items are described."))
rec('text_structure_purpose', 0,
    "At first, the new playground was empty; children in the neighborhood said it looked boring. Then the city asked the children to help redesign it. They suggested a climbing wall, a sandpit, and a tunnel. After the changes were made, the playground was full every afternoon.",
    Q_STRUCT, ("It shows a problem, a fix, and the result.", "An empty playground, a redesign with children&rsquo;s ideas, then a full playground."),
    ("It compares two playgrounds in the city and explains why children prefer one to the other.", "Only one playground is described."),
    ("It lists what children find boring.", "The children suggest features they want; nothing lists what they find boring."),
    ("It describes how the city built a new playground and then explains why it was later removed.", "The playground was redesigned and became popular."))
# ---- medium
rec('text_structure_purpose', 1,
    "Engineers designing Japan&rsquo;s high-speed trains faced a problem: when a train shot out of a tunnel, it produced a loud boom that disturbed nearby residents. <u>One engineer, a bird-watcher, noticed that kingfishers dive into water with barely a splash.</u> Reshaping the train&rsquo;s nose to resemble a kingfisher&rsquo;s beak greatly reduced the noise.",
    Q_FUNC, ("It introduces the observation that inspired the solution.", "The kingfisher observation leads to the new nose design."),
    ("It explains why kingfishers dive into water so quietly and how their beaks are shaped.", "The reason for the quiet dive is not the point."),
    ("It describes a second problem the engineers faced after solving the problem of the loud boom.", "It gives the source of a solution, not a new problem."),
    ("It urges engineers to study birds.", "No general recommendation is made."))
rec('text_structure_purpose', 1,
    "Scientists once thought that the deep ocean floor, lacking sunlight, could support little life. Then, in 1977, researchers exploring vents on the Pacific seafloor found crowded communities of tubeworms, clams, and crabs. These animals depend on bacteria that make food from chemicals in the vent water rather than from sunlight.",
    Q_STRUCT, ("It gives an earlier belief and then a discovery that overturned it.", "The expectation of little life is followed by the vent communities."),
    ("It compares two methods that researchers used to explore the Pacific seafloor in 1977.", "No methods are compared."),
    ("It describes a problem facing deep-sea animals and then explains how bacteria solved it for them.", "The passage explains how the animals get food, not a problem they solved."),
    ("It lists deep-sea animals from largest to smallest and explains what each of them eats.", "The animals are not ranked, and only their shared food source is explained."))
rec('text_structure_purpose', 1,
    "The following text is from a 1911 novel. Anne is waiting for news of a job she applied for.<br><br>Anne told herself she did not care whether the letter came. She swept the porch, which did not need sweeping, and then swept it again. <u>Every time a cart rattled down the road, the broom paused in her hands.</u>",
    Q_FUNC, ("It shows Anne is more anxious than she admits.", "She stops at every sound of a cart despite claiming not to care."),
    ("It shows that Anne is tired.", "The pause is about the road, not fatigue."),
    ("It explains that the road near Anne&rsquo;s house is so busy that the noise interrupts her work.", "The focus is her reaction, not the traffic."),
    ("It suggests that Anne has already received the letter and is hiding the news from her family.", "She is still waiting."))
rec('text_structure_purpose', 1,
    "Archaeologists studying ancient Roman concrete have long wondered why some harbor walls have survived two thousand years of pounding waves. Recent analysis showed that seawater seeping into the concrete reacted with volcanic ash in the mix, growing new minerals that strengthened the material over time. Modern concrete, by contrast, tends to weaken when exposed to seawater.",
    Q_PURPOSE, ("To explain why some Roman concrete has lasted, in contrast to modern concrete.", "It gives the explanation and then the contrast."),
    ("To argue that Roman builders understood how seawater would react with volcanic ash in their concrete.", "What Roman builders understood is not discussed."),
    ("To describe how modern engineers are adding volcanic ash to concrete used in harbor walls.", "Modern building methods are not described."),
    ("To explain why archaeologists have found so few Roman harbor walls that survived the pounding of waves.", "The passage is about walls that did survive."))
rec('text_structure_purpose', 1,
    "Many music apps recommend songs based on what users have already played. <u>Critics worry that this can trap listeners in a narrow range of styles.</u> A study by media researcher Daniel Ortega, however, found that heavy app users actually listened to more genres over time than they had before using the apps.",
    Q_FUNC, ("It introduces a concern that the study then challenges.", "Ortega&rsquo;s results run against the critics&rsquo; worry."),
    ("It summarizes the finding of Ortega&rsquo;s study about how heavy app users&rsquo; listening changed over time.", "The study&rsquo;s results come in the next sentence."),
    ("It explains how music apps decide which songs to recommend based on what users have already played.", "That explanation is in the first sentence."),
    ("It shows listeners prefer one genre.", "It states a worry, not evidence."))
rec('text_structure_purpose', 1,
    "In the late 1800s, most American cities drew drinking water from nearby rivers, and diseases such as typhoid spread easily. When cities began filtering and chlorinating their water in the early 1900s, typhoid death rates fell sharply. Some historians consider clean water one of the most important public-health advances of the twentieth century.",
    Q_STRUCT, ("It gives a health problem, a response, and why the response mattered.", "Typhoid, water treatment, then its importance."),
    ("It compares the health of people in American cities with the health of people living in the countryside.", "No rural comparison appears."),
    ("It argues that American cities should stop drawing drinking water from nearby rivers today.", "No present-day recommendation is made."),
    ("It explains how filtering and chlorine remove the bacteria that cause typhoid from river water.", "The mechanism is not described."))
rec('text_structure_purpose', 1,
    "Painter Rosa Lin works in two very different ways. For portraits, she spends weeks on a single canvas, adding thin layers of paint one at a time. For her landscapes, she paints outdoors in one sitting, often finishing in under an hour to capture a particular light.",
    Q_STRUCT, ("It contrasts two ways the painter works.", "Slow layered portraits are set against fast outdoor landscapes."),
    ("It traces how the painter&rsquo;s style changed from slow, layered portraits to quick outdoor landscapes.", "Both methods are current; no change over time is described."),
    ("It ranks landscapes above portraits.", "No such judgment is made."),
    ("It explains how the painter decides whether a subject is better suited to a portrait or a landscape.", "How she chooses subjects is not discussed."))
rec('text_structure_purpose', 1,
    "Honeyguides are African birds that lead people to wild bees&rsquo; nests. <u>In parts of Mozambique, honey hunters call to the birds with a special trilling sound, and the birds respond far more often to that call than to other human sounds.</u> After the hunters open the nest and take the honey, the birds eat the leftover wax.",
    Q_FUNC, ("It suggests the birds recognize a specific signal.", "The birds respond more to the trill than to other sounds."),
    ("It explains why honeyguides eat the wax that honey hunters leave behind after opening a nest.", "Wax-eating is mentioned later and not explained."),
    ("It describes the method that honey hunters in Mozambique use to open bees&rsquo; nests safely.", "Opening nests is mentioned in the next sentence and not described."),
    ("It argues that honey hunting harms bees.", "No harm is discussed."))
# ---- hard
rec('text_structure_purpose', 2,
    "Economists often assume that when two stores sell identical products, the cheaper store will win customers. Yet shoppers routinely pay more at a store they already know. <u>Part of the explanation is that comparing prices takes time and effort, costs that do not appear on any receipt.</u> Once those costs are counted, choosing the familiar store can be perfectly rational.",
    Q_FUNC, ("It names a hidden cost that makes the shoppers&rsquo; choice rational.", "Search costs explain why paying more can still be rational."),
    ("It confirms the economists&rsquo; assumption by showing that shoppers eventually switch to the cheaper store.", "The passage complicates the assumption; no switching is described."),
    ("It argues that shoppers who pay more at familiar stores are making an irrational choice they would regret.", "The conclusion is that the behavior can be rational."),
    ("It explains that stores raise their prices once they know shoppers will not compare them with competitors.", "How stores set prices is not discussed."))
rec('text_structure_purpose', 2,
    "Biologist Leah Stone first noticed that a species of wildflower in her study area bloomed nearly two weeks earlier than records from the 1950s described. She then checked herbarium specimens&mdash;pressed flowers collected over the past century, each labeled with its collection date&mdash;and found that the shift had occurred gradually, tracking a rise in spring temperatures. Stone cautions that herbarium collections were not designed for such studies, but she argues that they remain one of the few long-term records available.",
    Q_STRUCT, ("It reports an observation, a test using old records, and the limits and value of those records.", "Observation, herbarium evidence, then caution and defense of the method."),
    ("It presents a hypothesis about wildflowers, reports evidence that disproves it, and proposes a new explanation.", "Nothing is disproved; the records confirm a gradual shift."),
    ("It compares two species of wildflower and uses herbarium specimens to explain why one blooms earlier.", "Only one species is studied over time."),
    ("It criticizes herbarium collections as unreliable and recommends that biologists rely on field observations instead.", "Stone defends the collections&rsquo; value despite their limits."))
rec('text_structure_purpose', 2,
    "The following text is adapted from a 1915 essay.<br><br>We are told that the modern city has made neighbors into strangers. There is truth in this. Yet the same crowded streets that let a man pass a thousand faces unnoticed also let him find, among those thousands, the three or four who share his odd enthusiasm for beetles or Byzantine coins. <u>The village offers intimacy with everyone; the city offers it with the right few.</u>",
    Q_FUNC, ("It sums up the essay&rsquo;s qualified view of what each setting offers.", "It balances the village&rsquo;s broad intimacy against the city&rsquo;s selective one."),
    ("It rejects the claim that the city makes neighbors into strangers by arguing that city dwellers know everyone.", "The essay concedes there is truth in that claim, and the city offers intimacy only with a few."),
    ("It argues that villages are better than cities.", "It does not rank the two settings."),
    ("It introduces a new topic, the collecting of beetles and coins, that the essay will go on to discuss.", "It concludes the preceding argument; the hobbies are examples."))
rec('text_structure_purpose', 2,
    "Critics of standardized recipes argue that precise measurements stifle cooks&rsquo; creativity. Food historian Nadia Farouk takes a different view. <u>She notes that the first cookbooks to give exact quantities were written for readers who had never watched an experienced cook at work and so had no other way to learn.</u> For such readers, Farouk argues, precision was not a constraint but an invitation.",
    Q_FUNC, ("It gives historical context that supports Farouk&rsquo;s challenge.", "It explains who the first precise recipes served, backing her claim."),
    ("It concedes that the critics are right that exact quantities kept early readers from cooking creatively.", "Farouk takes a different view; the sentence supports it."),
    ("It describes the dishes in the first cookbooks that gave exact quantities and explains how they were made.", "The recipes themselves are not described."),
    ("It explains why experienced cooks of the period refused to use cookbooks that listed precise measurements.", "Experienced cooks&rsquo; views are not discussed."))
rec('text_structure_purpose', 2,
    "Planetary scientists long assumed that Mars&rsquo;s thin atmosphere had been lost early in the planet&rsquo;s history. Measurements from an orbiting spacecraft now indicate that the solar wind continues to strip gas from the upper atmosphere today, at a rate that increases sharply during solar storms. The findings do not show that this process alone thinned the atmosphere, but they identify a mechanism that could have done so over billions of years.",
    Q_PURPOSE, ("To report evidence of a process that may explain Mars&rsquo;s lost atmosphere, noting its limits.", "It presents the finding and the caution that it does not prove sole cause."),
    ("To show that solar storms alone stripped away Mars&rsquo;s atmosphere early in the planet&rsquo;s history.", "The passage says the findings do not show that this process alone did it."),
    ("To argue that Mars had a thicker atmosphere than Earth until the solar wind began to strip it away.", "Earth is never compared."),
    ("To explain how an orbiting spacecraft measures the rate at which gas escapes from a planet&rsquo;s upper atmosphere.", "Measurement methods are not described."))
rec('text_structure_purpose', 2,
    "In many novels, a storm arrives just as the characters&rsquo; conflict peaks, as if the weather were responding to them. Critics have called this device, sometimes termed the pathetic fallacy, a crude shortcut. Scholar Idris Bello argues that in the hands of skilled writers it works differently: the storm often mirrors not what the characters feel but what they refuse to feel, so the weather speaks the emotion the dialogue suppresses.",
    Q_STRUCT, ("It names a device, notes a criticism, and gives a scholar&rsquo;s reinterpretation.", "Device, critics&rsquo; view, then Bello&rsquo;s alternative reading."),
    ("It traces the device&rsquo;s history.", "No history is traced."),
    ("It lists several novels that use storms at moments of conflict and ranks them by how skillfully they do so.", "No novels are named or ranked."),
    ("It explains what causes storms and then compares realistic weather in novels with the pathetic fallacy.", "No scientific explanation is given."))
rec('text_structure_purpose', 2,
    "A common explanation for why zebras have stripes is that the pattern confuses predators. Field studies, however, have found little evidence that lions or hyenas are confused by stripes. <u>In contrast, experiments with horses dressed in striped coats found that biting flies landed on them far less often than on horses in plain coats.</u> Many researchers now favor fly deterrence as the stripes&rsquo; main function.",
    Q_FUNC, ("It supports an alternative after the common explanation is questioned.", "The fly experiment supports the explanation researchers now favor."),
    ("It provides further support for the idea that stripes protect zebras by confusing lions and hyenas.", "It supports a different explanation."),
    ("It explains that horses and zebras are closely related, so experiments on one apply to the other.", "Their relationship is not discussed."),
    ("It shows that zebras are rarely bitten by flies because the plants they eat make them unappealing to insects.", "Diet is not mentioned; stripes are the factor."))
rec('text_structure_purpose', 2,
    "Twentieth-century histories of science often celebrated lone geniuses. Historian Ana Kowalczyk argues that this emphasis obscures the work of instrument makers, whose telescopes, thermometers, and balances made many discoveries possible. She points out that when astronomers disputed an observation, the argument often turned on whose instrument could be trusted. For Kowalczyk, then, the history of science is also a history of craft.",
    Q_PURPOSE, ("To present an argument that instrument makers&rsquo; role in discovery has been overlooked.", "The passage builds Kowalczyk&rsquo;s case for the importance of instrument craft."),
    ("To argue that famous scientists deserve less credit for their discoveries than the instrument makers who assisted them.", "She broadens the story rather than taking credit away."),
    ("To explain how telescopes, thermometers, and balances were made and why some were more trusted than others.", "How the instruments were made is not explained."),
    ("To describe a specific dispute between two astronomers and explain which of their instruments was more accurate.", "Disputes are mentioned in general, not a specific one."))

# =============================================================== COMMAND OF EVIDENCE: TEXTUAL
# ---- easy
rec('coe_textual', 0,
    "Nutrition researcher Ivan Petrov claims that eating breakfast helps students concentrate during morning classes.",
    Q_SUP, ("Students who ate breakfast scored higher on morning attention tests.", "It links breakfast directly to better concentration in the morning."),
    ("Students who ate breakfast were more likely than other students to eat a full lunch later in the day.", "Lunch habits say nothing about concentration."),
    ("Most students prefer cereal to eggs.", "Food preference does not address concentration."),
    ("Students who skipped breakfast on school days tended to sleep later on weekends than other students.", "Weekend sleep is unrelated to morning concentration."))
rec('coe_textual', 0,
    "City planner Grace Obi claims that adding bike lanes to Main Street will increase the number of people who bike to work.",
    Q_WEAK, ("Similar bike lanes in nearby cities did not change the number of bike commuters.", "If similar lanes elsewhere had no effect, Obi&rsquo;s prediction is less likely."),
    ("Many residents who drive to work said in a survey that they would bike if they felt safer on Main Street.", "This supports the claim."),
    ("In another city that added bike lanes to its main street, the number of bike commuters rose sharply.", "This supports the claim."),
    ("Main Street carries more car traffic than any other road in the city during the morning rush hour.", "Traffic volume alone does not weaken the claim."))
rec('coe_textual', 0,
    "The following text is from a 1906 novel.<br><br>Ben is a boy who is described as unusually curious about how things work.",
    Q_QUOTE, ("&ldquo;He took apart his father&rsquo;s watch to see what made it tick.&rdquo;", "Taking apart a watch to see how it works shows curiosity about mechanisms."),
    ("&ldquo;He liked to sit by the river for hours and watch the steamboats go by on their way downstream.&rdquo;", "Watching boats is not about how things work."),
    ("&ldquo;He was the tallest boy in his class.&rdquo;", "Height is unrelated to curiosity."),
    ("&ldquo;He always finished his supper before his sisters and asked politely to leave the table.&rdquo;", "This says nothing about curiosity."))
rec('coe_textual', 0,
    "A zoologist hypothesizes that elephants can recognize the voices of elephants from their own family group.",
    Q_SUP, ("Elephants moved toward recordings of family members but ignored recordings of strangers.", "Different reactions to family and strangers show recognition."),
    ("Elephants made loud, low calls whenever their family group arrived at a watering hole together.", "Calling at a watering hole does not show recognition of voices."),
    ("Elephant family groups usually travel together and are led by the oldest female in the group.", "Traveling together does not show voice recognition."),
    ("Young elephants in family groups drank more water each day than older elephants in the same groups.", "Water intake is unrelated."))
rec('coe_textual', 0,
    "A school principal claims that the new longer lunch period has reduced the number of students who feel rushed while eating.",
    Q_SUP, ("Far fewer students said they felt rushed at lunch after the change.", "This directly measures feeling rushed before and after."),
    ("The cafeteria added two new menu items this year, and both have become popular with students.", "Menu items do not show whether students feel rushed."),
    ("Most students eat with the same friends.", "Seating habits do not address feeling rushed."),
    ("Because of the longer lunch period, the school day now ends ten minutes later than it did last year.", "This does not show how students feel at lunch."))
rec('coe_textual', 0,
    "A marine biologist claims that a coral reef near Lanai Island has begun to recover from damage caused by a storm.",
    Q_SUP, ("Surveys found more living coral this year than in the two years after the storm.", "Increasing living coral shows recovery."),
    ("The storm that damaged the reef was the strongest to hit Lanai Island in more than fifty years.", "This describes the damage, not recovery."),
    ("Tourists often visit the reef near Lanai Island to snorkel and to photograph its colorful fish.", "Tourism does not show recovery."),
    ("The reef near Lanai Island is home to more than a hundred species of fish and many kinds of coral.", "A count at one time does not show change."))
rec('coe_textual', 0,
    "A researcher claims that a new type of window glass keeps homes cooler in summer.",
    Q_WEAK, ("Homes with the new glass were no cooler in summer than similar homes with ordinary glass.", "If there is no temperature difference, the glass does not keep homes cooler."),
    ("The new glass costs more than ordinary glass, so few homeowners have installed it so far.", "Cost does not affect whether it keeps homes cooler."),
    ("Homes with the new glass used less air conditioning during the summer than similar homes did.", "This supports the claim."),
    ("The new glass blocks more of the sun&rsquo;s heat than ordinary glass does on bright summer days.", "This would tend to support the claim."))
rec('coe_textual', 0,
    "The following text is from a 1912 short story.<br><br>Grandmother Hale is described as a generous person.",
    Q_QUOTE, ("&ldquo;Whatever she baked, she gave half of it away to the neighbors.&rdquo;", "Giving away half of her baking shows generosity."),
    ("&ldquo;She woke every morning before the sun rose and walked the long way around the pond.&rdquo;", "Waking early is not generosity."),
    ("&ldquo;She kept her garden neat.&rdquo;", "Neatness and pride are not generosity."),
    ("&ldquo;She had lived in the same house on Elm Street for sixty years and knew every family on it.&rdquo;", "Knowing her neighbors is not generosity."))
# ---- medium
rec('coe_textual', 1,
    "Psychologist Amara Nwosu hypothesizes that people remember information better when they explain it aloud to someone else than when they simply reread it.",
    Q_SUP, ("People who explained a passage to a partner recalled more of it a week later than people who reread it for the same time.", "It compares explaining with rereading for the same time and finds better recall."),
    ("Participants who reread a passage said they enjoyed the task more than participants who explained it.", "Enjoyment does not measure memory."),
    ("Participants who explained a passage spoke for an average of five minutes before their partner asked questions.", "Duration of speaking says nothing about recall."),
    ("Participants in both groups recalled more of a short passage than of a long passage a week later.", "Passage length does not compare the two study methods."))
rec('coe_textual', 1,
    "Historian Paul Mensah argues that a certain 1850s diary, long attributed to a ship&rsquo;s captain, was actually written by the captain&rsquo;s wife, who sailed with him.",
    Q_SUP, ("The diary covers days at sea when the captain&rsquo;s log shows he was ashore.", "The diarist was aboard when the captain was not, pointing to someone else, such as his wife."),
    ("The diary describes in detail several storms that the ship encountered while crossing the Atlantic.", "Anyone aboard could describe storms."),
    ("The captain kept careful records.", "This fits the old attribution, if anything."),
    ("Diaries were commonly kept by passengers and officers on long sea voyages during the 1850s.", "A general fact does not identify this diary&rsquo;s author."))
rec('coe_textual', 1,
    "Agricultural scientist Lucia Moreno claims that planting clover between rows of vegetables improves soil fertility enough to raise vegetable yields.",
    Q_WEAK, ("Clover raised soil nitrogen in a three-year trial but did not raise vegetable yields.", "Fertility rose but yields did not, undercutting the claim that clover raises yields."),
    ("Clover plants add nitrogen to the soil through bacteria that live in small growths on their roots.", "This explains how clover could help and supports the claim."),
    ("Farmers who planted clover between rows of vegetables reported spending less time pulling weeds.", "Fewer weeds would tend to support better yields."),
    ("Vegetable yields on all of the trial&rsquo;s plots rose and fell from year to year along with rainfall.", "Year-to-year variation affects both kinds of plots and does not undercut the claim."))
rec('coe_textual', 1,
    "The following text is from a 1917 novel.<br><br>In the novel, Mr. Crane is portrayed as a man whose cheerful manner hides deep loneliness.",
    Q_QUOTE, ("&ldquo;He laughed loudest at every dinner, then walked home to rooms where no one waited.&rdquo;", "It pairs outward cheer with a lonely home life."),
    ("&ldquo;He told the same three jokes at every dinner party, and the guests laughed at them each time as if they were new.&rdquo;", "This shows cheer but no loneliness."),
    ("&ldquo;He had lived alone on the second floor of Mrs. Dwyer&rsquo;s boarding house since the spring of 1899.&rdquo;", "Living alone is not necessarily loneliness, and no cheerful manner is shown."),
    ("&ldquo;He worked as a clerk at the county courthouse, where he was known for his neat handwriting.&rdquo;", "His job reveals neither trait."))
rec('coe_textual', 1,
    "An economist claims that a city&rsquo;s new tax on sugary drinks reduced residents&rsquo; consumption of those drinks.",
    Q_WEAK, ("Sales just outside the city rose about as much as sales inside it fell.", "Residents may have bought the drinks elsewhere, so consumption may not have fallen."),
    ("Sales of sugary drinks in stores inside the city fell sharply in the year after the tax took effect.", "This supports the claim."),
    ("In a survey, some residents said they had been drinking more water since the tax was introduced.", "This mildly supports the claim."),
    ("Other cities have similar taxes.", "This does not bear on this city&rsquo;s consumption."))
rec('coe_textual', 1,
    "Ornithologist Kwame Asante hypothesizes that city-dwelling great tits sing at a higher pitch than forest-dwelling ones because higher notes are easier to hear over low-pitched traffic noise.",
    Q_SUP, ("City great tits sang higher on noisy weekday mornings than on quiet Sundays.", "Pitch rose with traffic noise within the same birds, linking pitch to noise."),
    ("City great tits were, on average, slightly smaller and lighter than great tits living in nearby forests.", "Size does not address the noise explanation."),
    ("Forest great tits sang more often in the spring breeding season than they did in autumn or winter.", "Seasonal frequency is not about pitch and noise."),
    ("Both city and forest great tits fed mainly on insects and caterpillars during the breeding season.", "Diet is unrelated to song pitch."))
rec('coe_textual', 1,
    "A literary scholar argues that the poet Edith Crane revised her poems to make them less formal over the course of her career.",
    Q_SUP, ("Crane&rsquo;s later drafts swap words like &ldquo;thee&rdquo; and &ldquo;whilst&rdquo; for &ldquo;you&rdquo; and &ldquo;while.&rdquo;", "Replacing formal words with plain ones in revisions shows movement toward informality."),
    ("Crane wrote and published many more poems in the last decade of her career than she did in her first.", "Quantity says nothing about formality."),
    ("Several of Crane&rsquo;s early poems were published in well-known literary magazines of the period.", "Publication does not show a change in style."),
    ("Crane often wrote poems about rivers, forests, and the changing seasons throughout her career.", "Subject matter is unrelated to formality."))
rec('coe_textual', 1,
    "A team of engineers claims that their new bridge sensor can detect small cracks before they become visible to inspectors.",
    Q_SUP, ("The sensor flagged cracks months before inspectors could see them.", "It shows detection preceding visibility."),
    ("The new sensor is smaller, lighter, and less expensive to install than earlier models of bridge sensors.", "Size and cost do not show detection ability."),
    ("Inspectors in most states examine each highway bridge in person at least once every two years.", "Inspection schedules do not show what the sensor detects."),
    ("The sensor is used in three states.", "Installation does not show performance."))
# ---- hard
rec('coe_textual', 2,
    "Anthropologist Sara Lindqvist argues that a set of carved bones found at a prehistoric site were used as tallies to record the phases of the moon, not merely as decorations.",
    Q_SUP, ("The notches fall into groups of 29 or 30, the days in a lunar cycle, set off by marks of a different shape.", "Groupings that match lunar months, with distinct separators, suggest counting rather than decoration."),
    ("The bones come from animals such as reindeer and horses that were commonly hunted by people living near the site.", "The animal source does not bear on the notches&rsquo; purpose."),
    ("Decorative carvings with similar notches have been found on pottery from the same period at the site.", "This, if anything, supports the decoration interpretation."),
    ("Microscopic analysis shows that the notches were cut with a sharp stone tool rather than with a bone or antler tool.", "The tool does not reveal the purpose."))
rec('coe_textual', 2,
    "Some researchers claim that a certain medication improves memory in older adults. In the study cited as evidence, adults who took the medication for a year scored higher on memory tests at the end of the year than they had at the start.",
    Q_WEAK, ("A placebo group tested over the same year improved just as much.", "If the placebo group improved just as much, the gain may come from practice with the tests, not the medication."),
    ("About one in ten participants who took the medication reported mild side effects such as headaches during the first month.", "Side effects do not bear on whether memory improved."),
    ("Participants averaged about 70 years old.", "Age and health alone do not challenge the finding."),
    ("The memory tests used in the study had been used in many earlier studies of adults over the age of sixty.", "Wide use of the tests does not weaken the result."))
rec('coe_textual', 2,
    "The following text is from a 1922 novel.<br><br>Throughout the novel, the narrator suggests that Mrs. Arden values her reputation in the village more than her own comfort.",
    Q_QUOTE, ("&ldquo;The cold chapel set her coughing, but she never missed a Sunday, for the village noted who was absent.&rdquo;", "She endures discomfort because the village notices absences."),
    ("&ldquo;Mrs. Arden kept a fire burning in every room of the house from the first frost in October until the lilacs bloomed in May.&rdquo;", "This shows concern for comfort, not reputation."),
    ("&ldquo;The villagers spoke of Mrs. Arden as a woman of good family, firm opinions, and a very long memory for slights.&rdquo;", "It shows her reputation but not a trade-off with comfort."),
    ("&ldquo;Mrs. Arden rarely visited the village shops herself, preferring to send her maid with a carefully written list.&rdquo;", "This does not weigh reputation against comfort."))
rec('coe_textual', 2,
    "Political scientist Leon Ferreira claims that local newspapers help keep municipal governments efficient. He notes that after a town&rsquo;s newspaper closes, the town&rsquo;s borrowing costs tend to rise, which he attributes to reduced scrutiny of officials.",
    Q_SUP, ("Borrowing costs rose where papers closed but held steady in similar nearby towns whose papers stayed open.", "A matched comparison rules out region-wide trends and points to the closure."),
    ("Borrowing costs for towns rose across the entire country during the period that Ferreira studied.", "A national rise would weaken the link to newspaper closures."),
    ("Many local newspapers closed during the period because advertisers moved their spending to websites.", "The cause of closures does not show their effect on government."),
    ("Residents who read a local newspaper are more likely than other residents to vote in town elections.", "This is related but does not bear on borrowing costs."))
rec('coe_textual', 2,
    "A paleontologist hypothesizes that a certain species of small dinosaur hunted at night.",
    Q_SUP, ("Its eye sockets and scleral rings match those of modern night-active animals.", "Eye structures matching nocturnal animals are direct anatomical evidence."),
    ("Its fossils appear on two continents.", "Geographic range says nothing about activity time."),
    ("The species had sharp, curved teeth and grasping claws suited to catching and eating small animals.", "It shows hunting, but not hunting at night."),
    ("Several other small dinosaurs that lived in the same region and period were active mainly during the day.", "Other species&rsquo; habits do not show this one&rsquo;s."))
rec('coe_textual', 2,
    "Urban economist Jae-won Park argues that a city&rsquo;s new light-rail line increased property values near its stations, pointing to a 12 percent rise in home prices within half a mile of stations in the two years after the line opened.",
    Q_WEAK, ("Home prices rose about 12 percent citywide, even far from any station.", "If prices rose equally everywhere, the rail line likely did not cause the rise near stations."),
    ("Neighbors complained about construction noise.", "Complaints do not undercut the price data."),
    ("In its first year of service, ridership on the new light-rail line was about 20 percent higher than projected.", "Ridership does not address property values."),
    ("Homes within half a mile of the stations were, on average, older and smaller than homes elsewhere in the city.", "Home age and size do not explain away the rise."))
rec('coe_textual', 2,
    "The following text is from a 1919 poem. The poem&rsquo;s speaker is described as feeling both grateful for and burdened by a family inheritance.",
    Q_QUOTE, ("&ldquo;I bless the hands that left me this old house, / and curse the roof I cannot keep from rain.&rdquo;", "Blessing the giver shows gratitude; failing to keep up the roof shows burden."),
    ("&ldquo;The house stands where my grandfather built it, / facing the long field and the road that leads to town.&rdquo;", "This describes the house but no feeling."),
    ("&ldquo;I walk each room at evening when the light is low, / and every room is still, and every room is mine.&rdquo;", "It suggests quiet ownership, not gratitude and burden."),
    ("&ldquo;My brothers went to the city for work and wages; / I stayed and learned the names of trees.&rdquo;", "It describes a choice, not feelings about the inheritance."))
rec('coe_textual', 2,
    "Materials scientist Ines Duarte hypothesizes that a new coating prevents ice from forming on aircraft wings mainly by repelling water droplets before they can freeze, rather than by lowering the freezing point of water on the surface.",
    Q_SUP, ("Droplets bounced off coated surfaces within milliseconds, yet water froze at the same temperature on coated and uncoated ones.", "Droplets are repelled and the freezing point is unchanged, favoring Duarte&rsquo;s mechanism."),
    ("In wind-tunnel tests, wings with the coating accumulated far less ice than uncoated wings under identical conditions.", "This shows the coating works but not by which mechanism."),
    ("Water placed on the coated surfaces froze at a lower temperature than water placed on uncoated surfaces.", "This supports the alternative mechanism."),
    ("The coating remained effective at preventing ice after hundreds of flights through cold, wet clouds.", "Durability does not address the mechanism."))
