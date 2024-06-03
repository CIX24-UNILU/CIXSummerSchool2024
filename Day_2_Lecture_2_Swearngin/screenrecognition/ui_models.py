import numpy as np

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd

from mean_average_precision import MetricBuilder
import pytorch_lightning as pl
import torch
import torchvision
import random


class UIElementDetector(pl.LightningModule):
    def __init__(
        self,
        num_classes=25,
        min_size=320,
        max_size=640,
        lr=0.0001,
        val_weights=None,
        test_weights=None,
        arch="fcos",
    ):
        super(UIElementDetector, self).__init__()
        self.save_hyperparameters()
        if arch == "fcos":
            model = torchvision.models.detection.fcos_resnet50_fpn(
                min_size=min_size,
                max_size=max_size,
                num_classes=num_classes,
                trainable_backbone_layers=5,
            )

        # Single shot multibox detector used by the notebook.
        elif arch == "ssd":
            model = torchvision.models.detection.ssd300_vgg16(
                num_classes=num_classes,
                trainable_backbone_layers=5,  # adjust number of backbone layers here.
            )

        elif arch == "fasterrcnn":
            model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
                num_classes=num_classes,
                trainable_backbone_layers=5,
            )
        self.model = model

    def training_step(self, batch, batch_idx):
        # Compute the loss for a training step.
        images, targets = batch
        images = list(image for image in images)
        targets = [{k: v for k, v in t.items()} for t in targets]

        loss_dict = self.model(images, targets)
        loss = sum(loss for loss in loss_dict.values())
        self.log_dict({"loss": float(loss)})
        return loss

    def validation_step(self, batch, batch_idx):
        images, targets = batch
        images = list(image for image in images)
        targets = [{k: v for k, v in t.items()} for t in targets]
        outputs = self.model(images)
        preds = []
        gts = []
        for batch_i in range(len(outputs)):
            pred_box = outputs[batch_i]["boxes"]
            pred_score = outputs[batch_i]["scores"]
            pred_label = outputs[batch_i]["labels"]

            preds.append(
                torch.cat(
                    (pred_box, pred_label.unsqueeze(-1), pred_score.unsqueeze(-1)),
                    dim=-1,
                )
            )

            gtsi = []
            target_len = targets[batch_i]["boxes"].shape[0]
            for i in range(target_len):
                target_box = targets[batch_i]["boxes"][i]
                target_label = targets[batch_i]["labels"][i]

                if len(target_label.shape) == 1:
                    for ci in range(target_label.shape[0]):
                        if target_label[ci] > 0:
                            gtsi.append(
                                torch.cat(
                                    (
                                        target_box,
                                        torch.tensor(
                                            [ci, 0, 0], device=target_box.device
                                        ),
                                    ),
                                    dim=-1,
                                )
                            )
                else:
                    gtsi.append(
                        torch.cat(
                            (
                                target_box,
                                torch.tensor(
                                    [target_label, 0, 0], device=target_box.device
                                ),
                            ),
                            dim=-1,
                        )
                    )
            gts.append(
                torch.stack(gtsi)
                if len(gtsi) > 0
                else torch.zeros(0, 7, device=self.device)
            )

        return preds, gts

    def validation_epoch_end(self, outputs):
        metric_fn = MetricBuilder.build_evaluation_metric(
            "map_2d", async_mode=True, num_classes=self.hparams.num_classes
        )
        for batch_output in outputs:
            for i in range(len(batch_output[0])):
                metric_fn.add(
                    batch_output[0][i].detach().cpu().float().numpy(),
                    batch_output[1][i].detach().cpu().float().numpy(),
                )

        metrics = metric_fn.value(iou_thresholds=0.5)

        if self.hparams.val_weights is None:
            mapscore = metrics["mAP"]
        else:
            weights = np.array(self.hparams.val_weights)
            aps = np.array([metrics[0.5][c]["ap"] for c in metrics[0.5]])
            mapscore = (aps * weights).sum()

        self.log_dict({"mAP": mapscore})
        print(f"mAP: {mapscore}")

    def test_step(self, batch, batch_idx):
        images, targets = batch
        images = list(image for image in images)
        targets = [{k: v for k, v in t.items()} for t in targets]
        outputs = self.model(images)
        preds = []
        gts = []
        for batch_i in range(len(outputs)):
            batch_len = outputs[batch_i]["boxes"].shape[0]

            pred_box = outputs[batch_i]["boxes"]
            pred_score = outputs[batch_i]["scores"]
            pred_label = outputs[batch_i]["labels"]

            preds.append(
                torch.cat(
                    (pred_box, pred_label.unsqueeze(-1), pred_score.unsqueeze(-1)),
                    dim=-1,
                )
            )

            gtsi = []
            target_len = targets[batch_i]["boxes"].shape[0]
            for i in range(target_len):
                target_box = targets[batch_i]["boxes"][i]
                target_label = targets[batch_i]["labels"][i]

                if len(target_label.shape) == 1:
                    for ci in range(target_label.shape[0]):
                        if target_label[ci] > 0:
                            gtsi.append(
                                torch.cat(
                                    (
                                        target_box,
                                        torch.tensor(
                                            [ci, 0, 0], device=target_box.device
                                        ),
                                    ),
                                    dim=-1,
                                )
                            )
                else:
                    gtsi.append(
                        torch.cat(
                            (
                                target_box,
                                torch.tensor(
                                    [target_label, 0, 0], device=target_box.device
                                ),
                            ),
                            dim=-1,
                        )
                    )
            gts.append(
                torch.stack(gtsi)
                if len(gtsi) > 0
                else torch.zeros(0, 7, device=self.device)
            )

        return preds, gts

    def test_epoch_end(self, outputs):
        metric_fn = MetricBuilder.build_evaluation_metric(
            "map_2d", async_mode=True, num_classes=self.hparams.num_classes
        )
        for batch_output in outputs:
            for i in range(len(batch_output[0])):
                metric_fn.add(
                    batch_output[0][i].detach().cpu().numpy(),
                    batch_output[1][i].detach().cpu().numpy(),
                )

        metrics = metric_fn.value(iou_thresholds=0.5)

        if self.hparams.test_weights is None:
            mapscore = metrics["mAP"]
        else:
            weights = np.array(self.hparams.test_weights)

            aps = np.array([metrics[0.5][c]["ap"] for c in metrics[0.5]])

            mapscore = (aps * weights).sum()

        self.log_dict({"mAP": mapscore})
        print(f"mAP: {mapscore}")

    # Configure the optimizer
    def configure_optimizers(self):
        # Use the SGD optimizer (stochastic gradient descent)
        return torch.optim.SGD(
            filter(lambda p: p.requires_grad, self.parameters()), lr=self.hparams.lr
        )
