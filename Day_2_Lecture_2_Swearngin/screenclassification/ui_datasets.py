import torch
import os
from PIL import Image
import json
from torchvision import transforms
import pytorch_lightning as pl
import pandas as pd
from collections import Counter
from tqdm import tqdm
from collections import defaultdict
import numpy as np
from random import choices
import random


def makeOneHotVec(idx, num_classes):
    vec = [1 if i == idx else 0 for i in range(num_classes)]
    return vec


def collate_fn(batch):
    res = defaultdict(list)

    for d in batch:
        for k, v in d.items():
            res[k].append(v)

    res["label"] = torch.stack(res["label"])
    return res


def collate_fn_enrico(batch):
    res = defaultdict(list)

    for d in batch:
        for k, v in d.items():
            res[k].append(v)

    res["label"] = torch.tensor(res["label"], dtype=torch.long)
    return res


class EnricoImageDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        id_list_path,
        csv="metadata/screenclassification/design_topics.csv",
        class_map_file="metadata/screenclassification/class_map_enrico.json",
        img_folder=(
            os.environ["SM_CHANNEL_TRAINING"]
            if "SM_CHANNEL_TRAINING" in os.environ
            else "downloads/enrico/screenshots"
        ),
        img_size=128,
        ra_num_ops=-1,
        ra_magnitude=-1,
        one_hot_labels=False,
    ):
        super(EnricoImageDataset, self).__init__()
        self.csv = pd.read_csv(csv)
        self.img_folder = img_folder
        self.one_hot_labels = one_hot_labels
        img_transforms = [
            transforms.Resize(img_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]

        if ra_num_ops > 0 and ra_magnitude > 0:
            img_transforms = [
                transforms.RandAugment(ra_num_ops, ra_magnitude)
            ] + img_transforms

        self.img_transforms = transforms.Compose(img_transforms)

        self.image_names = list(self.csv["screen_id"])
        self.labels = list(self.csv["topic"])

        self.class_counter = Counter(self.labels)

        with open(id_list_path, "r") as f:
            split_ids = set(json.load(f))

        keep_inds = [
            i
            for i in range(len(self.image_names))
            if str(self.image_names[i]) in split_ids
        ]

        self.image_names = [self.image_names[i] for i in keep_inds]
        self.labels = [self.labels[i] for i in keep_inds]

        with open(class_map_file, "r") as f:
            map_dict = json.load(f)

        self.label2Idx = map_dict["label2Idx"]
        self.idx2Label = map_dict["idx2Label"]

    # The __len__ function returns the number of samples in our dataset.
    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, index):
        img_path = os.path.join(self.img_folder, str(self.image_names[index]) + ".jpg")
        image = Image.open(img_path).convert("RGB")

        image = self.img_transforms(image)
        targets = self.label2Idx[self.labels[index]]
        if self.one_hot_labels:
            targets = torch.tensor(
                makeOneHotVec(targets, len(self.idx2Label.keys())), dtype=torch.long
            )

        return {"image": image, "label": targets}


class EnricoDataModule(pl.LightningDataModule):
    def __init__(
        self, batch_size=16, num_workers=4, img_size=128, ra_num_ops=-1, ra_magnitude=-1
    ):
        super(EnricoDataModule, self).__init__()
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.train_dataset = EnricoImageDataset(
            id_list_path="metadata/screenclassification/filtered_train_ids.json",
            ra_num_ops=ra_num_ops,
            ra_magnitude=ra_magnitude,
            img_size=img_size,
        )
        self.val_dataset = EnricoImageDataset(
            id_list_path="metadata/screenclassification/filtered_val_ids.json",
            img_size=img_size,
        )
        self.test_dataset = EnricoImageDataset(
            id_list_path="metadata/screenclassification/filtered_test_ids.json",
            img_size=img_size,
        )

    def train_dataloader(self):
        samples_weight = torch.tensor(
            [1 / self.train_dataset.class_counter[t] for t in self.train_dataset.labels]
        )
        sampler = torch.utils.data.sampler.WeightedRandomSampler(
            samples_weight, len(samples_weight)
        )
        return torch.utils.data.DataLoader(
            self.train_dataset,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
            sampler=sampler,
            collate_fn=collate_fn_enrico,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
            collate_fn=collate_fn_enrico,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.test_dataset,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
            collate_fn=collate_fn_enrico,
        )
