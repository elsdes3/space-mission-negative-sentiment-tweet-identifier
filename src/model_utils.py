#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Transformer model training and inference utilities."""

import numpy as np
import pandas as pd
from transformers import EvalPrediction, pipeline

from metrics_utils import get_metrics

# pylint: disable=dangerous-default-value
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


def tokenize_function(examples, mytokenizer):
    """Tokenize text."""
    return mytokenizer(examples["text"], truncation=True, max_length=512)


def make_predictions(tokenized_dataset, trainer):
    """Make predictions using the HuggingFace Trainer API."""
    predictions_test = trainer.predict(tokenized_dataset)
    preds_proba, labels = [
        predictions_test.predictions,
        predictions_test.label_ids,
    ]
    assert len(preds_proba) == len(labels)
    preds_test = np.argmax(preds_proba, axis=-1)
    return [preds_test, preds_proba]


def compute_metrics(eval_pred: EvalPrediction):
    """Calculate metrics as part of Trainer class."""
    labels = eval_pred.label_ids
    predictions = eval_pred.predictions.argmax(-1)
    metrics, _ = get_metrics(labels, predictions, "weighted", 0, False)
    return metrics


def extract_sentiment_using_pretrained_model(
    pretrained_model: pipeline, data: pd.Series
) -> pd.DataFrame:
    """."""
    y_list = np.vectorize(pretrained_model)(data).tolist()
    df_pred = (
        pd.DataFrame.from_records([pred[0] for pred in y_list])
        .assign(index=data.index)
        .set_index("index")
    )
    return df_pred
