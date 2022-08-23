



## Step 4: Analysis
### What analysis needs to be done?
A binary classification ML model will be trained on all available (labeled) tweets up to but not including 2022-01-10 00:00:00. The trained model will be used on-demand to predict whether a tweet needs support from a mission team member (negative or neutral sentiment) or not (positive sentiment).

### Does it involve description, detection, prediction, or behavior change?
Prediction.

### How will the analysis be validated?
A pilot study period of two and a half days starting from 2022-01-07 12:00:00 and ending on (but not including) 2022-01-10 00:00:00 has been defined. The trained ML model will be used to predict the label (needs support not does not need support) of 12 hours of tweets starting at 2022-01-07 12:00:00. This will be repeated for 12-hour blocks concluding at the end of the pilot study period.

Predictions will be scored against true labels for tweets posted during the pilot study period, obtained from one of
- hand labeling
- NLP (transformer) model

and the average scoring metric over all 12-hour periods for which predictions were made will be calculated.

A simple (naive) approach to making predictions will also be scored and its average will be calculated over all the 12-hour periods comprising the study period.

The average of both approaches will be compared to eachother to determine if the ML-based approach is outperforming the simple (naive) approach.

#### Choice of Evaluation Metric
False negatives (tweets that should have been responded to but were predicted to not need a response) and false positives (tweets that did not need review by a team member but were predicted as requiring a review) are the most important types of errors. So the [candidate metrics to be used to assess ML model performance](https://machinelearningmastery.com/tour-of-evaluation-metrics-for-imbalanced-classification/) are
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
4. FP: actual = does not need support, predicted = needs support
   - sentiment is not negative/neutral (does not need support)
   - prediction is negative/neutral (needs support)
   - the loss/harm incurred is that team members unnecessarily spend time reading through tweets that are potentially not harmful to public image of the mission

Since FN (false negatives) are more costly than FP (false positives), the scoring metric chosen to evaluate predictions made using the ML model is [F2-score](https://machinelearningmastery.com/fbeta-measure-for-machine-learning/).
