import os
import streamlit as st
from openai import OpenAI
import json
import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
import PyPDF2
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter


def get_response(chapter, font_size, lineheight):
  # Set up OpenAI API client
    
  client = OpenAI(api_key = st.secrets["Openai_api"])
  font_size_px = f"{font_size}px"
  line_height_val = str(lineheight)
  max_chars = 37000
  # Set up OpenAI model and prompt
  model="gpt-4o-mini-2024-07-18"
  # Split the chapter into two parts based on character count
  if len(chapter) <= max_chars:
    # If the chapter is within the limit, process normally
    prompt_template = """You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.

I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.
The morning after another such bizarre and blurry night, he woke up with a splitting
headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
clutching his guitar and his journal close to him, pouring his grief into writing a song, but
even creating new music reminded him of her. How they spent so many afternoons in his
basement studio recording covers of their favourite Coldplay songs, after which she would
drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.
To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
covered his gullible boyish charm, making him look jagged and intimidating. He spent most
of his time holed up in his room. The only time he left the house was to hit the gym. His
social circle diminished and his grades began falling quickly.
Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
favourite. Lead guitarist at the college band, straight As with an impressive academic record,
broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
going for him. Until he met the stunning Anisha Singhania.
She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
rain, but before he knew it, he had been struck by lightning.
In the summer of his pre-final year at engineering college, when he was conducting auditions
for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him.
&quot;Hey, I&#39;m Anisha.&quot; She extended her hand.
&quot;Hi! I’m Dhruv,&quot; he responded softly and shook hands with her. He couldn&#39;t help but notice
the striking manicured nails polished with a deep black color.
&quot;I have heard a lot about you.” she said with a strikingly odd smile.
“Oh is that so?” He appeared visibly embarrassed.
“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
little myself. And I was wondering if I could join the band too.&quot;
&quot;Thank you, that&#39;s very kind of you. You&#39;re welcome to the auditions.&quot;
&quot;Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
turn is in half an hour, so I thought it&#39;d be a good use of time to get to know one of the finest
seniors in college.&quot;
&quot;That&#39;s really kind of you. I&#39;d love to catch up, but I&#39;m sorry, I need to focus on these
auditions right now.&quot; He shrugged and excused himself.
&quot;No worries. It was nice talking to you.&quot;
&quot;All the best for the audition, Anisha,&quot; he said with a placid smile.

Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
couple of times, she caught him stealing glances at her and returned an alluring smile.
Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
performance. And then as her name was announced, she walked up to the stage, gazing
fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.
&quot;You could buy me diamonds
You could buy me pearls
Take me on a cruise around the world
Baby, you know I&#39;m worth it...”
Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
there, she was literally ‘worth it’.
Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
Just then his phone vibrated to notify Anisha&#39;s friend request on Facebook.
&quot;Who is it?&quot; Arnav enquired.
&quot;Well remember that girl, Anisha, from the auditions today?&quot;
&quot;Yeah, the hot chick who sang, &#39;A woman’s worth&#39;?&quot;
&#39;Yep. It&#39;s her friend-request.&quot;
&quot;Dude, I saw how she was talking to you. She is totally into you.&quot;
&quot;Well let’s not jump to conclusions. It’s just a friend request.”
“That’s her move.”
“Well she could simply be interested in friendship. But she sure is very hot though.&quot;
&quot;Well for starters, you don&#39;t look like a pig yourself.”
“Way to make a guy feel good about himself.” Dhruv smirked.
“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
you&#39;re quite a catch, so go for it!&quot; Arnav said to him sarcastically while grabbing his phone
from his hands and checking out Anisha&#39;s Facebook profile.
&quot;Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.
Arnav rolled his eyes and continued stalking her profile.
Dhruv looked at him with a slackened expression and accepted the friend request.
In less than five minutes his phone buzzed again. This time it was a message from her. He
opened his phone to a, &quot;Hey! How&#39;re you doing?&quot;
&quot;See? So what happened to Mr Righteous, Let&#39;s not generalise and jump to conclusions&#39;,
Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
intellectual side for her!&quot; He joked.

“As you say, sir!” Dhruv resigned to his friend’s comments.
&quot;Good! Now you have fun with your new and smoking hot endeavours.&quot; Arnav smirked
bidding his goodbye.
&quot;See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
phone and checked out Anisha&#39;s profile. Her display picture was a stunning portrait of her
clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv&#39;s attention before
another message from her popped up on the screen.
&quot;Hey! Are you there?&quot; her message read.
Dhruv opened the chat box to text her back.
&quot;Hey! What&#39;s up?&quot;
&quot;Nothing much. Was listening to some classical jazz.&quot;
&quot;Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.&quot;
&quot;You do? I thought only girls dig those kinds of songs,&quot; Anisha replied.
&quot;I am a huge fan of Sinatra and a lot of other artists from that time. I think if you&#39;re
passionate about music, then you tend to appreciate good work, irrespective of the genre or
the artist. Besides, those are classics,&quot; Dhruv typed.
&quot;Oh, I think I am talking to a proper musician here.&quot; she added a few blushing emojis.
“Haha come on, you’re embarrassing me.&quot;
&quot;You know what&#39;s better than a passionate musician?&quot;
&quot;What?&quot;
&quot;A modest one.&quot;
&quot;Hahaha! Is that so?&quot;
&quot;Oh, it is so. Anyway, who&#39;s your favourite artist or band?&quot; she asked.
&quot;Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
too.&quot;
&quot;Ahh, ‘Tears in heaven’!&quot;
&quot;Oh, it transports me to another world every time I listen to it. In fact I was planning on
doing a cover on it tomorrow.&quot;
&quot;Really? If you don&#39;t mind, can I join? Like I won&#39;t sing, but I can help, you know?&quot;
&quot;Yeah, sure. That&#39;d be great.&quot;
&quot;Perfect, when and where?&quot;
&quot;Umm… tomorrow, my place, around six?&quot;
&quot;Sounds great. I can&#39;t wait!&quot;

&quot;Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
Alicia Keys is phenomenal, and you did absolute justice to her.&quot;
&quot;Did I? I thought I blew it.&quot;
&quot;Are you kidding me? No, you had the whole crowd going crazy over your voice.&quot;
&quot;Oh really, you too?&quot;
Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
emoji.
The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
half an hour, they spent the rest of the two hours hanging out in his room and talking about
everything from college, the band, music, career plans and dream cities.
“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
small and big city, and perform at every stage. Have my voice be heard.”
“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”
“What do you want to do?”
“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
with anything but the best. And then once I have my MBA degree, he’d rather have me join
the family business. Try to digitise things and expand to newer markets.”
“You just told me what your dad wants. I asked you, ‘What do you want?’”
He looked at her and let out a deep breath.
“Well, I want to build a life of my own.”
“And what does that life look like?”
“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”
“That’s so abstract.”
“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
I want to have meaningful relationships and experience life from different lenses. Travel
travel, but not to just see the world, but experience cultures and learn about people and what
drives them.”
“Your plan sounds so fancy and existential at the same time. How do you do it?”
“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”
“Hmm”
“Have you watched Before Sunrise?”
“No.”
“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”
Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
created by the dilapidated rooftops of neighbourhood houses.
“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
than he loved any of us…”
You know, I loved him the most. And when he passed away, I was a total wreck. I began
hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
him, I stopped eating, studying, everything. Can you be mad at the dead?&quot; she asked, but
Dhruv had no answers. He barely processed Anisha&#39;s confessions. He had no idea she cloaked
such things behind her cheery demeanour.
&quot;It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
his old white shirt.
On the evening of 3 rd September, I drove to the small cliff ten kilometres down from our Goa
house. I barely knew how to drive, but anger makes you do strange things.
Before leaving, I had grabbed the last pack of cigarettes from dad&#39;s belongings and there at
the cliff, I stood by the sea and lit my first ever cigarette. I still don&#39;t know why I did it.

I think I did it partly because I was mad at him and wanted those cigarettes to consume me
the same way. And partly because I felt it was the last thing that connected me to dad, the one
thing he couldn&#39;t give up. I embraced it as a part of my life. Every time I smoke now; it
reminds me of him. And I hate it. But I also love it. And I miss him.&quot; She completed her
monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
with his index finger.
She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
looked at her, and he couldn&#39;t help but think that the more he got to know her, the more of a
mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
cigarette between her index and middle finger and stuck out her hand in his direction to offer
him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
exchanging a single word, they sat there smoking late into the evening, until the entire place
got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
body, and he could feel his lips slowly brush against hers. She tasted like coffee and
cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other&#39;s smoke-
stained breath.

****

For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
terrace when she opened up about her childhood, things quickly picked up between them.
And before he knew it, every small and big thing about her seemed extraordinary to him. Her
passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
inappropriate times and then suddenly shifting gears to share a deeply personal childhood
story and always lighting a smoke while she told it.
In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
with her. They began bunking classes and hanging out at a tapri near college, smoking
cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
Delhi to explore the food scene, visit local pubs, art galleries and old architectural
monuments.
On her birthday, he planned a surprise terrace party at his place and invited all their friends.
She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
and a big custom cake that had a picture of her singing at the band auditions.
“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
my life.” They cut the cake, got drunk on cheap tequila and danced the night away.
As their social circle expanded, they began getting more invites to parties of common friends,
where they went as a couple. But oftentimes Anisha would just be outside in the smoking
zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
with someone she borrowed a lighter from.
“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
lent her the lighter, had asked her.

“Why?” She inquired bright-eyed.
“I’d love to take you out for coffee. I know a really nice place here.”
She took a moment and smiled, as though assessing the situation.
“Is there so much to think about?” He smirked.
She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
won’t hurt anyone.”
Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
seeing Anisha work her way through all these social events, getting enormously drunk and
dancing voluptuously with many strange, new men. At first, he thought he was being too
sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
concerned, and hoped she would come around. But when he confronted her, he was only met
with contempt and accusations of being an overprotective and jealous boyfriend.
He started feeling increasingly anxious when Anisha wasn&#39;t around. And ever since he had
heard from a couple of common friends that Anisha got so wasted at a party, she puked for
two hours straight, he started showing up at parties he wasn&#39;t even invited to, just to take care
of her, drive her home safe and make sure she didn’t do something that she would regret
later.
To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
Kunj, pretty near to Dhruv&#39;s place, but he still went all the way to pick up Anisha from her
hostel.
She was wearing a little black dress and high-heeled gladiators.
“Hi babe!” Dhruv smiled as she entered the car.
“Hey” she replied distantly as she adjusted the seat to make herself comfortable.
“You’re looking stunning tonight.”
“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”
Laughing at her own remark, she fixed the collar of his shirt.
Like always she began touching up her make-up in the mirror.
“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.
Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
to put it on silent.
“Who is it?”

“Some sales call or something, been getting too many of these lately.” She replied, visibly
bothered, and threw her phone back in her clutch in a haphazard manner.
“Then why are you so flustered?” He asked, eyes fixed on the road.
“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.
He pulled a tissue and offered it to her. She looked at him for a second and then took the
tissue reluctantly.
“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
her forehead and cheek.
“There’s water in the back if you want.”
“No. I am good. Thanks.”
After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
hear about the auditions that happened last week?”
“Uh hmm”she replied, still staring out the window.
“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
Avinash, I think.”
“Well, good for him.”
“I think the band is to see some great talent this year.”
“Yeah. I guess.”
“Anisha..”
“Hmm?”
“We met around the same time last year.”
“Yeah”
“You know, we owe this relationship to the band.”
“Maybe”
“Had you not come to audition, we probably wouldn’t have been dating.”
“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
are you so sentimental today?” she frowned and looked out the window.
“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.
“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
window.
“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”
“No. It’s fine. Let’s just go.”
“No, seriously? Whatever makes you feel better.”
“Honestly. Just getting there would make me feel better.” She snapped back.

They drove the rest of the way without exchanging a single word.
At the party, they received a warm welcome. Dhruv was among the senior-most members of
the band. A flock of junior boys and girls surrounded him.
After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
around to look for Anisha. Making his way past big crowds of people dancing and singing
loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
fuelled his worries. She never slipped away from a party without telling him. He didn&#39;t know
what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
and checked with a few people but nobody knew where she was.
All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
the restroom, he heard moaning sounds from the adjacent women&#39;s loo. A weird feeling rose
in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
door.
Dhruv received the shock of his life.
Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
seeing Dhruv standing over them.
Dhruv couldn&#39;t believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
hand and stepped back, incapable of letting her touch him.
She saw a burning rage in his eyes that she had never seen before.
&quot;Dhruv…&quot; she cried and ran after him as he raced down the stairs.
The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
premises and a weepy, guilt-ridden Anisha chasing him down the parking lot.
But before she could catch hold of him, Dhruv was already speeding off in his car. The
screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
down.
&quot;Dhruv…&quot; Anisha screamed in the middle of the street and wept inconsolably.

****

A whole week went by and Dhruv didn&#39;t show up at college at all. He barely picked calls
from any of his friends, and simply spent all his days and nights locked up in his room.
Sometimes the sound of a guitar echoing through his room was the only signal that he was
alive. Worried sick, Mrs Malhotra called Arnav.

“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness.
&quot;Oh Hi…I didn’t know you were coming.&quot; Dhruv got up, taken aback. His weight loss was
apparent. With a thickly grown unkempt beard, he looked shabbier than ever.
Arnav entered and switched on the lights.
Dhruv flinched. &quot;Ah, switch off the lights,&quot; He groaned.
&quot;No&quot;
&quot;Arnav…&quot;
&quot;Bro, you&#39;re a mess,&quot; he reprimanded, kicking him out of bed. &quot;That’s it. We’re going out
tonight. It&#39;s been ten days you haven&#39;t shown your stupid face to any of us.&quot;
&quot;Man, I don&#39;t feel like it.&quot;
&quot;I don&#39;t care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
friend Dhruv. Period.&quot;
&quot;What are your plans?&quot;
&quot;Clubbing!&quot;
&quot;Ugh! I don&#39;t want to go to a stupid club.&quot;
&quot;We&#39;ll get some booze, have some fun, meet some hot chicks and we&#39;ll get you over that
bitch.&quot;
&quot;You don&#39;t have to call her that.&quot; Dhruv shrugged.
&quot;She is a bitch.&quot; Arnav&#39;s face stiffened.
&quot;Arnav, please...&quot; Dhruv tried to raise his voice.
&quot;Okay, just go take a shower,&quot; Arnav resigned.
&quot;Arnav please, I swear I would have come, but I just don&#39;t feel like going out tonight.&quot;
&quot;Get your ass off this couch right now, trim your messy beard, take a shower, put on clean
clothes. We&#39;re going clubbing tonight. It&#39;s settled.&quot;
Dhruv protested, but before he could make an argument, Arnav shut him up and said, &quot;Listen,
dude, your &#39;sad boy vibe&#39; days are over. Enough of being this caveman. We&#39;re getting you
cleaned up and out on the scene tonight. The world has too many beautiful people. And it&#39;s a
shame you’re holed up in your room behaving like some psychopath. Stop wasting away your
youth and good looks, my friend. Carpe Diem!&quot; Arnav smirked and Dhruv hung his head low
in resignation.
“By the way, you stink,&quot; Arnav threw a towel on Dhruv’s face.
&quot;And, don&#39;t forget to shave that god-awful beard,&quot; he added.

Half an hour later, he emerged out of the bathroom looking like the same old Dhruv again.
The clean-shaven face highlighted his boyish features. On the inside though, Dhruv didn’t
feel any less miserable than before, but Arnav didn&#39;t give up on his friend.  He forced him
into the car, as they went on to pick up their other two friends from college Rohan and
Sameer.
Rohan had bought a new bottle of scotch. He raised a toast to Dhruv, &quot;Here&#39;s to our boy and
the return of his days of freedom and fun.&quot;
The night continued, hopping from nightclub to nightclub, drinking gallons of alcohol and
meeting new women. Dhruv got way too drunk in an attempt to wash away Anisha’s
memories. The more they flashed across his eyes, the more he drank in the hope to fade it all
out into nothingness. At one point, he barely recognized anything or anyone. It was all a giant
blur. Small fragments of consciousness kept escaping his mind like pieces of spatial matter
gallivanting across the sky. He felt like he was getting pulled into an expanding labyrinth and
his sense of self slowly continued sinking to newer lows.
Later in the night; he ended up sleeping with a slick woman who he’d met at the club a few
hours ago. The next morning, the memory of the night had almost vanished, but the hole in
his heart had widened.
This is the sample HTML : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 25vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    <p>The morning after another such bizarre and blurry night, he woke up with a splitting
    headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
    drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
    clutching his guitar and his journal close to him, pouring his grief into writing a song, but
    even creating new music reminded him of her. How they spent so many afternoons in his
    basement studio recording covers of their favourite Coldplay songs, after which she would
    drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
    that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.</p>
    <p>To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
    covered his gullible boyish charm, making him look jagged and intimidating. He spent most
    of his time holed up in his room. The only time he left the house was to hit the gym. His
    social circle diminished and his grades began falling quickly.</p>
    <p>Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
    favourite. Lead guitarist at the college band, straight As with an impressive academic record,
    broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
    going for him. Until he met the stunning Anisha Singhania.</p>
    <p>She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
    rain, but before he knew it, he had been struck by lightning.</p>

    <p>In the summer of his pre-final year at engineering college, when he was conducting auditions
    for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him. </p>
    <p>“Hey, I'm Anisha.” She extended her hand. </p>
    <p>“Hi! I’m Dhruv,” he responded softly and shook hands with her. He couldn't help but notice
    the striking manicured nails polished with a deep black color.</p>
    <p>“I have heard a lot about you.” she said with a strikingly odd smile.</p>
    <p>“Oh is that so?” He appeared visibly embarrassed.</p>
    <p>“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
    little myself. And I was wondering if I could join the band too.”</p>
    <p>“Thank you, that's very kind of you. You're welcome to the auditions.”</p>
    <p>“Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
    turn is in half an hour, so I thought it'd be a good use of time to get to know one of the finest
    seniors in college.” </p>
    <p>“That's really kind of you. I'd love to catch up, but I'm sorry, I need to focus on these
    auditions right now.” He shrugged and excused himself.</p>
    <p>“No worries. It was nice talking to you.”</p>
    <p>“All the best for the audition, Anisha,” he said with a placid smile.</p>

    <p>Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
    He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
    couple of times, she caught him stealing glances at her and returned an alluring smile. </p>
    <p>Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
    performance. And then as her name was announced, she walked up to the stage, gazing
    fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.</p>

    <div class="poetry">
    “You could buy me diamonds<br>
    You could buy me pearls<br>
    Take me on a cruise around the world<br>
    Baby, you know I'm worth it...”
    </div>

    <p>Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
    there, she was literally ‘worth it’. </p>
    <p>Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
    Just then his phone vibrated to notify Anisha's friend request on Facebook. </p>
    <p>“Who is it?” Arnav enquired.</p>
    <p>“Well remember that girl, Anisha, from the auditions today?”</p>
    <p>“Yeah, the hot chick who sang, ‘A woman’s worth’?”</p>
    <p>“Yep. It’s her friend-request.”</p>
    <p>“Dude, I saw how she was talking to you. She is totally into you.”</p>
    <p>“Well let’s not jump to conclusions. It’s just a friend request.”</p>
    <p>“That’s her move.”</p>
    <p>“Well she could simply be interested in friendship. But she sure is very hot though.”</p>
    <p>“Well for starters, you don’t look like a pig yourself.”</p>
    <p>“Way to make a guy feel good about himself.” Dhruv smirked.</p>
    <p>“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
    you're quite a catch, so go for it!” Arnav said to him sarcastically while grabbing his phone
    from his hands and checking out Anisha's Facebook profile.  </p>
    <p>“Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.</p>
    <p>Arnav rolled his eyes and continued stalking her profile.</p>
    <p>Dhruv looked at him with a slackened expression and accepted the friend request. </p>
    <p>In less than five minutes his phone buzzed again. This time it was a message from her. He
    opened his phone to a, “Hey! How’re you doing?”</p>
    <p>“See? So what happened to Mr Righteous, Let’s not generalise and jump to conclusions’,
    Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
    intellectual side for her!” He joked.</p>
    <p>“As you say, sir!” Dhruv resigned to his friend’s comments.</p>
    <p>“Good! Now you have fun with your new and smoking hot endeavours.” Arnav smirked
    bidding his goodbye.</p>
    <p>“See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
    phone and checked out Anisha's profile. Her display picture was a stunning portrait of her
    clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
    bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv's attention before
    another message from her popped up on the screen.</p>
    <p>“Hey! Are you there?” her message read.</p>
    <p>Dhruv opened the chat box to text her back. </p>
    <p>“Hey! What’s up?”</p>
    <p>“Nothing much. Was listening to some classical jazz.”</p>
    <p>“Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.”</p>
    <p>“You do? I thought only girls dig those kinds of songs,” Anisha replied.</p>
    <p>“I am a huge fan of Sinatra and a lot of other artists from that time. I think if you're
    passionate about music, then you tend to appreciate good work, irrespective of the genre or
    the artist. Besides, those are classics,” Dhruv typed.</p>
    <p>“Oh, I think I am talking to a proper musician here.” she added a few blushing emojis.</p>
    <p>“Haha come on, you’re embarrassing me.” </p>
    <p>“You know what's better than a passionate musician?”</p>
    <p>“What?”</p>
    <p>“A modest one.”</p>
    <p>“Hahaha! Is that so?”  </p>
    <p>“Oh, it is so. Anyway, who's your favourite artist or band?” she asked.</p>
    <p>“Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
    too.”</p>
    <p>“Ahh, ‘Tears in heaven’!”</p>
    <p>“Oh, it transports me to another world every time I listen to it. In fact I was planning on
    doing a cover on it tomorrow.”</p>
    <p>“Really? If you don't mind, can I join? Like I won't sing, but I can help, you know?”</p>
    <p>“Yeah, sure. That'd be great.”</p>
    <p>“Perfect, when and where?”</p>
    <p>“Umm… tomorrow, my place, around six?”</p>
    <p>“Sounds great. I can't wait!”</p>
    <p>“Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
    Alicia Keys is phenomenal, and you did absolute justice to her.” </p>
    <p>“Did I? I thought I blew it.”</p>
    <p>“Are you kidding me? No, you had the whole crowd going crazy over your voice.”</p>
    <p>“Oh really, you too?”</p>
    <p>Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
    emoji.</p>
    <p>The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
    in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
    half an hour, they spent the rest of the two hours hanging out in his room and talking about
    everything from college, the band, music, career plans and dream cities.</p>
    <p>“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
    small and big city, and perform at every stage. Have my voice be heard.”</p>
    <p>“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”</p>
    <p>“What do you want to do?”</p>
    <p>“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
    with anything but the best. And then once I have my MBA degree, he’d rather have me join
    the family business. Try to digitise things and expand to newer markets.”</p>
    <p>“You just told me what your dad wants. I asked you, ‘What do you want?’”</p>
    <p>He looked at her and let out a deep breath.</p>
    <p>“Well, I want to build a life of my own.”</p>
    <p>“And what does that life look like?”</p>
    <p>“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”</p>
    <p>“That’s so abstract.”</p>
    <p>“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
    I want to have meaningful relationships and experience life from different lenses. Travel
    travel, but not to just see the world, but experience cultures and learn about people and what
    drives them.”</p>
    <p>“Your plan sounds so fancy and existential at the same time. How do you do it?”</p>
    <p>“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”</p>
    <p>“Hmm”</p>
    <p>“Have you watched Before Sunrise?”</p>
    <p>“No.”</p>
    <p>“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
    time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”</p>
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    <p>Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
    created by the dilapidated rooftops of neighbourhood houses.</p>
    <p>“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
    than he loved any of us…”</p>
    <p>You know, I loved him the most. And when he passed away, I was a total wreck. I began
    hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
    him, I stopped eating, studying, everything. Can you be mad at the dead?” she asked, but
    Dhruv had no answers. He barely processed Anisha's confessions. He had no idea she cloaked
    such things behind her cheery demeanour. </p>
    <p>“It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
    even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
    his old white shirt.
    On the evening of 3rd September, I drove to the small cliff ten kilometres down from our Goa
    house. I barely knew how to drive, but anger makes you do strange things.
    Before leaving, I had grabbed the last pack of cigarettes from dad's belongings and there at
    the cliff, I stood by the sea and lit my first ever cigarette. I still don't know why I did it.</p>
    <p>I think I did it partly because I was mad at him and wanted those cigarettes to consume me
    the same way. And partly because I felt it was the last thing that connected me to dad, the one
    thing he couldn't give up. I embraced it as a part of my life. Every time I smoke now; it
    reminds me of him. And I hate it. But I also love it. And I miss him.” She completed her
    monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
    with his index finger.</p>
    <p>She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
    the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
    looked at her, and he couldn't help but think that the more he got to know her, the more of a
    mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
    cigarette between her index and middle finger and stuck out her hand in his direction to offer
    him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
    exchanging a single word, they sat there smoking late into the evening, until the entire place
    got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
    body, and he could feel his lips slowly brush against hers. She tasted like coffee and
    cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other's smoke-
    stained breath. </p>

    <p>****</p>

    <p>For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
    terrace when she opened up about her childhood, things quickly picked up between them.
    And before he knew it, every small and big thing about her seemed extraordinary to him. Her
    passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
    inappropriate times and then suddenly shifting gears to share a deeply personal childhood
    story and always lighting a smoke while she told it.</p>
    <p>In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
    usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
    with her. They began bunking classes and hanging out at a <i>tapri</i> near college, smoking
    cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
    Delhi to explore the food scene, visit local pubs, art galleries and old architectural
    monuments.</p>
    <p>On her birthday, he planned a surprise terrace party at his place and invited all their friends.
    She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
    and a big custom cake that had a picture of her singing at the band auditions.</p>
    <p>“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
    my life.” They cut the cake, got drunk on cheap tequila and danced the night away.</p>
    <p>As their social circle expanded, they began getting more invites to parties of common friends,
    where they went as a couple. But oftentimes Anisha would just be outside in the smoking
    zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
    with someone she borrowed a lighter from.</p>
    <p>“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
    lent her the lighter, had asked her.</p>
    <p>“Why?” She inquired bright-eyed.</p>
    <p>“I’d love to take you out for coffee. I know a really nice place here.”</p>
    <p>She took a moment and smiled, as though assessing the situation.</p>
    <p>“Is there so much to think about?” He smirked.</p>
    <p>She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
    won’t hurt anyone.”</p>
    <p>Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
    talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
    wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
    seeing Anisha work her way through all these social events, getting enormously drunk and
    dancing voluptuously with many strange, new men. At first, he thought he was being too
    sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
    lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
    concerned, and hoped she would come around. But when he confronted her, he was only met
    with contempt and accusations of being an overprotective and jealous boyfriend.</p>
    <p>He started feeling increasingly anxious when Anisha wasn't around. And ever since he had
    heard from a couple of common friends that Anisha got so wasted at a party, she puked for
    two hours straight, he started showing up at parties he wasn't even invited to, just to take care
    of her, drive her home safe and make sure she didn’t do something that she would regret
    later. </p>
    <p>To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
    Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
    Kunj, pretty near to Dhruv's place, but he still went all the way to pick up Anisha from her
    hostel.</p>
    <p>She was wearing a little black dress and high-heeled gladiators.</p>
    <p>“Hi babe!” Dhruv smiled as she entered the car.</p>
    <p>“Hey” she replied distantly as she adjusted the seat to make herself comfortable.</p>
    <p>“You’re looking stunning tonight.”</p>
    <p>“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
    for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”</p>
    <p>Laughing at her own remark, she fixed the collar of his shirt.</p>
    <p>Like always she began touching up her make-up in the mirror.</p>
    <p>“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.</p>
    <p>Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
    to put it on silent.</p>
    <p>“Who is it?”</p>
    <p>“Some sales call or something, been getting too many of these lately.” She replied, visibly
    bothered, and threw her phone back in her clutch in a haphazard manner.</p>
    <p>“Then why are you so flustered?” He asked, eyes fixed on the road.</p>
    <p>“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.</p>
    <p>He pulled a tissue and offered it to her. She looked at him for a second and then took the
    tissue reluctantly.</p>
    <p>“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
    her forehead and cheek.</p>
    <p>“There’s water in the back if you want.”</p>
    <p>“No. I am good. Thanks.”</p>
    <p>After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
    hear about the auditions that happened last week?”</p>
    <p>“Uh hmm”she replied, still staring out the window.</p>
    <p>“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
    Avinash, I think.”</p>
    <p>“Well, good for him.”</p>
    <p>“I think the band is to see some great talent this year.”</p>
    <p>“Yeah. I guess.”</p>
    <p>“Anisha..”</p>
    <p>“Hmm?”</p>
    <p>“We met around the same time last year.”</p>
    <p>“Yeah”</p>
    <p>“You know, we owe this relationship to the band.”</p>
    <p>“Maybe”</p>
    <p>“Had you not come to audition, we probably wouldn’t have been dating.”</p>
    <p>“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
    are you so sentimental today?” she frowned and looked out the window.</p>
    <p>“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.</p>
    <p>“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
    window.</p>
    <p>“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”</p>
    <p>“No. It’s fine. Let’s just go.”</p>
    <p>“No, seriously? Whatever makes you feel better.”</p>
    <p>“Honestly. Just getting there would make me feel better.” She snapped back. </p>
    <p>They drove the rest of the way without exchanging a single word.</p>
    <p>At the party, they received a warm welcome. Dhruv was among the senior-most members of
    the band. A flock of junior boys and girls surrounded him.</p>
    <p>After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
    around to look for Anisha. Making his way past big crowds of people dancing and singing
    loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
    surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
    his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
    fuelled his worries. She never slipped away from a party without telling him. He didn't know
    what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
    and checked with a few people but nobody knew where she was.</p>
    <p>All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
    the restroom, he heard moaning sounds from the adjacent women's loo. A weird feeling rose
    in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
    door. </p>
    <p>Dhruv received the shock of his life.</p>
    <p>Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
    seeing Dhruv standing over them.</p>
    <p>Dhruv couldn't believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
    whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
    support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
    hand and stepped back, incapable of letting her touch him.</p>
    <p>She saw a burning rage in his eyes that she had never seen before. </p>
    <p>“Dhruv…” she cried and ran after him as he raced down the stairs. </p>
    <p>The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
    silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
    premises and a weepy, guilt-ridden Anisha chasing him down the parking lot. </p>
    <p>But before she could catch hold of him, Dhruv was already speeding off in his car. The
    screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
    down. </p>
    <p>“Dhruv…” Anisha screamed in the middle of the street and wept inconsolably. </p>

    <p>****</p>

    <p>A whole week went by and Dhruv didn't show up at college at all. He barely picked calls
    from any of his friends, and simply spent all his days and nights locked up in his room.
    Sometimes the sound of a guitar echoing through his room was the only signal that he was
    alive. Worried sick, Mrs Malhotra called Arnav.</p>
    <p>“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
    the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
    the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness. </p>
    <p>“Oh Hi…I didn’t know you were coming.” Dhruv got up, taken aback. His weight loss was
    apparent. With a thickly grown unkempt beard, he looked shabbier than ever. </p>
    <p>Arnav entered and switched on the lights.</p>
    <p>Dhruv flinched. “Ah, switch off the lights,” He groaned. </p>
    <p>“No”</p>
    <p>“Arnav…”</p>
    <p>“Bro, you're a mess,” he reprimanded, kicking him out of bed. “That’s it. We’re going out
    tonight. It's been ten days you haven't shown your stupid face to any of us.”</p>
    <p>“Man, I don't feel like it.”</p>
    <p>“I don't care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
    friend Dhruv. Period.”</p>
    <p>“What are your plans?”</p>
    <p>“Clubbing!”</p>
    <p>“Ugh! I don't want to go to a stupid club.”</p>
    <p>“We'll get some booze, have some fun, meet some hot chicks and we'll get you over that
    bitch.”</p>
    <p>“You don't have to call her that.” Dhruv shrugged. </p>
    <p>“She is a bitch.” Arnav's face stiffened. </p>
    <p>“Arnav, please...” Dhruv tried to raise his voice. </p>
    <p>“Okay, just go take a shower,” Arnav resigned. </p>
    <p>“Arnav please,

    Here is the target chapter: <<CHAPTER_TEXT>>"""
    prompt = prompt_template.replace("<<CHAPTER_TEXT>>", chapter).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0
        )
    response = chat_completion.choices[0].message.content
    return response

  elif(len(chapter) > max_chars and len(chapter) <= 74000):
        # If the chapter exceeds the limit, split into two parts
        split_pos = chapter.rfind('.', 0, max_chars)
        first_part = chapter[:split_pos + 1]
        second_part = chapter[split_pos + 1:]

        # Process the first part normally
        prompt_template_1 = """
        You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.

I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.
The morning after another such bizarre and blurry night, he woke up with a splitting
headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
clutching his guitar and his journal close to him, pouring his grief into writing a song, but
even creating new music reminded him of her. How they spent so many afternoons in his
basement studio recording covers of their favourite Coldplay songs, after which she would
drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.
To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
covered his gullible boyish charm, making him look jagged and intimidating. He spent most
of his time holed up in his room. The only time he left the house was to hit the gym. His
social circle diminished and his grades began falling quickly.
Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
favourite. Lead guitarist at the college band, straight As with an impressive academic record,
broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
going for him. Until he met the stunning Anisha Singhania.
She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
rain, but before he knew it, he had been struck by lightning.
In the summer of his pre-final year at engineering college, when he was conducting auditions
for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him.
&quot;Hey, I&#39;m Anisha.&quot; She extended her hand.
&quot;Hi! I’m Dhruv,&quot; he responded softly and shook hands with her. He couldn&#39;t help but notice
the striking manicured nails polished with a deep black color.
&quot;I have heard a lot about you.” she said with a strikingly odd smile.
“Oh is that so?” He appeared visibly embarrassed.
“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
little myself. And I was wondering if I could join the band too.&quot;
&quot;Thank you, that&#39;s very kind of you. You&#39;re welcome to the auditions.&quot;
&quot;Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
turn is in half an hour, so I thought it&#39;d be a good use of time to get to know one of the finest
seniors in college.&quot;
&quot;That&#39;s really kind of you. I&#39;d love to catch up, but I&#39;m sorry, I need to focus on these
auditions right now.&quot; He shrugged and excused himself.
&quot;No worries. It was nice talking to you.&quot;
&quot;All the best for the audition, Anisha,&quot; he said with a placid smile.

Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
couple of times, she caught him stealing glances at her and returned an alluring smile.
Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
performance. And then as her name was announced, she walked up to the stage, gazing
fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.
&quot;You could buy me diamonds
You could buy me pearls
Take me on a cruise around the world
Baby, you know I&#39;m worth it...”
Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
there, she was literally ‘worth it’.
Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
Just then his phone vibrated to notify Anisha&#39;s friend request on Facebook.
&quot;Who is it?&quot; Arnav enquired.
&quot;Well remember that girl, Anisha, from the auditions today?&quot;
&quot;Yeah, the hot chick who sang, &#39;A woman’s worth&#39;?&quot;
&#39;Yep. It&#39;s her friend-request.&quot;
&quot;Dude, I saw how she was talking to you. She is totally into you.&quot;
&quot;Well let’s not jump to conclusions. It’s just a friend request.”
“That’s her move.”
“Well she could simply be interested in friendship. But she sure is very hot though.&quot;
&quot;Well for starters, you don&#39;t look like a pig yourself.”
“Way to make a guy feel good about himself.” Dhruv smirked.
“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
you&#39;re quite a catch, so go for it!&quot; Arnav said to him sarcastically while grabbing his phone
from his hands and checking out Anisha&#39;s Facebook profile.
&quot;Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.
Arnav rolled his eyes and continued stalking her profile.
Dhruv looked at him with a slackened expression and accepted the friend request.
In less than five minutes his phone buzzed again. This time it was a message from her. He
opened his phone to a, &quot;Hey! How&#39;re you doing?&quot;
&quot;See? So what happened to Mr Righteous, Let&#39;s not generalise and jump to conclusions&#39;,
Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
intellectual side for her!&quot; He joked.

“As you say, sir!” Dhruv resigned to his friend’s comments.
&quot;Good! Now you have fun with your new and smoking hot endeavours.&quot; Arnav smirked
bidding his goodbye.
&quot;See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
phone and checked out Anisha&#39;s profile. Her display picture was a stunning portrait of her
clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv&#39;s attention before
another message from her popped up on the screen.
&quot;Hey! Are you there?&quot; her message read.
Dhruv opened the chat box to text her back.
&quot;Hey! What&#39;s up?&quot;
&quot;Nothing much. Was listening to some classical jazz.&quot;
&quot;Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.&quot;
&quot;You do? I thought only girls dig those kinds of songs,&quot; Anisha replied.
&quot;I am a huge fan of Sinatra and a lot of other artists from that time. I think if you&#39;re
passionate about music, then you tend to appreciate good work, irrespective of the genre or
the artist. Besides, those are classics,&quot; Dhruv typed.
&quot;Oh, I think I am talking to a proper musician here.&quot; she added a few blushing emojis.
“Haha come on, you’re embarrassing me.&quot;
&quot;You know what&#39;s better than a passionate musician?&quot;
&quot;What?&quot;
&quot;A modest one.&quot;
&quot;Hahaha! Is that so?&quot;
&quot;Oh, it is so. Anyway, who&#39;s your favourite artist or band?&quot; she asked.
&quot;Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
too.&quot;
&quot;Ahh, ‘Tears in heaven’!&quot;
&quot;Oh, it transports me to another world every time I listen to it. In fact I was planning on
doing a cover on it tomorrow.&quot;
&quot;Really? If you don&#39;t mind, can I join? Like I won&#39;t sing, but I can help, you know?&quot;
&quot;Yeah, sure. That&#39;d be great.&quot;
&quot;Perfect, when and where?&quot;
&quot;Umm… tomorrow, my place, around six?&quot;
&quot;Sounds great. I can&#39;t wait!&quot;

&quot;Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
Alicia Keys is phenomenal, and you did absolute justice to her.&quot;
&quot;Did I? I thought I blew it.&quot;
&quot;Are you kidding me? No, you had the whole crowd going crazy over your voice.&quot;
&quot;Oh really, you too?&quot;
Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
emoji.
The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
half an hour, they spent the rest of the two hours hanging out in his room and talking about
everything from college, the band, music, career plans and dream cities.
“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
small and big city, and perform at every stage. Have my voice be heard.”
“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”
“What do you want to do?”
“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
with anything but the best. And then once I have my MBA degree, he’d rather have me join
the family business. Try to digitise things and expand to newer markets.”
“You just told me what your dad wants. I asked you, ‘What do you want?’”
He looked at her and let out a deep breath.
“Well, I want to build a life of my own.”
“And what does that life look like?”
“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”
“That’s so abstract.”
“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
I want to have meaningful relationships and experience life from different lenses. Travel
travel, but not to just see the world, but experience cultures and learn about people and what
drives them.”
“Your plan sounds so fancy and existential at the same time. How do you do it?”
“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”
“Hmm”
“Have you watched Before Sunrise?”
“No.”
“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”
Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
created by the dilapidated rooftops of neighbourhood houses.
“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
than he loved any of us…”
You know, I loved him the most. And when he passed away, I was a total wreck. I began
hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
him, I stopped eating, studying, everything. Can you be mad at the dead?&quot; she asked, but
Dhruv had no answers. He barely processed Anisha&#39;s confessions. He had no idea she cloaked
such things behind her cheery demeanour.
&quot;It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
his old white shirt.
On the evening of 3 rd September, I drove to the small cliff ten kilometres down from our Goa
house. I barely knew how to drive, but anger makes you do strange things.
Before leaving, I had grabbed the last pack of cigarettes from dad&#39;s belongings and there at
the cliff, I stood by the sea and lit my first ever cigarette. I still don&#39;t know why I did it.

I think I did it partly because I was mad at him and wanted those cigarettes to consume me
the same way. And partly because I felt it was the last thing that connected me to dad, the one
thing he couldn&#39;t give up. I embraced it as a part of my life. Every time I smoke now; it
reminds me of him. And I hate it. But I also love it. And I miss him.&quot; She completed her
monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
with his index finger.
She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
looked at her, and he couldn&#39;t help but think that the more he got to know her, the more of a
mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
cigarette between her index and middle finger and stuck out her hand in his direction to offer
him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
exchanging a single word, they sat there smoking late into the evening, until the entire place
got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
body, and he could feel his lips slowly brush against hers. She tasted like coffee and
cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other&#39;s smoke-
stained breath.

****

For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
terrace when she opened up about her childhood, things quickly picked up between them.
And before he knew it, every small and big thing about her seemed extraordinary to him. Her
passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
inappropriate times and then suddenly shifting gears to share a deeply personal childhood
story and always lighting a smoke while she told it.
In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
with her. They began bunking classes and hanging out at a tapri near college, smoking
cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
Delhi to explore the food scene, visit local pubs, art galleries and old architectural
monuments.
On her birthday, he planned a surprise terrace party at his place and invited all their friends.
She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
and a big custom cake that had a picture of her singing at the band auditions.
“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
my life.” They cut the cake, got drunk on cheap tequila and danced the night away.
As their social circle expanded, they began getting more invites to parties of common friends,
where they went as a couple. But oftentimes Anisha would just be outside in the smoking
zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
with someone she borrowed a lighter from.
“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
lent her the lighter, had asked her.

“Why?” She inquired bright-eyed.
“I’d love to take you out for coffee. I know a really nice place here.”
She took a moment and smiled, as though assessing the situation.
“Is there so much to think about?” He smirked.
She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
won’t hurt anyone.”
Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
seeing Anisha work her way through all these social events, getting enormously drunk and
dancing voluptuously with many strange, new men. At first, he thought he was being too
sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
concerned, and hoped she would come around. But when he confronted her, he was only met
with contempt and accusations of being an overprotective and jealous boyfriend.
He started feeling increasingly anxious when Anisha wasn&#39;t around. And ever since he had
heard from a couple of common friends that Anisha got so wasted at a party, she puked for
two hours straight, he started showing up at parties he wasn&#39;t even invited to, just to take care
of her, drive her home safe and make sure she didn’t do something that she would regret
later.
To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
Kunj, pretty near to Dhruv&#39;s place, but he still went all the way to pick up Anisha from her
hostel.
She was wearing a little black dress and high-heeled gladiators.
“Hi babe!” Dhruv smiled as she entered the car.
“Hey” she replied distantly as she adjusted the seat to make herself comfortable.
“You’re looking stunning tonight.”
“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”
Laughing at her own remark, she fixed the collar of his shirt.
Like always she began touching up her make-up in the mirror.
“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.
Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
to put it on silent.
“Who is it?”

“Some sales call or something, been getting too many of these lately.” She replied, visibly
bothered, and threw her phone back in her clutch in a haphazard manner.
“Then why are you so flustered?” He asked, eyes fixed on the road.
“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.
He pulled a tissue and offered it to her. She looked at him for a second and then took the
tissue reluctantly.
“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
her forehead and cheek.
“There’s water in the back if you want.”
“No. I am good. Thanks.”
After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
hear about the auditions that happened last week?”
“Uh hmm”she replied, still staring out the window.
“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
Avinash, I think.”
“Well, good for him.”
“I think the band is to see some great talent this year.”
“Yeah. I guess.”
“Anisha..”
“Hmm?”
“We met around the same time last year.”
“Yeah”
“You know, we owe this relationship to the band.”
“Maybe”
“Had you not come to audition, we probably wouldn’t have been dating.”
“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
are you so sentimental today?” she frowned and looked out the window.
“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.
“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
window.
“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”
“No. It’s fine. Let’s just go.”
“No, seriously? Whatever makes you feel better.”
“Honestly. Just getting there would make me feel better.” She snapped back.

They drove the rest of the way without exchanging a single word.
At the party, they received a warm welcome. Dhruv was among the senior-most members of
the band. A flock of junior boys and girls surrounded him.
After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
around to look for Anisha. Making his way past big crowds of people dancing and singing
loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
fuelled his worries. She never slipped away from a party without telling him. He didn&#39;t know
what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
and checked with a few people but nobody knew where she was.
All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
the restroom, he heard moaning sounds from the adjacent women&#39;s loo. A weird feeling rose
in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
door.
Dhruv received the shock of his life.
Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
seeing Dhruv standing over them.
Dhruv couldn&#39;t believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
hand and stepped back, incapable of letting her touch him.
She saw a burning rage in his eyes that she had never seen before.
&quot;Dhruv…&quot; she cried and ran after him as he raced down the stairs.
The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
premises and a weepy, guilt-ridden Anisha chasing him down the parking lot.
But before she could catch hold of him, Dhruv was already speeding off in his car. The
screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
down.
&quot;Dhruv…&quot; Anisha screamed in the middle of the street and wept inconsolably.

****

A whole week went by and Dhruv didn&#39;t show up at college at all. He barely picked calls
from any of his friends, and simply spent all his days and nights locked up in his room.
Sometimes the sound of a guitar echoing through his room was the only signal that he was
alive. Worried sick, Mrs Malhotra called Arnav.

“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness.
&quot;Oh Hi…I didn’t know you were coming.&quot; Dhruv got up, taken aback. His weight loss was
apparent. With a thickly grown unkempt beard, he looked shabbier than ever.
Arnav entered and switched on the lights.
Dhruv flinched. &quot;Ah, switch off the lights,&quot; He groaned.
&quot;No&quot;
&quot;Arnav…&quot;
&quot;Bro, you&#39;re a mess,&quot; he reprimanded, kicking him out of bed. &quot;That’s it. We’re going out
tonight. It&#39;s been ten days you haven&#39;t shown your stupid face to any of us.&quot;
&quot;Man, I don&#39;t feel like it.&quot;
&quot;I don&#39;t care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
friend Dhruv. Period.&quot;
&quot;What are your plans?&quot;
&quot;Clubbing!&quot;
&quot;Ugh! I don&#39;t want to go to a stupid club.&quot;
&quot;We&#39;ll get some booze, have some fun, meet some hot chicks and we&#39;ll get you over that
bitch.&quot;
&quot;You don&#39;t have to call her that.&quot; Dhruv shrugged.
&quot;She is a bitch.&quot; Arnav&#39;s face stiffened.
&quot;Arnav, please...&quot; Dhruv tried to raise his voice.
&quot;Okay, just go take a shower,&quot; Arnav resigned.
&quot;Arnav please, I swear I would have come, but I just don&#39;t feel like going out tonight.&quot;
&quot;Get your ass off this couch right now, trim your messy beard, take a shower, put on clean
clothes. We&#39;re going clubbing tonight. It&#39;s settled.&quot;
Dhruv protested, but before he could make an argument, Arnav shut him up and said, &quot;Listen,
dude, your &#39;sad boy vibe&#39; days are over. Enough of being this caveman. We&#39;re getting you
cleaned up and out on the scene tonight. The world has too many beautiful people. And it&#39;s a
shame you’re holed up in your room behaving like some psychopath. Stop wasting away your
youth and good looks, my friend. Carpe Diem!&quot; Arnav smirked and Dhruv hung his head low
in resignation.
“By the way, you stink,&quot; Arnav threw a towel on Dhruv’s face.
&quot;And, don&#39;t forget to shave that god-awful beard,&quot; he added.

Half an hour later, he emerged out of the bathroom looking like the same old Dhruv again.
The clean-shaven face highlighted his boyish features. On the inside though, Dhruv didn’t
feel any less miserable than before, but Arnav didn&#39;t give up on his friend.  He forced him
into the car, as they went on to pick up their other two friends from college Rohan and
Sameer.
Rohan had bought a new bottle of scotch. He raised a toast to Dhruv, &quot;Here&#39;s to our boy and
the return of his days of freedom and fun.&quot;
The night continued, hopping from nightclub to nightclub, drinking gallons of alcohol and
meeting new women. Dhruv got way too drunk in an attempt to wash away Anisha’s
memories. The more they flashed across his eyes, the more he drank in the hope to fade it all
out into nothingness. At one point, he barely recognized anything or anyone. It was all a giant
blur. Small fragments of consciousness kept escaping his mind like pieces of spatial matter
gallivanting across the sky. He felt like he was getting pulled into an expanding labyrinth and
his sense of self slowly continued sinking to newer lows.
Later in the night; he ended up sleeping with a slick woman who he’d met at the club a few
hours ago. The next morning, the memory of the night had almost vanished, but the hole in
his heart had widened.
This is the sample HTML : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 25vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    <p>The morning after another such bizarre and blurry night, he woke up with a splitting
    headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
    drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
    clutching his guitar and his journal close to him, pouring his grief into writing a song, but
    even creating new music reminded him of her. How they spent so many afternoons in his
    basement studio recording covers of their favourite Coldplay songs, after which she would
    drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
    that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.</p>
    <p>To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
    covered his gullible boyish charm, making him look jagged and intimidating. He spent most
    of his time holed up in his room. The only time he left the house was to hit the gym. His
    social circle diminished and his grades began falling quickly.</p>
    <p>Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
    favourite. Lead guitarist at the college band, straight As with an impressive academic record,
    broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
    going for him. Until he met the stunning Anisha Singhania.</p>
    <p>She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
    rain, but before he knew it, he had been struck by lightning.</p>

    <p>In the summer of his pre-final year at engineering college, when he was conducting auditions
    for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him. </p>
    <p>“Hey, I'm Anisha.” She extended her hand. </p>
    <p>“Hi! I’m Dhruv,” he responded softly and shook hands with her. He couldn't help but notice
    the striking manicured nails polished with a deep black color.</p>
    <p>“I have heard a lot about you.” she said with a strikingly odd smile.</p>
    <p>“Oh is that so?” He appeared visibly embarrassed.</p>
    <p>“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
    little myself. And I was wondering if I could join the band too.”</p>
    <p>“Thank you, that's very kind of you. You're welcome to the auditions.”</p>
    <p>“Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
    turn is in half an hour, so I thought it'd be a good use of time to get to know one of the finest
    seniors in college.” </p>
    <p>“That's really kind of you. I'd love to catch up, but I'm sorry, I need to focus on these
    auditions right now.” He shrugged and excused himself.</p>
    <p>“No worries. It was nice talking to you.”</p>
    <p>“All the best for the audition, Anisha,” he said with a placid smile.</p>

    <p>Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
    He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
    couple of times, she caught him stealing glances at her and returned an alluring smile. </p>
    <p>Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
    performance. And then as her name was announced, she walked up to the stage, gazing
    fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.</p>

    <div class="poetry">
    “You could buy me diamonds<br>
    You could buy me pearls<br>
    Take me on a cruise around the world<br>
    Baby, you know I'm worth it...”
    </div>

    <p>Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
    there, she was literally ‘worth it’. </p>
    <p>Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
    Just then his phone vibrated to notify Anisha's friend request on Facebook. </p>
    <p>“Who is it?” Arnav enquired.</p>
    <p>“Well remember that girl, Anisha, from the auditions today?”</p>
    <p>“Yeah, the hot chick who sang, ‘A woman’s worth’?”</p>
    <p>“Yep. It’s her friend-request.”</p>
    <p>“Dude, I saw how she was talking to you. She is totally into you.”</p>
    <p>“Well let’s not jump to conclusions. It’s just a friend request.”</p>
    <p>“That’s her move.”</p>
    <p>“Well she could simply be interested in friendship. But she sure is very hot though.”</p>
    <p>“Well for starters, you don’t look like a pig yourself.”</p>
    <p>“Way to make a guy feel good about himself.” Dhruv smirked.</p>
    <p>“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
    you're quite a catch, so go for it!” Arnav said to him sarcastically while grabbing his phone
    from his hands and checking out Anisha's Facebook profile.  </p>
    <p>“Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.</p>
    <p>Arnav rolled his eyes and continued stalking her profile.</p>
    <p>Dhruv looked at him with a slackened expression and accepted the friend request. </p>
    <p>In less than five minutes his phone buzzed again. This time it was a message from her. He
    opened his phone to a, “Hey! How’re you doing?”</p>
    <p>“See? So what happened to Mr Righteous, Let’s not generalise and jump to conclusions’,
    Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
    intellectual side for her!” He joked.</p>
    <p>“As you say, sir!” Dhruv resigned to his friend’s comments.</p>
    <p>“Good! Now you have fun with your new and smoking hot endeavours.” Arnav smirked
    bidding his goodbye.</p>
    <p>“See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
    phone and checked out Anisha's profile. Her display picture was a stunning portrait of her
    clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
    bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv's attention before
    another message from her popped up on the screen.</p>
    <p>“Hey! Are you there?” her message read.</p>
    <p>Dhruv opened the chat box to text her back. </p>
    <p>“Hey! What’s up?”</p>
    <p>“Nothing much. Was listening to some classical jazz.”</p>
    <p>“Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.”</p>
    <p>“You do? I thought only girls dig those kinds of songs,” Anisha replied.</p>
    <p>“I am a huge fan of Sinatra and a lot of other artists from that time. I think if you're
    passionate about music, then you tend to appreciate good work, irrespective of the genre or
    the artist. Besides, those are classics,” Dhruv typed.</p>
    <p>“Oh, I think I am talking to a proper musician here.” she added a few blushing emojis.</p>
    <p>“Haha come on, you’re embarrassing me.” </p>
    <p>“You know what's better than a passionate musician?”</p>
    <p>“What?”</p>
    <p>“A modest one.”</p>
    <p>“Hahaha! Is that so?”  </p>
    <p>“Oh, it is so. Anyway, who's your favourite artist or band?” she asked.</p>
    <p>“Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
    too.”</p>
    <p>“Ahh, ‘Tears in heaven’!”</p>
    <p>“Oh, it transports me to another world every time I listen to it. In fact I was planning on
    doing a cover on it tomorrow.”</p>
    <p>“Really? If you don't mind, can I join? Like I won't sing, but I can help, you know?”</p>
    <p>“Yeah, sure. That'd be great.”</p>
    <p>“Perfect, when and where?”</p>
    <p>“Umm… tomorrow, my place, around six?”</p>
    <p>“Sounds great. I can't wait!”</p>
    <p>“Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
    Alicia Keys is phenomenal, and you did absolute justice to her.” </p>
    <p>“Did I? I thought I blew it.”</p>
    <p>“Are you kidding me? No, you had the whole crowd going crazy over your voice.”</p>
    <p>“Oh really, you too?”</p>
    <p>Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
    emoji.</p>
    <p>The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
    in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
    half an hour, they spent the rest of the two hours hanging out in his room and talking about
    everything from college, the band, music, career plans and dream cities.</p>
    <p>“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
    small and big city, and perform at every stage. Have my voice be heard.”</p>
    <p>“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”</p>
    <p>“What do you want to do?”</p>
    <p>“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
    with anything but the best. And then once I have my MBA degree, he’d rather have me join
    the family business. Try to digitise things and expand to newer markets.”</p>
    <p>“You just told me what your dad wants. I asked you, ‘What do you want?’”</p>
    <p>He looked at her and let out a deep breath.</p>
    <p>“Well, I want to build a life of my own.”</p>
    <p>“And what does that life look like?”</p>
    <p>“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”</p>
    <p>“That’s so abstract.”</p>
    <p>“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
    I want to have meaningful relationships and experience life from different lenses. Travel
    travel, but not to just see the world, but experience cultures and learn about people and what
    drives them.”</p>
    <p>“Your plan sounds so fancy and existential at the same time. How do you do it?”</p>
    <p>“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”</p>
    <p>“Hmm”</p>
    <p>“Have you watched Before Sunrise?”</p>
    <p>“No.”</p>
    <p>“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
    time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”</p>
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    <p>Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
    created by the dilapidated rooftops of neighbourhood houses.</p>
    <p>“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
    than he loved any of us…”</p>
    <p>You know, I loved him the most. And when he passed away, I was a total wreck. I began
    hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
    him, I stopped eating, studying, everything. Can you be mad at the dead?” she asked, but
    Dhruv had no answers. He barely processed Anisha's confessions. He had no idea she cloaked
    such things behind her cheery demeanour. </p>
    <p>“It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
    even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
    his old white shirt.
    On the evening of 3rd September, I drove to the small cliff ten kilometres down from our Goa
    house. I barely knew how to drive, but anger makes you do strange things.
    Before leaving, I had grabbed the last pack of cigarettes from dad's belongings and there at
    the cliff, I stood by the sea and lit my first ever cigarette. I still don't know why I did it.</p>
    <p>I think I did it partly because I was mad at him and wanted those cigarettes to consume me
    the same way. And partly because I felt it was the last thing that connected me to dad, the one
    thing he couldn't give up. I embraced it as a part of my life. Every time I smoke now; it
    reminds me of him. And I hate it. But I also love it. And I miss him.” She completed her
    monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
    with his index finger.</p>
    <p>She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
    the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
    looked at her, and he couldn't help but think that the more he got to know her, the more of a
    mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
    cigarette between her index and middle finger and stuck out her hand in his direction to offer
    him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
    exchanging a single word, they sat there smoking late into the evening, until the entire place
    got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
    body, and he could feel his lips slowly brush against hers. She tasted like coffee and
    cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other's smoke-
    stained breath. </p>

    <p>****</p>

    <p>For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
    terrace when she opened up about her childhood, things quickly picked up between them.
    And before he knew it, every small and big thing about her seemed extraordinary to him. Her
    passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
    inappropriate times and then suddenly shifting gears to share a deeply personal childhood
    story and always lighting a smoke while she told it.</p>
    <p>In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
    usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
    with her. They began bunking classes and hanging out at a <i>tapri</i> near college, smoking
    cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
    Delhi to explore the food scene, visit local pubs, art galleries and old architectural
    monuments.</p>
    <p>On her birthday, he planned a surprise terrace party at his place and invited all their friends.
    She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
    and a big custom cake that had a picture of her singing at the band auditions.</p>
    <p>“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
    my life.” They cut the cake, got drunk on cheap tequila and danced the night away.</p>
    <p>As their social circle expanded, they began getting more invites to parties of common friends,
    where they went as a couple. But oftentimes Anisha would just be outside in the smoking
    zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
    with someone she borrowed a lighter from.</p>
    <p>“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
    lent her the lighter, had asked her.</p>
    <p>“Why?” She inquired bright-eyed.</p>
    <p>“I’d love to take you out for coffee. I know a really nice place here.”</p>
    <p>She took a moment and smiled, as though assessing the situation.</p>
    <p>“Is there so much to think about?” He smirked.</p>
    <p>She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
    won’t hurt anyone.”</p>
    <p>Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
    talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
    wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
    seeing Anisha work her way through all these social events, getting enormously drunk and
    dancing voluptuously with many strange, new men. At first, he thought he was being too
    sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
    lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
    concerned, and hoped she would come around. But when he confronted her, he was only met
    with contempt and accusations of being an overprotective and jealous boyfriend.</p>
    <p>He started feeling increasingly anxious when Anisha wasn't around. And ever since he had
    heard from a couple of common friends that Anisha got so wasted at a party, she puked for
    two hours straight, he started showing up at parties he wasn't even invited to, just to take care
    of her, drive her home safe and make sure she didn’t do something that she would regret
    later. </p>
    <p>To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
    Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
    Kunj, pretty near to Dhruv's place, but he still went all the way to pick up Anisha from her
    hostel.</p>
    <p>She was wearing a little black dress and high-heeled gladiators.</p>
    <p>“Hi babe!” Dhruv smiled as she entered the car.</p>
    <p>“Hey” she replied distantly as she adjusted the seat to make herself comfortable.</p>
    <p>“You’re looking stunning tonight.”</p>
    <p>“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
    for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”</p>
    <p>Laughing at her own remark, she fixed the collar of his shirt.</p>
    <p>Like always she began touching up her make-up in the mirror.</p>
    <p>“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.</p>
    <p>Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
    to put it on silent.</p>
    <p>“Who is it?”</p>
    <p>“Some sales call or something, been getting too many of these lately.” She replied, visibly
    bothered, and threw her phone back in her clutch in a haphazard manner.</p>
    <p>“Then why are you so flustered?” He asked, eyes fixed on the road.</p>
    <p>“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.</p>
    <p>He pulled a tissue and offered it to her. She looked at him for a second and then took the
    tissue reluctantly.</p>
    <p>“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
    her forehead and cheek.</p>
    <p>“There’s water in the back if you want.”</p>
    <p>“No. I am good. Thanks.”</p>
    <p>After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
    hear about the auditions that happened last week?”</p>
    <p>“Uh hmm”she replied, still staring out the window.</p>
    <p>“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
    Avinash, I think.”</p>
    <p>“Well, good for him.”</p>
    <p>“I think the band is to see some great talent this year.”</p>
    <p>“Yeah. I guess.”</p>
    <p>“Anisha..”</p>
    <p>“Hmm?”</p>
    <p>“We met around the same time last year.”</p>
    <p>“Yeah”</p>
    <p>“You know, we owe this relationship to the band.”</p>
    <p>“Maybe”</p>
    <p>“Had you not come to audition, we probably wouldn’t have been dating.”</p>
    <p>“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
    are you so sentimental today?” she frowned and looked out the window.</p>
    <p>“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.</p>
    <p>“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
    window.</p>
    <p>“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”</p>
    <p>“No. It’s fine. Let’s just go.”</p>
    <p>“No, seriously? Whatever makes you feel better.”</p>
    <p>“Honestly. Just getting there would make me feel better.” She snapped back. </p>
    <p>They drove the rest of the way without exchanging a single word.</p>
    <p>At the party, they received a warm welcome. Dhruv was among the senior-most members of
    the band. A flock of junior boys and girls surrounded him.</p>
    <p>After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
    around to look for Anisha. Making his way past big crowds of people dancing and singing
    loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
    surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
    his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
    fuelled his worries. She never slipped away from a party without telling him. He didn't know
    what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
    and checked with a few people but nobody knew where she was.</p>
    <p>All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
    the restroom, he heard moaning sounds from the adjacent women's loo. A weird feeling rose
    in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
    door. </p>
    <p>Dhruv received the shock of his life.</p>
    <p>Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
    seeing Dhruv standing over them.</p>
    <p>Dhruv couldn't believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
    whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
    support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
    hand and stepped back, incapable of letting her touch him.</p>
    <p>She saw a burning rage in his eyes that she had never seen before. </p>
    <p>“Dhruv…” she cried and ran after him as he raced down the stairs. </p>
    <p>The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
    silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
    premises and a weepy, guilt-ridden Anisha chasing him down the parking lot. </p>
    <p>But before she could catch hold of him, Dhruv was already speeding off in his car. The
    screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
    down. </p>
    <p>“Dhruv…” Anisha screamed in the middle of the street and wept inconsolably. </p>

    <p>****</p>

    <p>A whole week went by and Dhruv didn't show up at college at all. He barely picked calls
    from any of his friends, and simply spent all his days and nights locked up in his room.
    Sometimes the sound of a guitar echoing through his room was the only signal that he was
    alive. Worried sick, Mrs Malhotra called Arnav.</p>
    <p>“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
    the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
    the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness. </p>
    <p>“Oh Hi…I didn’t know you were coming.” Dhruv got up, taken aback. His weight loss was
    apparent. With a thickly grown unkempt beard, he looked shabbier than ever. </p>
    <p>Arnav entered and switched on the lights.</p>
    <p>Dhruv flinched. “Ah, switch off the lights,” He groaned. </p>
    <p>“No”</p>
    <p>“Arnav…”</p>
    <p>“Bro, you're a mess,” he reprimanded, kicking him out of bed. “That’s it. We’re going out
    tonight. It's been ten days you haven't shown your stupid face to any of us.”</p>
    <p>“Man, I don't feel like it.”</p>
    <p>“I don't care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
    friend Dhruv. Period.”</p>
    <p>“What are your plans?”</p>
    <p>“Clubbing!”</p>
    <p>“Ugh! I don't want to go to a stupid club.”</p>
    <p>“We'll get some booze, have some fun, meet some hot chicks and we'll get you over that
    bitch.”</p>
    <p>“You don't have to call her that.” Dhruv shrugged. </p>
    <p>“She is a bitch.” Arnav's face stiffened. </p>
    <p>“Arnav, please...” Dhruv tried to raise his voice. </p>
    <p>“Okay, just go take a shower,” Arnav resigned. </p>
    <p>“Arnav please,

    Here is the target chapter: <<CHAPTER_TEXT>>
        """
        prompt_1 = prompt_template_1.replace("<<CHAPTER_TEXT>>", first_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_1 = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_1,
                }
            ],
            model=model,
            temperature=0
        )

        response_1 = chat_completion_1.choices[0].message.content

        # Process the second part with a modified prompt (no HTML headers)
        prompt_template_2 = """
        You are an expert book formatter.
        Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
        Font size = <<fontsize>>
        Line height = <<lineheight>>
        Include these features in html:
        1. Paragraph Formatting
        Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
        2. Line Length
        Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
        3.Line Spacing (Leading)
        Comfortable Reading: The line spacing should be the same as given in the example.
        4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
        8. Left and Right margins are minimum so the pdf looks like a book.
        7.  Consistency
        Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
        8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
        9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
        Keep this in mind : Left and Right margins are minimum.
        10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
        11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

        Here is the continuation of the chapter:
        <<CHAPTER_TEXT>>
        """
        prompt_2 = prompt_template_2.replace("<<CHAPTER_TEXT>>", second_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_2 = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_2,
                }
            ],
            model=model,
            temperature=0
        )

        response_2 = chat_completion_2.choices[0].message.content

        # Now, merge the two responses
        # Extract the <body> content from the first response and append the second response

        # Find the closing </body> and </html> tags in the first response
        body_close_index = response_1.rfind("</body>")
        html_close_index = response_1.rfind("</html>")

        if body_close_index != -1:
            # Insert the second response before the closing </body> tag
            merged_html = response_1[:body_close_index] + "\n" + response_2 + "\n" + response_1[body_close_index:]
        elif html_close_index != -1:
            # Insert before </html> if </body> is not found
            merged_html = response_1[:html_close_index] + "\n" + response_2 + "\n" + response_1[html_close_index:]
        else:
            # If no closing tags are found, simply concatenate
            merged_html = response_1 + "\n" + response_2

        return merged_html
    
  else:
        # If the chapter exceeds the limit, split into two parts
        split_pos_1 = chapter.rfind('.', 0, max_chars)
        split_pos_2 = chapter.rfind('.', max_chars, 74000)
        first_part = chapter[:split_pos_1 + 1]
        second_part = chapter[split_pos_1 + 1 : split_pos_2 + 1]
        third_part = chapter[split_pos_2 + 1:]
        # Process the first part normally
        prompt_template_1 = """
        You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.

I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.
The morning after another such bizarre and blurry night, he woke up with a splitting
headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
clutching his guitar and his journal close to him, pouring his grief into writing a song, but
even creating new music reminded him of her. How they spent so many afternoons in his
basement studio recording covers of their favourite Coldplay songs, after which she would
drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.
To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
covered his gullible boyish charm, making him look jagged and intimidating. He spent most
of his time holed up in his room. The only time he left the house was to hit the gym. His
social circle diminished and his grades began falling quickly.
Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
favourite. Lead guitarist at the college band, straight As with an impressive academic record,
broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
going for him. Until he met the stunning Anisha Singhania.
She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
rain, but before he knew it, he had been struck by lightning.
In the summer of his pre-final year at engineering college, when he was conducting auditions
for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him.
&quot;Hey, I&#39;m Anisha.&quot; She extended her hand.
&quot;Hi! I’m Dhruv,&quot; he responded softly and shook hands with her. He couldn&#39;t help but notice
the striking manicured nails polished with a deep black color.
&quot;I have heard a lot about you.” she said with a strikingly odd smile.
“Oh is that so?” He appeared visibly embarrassed.
“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
little myself. And I was wondering if I could join the band too.&quot;
&quot;Thank you, that&#39;s very kind of you. You&#39;re welcome to the auditions.&quot;
&quot;Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
turn is in half an hour, so I thought it&#39;d be a good use of time to get to know one of the finest
seniors in college.&quot;
&quot;That&#39;s really kind of you. I&#39;d love to catch up, but I&#39;m sorry, I need to focus on these
auditions right now.&quot; He shrugged and excused himself.
&quot;No worries. It was nice talking to you.&quot;
&quot;All the best for the audition, Anisha,&quot; he said with a placid smile.

Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
couple of times, she caught him stealing glances at her and returned an alluring smile.
Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
performance. And then as her name was announced, she walked up to the stage, gazing
fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.
&quot;You could buy me diamonds
You could buy me pearls
Take me on a cruise around the world
Baby, you know I&#39;m worth it...”
Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
there, she was literally ‘worth it’.
Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
Just then his phone vibrated to notify Anisha&#39;s friend request on Facebook.
&quot;Who is it?&quot; Arnav enquired.
&quot;Well remember that girl, Anisha, from the auditions today?&quot;
&quot;Yeah, the hot chick who sang, &#39;A woman’s worth&#39;?&quot;
&#39;Yep. It&#39;s her friend-request.&quot;
&quot;Dude, I saw how she was talking to you. She is totally into you.&quot;
&quot;Well let’s not jump to conclusions. It’s just a friend request.”
“That’s her move.”
“Well she could simply be interested in friendship. But she sure is very hot though.&quot;
&quot;Well for starters, you don&#39;t look like a pig yourself.”
“Way to make a guy feel good about himself.” Dhruv smirked.
“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
you&#39;re quite a catch, so go for it!&quot; Arnav said to him sarcastically while grabbing his phone
from his hands and checking out Anisha&#39;s Facebook profile.
&quot;Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.
Arnav rolled his eyes and continued stalking her profile.
Dhruv looked at him with a slackened expression and accepted the friend request.
In less than five minutes his phone buzzed again. This time it was a message from her. He
opened his phone to a, &quot;Hey! How&#39;re you doing?&quot;
&quot;See? So what happened to Mr Righteous, Let&#39;s not generalise and jump to conclusions&#39;,
Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
intellectual side for her!&quot; He joked.

“As you say, sir!” Dhruv resigned to his friend’s comments.
&quot;Good! Now you have fun with your new and smoking hot endeavours.&quot; Arnav smirked
bidding his goodbye.
&quot;See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
phone and checked out Anisha&#39;s profile. Her display picture was a stunning portrait of her
clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv&#39;s attention before
another message from her popped up on the screen.
&quot;Hey! Are you there?&quot; her message read.
Dhruv opened the chat box to text her back.
&quot;Hey! What&#39;s up?&quot;
&quot;Nothing much. Was listening to some classical jazz.&quot;
&quot;Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.&quot;
&quot;You do? I thought only girls dig those kinds of songs,&quot; Anisha replied.
&quot;I am a huge fan of Sinatra and a lot of other artists from that time. I think if you&#39;re
passionate about music, then you tend to appreciate good work, irrespective of the genre or
the artist. Besides, those are classics,&quot; Dhruv typed.
&quot;Oh, I think I am talking to a proper musician here.&quot; she added a few blushing emojis.
“Haha come on, you’re embarrassing me.&quot;
&quot;You know what&#39;s better than a passionate musician?&quot;
&quot;What?&quot;
&quot;A modest one.&quot;
&quot;Hahaha! Is that so?&quot;
&quot;Oh, it is so. Anyway, who&#39;s your favourite artist or band?&quot; she asked.
&quot;Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
too.&quot;
&quot;Ahh, ‘Tears in heaven’!&quot;
&quot;Oh, it transports me to another world every time I listen to it. In fact I was planning on
doing a cover on it tomorrow.&quot;
&quot;Really? If you don&#39;t mind, can I join? Like I won&#39;t sing, but I can help, you know?&quot;
&quot;Yeah, sure. That&#39;d be great.&quot;
&quot;Perfect, when and where?&quot;
&quot;Umm… tomorrow, my place, around six?&quot;
&quot;Sounds great. I can&#39;t wait!&quot;

&quot;Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
Alicia Keys is phenomenal, and you did absolute justice to her.&quot;
&quot;Did I? I thought I blew it.&quot;
&quot;Are you kidding me? No, you had the whole crowd going crazy over your voice.&quot;
&quot;Oh really, you too?&quot;
Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
emoji.
The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
half an hour, they spent the rest of the two hours hanging out in his room and talking about
everything from college, the band, music, career plans and dream cities.
“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
small and big city, and perform at every stage. Have my voice be heard.”
“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”
“What do you want to do?”
“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
with anything but the best. And then once I have my MBA degree, he’d rather have me join
the family business. Try to digitise things and expand to newer markets.”
“You just told me what your dad wants. I asked you, ‘What do you want?’”
He looked at her and let out a deep breath.
“Well, I want to build a life of my own.”
“And what does that life look like?”
“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”
“That’s so abstract.”
“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
I want to have meaningful relationships and experience life from different lenses. Travel
travel, but not to just see the world, but experience cultures and learn about people and what
drives them.”
“Your plan sounds so fancy and existential at the same time. How do you do it?”
“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”
“Hmm”
“Have you watched Before Sunrise?”
“No.”
“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”
Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
created by the dilapidated rooftops of neighbourhood houses.
“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
than he loved any of us…”
You know, I loved him the most. And when he passed away, I was a total wreck. I began
hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
him, I stopped eating, studying, everything. Can you be mad at the dead?&quot; she asked, but
Dhruv had no answers. He barely processed Anisha&#39;s confessions. He had no idea she cloaked
such things behind her cheery demeanour.
&quot;It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
his old white shirt.
On the evening of 3 rd September, I drove to the small cliff ten kilometres down from our Goa
house. I barely knew how to drive, but anger makes you do strange things.
Before leaving, I had grabbed the last pack of cigarettes from dad&#39;s belongings and there at
the cliff, I stood by the sea and lit my first ever cigarette. I still don&#39;t know why I did it.

I think I did it partly because I was mad at him and wanted those cigarettes to consume me
the same way. And partly because I felt it was the last thing that connected me to dad, the one
thing he couldn&#39;t give up. I embraced it as a part of my life. Every time I smoke now; it
reminds me of him. And I hate it. But I also love it. And I miss him.&quot; She completed her
monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
with his index finger.
She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
looked at her, and he couldn&#39;t help but think that the more he got to know her, the more of a
mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
cigarette between her index and middle finger and stuck out her hand in his direction to offer
him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
exchanging a single word, they sat there smoking late into the evening, until the entire place
got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
body, and he could feel his lips slowly brush against hers. She tasted like coffee and
cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other&#39;s smoke-
stained breath.

****

For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
terrace when she opened up about her childhood, things quickly picked up between them.
And before he knew it, every small and big thing about her seemed extraordinary to him. Her
passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
inappropriate times and then suddenly shifting gears to share a deeply personal childhood
story and always lighting a smoke while she told it.
In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
with her. They began bunking classes and hanging out at a tapri near college, smoking
cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
Delhi to explore the food scene, visit local pubs, art galleries and old architectural
monuments.
On her birthday, he planned a surprise terrace party at his place and invited all their friends.
She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
and a big custom cake that had a picture of her singing at the band auditions.
“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
my life.” They cut the cake, got drunk on cheap tequila and danced the night away.
As their social circle expanded, they began getting more invites to parties of common friends,
where they went as a couple. But oftentimes Anisha would just be outside in the smoking
zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
with someone she borrowed a lighter from.
“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
lent her the lighter, had asked her.

“Why?” She inquired bright-eyed.
“I’d love to take you out for coffee. I know a really nice place here.”
She took a moment and smiled, as though assessing the situation.
“Is there so much to think about?” He smirked.
She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
won’t hurt anyone.”
Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
seeing Anisha work her way through all these social events, getting enormously drunk and
dancing voluptuously with many strange, new men. At first, he thought he was being too
sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
concerned, and hoped she would come around. But when he confronted her, he was only met
with contempt and accusations of being an overprotective and jealous boyfriend.
He started feeling increasingly anxious when Anisha wasn&#39;t around. And ever since he had
heard from a couple of common friends that Anisha got so wasted at a party, she puked for
two hours straight, he started showing up at parties he wasn&#39;t even invited to, just to take care
of her, drive her home safe and make sure she didn’t do something that she would regret
later.
To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
Kunj, pretty near to Dhruv&#39;s place, but he still went all the way to pick up Anisha from her
hostel.
She was wearing a little black dress and high-heeled gladiators.
“Hi babe!” Dhruv smiled as she entered the car.
“Hey” she replied distantly as she adjusted the seat to make herself comfortable.
“You’re looking stunning tonight.”
“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”
Laughing at her own remark, she fixed the collar of his shirt.
Like always she began touching up her make-up in the mirror.
“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.
Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
to put it on silent.
“Who is it?”

“Some sales call or something, been getting too many of these lately.” She replied, visibly
bothered, and threw her phone back in her clutch in a haphazard manner.
“Then why are you so flustered?” He asked, eyes fixed on the road.
“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.
He pulled a tissue and offered it to her. She looked at him for a second and then took the
tissue reluctantly.
“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
her forehead and cheek.
“There’s water in the back if you want.”
“No. I am good. Thanks.”
After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
hear about the auditions that happened last week?”
“Uh hmm”she replied, still staring out the window.
“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
Avinash, I think.”
“Well, good for him.”
“I think the band is to see some great talent this year.”
“Yeah. I guess.”
“Anisha..”
“Hmm?”
“We met around the same time last year.”
“Yeah”
“You know, we owe this relationship to the band.”
“Maybe”
“Had you not come to audition, we probably wouldn’t have been dating.”
“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
are you so sentimental today?” she frowned and looked out the window.
“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.
“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
window.
“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”
“No. It’s fine. Let’s just go.”
“No, seriously? Whatever makes you feel better.”
“Honestly. Just getting there would make me feel better.” She snapped back.

They drove the rest of the way without exchanging a single word.
At the party, they received a warm welcome. Dhruv was among the senior-most members of
the band. A flock of junior boys and girls surrounded him.
After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
around to look for Anisha. Making his way past big crowds of people dancing and singing
loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
fuelled his worries. She never slipped away from a party without telling him. He didn&#39;t know
what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
and checked with a few people but nobody knew where she was.
All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
the restroom, he heard moaning sounds from the adjacent women&#39;s loo. A weird feeling rose
in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
door.
Dhruv received the shock of his life.
Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
seeing Dhruv standing over them.
Dhruv couldn&#39;t believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
hand and stepped back, incapable of letting her touch him.
She saw a burning rage in his eyes that she had never seen before.
&quot;Dhruv…&quot; she cried and ran after him as he raced down the stairs.
The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
premises and a weepy, guilt-ridden Anisha chasing him down the parking lot.
But before she could catch hold of him, Dhruv was already speeding off in his car. The
screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
down.
&quot;Dhruv…&quot; Anisha screamed in the middle of the street and wept inconsolably.

****

A whole week went by and Dhruv didn&#39;t show up at college at all. He barely picked calls
from any of his friends, and simply spent all his days and nights locked up in his room.
Sometimes the sound of a guitar echoing through his room was the only signal that he was
alive. Worried sick, Mrs Malhotra called Arnav.

“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness.
&quot;Oh Hi…I didn’t know you were coming.&quot; Dhruv got up, taken aback. His weight loss was
apparent. With a thickly grown unkempt beard, he looked shabbier than ever.
Arnav entered and switched on the lights.
Dhruv flinched. &quot;Ah, switch off the lights,&quot; He groaned.
&quot;No&quot;
&quot;Arnav…&quot;
&quot;Bro, you&#39;re a mess,&quot; he reprimanded, kicking him out of bed. &quot;That’s it. We’re going out
tonight. It&#39;s been ten days you haven&#39;t shown your stupid face to any of us.&quot;
&quot;Man, I don&#39;t feel like it.&quot;
&quot;I don&#39;t care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
friend Dhruv. Period.&quot;
&quot;What are your plans?&quot;
&quot;Clubbing!&quot;
&quot;Ugh! I don&#39;t want to go to a stupid club.&quot;
&quot;We&#39;ll get some booze, have some fun, meet some hot chicks and we&#39;ll get you over that
bitch.&quot;
&quot;You don&#39;t have to call her that.&quot; Dhruv shrugged.
&quot;She is a bitch.&quot; Arnav&#39;s face stiffened.
&quot;Arnav, please...&quot; Dhruv tried to raise his voice.
&quot;Okay, just go take a shower,&quot; Arnav resigned.
&quot;Arnav please, I swear I would have come, but I just don&#39;t feel like going out tonight.&quot;
&quot;Get your ass off this couch right now, trim your messy beard, take a shower, put on clean
clothes. We&#39;re going clubbing tonight. It&#39;s settled.&quot;
Dhruv protested, but before he could make an argument, Arnav shut him up and said, &quot;Listen,
dude, your &#39;sad boy vibe&#39; days are over. Enough of being this caveman. We&#39;re getting you
cleaned up and out on the scene tonight. The world has too many beautiful people. And it&#39;s a
shame you’re holed up in your room behaving like some psychopath. Stop wasting away your
youth and good looks, my friend. Carpe Diem!&quot; Arnav smirked and Dhruv hung his head low
in resignation.
“By the way, you stink,&quot; Arnav threw a towel on Dhruv’s face.
&quot;And, don&#39;t forget to shave that god-awful beard,&quot; he added.

Half an hour later, he emerged out of the bathroom looking like the same old Dhruv again.
The clean-shaven face highlighted his boyish features. On the inside though, Dhruv didn’t
feel any less miserable than before, but Arnav didn&#39;t give up on his friend.  He forced him
into the car, as they went on to pick up their other two friends from college Rohan and
Sameer.
Rohan had bought a new bottle of scotch. He raised a toast to Dhruv, &quot;Here&#39;s to our boy and
the return of his days of freedom and fun.&quot;
The night continued, hopping from nightclub to nightclub, drinking gallons of alcohol and
meeting new women. Dhruv got way too drunk in an attempt to wash away Anisha’s
memories. The more they flashed across his eyes, the more he drank in the hope to fade it all
out into nothingness. At one point, he barely recognized anything or anyone. It was all a giant
blur. Small fragments of consciousness kept escaping his mind like pieces of spatial matter
gallivanting across the sky. He felt like he was getting pulled into an expanding labyrinth and
his sense of self slowly continued sinking to newer lows.
Later in the night; he ended up sleeping with a slick woman who he’d met at the club a few
hours ago. The next morning, the memory of the night had almost vanished, but the hole in
his heart had widened.
This is the sample HTML : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 25vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    <p>The morning after another such bizarre and blurry night, he woke up with a splitting
    headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
    drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
    clutching his guitar and his journal close to him, pouring his grief into writing a song, but
    even creating new music reminded him of her. How they spent so many afternoons in his
    basement studio recording covers of their favourite Coldplay songs, after which she would
    drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
    that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.</p>
    <p>To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
    covered his gullible boyish charm, making him look jagged and intimidating. He spent most
    of his time holed up in his room. The only time he left the house was to hit the gym. His
    social circle diminished and his grades began falling quickly.</p>
    <p>Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
    favourite. Lead guitarist at the college band, straight As with an impressive academic record,
    broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
    going for him. Until he met the stunning Anisha Singhania.</p>
    <p>She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
    rain, but before he knew it, he had been struck by lightning.</p>

    <p>In the summer of his pre-final year at engineering college, when he was conducting auditions
    for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him. </p>
    <p>“Hey, I'm Anisha.” She extended her hand. </p>
    <p>“Hi! I’m Dhruv,” he responded softly and shook hands with her. He couldn't help but notice
    the striking manicured nails polished with a deep black color.</p>
    <p>“I have heard a lot about you.” she said with a strikingly odd smile.</p>
    <p>“Oh is that so?” He appeared visibly embarrassed.</p>
    <p>“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
    little myself. And I was wondering if I could join the band too.”</p>
    <p>“Thank you, that's very kind of you. You're welcome to the auditions.”</p>
    <p>“Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
    turn is in half an hour, so I thought it'd be a good use of time to get to know one of the finest
    seniors in college.” </p>
    <p>“That's really kind of you. I'd love to catch up, but I'm sorry, I need to focus on these
    auditions right now.” He shrugged and excused himself.</p>
    <p>“No worries. It was nice talking to you.”</p>
    <p>“All the best for the audition, Anisha,” he said with a placid smile.</p>

    <p>Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
    He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
    couple of times, she caught him stealing glances at her and returned an alluring smile. </p>
    <p>Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
    performance. And then as her name was announced, she walked up to the stage, gazing
    fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.</p>

    <div class="poetry">
    “You could buy me diamonds<br>
    You could buy me pearls<br>
    Take me on a cruise around the world<br>
    Baby, you know I'm worth it...”
    </div>

    <p>Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
    there, she was literally ‘worth it’. </p>
    <p>Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
    Just then his phone vibrated to notify Anisha's friend request on Facebook. </p>
    <p>“Who is it?” Arnav enquired.</p>
    <p>“Well remember that girl, Anisha, from the auditions today?”</p>
    <p>“Yeah, the hot chick who sang, ‘A woman’s worth’?”</p>
    <p>“Yep. It’s her friend-request.”</p>
    <p>“Dude, I saw how she was talking to you. She is totally into you.”</p>
    <p>“Well let’s not jump to conclusions. It’s just a friend request.”</p>
    <p>“That’s her move.”</p>
    <p>“Well she could simply be interested in friendship. But she sure is very hot though.”</p>
    <p>“Well for starters, you don’t look like a pig yourself.”</p>
    <p>“Way to make a guy feel good about himself.” Dhruv smirked.</p>
    <p>“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
    you're quite a catch, so go for it!” Arnav said to him sarcastically while grabbing his phone
    from his hands and checking out Anisha's Facebook profile.  </p>
    <p>“Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.</p>
    <p>Arnav rolled his eyes and continued stalking her profile.</p>
    <p>Dhruv looked at him with a slackened expression and accepted the friend request. </p>
    <p>In less than five minutes his phone buzzed again. This time it was a message from her. He
    opened his phone to a, “Hey! How’re you doing?”</p>
    <p>“See? So what happened to Mr Righteous, Let’s not generalise and jump to conclusions’,
    Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
    intellectual side for her!” He joked.</p>
    <p>“As you say, sir!” Dhruv resigned to his friend’s comments.</p>
    <p>“Good! Now you have fun with your new and smoking hot endeavours.” Arnav smirked
    bidding his goodbye.</p>
    <p>“See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
    phone and checked out Anisha's profile. Her display picture was a stunning portrait of her
    clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
    bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv's attention before
    another message from her popped up on the screen.</p>
    <p>“Hey! Are you there?” her message read.</p>
    <p>Dhruv opened the chat box to text her back. </p>
    <p>“Hey! What’s up?”</p>
    <p>“Nothing much. Was listening to some classical jazz.”</p>
    <p>“Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.”</p>
    <p>“You do? I thought only girls dig those kinds of songs,” Anisha replied.</p>
    <p>“I am a huge fan of Sinatra and a lot of other artists from that time. I think if you're
    passionate about music, then you tend to appreciate good work, irrespective of the genre or
    the artist. Besides, those are classics,” Dhruv typed.</p>
    <p>“Oh, I think I am talking to a proper musician here.” she added a few blushing emojis.</p>
    <p>“Haha come on, you’re embarrassing me.” </p>
    <p>“You know what's better than a passionate musician?”</p>
    <p>“What?”</p>
    <p>“A modest one.”</p>
    <p>“Hahaha! Is that so?”  </p>
    <p>“Oh, it is so. Anyway, who's your favourite artist or band?” she asked.</p>
    <p>“Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
    too.”</p>
    <p>“Ahh, ‘Tears in heaven’!”</p>
    <p>“Oh, it transports me to another world every time I listen to it. In fact I was planning on
    doing a cover on it tomorrow.”</p>
    <p>“Really? If you don't mind, can I join? Like I won't sing, but I can help, you know?”</p>
    <p>“Yeah, sure. That'd be great.”</p>
    <p>“Perfect, when and where?”</p>
    <p>“Umm… tomorrow, my place, around six?”</p>
    <p>“Sounds great. I can't wait!”</p>
    <p>“Great, see you then. Also, how could I forget to mention, you were terrific today. I mean
    Alicia Keys is phenomenal, and you did absolute justice to her.” </p>
    <p>“Did I? I thought I blew it.”</p>
    <p>“Are you kidding me? No, you had the whole crowd going crazy over your voice.”</p>
    <p>“Oh really, you too?”</p>
    <p>Dhruv didn’t know what to say, so he let her comment slide and replied with a laughing
    emoji.</p>
    <p>The next evening she came to his place and they had a lot of fun recording a cover of ‘Tears
    in Heaven’ in his basement studio. Although the actual recording didn’t happen for more than
    half an hour, they spent the rest of the two hours hanging out in his room and talking about
    everything from college, the band, music, career plans and dream cities.</p>
    <p>“I don’t want to be tied to one place.” Anisha said. “I want to travel the world. Go to every
    small and big city, and perform at every stage. Have my voice be heard.”</p>
    <p>“Sounds like a fancy plan. I hope you’re able to create this life for yourself.”</p>
    <p>“What do you want to do?”</p>
    <p>“Umm. I am not too sure. Dad wants me to go to a Business school. But they won’t be happy
    with anything but the best. And then once I have my MBA degree, he’d rather have me join
    the family business. Try to digitise things and expand to newer markets.”</p>
    <p>“You just told me what your dad wants. I asked you, ‘What do you want?’”</p>
    <p>He looked at her and let out a deep breath.</p>
    <p>“Well, I want to build a life of my own.”</p>
    <p>“And what does that life look like?”</p>
    <p>“I don’t know. Simple yet meaningful and fulfilling. Something I can be proud of.”</p>
    <p>“That’s so abstract.”</p>
    <p>“Yeah. I guess. It’s not just about what I want to do for work but the impact I have in this life.
    I want to have meaningful relationships and experience life from different lenses. Travel
    travel, but not to just see the world, but experience cultures and learn about people and what
    drives them.”</p>
    <p>“Your plan sounds so fancy and existential at the same time. How do you do it?”</p>
    <p>“Hahaha I don’t think it’s a plan. It’s just something I hope I get to do.”</p>
    <p>“Hmm”</p>
    <p>“Have you watched Before Sunrise?”</p>
    <p>“No.”</p>
    <p>“In that movie Julie Delpy says this one thing to Ethan Hawke, that hits me so hard every
    time I think about it, ‘Isn’t everything we do, a way to be loved a little more?”</p>
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    <p>Dhruv looked at her, not knowing what to say, as she stared at the drab mesh-like figure
    created by the dilapidated rooftops of neighbourhood houses.</p>
    <p>“My mother always asked him to quit smoking. But it was as though he loved cigarettes more
    than he loved any of us…”</p>
    <p>You know, I loved him the most. And when he passed away, I was a total wreck. I began
    hating him for choosing the filthy carcinogenic addiction over his family. I was so mad at
    him, I stopped eating, studying, everything. Can you be mad at the dead?” she asked, but
    Dhruv had no answers. He barely processed Anisha's confessions. He had no idea she cloaked
    such things behind her cheery demeanour. </p>
    <p>“It was the 3rd of September, I clearly remember. Ten days after dad passed away. We barely
    even sorted out his belongings. My mom would spend hours, just sitting in his chair, hugging
    his old white shirt.
    On the evening of 3rd September, I drove to the small cliff ten kilometres down from our Goa
    house. I barely knew how to drive, but anger makes you do strange things.
    Before leaving, I had grabbed the last pack of cigarettes from dad's belongings and there at
    the cliff, I stood by the sea and lit my first ever cigarette. I still don't know why I did it.</p>
    <p>I think I did it partly because I was mad at him and wanted those cigarettes to consume me
    the same way. And partly because I felt it was the last thing that connected me to dad, the one
    thing he couldn't give up. I embraced it as a part of my life. Every time I smoke now; it
    reminds me of him. And I hate it. But I also love it. And I miss him.” She completed her
    monologue and lit another cigarette. He held her hand and ran concentric circles on her skin
    with his index finger.</p>
    <p>She kept smoking; her eyes fixed rigidly on a broken stool lying in the corner. The cawing of
    the black crows on the thin wires between electricity poles, created an eerie atmosphere. He
    looked at her, and he couldn't help but think that the more he got to know her, the more of a
    mystery she seemed to him, but one that he was quickly getting spiralled into. She held the
    cigarette between her index and middle finger and stuck out her hand in his direction to offer
    him the cigarette. He stared into her dark eyes and accepted the cigarette. Without
    exchanging a single word, they sat there smoking late into the evening, until the entire place
    got bathed in darkness. Suddenly, he felt her smoky lips on his. Her hands slowly traced his
    body, and he could feel his lips slowly brush against hers. She tasted like coffee and
    cigarettes. His hands grazed her inner-thigh, and they kept getting lost in each other's smoke-
    stained breath. </p>

    <p>****</p>

    <p>For a whole year, Dhruv dated Anisha. Since that strange and significant evening on his
    terrace when she opened up about her childhood, things quickly picked up between them.
    And before he knew it, every small and big thing about her seemed extraordinary to him. Her
    passion for music, her funky nails and eccentric tattoos. Her habit of making jokes at the most
    inappropriate times and then suddenly shifting gears to share a deeply personal childhood
    story and always lighting a smoke while she told it.</p>
    <p>In a matter of a few months, Anisha’s personality started rubbing on him like sandpaper. The
    usually quiet and absorbed-in-his-own-world Dhruv began going to parties and social events
    with her. They began bunking classes and hanging out at a <i>tapri</i> near college, smoking
    cigarettes and drinking adrak chai before setting out to drive around the colourful lanes of old
    Delhi to explore the food scene, visit local pubs, art galleries and old architectural
    monuments.</p>
    <p>On her birthday, he planned a surprise terrace party at his place and invited all their friends.
    She walked in at midnight to see the whole place dazzling with fairy-lights, helium balloons
    and a big custom cake that had a picture of her singing at the band auditions.</p>
    <p>“This is straight out of a dream!” She’d said and kissed him on the lips. “Thanks for being in
    my life.” They cut the cake, got drunk on cheap tequila and danced the night away.</p>
    <p>As their social circle expanded, they began getting more invites to parties of common friends,
    where they went as a couple. But oftentimes Anisha would just be outside in the smoking
    zone and end up talking to a lot of new people. At another such party, Anisha struck a chord
    with someone she borrowed a lighter from.</p>
    <p>“What are you doing tomorrow evening?” The man with a giant tattoo and broad build who
    lent her the lighter, had asked her.</p>
    <p>“Why?” She inquired bright-eyed.</p>
    <p>“I’d love to take you out for coffee. I know a really nice place here.”</p>
    <p>She took a moment and smiled, as though assessing the situation.</p>
    <p>“Is there so much to think about?” He smirked.</p>
    <p>She laughed and rolled her eyes at his remark before finally agreeing. “An innocent coffee
    won’t hurt anyone.”</p>
    <p>Dhruv attracted plenty of eye-balls too, but he usually kept to himself. He’d grab a drink and
    talk to a few people, before starting to look for Anisha and ensure she wasn’t getting too
    wasted. Initially though, he appreciated how tactile she was, but eventually he grew jealous
    seeing Anisha work her way through all these social events, getting enormously drunk and
    dancing voluptuously with many strange, new men. At first, he thought he was being too
    sceptical and conventional. So he tried to shove away his thoughts, but then Anisha began
    lying to him about her whereabouts, drinking, smoking and partying heavily. Dhruv was
    concerned, and hoped she would come around. But when he confronted her, he was only met
    with contempt and accusations of being an overprotective and jealous boyfriend.</p>
    <p>He started feeling increasingly anxious when Anisha wasn't around. And ever since he had
    heard from a couple of common friends that Anisha got so wasted at a party, she puked for
    two hours straight, he started showing up at parties he wasn't even invited to, just to take care
    of her, drive her home safe and make sure she didn’t do something that she would regret
    later. </p>
    <p>To an informal fresher’s party hosted by the band, Dhruv who was in his final year and
    Anisha who was now a sophomore, were invited as seniors. It was at a coveted club in Vasant
    Kunj, pretty near to Dhruv's place, but he still went all the way to pick up Anisha from her
    hostel.</p>
    <p>She was wearing a little black dress and high-heeled gladiators.</p>
    <p>“Hi babe!” Dhruv smiled as she entered the car.</p>
    <p>“Hey” she replied distantly as she adjusted the seat to make herself comfortable.</p>
    <p>“You’re looking stunning tonight.”</p>
    <p>“Thank-you” She said with a bright smile. And then after assessing him from top to bottom
    for a full minute, she squinted her eyes and said, “You don’t look too bad yourself!”</p>
    <p>Laughing at her own remark, she fixed the collar of his shirt.</p>
    <p>Like always she began touching up her make-up in the mirror.</p>
    <p>“Eyes on the road, mister!” she teased him, as he looked at her, adoring her antics.</p>
    <p>Just then her phone rang. Before Dhruv could see the screen, she quickly pressed the buzzer
    to put it on silent.</p>
    <p>“Who is it?”</p>
    <p>“Some sales call or something, been getting too many of these lately.” She replied, visibly
    bothered, and threw her phone back in her clutch in a haphazard manner.</p>
    <p>“Then why are you so flustered?” He asked, eyes fixed on the road.</p>
    <p>“I am not flustered.” She shot back. A tiny bead of sweat formed on her forehead.</p>
    <p>He pulled a tissue and offered it to her. She looked at him for a second and then took the
    tissue reluctantly.</p>
    <p>“I think this new moisturiser is not suiting my skin.” She said, dabbing the tissue lightly on
    her forehead and cheek.</p>
    <p>“There’s water in the back if you want.”</p>
    <p>“No. I am good. Thanks.”</p>
    <p>After a few moments of awkward silence, Dhruv tried to lighten the atmosphere. “Did you
    hear about the auditions that happened last week?”</p>
    <p>“Uh hmm”she replied, still staring out the window.</p>
    <p>“People were going on and on about the guy who sang ‘Breathless.’ What’s his name?
    Avinash, I think.”</p>
    <p>“Well, good for him.”</p>
    <p>“I think the band is to see some great talent this year.”</p>
    <p>“Yeah. I guess.”</p>
    <p>“Anisha..”</p>
    <p>“Hmm?”</p>
    <p>“We met around the same time last year.”</p>
    <p>“Yeah”</p>
    <p>“You know, we owe this relationship to the band.”</p>
    <p>“Maybe”</p>
    <p>“Had you not come to audition, we probably wouldn’t have been dating.”</p>
    <p>“I was still going to the same college. We could have met anywhere, Dhruv. Seriously, why
    are you so sentimental today?” she frowned and looked out the window.</p>
    <p>“I was just being nostalgic. What’s the matter with you tonight, Anisha?” He raised his voice.</p>
    <p>“I don’t know. I am sorry. I think I’m PMSing.” she groaned and continued staring out the
    window.</p>
    <p>“Okay. I am sorry. Do you want to stop on the way for a smoke or some tiramisu?”</p>
    <p>“No. It’s fine. Let’s just go.”</p>
    <p>“No, seriously? Whatever makes you feel better.”</p>
    <p>“Honestly. Just getting there would make me feel better.” She snapped back. </p>
    <p>They drove the rest of the way without exchanging a single word.</p>
    <p>At the party, they received a warm welcome. Dhruv was among the senior-most members of
    the band. A flock of junior boys and girls surrounded him.</p>
    <p>After a while, as the chatter slowly faded and he freed himself from the crowd, he strolled
    around to look for Anisha. Making his way past big crowds of people dancing and singing
    loudly, he finally reached the smoking corner, where he’d hoped to find Anisha. But to his
    surprise, she was not there. He felt a little anxious and decided to get himself a drink to ease
    his nerves first. Meanwhile, he tried reaching her phone, but it was switched off, which
    fuelled his worries. She never slipped away from a party without telling him. He didn't know
    what to do and ended up nervously downing four pegs of whiskey. He kept trying her phone
    and checked with a few people but nobody knew where she was.</p>
    <p>All the alcohol created pressure on his bladder, and he headed towards the loo. As he reached
    the restroom, he heard moaning sounds from the adjacent women's loo. A weird feeling rose
    in his stomach. He felt like he might throw up. Without thinking further, he pushed open the
    door. </p>
    <p>Dhruv received the shock of his life.</p>
    <p>Anisha was kissing a junior from sophomore year. The loud thud startled her, and she jumped
    seeing Dhruv standing over them.</p>
    <p>Dhruv couldn't believe his eyes. The abhorrent shock, coupled with the effect of three pegs of
    whiskey he had downed earlier, made him lose balance. He almost fell and held the door for
    support. Anisha was scared out of her wits and rushed to support him. But he shrugged her
    hand and stepped back, incapable of letting her touch him.</p>
    <p>She saw a burning rage in his eyes that she had never seen before. </p>
    <p>“Dhruv…” she cried and ran after him as he raced down the stairs. </p>
    <p>The pain and fury gleaming from his eyes peered at her. Almost everyone at the club fell
    silent and gathered around to see – A drunk and shell-shocked Dhruv rushing out of the
    premises and a weepy, guilt-ridden Anisha chasing him down the parking lot. </p>
    <p>But before she could catch hold of him, Dhruv was already speeding off in his car. The
    screeching sound of the tires on the road echoed in the deathly silence as everyone quieted
    down. </p>
    <p>“Dhruv…” Anisha screamed in the middle of the street and wept inconsolably. </p>

    <p>****</p>

    <p>A whole week went by and Dhruv didn't show up at college at all. He barely picked calls
    from any of his friends, and simply spent all his days and nights locked up in his room.
    Sometimes the sound of a guitar echoing through his room was the only signal that he was
    alive. Worried sick, Mrs Malhotra called Arnav.</p>
    <p>“Aunty, I’ve tried calling and texting him so much. But he barely responds.” He told her over
    the phone. Next evening Arnav showed up at the Malhotra house unannounced and opened
    the door to Dhruv’s room, only to see a bony figure lying on the bed in the darkness. </p>
    <p>“Oh Hi…I didn’t know you were coming.” Dhruv got up, taken aback. His weight loss was
    apparent. With a thickly grown unkempt beard, he looked shabbier than ever. </p>
    <p>Arnav entered and switched on the lights.</p>
    <p>Dhruv flinched. “Ah, switch off the lights,” He groaned. </p>
    <p>“No”</p>
    <p>“Arnav…”</p>
    <p>“Bro, you're a mess,” he reprimanded, kicking him out of bed. “That’s it. We’re going out
    tonight. It's been ten days you haven't shown your stupid face to any of us.”</p>
    <p>“Man, I don't feel like it.”</p>
    <p>“I don't care, buddy. If I feel like hanging out with my friend Dhruv, I will hang out with my
    friend Dhruv. Period.”</p>
    <p>“What are your plans?”</p>
    <p>“Clubbing!”</p>
    <p>“Ugh! I don't want to go to a stupid club.”</p>
    <p>“We'll get some booze, have some fun, meet some hot chicks and we'll get you over that
    bitch.”</p>
    <p>“You don't have to call her that.” Dhruv shrugged. </p>
    <p>“She is a bitch.” Arnav's face stiffened. </p>
    <p>“Arnav, please...” Dhruv tried to raise his voice. </p>
    <p>“Okay, just go take a shower,” Arnav resigned. </p>
    <p>“Arnav please,

    Here is the target chapter: <<CHAPTER_TEXT>>
        """
        prompt_1 = prompt_template_1.replace("<<CHAPTER_TEXT>>", first_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_1 = client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_1,
              }
          ],
          model=model,
          temperature=0
      )

        response_1 = chat_completion_1.choices[0].message.content

      # Process the second part with a modified prompt (no HTML headers)
        prompt_template_2 = """
      You are an expert book formatter.
      Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
      Font size = <<fontsize>>
      Line height = <<lineheight>>
      Include these features in html:
      1. Paragraph Formatting
      Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
      2. Line Length
      Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
      3.Line Spacing (Leading)
      Comfortable Reading: The line spacing should be the same as given in the example.
      4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
      8. Left and Right margins are minimum so the pdf looks like a book.
      7.  Consistency
      Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
      8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
      9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
      Keep this in mind : Left and Right margins are minimum.
      10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
      11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

      Here is the continuation of the chapter:
      <<CHAPTER_TEXT>>
      """
        prompt_2 = prompt_template_2.replace("<<CHAPTER_TEXT>>", second_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_2 = client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_2,
              }
          ],
          model=model,
          temperature=0
      )

        response_2 = chat_completion_2.choices[0].message.content

        # Process the second part with a modified prompt (no HTML headers)
        prompt_template_3 = """
      You are an expert book formatter.
      Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
      Font size = <<fontsize>>
      Line height = <<lineheight>>
      Include these features in html:
      1. Paragraph Formatting
      Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
      2. Line Length
      Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
      3.Line Spacing (Leading)
      Comfortable Reading: The line spacing should be the same as given in the example.
      4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
      8. Left and Right margins are minimum so the pdf looks like a book.
      7.  Consistency
      Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
      8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
      9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
      Keep this in mind : Left and Right margins are minimum.
      10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
      11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

      Here is the continuation of the chapter:
      <<CHAPTER_TEXT>>
      """
        prompt_3 = prompt_template_3.replace("<<CHAPTER_TEXT>>", third_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_3 = client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_3,
              }
          ],
          model=model,
          temperature=0
      )

        response_3 = chat_completion_3.choices[0].message.content

        # Now, merge the two responses
        # Extract the <body> content from the first response and append the second response

        # Find the closing </body> and </html> tags in the first response
        body_close_index = response_1.rfind("</body>")
        html_close_index = response_1.rfind("</html>")

        if body_close_index != -1:
		# Insert the second response before the closing </body> tag
          	merged_html = response_1[:body_close_index] + "\n" + response_2 + "\n" + response_3 + "\n" + response_1[body_close_index:]
        elif html_close_index != -1:
		# Insert before </html> if </body> is not found
          	merged_html = response_1[:html_close_index] + "\n" + response_2 + "\n" + response_3 + "\n" + response_1[html_close_index:]
        else:
          	# If no closing tags are found, simply concatenate
          	merged_html = response_1 + "\n" + response_2 + "\n" + response_3

        return merged_html

	
