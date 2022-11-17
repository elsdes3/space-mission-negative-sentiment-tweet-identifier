# Guidelines for Hand / Manual Labeling the Sentiment of Tweets

This is a guide for manually labeling tweet sentiment. This manually labeled data is used during
- initial model fine-tuning (training)
- fine-tuning (training) in production

Following a guide for handling how tweets should be labeled will help scale the labeling process as new tweets become available in production.

## POSITIVE Sentiment tweets
1. These are Tweets by
   - NASA annoucing
     - press conference discussing mission
     - changes to launch/operations livestream
   - publishers or blogs
     - posting a link to article discussing mission
   - NASA/publishers
     - status updates for the mission
   - Twitter users
     - expressing excitement/interest in or complimenting mission
     - questions to other Twitter users that do not require a tech-support response

## Questions that are not combined with an answer
- NEUTRAL
  - Mission-specific question by Twitter user and that need to be answered by the mission staff support team monitoring Twitter

## Questions that are combined with an answer
- Twitter user posts question follwed by answer (this might be a link to a news article or blog that answers the question)
  - POSITIVE

## Rhetorical Questions
- POSITIVE
  - tweet may compliment the achievement of launching the JWST mission and/or also include a rhetorical question (user is thinking out loud)

## Non-hateful speech with NEUTRAL sentiment
- NEUTRAL
  - focus on completed JWST operations but also pointing out those operations to be completed
  - tweet hilights achievement of JWST mission but also
    - surprise by lack of interest
    - make a critical comment about related or unrelated topic
  - tweet hilights related or unrelated topic in a positive light but also
    - makes a critical comment about JWST mission
  - looking for more information about mission science and/or operations

## Changing the name of the telescope (eg. to Betty White telescope, or other)
- NEGATIVE
  - posting that name should be changed
  - making false claim about name of mission
  - deragotory comments about James Webb and/or Betty White
- NEUTRAL
  - mixture of negative and positive phrase/sentence/tone
- POSITIVE
  - may or may not be related to the mission but talks about positive aspects of James Webb and/or Betty White

## Comparing Hubble to JWST
- POSITIVE
  - compliments one or both missions
  - points out benefit of one mission relative to other (without critizing either mission)
- NEUTRAL
  - tweet asks for comparison between two telescopes
- NEGATIVE
  - tweet berrates one mission relative to the other
  - tries to qualtify how much better JWST is compared to Hubble

## Scientific Merrit/Objectives/Operations of Mission or Design of Payload
- NEGATIVE
  - criticize mission objectives and/or operations
  - criticize design of payload
  - makes false claim about
    - how JWST will be used
    - aspect of mission
- POSITIVE
  - indicates theories that can be changed by JWST discoveries

## Cost of Mission
- NEGATIVE
  - tweet indicates mission costs too much
  - tweet references mission cost in a negative tone
- NEUTRAL
  - criticizes cost of unrelated topic but compliments low-cost of JWST mission
  - tweet references mission cost but contains positive and negative sentence/phrase/tone

## Nepharious Uses of JWST
- use telescope for
  - NEGATIVE
    - destruction
    - imaging specific group of people or animals on Earth

## Conspiracy Theories
- tweet questions if this or other mission(s) were faked
  - NEGATIVE

## Regarding Cameras to View Inside or Outside of JWST
- imply the absence of the camera to view the JWST is a bad thing
  - NEGATIVE

## Sending People on JWST
- imply a human should be sent inside the telescope (away from Earth), which is derogatory in nature towards the person
  - NEGATIVE

## Doomsday Scenarios involving (Damage to) JWST
- imply damage to the JWST
  - NEGATIVE
- both compliment the mission but also imply damage to the JWST
  - NEUTRAL

## UFOs or Aliens
- discovery of or interaction with aliens
  - POSITIVE
- claims can't find aliens with JWST but may make useful discoveries
  - NEGATIVE

## Civilian Contractors
- complimentary of their participatoin in JWST mission
  - POSITIVE
- critical (only references military spending)
  - NEGATIVE
- critical and complimentary about their projects
  - NEUTRAL

## Notes
1. This guide is in-progress and so currently does not capture guidelines for labeling sentiment for every type of topic in the data used for fine-tuning.
2. This guide has been applied to label the first 300 tweets from the initial test split (batch 1). Future work should focus on expanding this fully capture all tweets in the testing split as well as the training and validation splits.
