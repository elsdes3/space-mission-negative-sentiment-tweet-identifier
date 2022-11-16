#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Transformer model training and inference utilities."""


from collections import Counter
from typing import Dict, List, Union

import pandas as pd
import sklearn.metrics as skm

# pylint: disable=dangerous-default-value
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


def get_metrics(
    y_true,
    y_pred,
    average="binary",
    zero_division="warn",
    use_sample_weights=False,
) -> List[Union[Dict, List]]:
    """Use transformers library to calculate sklearn metrics."""
    if use_sample_weights:
        y_true_list = list(y_true)
        mapper = dict(Counter(y_true_list))
        sample_weights = [mapper[q] for q in y_true_list]
    else:
        sample_weights = None
    metrics_dict = dict(
        accuracy=skm.accuracy_score(y_true, y_pred),
        balanced_accuracy=skm.balanced_accuracy_score(y_true, y_pred),
        precision=skm.precision_score(
            y_true,
            y_pred,
            average=average,
            sample_weight=sample_weights,
            zero_division=zero_division,
        ),
        recall=skm.recall_score(
            y_true,
            y_pred,
            average=average,
            sample_weight=sample_weights,
            zero_division=zero_division,
        ),
        f1=skm.f1_score(
            y_true,
            y_pred,
            average=average,
            sample_weight=sample_weights,
            zero_division=zero_division,
        ),
        f05=skm.fbeta_score(
            y_true,
            y_pred,
            beta=0.5,
            average=average,
            sample_weight=sample_weights,
            zero_division=zero_division,
        ),
        f2=skm.fbeta_score(
            y_true,
            y_pred,
            beta=2.0,
            average=average,
            sample_weight=sample_weights,
            zero_division=zero_division,
        ),
    )
    return [metrics_dict, sample_weights]


def calculate_metrics(
    y_true,
    y_pred,
    classes=[0, 1, 2],
    labels=["Negative", "Neutral", "Positive"],
    average="binary",
    zero_division="warn",
    use_sample_weights=False,
):
    """Score predicted values against true values."""
    metrics_dict, sample_weights = get_metrics(
        y_true, y_pred, average, zero_division, use_sample_weights
    )
    df_cm = (
        pd.DataFrame(
            skm.confusion_matrix(y_true, y_pred, labels=classes),
            columns=labels,
            index=labels,
        )
        .reset_index()
        .rename(columns={"index": "Actual"})
    )
    df_cr = (
        pd.DataFrame(
            skm.classification_report(
                y_true,
                y_pred,
                output_dict=True,
                sample_weight=sample_weights,
                zero_division=zero_division,
                labels=classes,
                target_names=labels,
            )
        )
        .T.loc[labels]
        .astype({"support": pd.Int32Dtype()})
    )
    return [metrics_dict, df_cm, df_cr]


def get_metrics_summary(
    y_true,
    y_pred,
    label_mapper,
    id2label,
    batch_num,
    infer_bm_file_name,
):
    """Get evaluation metrics and evaluation reports."""
    metrics_dict, df_cm, df_cr = calculate_metrics(
        y_true.astype("int64").to_numpy(),
        y_pred.astype("int64").to_numpy(),
        list(label_mapper.values()),
        list(label_mapper.keys()),
        average="weighted",
        zero_division=0,
        use_sample_weights=False,
    )
    df_metrics = pd.DataFrame.from_dict(metrics_dict, orient="index").T.assign(
        batch_num=batch_num
    )
    df_cr = df_cr.merge(
        y_true.value_counts(normalize=True)
        .rename("freq")
        .reset_index()
        .assign(index=lambda df: df["index"].map(id2label))
        .set_index("index"),
        left_index=True,
        right_index=True,
        how="left",
    ).assign(batch_num=batch_num)
    df_cm = df_cm.assign(batch_num=batch_num)
    metrics_summary_dict = {
        "infer_bm_file_name": infer_bm_file_name,
        "batch_num": batch_num,
        "cm": df_cm,
        "cr": df_cr,
        "metrics": df_metrics,
        "true": y_true,
        "pred": y_pred,
    }
    return metrics_summary_dict