def save_response(response):
    html_pth = 'neww.html'
    with open(html_pth, 'w', encoding='utf-8') as file:
        file.write(response)
    return html_pth


nest_asyncio.apply()

async def html_to_pdf_with_margins(html_file, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        await page.set_content(html_content, wait_until='networkidle')

        pdf_options = {
            'path': output_pdf,
            'format': 'A4',
            'margin': {
                'top': '85px',
                'bottom': '60px',
                'left': '70px',
                'right': '40px'
            },
            'print_background': True
        }

        await page.pdf(**pdf_options)
        await browser.close()

def get_pdf_page_count(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)
    
def create_overlay_pdf(overlay_pdf, total_pages, starting_page_number, book_name, author_name, font, current_position):
    c = canvas.Canvas(overlay_pdf, pagesize=A4)
    width, height = A4

    def draw_header_footer(page_number, position):
        c.setFont(font, 12)

        if page_number == starting_page_number:
            # First page of the chapter: Draw page number at the bottom center
            footer_y = 30  # Adjust this value to match the bottom text's baseline
            c.drawCentredString(width / 2, footer_y, f'{page_number}')
        elif position == "Right":
            # Right-side pages: Draw header on the right and page number at the right
            c.drawCentredString(width / 2, height - 40, book_name)
            c.drawString(width - 84, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap
        elif position == "Left":
            # Left-side pages: Draw header on the left and page number at the left
            c.drawCentredString(width / 2, height - 40, author_name)
            c.drawString(62, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap

    # Create pages for the overlay
    for i in range(total_pages):
        current_page_number = starting_page_number + i  # Continuous page numbering
        draw_header_footer(current_page_number, current_position)

        # Alternate position for the next page
        current_position = "Left" if current_position == "Right" else "Right"

        c.showPage()

    c.save()

    # Return the final position for the next chapter
    return current_position

def overlay_headers_footers(main_pdf, overlay_pdf, output_pdf):
    pdf_writer = PdfWriter()

    # Load the main PDF and the overlay PDF
    with open(main_pdf, 'rb') as main_file, open(overlay_pdf, 'rb') as overlay_file:
        main_pdf_reader = PdfReader(main_file)
        overlay_pdf_reader = PdfReader(overlay_file)

        # Ensure the overlay PDF has the same number of pages as the main PDF
        print(len(overlay_pdf_reader.pages))
        print(len(main_pdf_reader.pages))
        if len(overlay_pdf_reader.pages) != len(main_pdf_reader.pages):
            raise ValueError("The number of pages in the overlay PDF does not match the number of pages in the main PDF.")

        # Overlay headers and footers on each page
        for page_num in range(len(main_pdf_reader.pages)):
            main_page = main_pdf_reader.pages[page_num]
            overlay_page = overlay_pdf_reader.pages[page_num]

            # Merge the overlay onto the main page
            main_page.merge_page(overlay_page)

            pdf_writer.add_page(main_page)

    # Write the combined PDF to the output file
    with open(output_pdf, 'wb') as outfile:
        pdf_writer.write(outfile)
