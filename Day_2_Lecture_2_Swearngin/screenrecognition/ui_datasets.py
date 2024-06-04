import torch
import os
from PIL import Image
import json

from torchvision import transforms
import pytorch_lightning as pl
import torch.nn.functional as F

import glob
import random
import zipfile
import xmltodict


class VINSUIDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        root="downloads/vins/All Dataset",
        class_dict_path="metadata/screenrecognition/class_map_vins_manual.json",
        id_list_path="metadata/screenrecognition/train_ids_vins.json",
    ):

        with open(id_list_path, "r") as f:
            self.id_list = json.load(f)

        self.root = root
        self.img_transforms = transforms.ToTensor()

        with open(class_dict_path, "r") as f:
            class_dict = json.load(f)

        self.idx2Label = class_dict["idx2Label"]
        self.label2Idx = class_dict["label2Idx"]

    def __len__(self):
        return len(self.id_list)

    def __getitem__(self, idx):
        def return_next():  # for debugging
            return VINSUIDataset.__getitem__(self, idx + 1)

        try:
            img_path = os.path.join(self.root, self.id_list[idx])

            pil_img = Image.open(img_path).convert("RGB")
            img = self.img_transforms(pil_img)

            # get bounding box coordinates for each mask
            with open(
                img_path.replace(".jpg", ".xml").replace("JPEGImages", "Annotations"),
                "r",
            ) as root_file:
                test_dat = root_file.read()

            dd = xmltodict.parse(test_dat)

            boxes = []
            labels = []

            for obj in dd["annotation"]["object"]:
                bbo = obj["bndbox"]
                bb = [
                    float(bbo["xmin"]),
                    float(bbo["ymin"]),
                    float(bbo["xmax"]),
                    float(bbo["ymax"]),
                ]
                boxes.append(bb)
                labels.append(self.label2Idx[obj["name"]])

            # convert everything into a torch.Tensor
            boxes = torch.as_tensor(boxes, dtype=torch.float32)
            labels = torch.tensor(labels, dtype=torch.long)
            image_id = torch.tensor([idx])
            area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])

            # Provide the boxes, labels and other metadata for model training.
            target = {}
            target["boxes"] = boxes
            target["labels"] = labels
            target["image_id"] = image_id
            target["img"] = pil_img
            target["area"] = area

            return img, target
        except Exception as e:
            print("failed", idx, self.id_list[idx], str(e))
            return return_next()


# https://lightning.ai/docs/pytorch/stable/data/datamodule.html
class VINSUIDataModule(pl.LightningDataModule):
    def __init__(self, batch_size=8, num_workers=4):
        super(VINSUIDataModule, self).__init__()
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.train_dataset = VINSUIDataset(
            id_list_path="metadata/screenrecognition/train_ids_vins.json"
        )
        self.val_dataset = VINSUIDataset(
            id_list_path="metadata/screenrecognition/val_ids_vins.json"
        )
        self.test_dataset = VINSUIDataset(
            id_list_path="metadata/screenrecognition/test_ids_vins.json"
        )

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
            shuffle=True,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.test_dataset,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            batch_size=self.batch_size,
        )


# https://github.com/pytorch/vision/blob/5985504cc32011fbd4312600b4492d8ae0dd13b4/references/detection/utils.py#L203
def collate_fn(batch):
    return tuple(zip(*batch))
