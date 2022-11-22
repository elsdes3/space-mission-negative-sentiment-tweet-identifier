# Project Scope

## Objective
The [James Web Space Telescope (JWST)](https://www.nasa.gov/mission_pages/webb/main/index.html) is the newest space [telescope imaging objects in the solar system beyond Mars](https://spaceplace.nasa.gov/james-webb-space-telescope/en/). The telescope was launched in the early winter of 2021.

Leading up to the launch, events were announced on social media ([1](https://www.nasa.gov/feature/join-the-webb-space-telescope-global-nasa-social), [2](https://twitter.com/i/notes/1546338454308544512?lang=en)) to engage with the public about the JWST mission. As with other space missions (eg. [Curiosity](https://twitter.com/marscuriosity), [Insight](https://twitter.com/NASAInSight?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)), a dedicated JWST Twitter account was also [set up](https://twitter.com/nasawebb). This allows mission support and communications team members to tweet interesting events, mission updates, share findings and respond to user questions/comments (eg. [1](https://twitter.com/ericwkoch/status/1587481864117157888), [2](https://twitter.com/NASAWebb/status/1590375061944270850), [3](https://twitter.com/astraughnomer/status/1587182060011225088), [4](https://twitter.com/NASAWebb/status/1584963255000350720), [5](https://twitter.com/NASAWebb/status/1590375038401781762)). Communicating with the mission team on Twitter is a great way for the public to stay up-to-date on the missio and get valuable information about the scientific research being conducted using the payload.

To ensure that all tweets with a question are responded to, team members would have to frequently monitor new tweets posted to Twitter about the mission and reply when appropriate (i.e. when a question or comment posted requires a response). Particular attention should be paid to tweets with incorrect or misleading information relating to the mission (i.e. those with a negative sentiment), including those posed as a question. Depending on the content of these tweets, a response from the mission support team may or may not be warranted.

Some of the [mission support/communications team members](https://webb.nasa.gov/content/meetTheTeam/index.html) are themselves involved in conducting research using data collected by the telescope. With a large possible audience worldwide, keeping up-to-date with user questions on Twitter can be challenging for the mission support team. A naive alternative to reading every tweet and responding to those with a negative sentiment, is randomly guessing the sentiment of a tweet (positive or negative) and then only proceeding to address those which were guessed to have a negative sentiment. Ofcourse, this can be very innaccurate.

So, the **goal of this project is to explore the feasibility of using machine learning to identify tweets related to the JWST mission with a negative sentiment**. Tracking brand sentiment allows mission support team members to efficiently detect misleading or inaccurate information posted to the Twitter platform. Team members can review such tweets manually and respond if needed. A ML-based approach would reduce time wasted and time missed (that should have been spent) by the support team manually reading tweets in order determine if the sentiment is negative and subsequently if a reply is needed.

## Step 0: Problem Understanding
### What is the problem?
Public perception of a mission could be harshly influenced by invalid or mis-information on social media. The brand of the mission and organization (NASA) and the mission's core management and operations teams could be negatively impacted by
- unfairly critical or inaccurate tweets
- unanswered questions

posted to the Twitter platform.

The benefit of using a social media such as Twitter to engage the public is that
- updates about deployment and launch operations
- understanding about the design of the instruments comprising the payload, and how they will be used
- objectives (eg. science experiments to be conducted)

can be provided in real-time by the mission support team that monitors the [@NASA](https://twitter.com/NASA) account on Twitter.

However, by using social media, members of the public can also pose questions and comments to the support team in response to updates, announcements, etc. posted by @NASA. Some of these posts may be intentionally inaccurate and lead to a negative sentiment of @NASA on the platform.

Mission support team members monitoring the @NASA account on Twitter are well-versed in the details of the mission and have clarity around its scientific goals. They are the Subject Matter Experts (SMEs) and so are best equipped to respond to Twitter posts in order to clarify or correct discrepencies related to the topic being discussed and avoid the spread of mis-information. With access to negative-sentiment tweets on Twitter, the mission team can make these clarifications faster and more efficiently than needing to read every tweet including positive-sentiment tweets that do not need a response. Indeed brand monitoring and customer support are two of the business use-cases of sentiment analysis ([1](https://monkeylearn.com/blog/sentiment-analysis-examples/#:~:text=Expressions%20can%20be%20classified%20as%20positive%2C%20negative%2C%20or,which%20can%20be%20used%20across%20industries%20and%20teams.)).

Manually capturing as many negative-sentiment tweets as possible for manual review is not feasible as it is time-consuming and involves reading every mission-related tweet or randomly guessing at the sentiment of tweets. This can result in support team members
- unnecessarily reading tweets with a positive sentiment (leads to time wasted)
- missing tweets with a negative sentiment that should have been read (leads to time missed)

A robust approach to predicting the sentiment of tweets can efficently flag only those tweets that have a negative sentiment and streamline the support team's workflow to address incorrect or misleading information on Twitter.

### Who does it impact and how much?
The following could be negatively impacted negative sentiment about the mission on the Twitter platform
- (directly) brand of the mission and organization, NASA
- (directly) mission support/communications team
- (indirectly) core management and operations teams
  - unjustified negative attitudes or public perception of the mission can hinder the management team's efforts to secure funding to support on-going science operations in the [annual federal budget](https://en.wikipedia.org/wiki/Budget_of_NASA)
  - lack of funding prevents the ability to
    - plan and conduct sound science experiments to meet the mission's science objectives
    - plan staffing for [science operations teams](https://mars.nasa.gov/mro/mission/timeline/mtscienceops/)

The current project is targeted to addressing the negative impact on the mission support team.

It is difficult to estimate the cost of having negative sentiment about a mission being pervasive across the Twitter platform. However, negative [public sentiment about any aspect of a space mission](https://www.encyclopedia.com/reference/culture-magazines/public-opinion-about-space-exploration) incorrectly undermines the mission managers and space agencies (NASA, ESA, CSA) involved in laying out robust scientific objectives for the mission. This subsequently undermines the operations team's ability to conduct valuable science expreiments.

One method of quantifying the impact of the problem on the mission support team is to estimate how much time would be
- missed
- wasted

using the approach of randomly guessing at the sentiment of tweets. Over 600 tweets (with a manually labeled sentiment) that arrived over a 25-hour period between 2022-01-09 01:18 EST and 2022-01-10 01:29 EST, the random-guessing (naive) approach resulted in approximately
- 130 minutes (2 hours 10 minutes) of time wasted reading unnecessary tweets (tweets with a positive sentiment)
- 100 minutes (1 hour 40 minutes) of time missed (time that should have been spent reading negative-sentiment tweets)

where approximately 40% of the tweets (236 out of 600) needed support (neutral or negative sentiment) and where the following assumptions were made
- average reading speed of 130 words per minute (relevant for reading negative-sentiment tweets)
- average typing speed of 40 words per minute (relevant for responding to negative-sentiment tweets that warranted a response from a human member of the support team)
- 100% of negative-sentiment tweets warranted a response from a human member of the support team

### How is it being solved today and what are some of the gaps?
Tweets with a negative sentiment can be identified by a human reading them and interpreting the text. Tweets are filtered to only capture those that contain a well-defined set of keywords - these are candidates for receiving a response from the mission support team. From these filtered tweets, only those with a negative sentiment need to be manually read and possibly responded to.

The non-ML current approach to pick out negative-sentiment tweets involves randomly guessing at the sentiment of a tweet. The problem with this approach is that it picks up some positive sentiment tweets as well. Unfortunately, when the randomly guessed tweets are flagged to mission support team members for review, they have to read the positive sentiment tweets (that are actually not of a concern and do not need a response), which results in reading tweets that were naively predicted (guessed)
- to need support but that actually do not need support (False Positives)
  - this results in wasted time
- to not need support but that actually do need support (False Negatives)
  - this results in time missed

In order to capture as many negative sentiment tweets as possible, both time wasted and time missed should be minimized.

Therefore, a more accurate approach to identifying tweets that have a negative sentiment (need support) is required in order to respond to them
- faster
- more effectively

than is possible by randomly guessing at the sentiment of tweets.

Currently, there isn't a concerted effort to read and possibly respond to as many negative-sentiment tweets as possible. Responses are only being provided to some of tweets posted by users. So the problem of negative sentiment related to the mission on Twitter is not being fully solved today. As mentioned earlier, it is difficult to estimate the financial cost from brand negative sentiment, for a single space mission, on social media. For this reason, the above-mentioned
- cost
- current method of solving the problem (and its gaps)

refer to the random-guessing approach of flagging such negative-sentiment tweets which can easily be accomplished without much overhead and its inefficiencies.

We should note that the mission team may wish to spend time reading a sampling or (depending on the number of tweets) all of the positive sentiment tweets, but these are a lower priority than reading (and responding to) the negative sentiment tweets. Moving forward through this project, we will assume that positive sentiment tweets will not be read.

## Step 1: Goals
### What are the goals of the project?
The objective of this project is to develop a ML model that accurately predicts Twitter sentiment in tweets related to the JWST mission that can minimize
- time wasted
- time missed
- show an improvement in time wasted and time missed compared to a non-ML (naive) prediction approach that involves randomly guessing the sentiment of tweets

### How will we know if our project is successful?
The ML scoring (evaluation) metric used to assess accuracy is the F2-score ([1](https://qr.ae/pGqe6S), [2](https://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scorers.html#f05-f1-and-f2), [3](https://hasty.ai/docs/mp-wiki/metrics/f-beta-score)) and this choice is discussed in the **Choice of Evaluation Metric** sub-section below.

The project will be successful if the ML-based approach to predicting if support is needed performs as follows (when evaluated against unseen data)
- (ML scoring metric) F2-score of the ML-based approach is higher than
  - 80%
    - this was empirically found to be the baseline score on the test split during initial model training without optimizing ML model hyper-parameters
  - that of the random guessing (naive) approach
- (business metrics) time-wasted and time missed are lower with the ML-based approach than with the random guessing (naive) approach
- (business metric) percent reduction in time-wasted and time missed with the ML-based approach relative to the naive approach is greater than zero

## Step 2: Actions
### What actions or interventions will this work inform?
The ML-model's predictions will be used to flag potentially harmful tweets and submit them to mission support team members for review, and a possible response. By only focusing on these negative-sentiment tweets, this will help mitigate the presence of harmful misinformation about the mission on the platform while minimizing time wasted reading tweets with a positive sentiment.

The trained model will be deployed to an endpoint that will be called to make batch predictions of new tweets. From predictions of the tweets, those predicted to `need_support` will be submitted to mission support team members for review.

## Step 3: Data
### What data do you have access to internally?
1. Tweets were streamed using the Twitter API and Amazon Kinesis Firehose. Metadata was extracted from the tweets, including user location, number of user followers, etc.
2. A list of terms related to the mission was created and used to filter these tweets. The purpose of this filtering is to exclude unrelated tweets since mission support team members should not be spending time reading such tweets. Only the filtered tweets are candidates for receiving support from mission support team members.

### What data do you need?
None.

### What can you augment from external and/or public sources?
None.

## Step 4: Analysis
### What analysis needs to be done?
The sentiment needs to be extracted from the filtered tweets. A NLP (transformer) model will be trained on a training split of the filtered data, to perform binary classification of (tweet) text sentiment (sentiment analysis), and then evaluated on a held-out (test) split representing unseen data.

All available filtered data will be manually labeled to determine the sentiment of the tweets by reading the text of each tweet and assigning a label
- 0 for negative sentiment
- 1 for neutral sentiment
- 2 for positive sentiment

In production, tweets with negative or neutral sentiment must be read by mission support team members as these are the tweets that might require support (response) from a mission team member. So, the three manually labeled sentiment will be binarized as follows
- a label of 0 (or *does not need support*) will be assigned to all tweets with a positive sentiment
  - this is the majority class in a binary classification problem
- a label of 1 (or *needs support*) will be assigned to all tweets with a negative or neutral sentiment
  - this is the minority class

Training, validation and testing splits will be created. As mentioned above, all data (tweets) in each split will be manually labeled to indicate the sentiment of the tweet.

A pre-trained transformers model will be fine-tuned using the labeled data in the training and validation split. The fine-tuned model will be evaluated using out-of-sample (unseen) labeled data, which is the test split.

### Does it involve description, detection, prediction, or behavior change?
Prediction.

### How will the analysis be validated?
Based on exploratory data analysis of the filtered data in `6_split_data.ipynb`, the median number of tweets per
- time of day is approximately 700
- hour of day is approximately 500

so, a batch size for inference of incoming tweets (referred to as *new data*) will be set to 600. This means that the trained model will make predictions of sentiment for batches of 600 tweets. So, during training, the ML model will be validated using a
- validation split with 600 tweets, chronologically following the training split
- test split with 600 tweets, chronologically following the validation split

Predictions will be scored against true labels for tweets obtained from one of hand labeling, which will be assigned to all filtered data, as mentioned earlier.

A non-ML (naive) approach to predicting the tweet label will also be scored for comparison. This approach will involve randomly guessing the sentiment of the tweet which, as mentioned earlier, is the alternative to a ML-based approach to identifying tweets to be read the by the mission support team.

The three business metrics identified earlier in the *How will we know if our project is successful?* section
- F2-score
- time wasted
- time missed

will be compared between the ML and non-ML (naive) approaches to classifying sentiment. These three metrics should fare better with the ML-based approach (F2-score should be higher and both of *time missed* and *time wasted* should be lower) than with the non-ML approach. Additionally, the F2-score should be higher than 80%. Also, in order for the ML-based approach to deliver value over the naive approach, the percent reduction in
- time-wasted
- time missed

when using the ML-based approach, relative to the naive one, should be greater than zero.

#### Choice of Evaluation Metric
False negatives (tweets that should have been responded to but were predicted to not need a response) and false positives (tweets that did not need review by a team member but were predicted as requiring a review) are the most important types of errors. So the [candidate metrics to be used to assess ML model performance](https://machinelearningmastery.com/tour-of-evaluation-metrics-for-imbalanced-classification/) are
- F1-score (if false negatives and false positives are equally important)
- F2-score (if false negatives are more important)
- F0.5-score (if false positives are more important)

The four possible ML prediction scenarios are listed below for the prediction of the outcome of a hypothetical tweet's review status
1. TP: actual = needs support, predicted = needs support
   - sentiment is negative/neutral (needs support)
   - prediction is negative/neutral (needs support)
   - all such tweets will correctly be flagged for review by the mission team
   - there is no loss/harm incurred by this scenario
2. TN: actual = does not need support, predicted = does not need support
   - sentiment is positive (does not need support)
   - prediction is positive (does not need support)
   - all such tweets will correctly not be flagged for review by the mission team
   - there is no loss/harm incurred by this scenario
3. FN: actual = needs support, predicted = does not need support
   - sentiment is negative/neutral (needs support)
   - prediction is not negative/neutral (does not need support)
   - the loss/harm is that tweets that are potentially harmful to public image of the mission are not responded to by a mission team member, even though they should have been addressed
     - this scenario must be avoided
     - potentially harmful tweets that slip through without review by team members result in missed time spent on reviewing tweets and this must be minimized
4. FP: actual = does not need support, predicted = needs support
   - sentiment is not negative/neutral (does not need support)
   - prediction is negative/neutral (needs support)
   - the loss/harm incurred is that team members unnecessarily spend time reading through tweets that are potentially not harmful to public image of the mission
     - avoiding time wasted on reading non-harmful tweets would be preferred but, with a distribued mission team, it is not the top priority
     - it would be better to spend more time reading tweets, including potentially harmless and harmful ones, than not spend the time and allow harmful ones to slip through and lead to mis-information about the mission to enter the public domain

Since FN (false negatives) are more costly than FP (false positives), the scoring metric chosen to evaluate predictions made using the ML model is [F2-score](https://machinelearningmastery.com/fbeta-measure-for-machine-learning/).

## Ethical Considerations
### What are the privacy, transparency, discrimination/equity, and accountability issues around this project and how will you tackle them?
1. No personally identifying demographic data was intentionally collected during streaming of Tweets. So, demographic data will not be factor for predicting tweet sentiment.
2. User location data is missing in many tweets and so can't be used as a predictive feature during ML model development.

## Additional Considerations
### How will you deploy your analysis as a new system so that it can be updated and integrated into the organization’s operations?
If the project is a success, then an AWS Sagemaker Pipeline similar to [this official Sagemaker example](https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-pipelines/tabular/abalone_build_train_deploy/sagemaker-pipelines-preprocess-train-evaluate-batch-transform_outputs.ipynb) will be created to operationalize
- ML model training (development)
- deployment to an endpoint which can be called on-demand to make predictions

### How will you evaluate the new system in the field to make sure it accomplishes your goals?
In the field
- labels are not available and so the ML evaluation (F2-score) and business metrics above cannot be used to evaluate the system's performance
- manual labeling will not be performed on every batch of new data (600 tweets) that arrives

So, during inference, the trends seen in ML prediction *probability* by
- Twitter Client
- time of the day (morning, afternoon, etc.)
- binned length of tweet in number of words

should be within 15% of the trends seen during **initial** model training. The statistic used to check for trends will be the relative error (the ratio of standard deviation to mean) of the prediction probability. The smaller this error the more tightly confined are its constituent values.

For the initial model training, trends in this statistic (relative standard error) are shown in `8_inference.ipynb`.

### How will you monitor your system to make sure it continues to perform well over time?
In the training, validation and test splits, a column with the batch number will be appended to the data. During
- initial model training
  - the batch number will be 1 for all three splits
- inference
  - when a new batch of data (600 new tweets) arrives, data will be filtered and then appended to the file containing the test split data used during training, and the batch number of the newly arrived data will be increased by 1
  - inference will be performed on the most current batch in the test split file
  - no new data will be appended to the file containing the training and validation split files

Every five batches of new data (tweets) will be manually labeled.

After every five batches of new data, evaluation will be performed as follows
- the existing model will be used to make inference predictions and the mission support team will begin reading and responding to negative-sentiment tweets as necessary
- (as mentioned above) the newest batch of tweets (in the test split) will be manually labeled
  - since evaluation occurs every five batches of new data (tweets), manual labeling is performed as part of this evaluation process
- the existing ML model's predictions will be evaluated using newest labeled batch of data
- if the existing model's metrics are
  - within 15 percent of the
    - F2-score
    - time wasted
    - time missed
    - percent reduction in time wasted and time missed relative to the naive approach

    then the current model will continue to be used to serve the next five batches of inference data
  - worse than the scores from the currently deployed model by more than 15 percent, then
    - a new model will be trained using all available data (detailed below)
    - a new model will be registered in Sagemaker's model registry
    - the new (re-trained) model will be deployed to a new endpoint for making subsequent inference predictions

Re-training will be performed as follows
- in the test split
  - the second-last labeled batch will become the validation split
  - all labeled batches up to but not including the second last labeled batch will be appended to the training split
- the newest labeled batch of tweets will become the test split
- the ML model will be re-trained using the updated training, validation and test splits
- the re-trained ML model predictions will be evaluated using the test split
- once performance is acceptable, the newest model will be deployed to a new endpoint for making future inference predictions

The manual labeling of tweets should be consistent. This means the labeling process should be guided where possible. This will help scale the manual labeling process in production. For this purpose, a guide has been created to indicate how labels are assigned to tweets, where possible. The first 300 tweets from the test split comply with this guide. All other tweets in the training, validation and test split generally follow this guide. Future work should
- verify that these other tweets also comply with these guidelines
- add more categories to this guide as necessary

--------

<p><small>Project scope based on the <a target="_blank" href="http://www.datasciencepublicpolicy.org/our-work/tools-guides/data-science-project-scoping-guide/">CMU data science project scoping guide</a>.</small></p>
