# Processed Data Files on S3

## List of Files
1. Files produced by `3_combine_data.ipynb`
   - `combined_data.zip`
     - combines all streamed tweets into hourly `.parquet.gzip` files per day
   - `sample_to_label_tweet_subject.xlsx`
     - used to create a list of candidate terms, atleast one of which must be present in a tweet in order for the tweet to be used in model development
2. `processed_data.zip`
   - filter out tweets with unwanted terms in the text of the tweet
   - keep tweets with wanted terms in the text
   - produced by `4_filter_data.ipynb`
3. `processed_text.zip`
   - processing text (removing whitespaces, special characters, punctuation, etc.)
     - this was done with the view towards using a PySpark MLlib-based approach to classify sentiment
     - transformers models do not require some of this text processing
   - filter out short tweets (two words or less)
   - produced by `5_process_data.ipynb`
4. Folders produced by `6_split_data.ipynb`
   - `nlp_splits/`
     - splits for [fine-tuning a pre-trained transformers model using PyTorch](https://huggingface.co/docs/transformers/training#train-in-native-pytorch)
     - `test_nlp__inference_starts_20220110_000000.csv.zip`
     - `test_nlp__inference_starts_20220110_000000.xlsx`
     - `train_nlp__inference_starts_20220110_000000.csv.zip`
     - `train_nlp__inference_starts_20220110_000000.xlsx`
     - `val_nlp__inference_starts_20220110_000000.csv.zip`
     - `val_nlp__inference_starts_20220110_000000.xlsx`

     where all `.xlsx` files are manually labeled with tweet sentiment
     - 0 (negative)
     - 1 (neutral)
     - 2 (positive)
   - `splits/`
     - batches for evaluating business metrics (contains a single column, `batch_num`, with the batch number)
       - `bus_metrics_split__inference_starts_20220110_000000.parquet.gzip`
       - `bus_metrics_split__inference_starts_20220110_000000.xlsx`
         - manually labeled with tweet sentiment
5. `7_train.ipynb`
   - does not produce any output that is saved to S3
6. Files produced by `8_make_inference.ipynb`
   - `splits/`
     - predictions for batch 1 from business metrics split
       - `bus_metrics_split__with_preds_batch_1_20221024_014539__inference_starts_20220110_000000.parquet.gzip`
     - predictions for batch 2 from business metrics split
       - `bus_metrics_split__with_preds_batch_2_20221024_014548__inference_starts_20220110_000000.parquet.gzip`
     - these are the same as `splits/bus_metrics_split__inference_starts_20220110_000000.xlsx` but with a new column showing the predictions made using the fine-tuned model
     - one file is produced per batch in `splits/bus_metrics_split__inference_starts_20220110_000000.xlsx`

## Dataset Sizes
1. `3-combine-data.ipynb`
   - cell 11
   - 58,432
2. `4-filter-data.ipynb`
   - cell 11
   - combined data = 1,155,499
     - all tweets streamed between 2021-12-30 and 2022-01-09
   - filtered data = 58,432
3. `5-process-data.ipynb`
   - cell 22
   - (text) processed data = 58,432
4. `6-split-data.ipynb`
   - cell 30
   - may-need-support = 3649
   - nlp-full = 3066
     - nlp-train = 2346
     - nlp-val = 336
     - nlp-test = 384
   - may-need-support-in-nlp-full = 2342
   - business-metrics = 1200
