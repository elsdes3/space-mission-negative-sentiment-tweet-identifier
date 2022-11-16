# Guide to Manual Labeling Tweet Sentiment in Training Data

## [Table of Contents](#table-of-contents)
1. [About](#about)
2. [Rules](#rules)
   - [POSITIVE Sentiment tweets](#positive-sentiment-tweets)
   - [Questions that are not combined with an answer](#questions-that-are-not-combined-with-an-answer)
   - [Questions that are combined with an answer](#questions-that-are-combined-with-an-answer)
   - [Rhetorical questions](#rhetorical-questions)
   - [Hateful, Hurtful or Religious speech](#hateful-hurtful-or-religious-speech)
   - [Non-hateful speech with NEUTRAL sentiment](#non-hateful-speech-with-neutral-sentiment)
   - [Changing the name of the telescope to Betty White telescope](#changing-the-name-of-the-telescope-to-betty-white-telescope)
   - [Cost of Mission](#cost-of-mission)
   - [Conspiracy Theories](#conspiracy-theories)
   - [Regarding Cameras to View Inside or Outside of JWST](#regarding-cameras-to-view-inside-or-outside-of-jwst)
   - [Sending People on JWST](#sending-people-on-jwst)
   - [Doomsday Scenarios involving JWST](#doomsday-scenarios-involving-jwst)
   - [UFOs or Aliens](#ufos-or-aliens)

## About
This a guide to help identify the sentiment of a tweet during manual labeling of training data. This guide is used to manually label sentiment in tweets in
- `train_nlp__inference_starts_20220110_000000.xlsx`
- `val_nlp__inference_starts_20220110_000000.xlsx`
- `test_nlp__inference_starts_20220110_000000__batch_1.xlsx`

in the S3 bucket.

## Rules
### POSITIVE Sentiment tweets - #
1. These are Tweets by
   - NASA annoucing
     - press conference discussing mission
     - changes to launch/operations livestream
   - publishers or blogs
     - posting a link to article discussing mission
       > Engineers from  have completed the unfolding of the James Webb space telescope! described as a “time machine” this telescope will allow to study the beginning of the universe shortly after the Big Bang.
       > Hackaday Links: January 9, 2022It looks like we have a new space observatory! According to NASA, all the major deployments on the James Webb Space Telescope have been completed successfully. This includes the tricky sunshield deployment and tensioning, which went off
   - NASA/publishers
     - status updates for the mission
       >  James Webb Space telescope fully deploys its sunshield. A major milestone crossed!
   - Twitter users
     - expressing excitement/interest in or complimenting mission
       > the only thing keeping me going rn is the webb telescope,,
       >  So, in a single person’s lifetime — if that person is Betty White — we went from general acceptance of a universe with 1 galaxy to a universe with 200 billion+ galaxies.  And the James Webb telescope will show us far more than we’ve seen so far. Something to look forward to!
       > As a space fanatic, I am extremely excited that the James Webb Space Telescope has been fully deployed. It's next course is helping humanity to answer the big questions in Life; to understand our origins and  answer the query; ARE WE ALONE IN THE UNIVERSE?
     - questions to other Twitter users that do not require a tech-support response
       >  Did anyone watch the unfolding of the Primary Mirror of the JamesWebb Telescope?
     - contains a positive/complimentary sentence/phrase/tone
       >  Looks like you're beating them at James Webb Space Telescoping

   are POSITIVE since they don't contain any negative phrase/sentence/tone. These tweets do not need to be answered by the mission staff support team monitoring Twitter.

### Questions that are not combined with an answer - #
1. Mission-specific question by Twitter user and that need to be answered by the mission staff support team monitoring Twitter
   - NEUTRAL
     >  hi David here watching in UK. When will we see the first image from the Webb telescope?
     >   A Question about JWST? How does the James Webb Telescope stop at the Lagrange point ?
     >  sent James Webb Space Telescope to a point 1.5 km away from earth named Lagrange Point 2 . But why  need to go to L-2 ? or what the heck is Lagrange Points ? A thread
       - the first sentence is positive and the second sentence is negative, so the overall sentiment is NEUTRAL
     >  As the James Webb telescope is said to be 100 times more powerful than Hubble, what are the chances of it capturing the face of God or Brian?

### Questions that are combined with an answer - #
1. These are POSITIVE sentiment tweets since they do not need to be answered by the mission staff support team monitoring Twitter
   - Twitter user posts question follwed by answer (this might be a link to a news article or blog that answers the question)
     > As a space fanatic, I am extremely excited that the James Webb Space Telescope has been fully deployed. It's next course is helping humanity to answer the big questions in Life; to understand our origins and  answer the query; ARE WE ALONE IN THE UNIVERSE?
     > Who is James Webb?You might be thinking, who gets the honour of having such a historic telescope named after them? Well, that title goes to James Edwin Webb, the second administrator of NASA, best known for heading up Apollo –
     > But why L-2 ‽The L2, where the James Webb Space Telescope is going, is ideal for astronomy because it can keep Sun, Earth and Moon behind the spacecraft for solar power and (with appropriate shielding) provides a clear view of deep space .

### Rhetorical questions - #
1. These can be
   - POSITIVE (this captures most tweets in this category)
     - tweet may compliment the achievement of launching the JWST mission and/or also include a rhetorical question (user is thinking out loud)
     - these questions do no need to be answered by the mission staff support team monitoring Twitter.
       >  Are you telling me that James Webb spaced this telescope?
       > James Webb telescope will able us to see almost 100 million light years after the big bang... That's almost 18 billion years of our universe... I wonder what we would find..
   - NEGATIVE
   - NEUTRAL

### Hateful, Hurtful or Religious speech
1. These are
   - NEGATIVE if the entire tweet text is a hurtful or angry phrase/sentence/tone
     >  Dont disgrace the name of James Webb
     >   What are the chances of a meteorite damaging James Webb's mirror?
     > hear me out, what if when they look through the james webb telescope, they collapse the wave function of humanity and we all get thanos snapped out of existence?
     >  spent $10B to develop James Webb Space Telescope and made it unserviceable.It's like buying Aston Martin made by hands and throwing it away when the windshield cracks from the small rock from the car in front
     > Has anyone made a joke about hoping NASA took the lens cap off the James Webb Telescope yet? Because that is a joke one, but no more than one, person might make to our mild amusement. But not thousands of people though, day after day after day after day. That would be too many.
       - all three sentences are NEGATIVE so the overall sentiment is labeled as NEGATIVE
     > I'm surprised evangelicals didn't try to sabotage the James Webb telescope.
   - may be NEUTRAL, if a hurtful phrase/sentence/tone is combined with positive phrase/sentence/tone
     > james webb space telescope is trans, sorry nasa not sorry
       - *sorry nasa not sorry* is NEGATIVE, while the reset of the text is POSITIVE, so the overall sentiment is labeled as NEUTRAL

### Non-hateful speech with NEUTRAL sentiment - #
1. These are NEUTRAL since
   - the negative phrase/sentence/tone is combined with a positive phrase/sentence/tone
     >  I'm going to ask you everyday for the next 365 days until I get a reply. Can you please put your SpaceX livestreams in 360 VR so I can watch on my Oculus Quest? (Day 254/365)
     >   Hopefully James Webb. Don't think I've ever seen him before
   - focus on JWST operations that are completed but also pointing out those that are left
     >  I breathed a sigh of relief when the secondary mirror deployed. But I too won't really relax till data comes down. I still remember the anguish when they found Hubble's mirror was ground precisely to spec--but the wrong spec. I know they tested the heck out of Webb, but still.
     > The tension continues as the Webb telescope continues to tension the layers of the sunshield. Three layers done and two left for tomorrow.
     > the James Webb telescope is going to look deep into the past in an attempt to comprehend the present but just kind of sit there otherwise and I think we can all relate
   - tweet hilights achievement of JWST mission but also surprise by lack of interest
     > How is it we have just launched one of the most exciting pieces of tech of our generation and no one's talking about it? The world should be watching the James Webb telescope in awe, the development, engineering  ,
     >  James Webb launch and subsequent unfolding success! Outside the 24/7 cable news doom cycle there are some great things happening. Your point stands though if the polls are to be believed (US as divided as ever, although I don't see it in my daily life).

### Changing the name of the telescope to Betty White telescope - #
1. The sentiment of these tweets can be
   - NEGATIVE
     - twitter users
       - posting that name should be changed
         > Petition to change JWST to Betty White Space Telescope
         > On Twitter, right now, people tweeting about changing the name of JWST to BWST - Betty White Space Telescope. A lot of them are serious about it.A lot of them.
       - making false claim about name of mission
         > JWST stands for Jbetty White Space Telescope
         > Now hear this: The James Webb Space Telescope has now transformed into the Betty White Space Telescope. Pass it on.  &gt;
       - deragotory comments about James Webb and/or Betty White
         >  hmm.. no.James Webb did far more for humanity then Betty White ever did. Not saying she was a bad person, but what is the fascination with that old woman?
           - *James Webb did far more for humanity then Betty White ever did* is NEUTRAL and the rest are NEGATIVE, so the overall sentiment is NEGATIVE
         >  The director of the James Webb space program supports the MEK. What a cult that the MEK have attracted all these people. And if that doesn't mean anything how about you show your "activities against the regime". Show proof of a single transaction between any country and the MEK.
   - NEUTRAL
     - mixture of negative and positive phrase/sentence/tone
     - see bullet-point for *Non-hateful speech with NEUTRAL sentiment*
       > Here's why it should be changed to the Betty White Space Telescope. She was not just an acting legend, but also an  ally. Webb was homophobic.
       >    can we petition to rename JWST to the Betty White Space Telescope?How many people knew &amp; loved Betty White? proly 5-6 orders of magnitude more. It would evoke warm memories and promote her life long message supporting all that is good.Who is James Webb?
         - the first sentence has a NEGATIVE tone for the mission, the remaining sentences are POSITIVE, so the overall sentiment is labeled as NEUTRAL
       >     the accomplishments of James webb fully outweigh Betty white and you have no real reason to rename this telescope. if you're psychotic enough to want a telescope named after her then name one that hasn't already been named.
         - *if you're psychotic enough* is NEGATIVE, while the reset of the text is POSITIVE, so the overall sentiment is labeled as NEUTRAL
       >  Good idea, but unlikely. What about calling it "The Betty White Lagrange Point" though?Then anchors could say "The James Webb Space Telescope located at point Betty White...."
         - the first sentence is mixed POSITIVE and NEGATIVE sentiment, the second sentence is NEGATIVE and the third sentence is POSITIVE, so the overall sentiment is labeled as NEUTRAL
       >   I had a really good discussion about it with a friend and yeah, no Webb, only "Betty White Space Telescope" from here on out.
         - *I had a really good discussion about it with a friend* is POSITIVE, while the reset of the text is NEGATIVE, so the overall sentiment is labeled as NEUTRAL
   - POSITIVE
     - may or may not be related to the mission but talks about positive aspects of James Webb and/or Betty White
       >  No. It's named after James Webb for a good reason the name of a theater to Betty White, or something along those lines
       > Betty White dies a few days after the launch of the James Webb telescope, she knew her secret could be kept no longer. As Webb gazes into the distant past, deep into the reionization period, all we will see is White. Betty White...
       >  Betty White was a much-loved entertainer whose great passion in life - besides fun - was animal welfare advocacy. The   should remain named for late NASA administrator James Webb. Remember Ms. White on Earth for the great person she was.
       >   No. James Webb deserves this honor. Name something else after Betty White. Please.
       > Really hope the James Webb Space Telescope finds Betty White on some distant planet drinking a Margarita poolside
       >   So is James Webb. (But between the two, I’d bet that Betty White is more internationally known than James Webb.)

### Comparing Hubble to JWST - #
1. These can be
   - POSITIVE
     - if there is no negative sentence/phrase/tone in the text
     - compliments one or both missions
   - NEUTRAL
     - tweet asks for comparison between two telescopes
       > What makes James Webb different and better than the Hubble telescope?
   - NEGATIVE
     - tweet berrates one mission relative to the other
       >  Don’t worry about JWST, he may be bigger and more sophisticated than you Hubble, but you’re more iconic, plus remember this, he’d be nothing without you, any and every space telescope is completely worthless without you
     - tries to qualtify how much better JWST is compared to Hubble
       > Hubble Telescope &lt;&lt;&lt; James Webb Telescope

### Scientific Merrit/Objectives of Mission or Design of Payload - #
1. These can be
   - NEGATIVE
     - criticize mission objectives and/or operations
       >  could you create more affordable alternatives for $10bln James Webb Space Telescope  to send more of it to explore cosmos?
     - criticize design of payload
       >  A 1994 Ford F150 is just about as complex as James Webb, right?
         - intentionally under-estimates complexity of payload

### Cost of Mission - #
1. These can be
   - NEGATIVE
     - tweet indicates mission costs too much
       >  Are you serious.. it’s cost £6 billion… James Webb telescope was £20billion… who is going to pay for it… It ends now. It’s endemic get on with you idiot.
     - tweet references mission cost in a negative tone
       >   The £37bn wasted on  Track &amp; Trace would have:- paid for 5 James Webb Space Telescopes- paid for 3,700 new stealth fighter-bombers @ £100m each !!!
       > James Webb telescope costs as much as the USA spends on Halloween Candy every single year.Humanity...
   - NEUTRAL
     - tweet references mission cost but contains positive and negative sentence/phrase/tone
       >  Ian £10 billion is such a small sum for the james Webb project considering the test track and trace cost £37 billion
         - tweet indicates mission does not cost too much (positive), but second part of tweet is negative, so overall sentiment is NEUTRAL

### Conspiracy Theories - #
1. These are related to whether space exploration is being staged (not real)
   - NEGATIVE sentiment
     - tweet questions if this or other mission(s) were faked
       >     This is such a contrived and narrow-minded comment.You make it sound like the US didn't send 5 rovers on Mars, build new rockets, construct a space station, fly a helicopter on Mars, and achieve dozens of other technological achievements.Ever heard of the James Webb telescope?
       > “The James Webb Hoax” will be a thing

### Regarding Cameras to View Inside or Outside of JWST - #
1. These are
   - NEGATIVE sentiment, since they imply the absence of the camera to view the JWST is a bad thing
     > NASA should immediately build and launch a space telescope capable of delivering breathtaking high resolution images of the James Webb Space Telescope floating unfolded in space

### Sending People on JWST - #
1. These are
   - NEGATIVE since they imply a human should be sent inside the telescope (away from Earth), which is derogatory in nature towards the person
     >  We should have sent him and the  crew up on the James Webb…

### Doomsday Scenarios involving JWST - #
1. These are
   - NEGATIVE since they imply damage to the JWST
     >  The James webb telescope has just gone off line. Apparently hit by an object leaving earth.
   - NEUTRAL since they both compliment the mission but also imply damage to the JWST
     >  An Ancient Solar System: The first week of the new year, off world: The James Webb space telescope deploys, craters on Titan and loads more...

### UFOs or Aliens - #
1. These can be
   - NEGATIVE
   - NEUTRAL
   - POSITIVE
     - discovery of or interaction with aliens
       > James webb will show and see a huge group of ufo comingBesides the universe revolve clock wise and another from out side anti clock wise
       >  My assumption on seeing Fesarius now is that James Webb will one day bump into an alien probe and get upgraded.

   depending on the sentence/phrase/tone of the tweet.
