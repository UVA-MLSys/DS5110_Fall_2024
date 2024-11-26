import torch
from torch import nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_chanels, **kwargs):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_chanels, **kwargs)
        self.bn = nn.BatchNorm2d(out_chanels)

    def forward(self, x):
        return F.relu(self.bn(self.conv(x)))


class InceptionBlock(nn.Module):
    def __init__(
        self,
        in_channels,
        out_1x1,
        red_3x3,
        out_3x3,
        red_5x5,
        out_5x5,
        out_pool,
        is_custom=False,
    ):
        super(InceptionBlock, self).__init__()
        self.is_custom = is_custom
        self.branch1 = ConvBlock(in_channels, out_1x1, kernel_size=1)
        self.branch2 = nn.Sequential(
            ConvBlock(in_channels, red_3x3, kernel_size=1, padding=0),
            ConvBlock(red_3x3, out_3x3, kernel_size=3, padding=1),
        )
        self.branch3 = nn.Sequential(
            ConvBlock(in_channels, red_5x5, kernel_size=1),
            ConvBlock(red_5x5, out_5x5, kernel_size=5, padding=2),
        )
        self.branch4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, padding=1, stride=1),
            ConvBlock(in_channels, out_pool, kernel_size=1),
        )

    def forward(self, x):
        if self.is_custom:
            branches = (self.branch1, self.branch2, self.branch4)
        else:
            branches = (self.branch1, self.branch2, self.branch3, self.branch4)

        return torch.cat([branch(x) for branch in branches], 1)


class Input_Mix_Model(nn.Module):
    def __init__(
        self, in_channel, out_channel, embed_dim, Inception_only, magnitude, uk_paper
    ):
        super(Input_Mix_Model, self).__init__()

        self.Inception_only = Inception_only
        self.magnitude = magnitude
        self.uk_paper = uk_paper
        self.embed_dim = embed_dim
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.conv2d_init = nn.Conv2d(
            in_channel, out_channel, kernel_size=(1, 1), padding_mode="zeros"
        )
        self.avgpool = nn.AvgPool2d(kernel_size=2, stride=2)
        self.avgpool2 = nn.AvgPool2d(kernel_size=2, stride=2)

        if self.Inception_only:
            self.Inception_head_block = nn.Sequential(
                nn.ReLU(),
                nn.Linear(1096, 1),
            )

        elif self.magnitude:
            self.magnitude_block = nn.Sequential(
                nn.Linear(5, 1024),
                nn.ReLU(),
                nn.Linear(1024, 1024),
                nn.ReLU(),
                nn.Linear(1024, 1024),
                nn.ReLU(),
                nn.Linear(1024, 1024),
                nn.ReLU(),
                nn.Linear(1024, 1024),
                # nn.LayerNorm(1024),
            )

            if self.uk_paper:
                self.head_incept_mag = nn.Sequential(
                    nn.Linear(2120, 1024),
                    nn.ReLU(),
                    # nn.Linear(1024, 1024),
                    # nn.ReLU(),
                    # nn.Linear(1024, 1024),
                    # nn.ReLU(),
                    nn.Linear(1024, 1),
                )

        self.config = [
            {
                "in_channel": 32,
                "out_11": 16,
                "in_33": 16,
                "out_33": 16,
                "in_55": 16,
                "out_55": 16,
                "out_mxpl": 16,
            },
            {
                "in_channel": 64,
                "out_11": 16,
                "in_33": 16,
                "out_33": 16,
                "in_55": 16,
                "out_55": 16,
                "out_mxpl": 16,
            },
            {
                "in_channel": 64,
                "out_11": 8,
                "in_33": 8,
                "out_33": 8,
                "in_55": 8,
                "out_55": 8,
                "out_mxpl": 8,
            },
            {
                "in_channel": 32,
                "out_11": 8,
                "in_33": 8,
                "out_33": 8,
                "in_55": 8,
                "out_55": 8,
                "out_mxpl": 8,
            },
            {
                "in_channel": 32,
                "out_11": 4,
                "in_33": 4,
                "out_33": 4,
                "in_55": 4,
                "out_55": 4,
                "out_mxpl": 4,
            },
        ]

        self.vis_inception = nn.Sequential(*self.vis_bulit())

    def vis_bulit(self):
        layers = []
        layers.append(self.conv2d_init)
        layers.append(self.avgpool)
        for i in range(5):
            if i != 4:
                layers.append(
                    InceptionBlock(
                        in_channels=self.config[i]["in_channel"],
                        out_1x1=self.config[i]["out_11"],
                        red_3x3=self.config[i]["in_33"],
                        out_3x3=self.config[i]["out_33"],
                        red_5x5=self.config[i]["in_55"],
                        out_5x5=self.config[i]["out_55"],
                        out_pool=self.config[i]["out_mxpl"],
                        is_custom=False,
                    ).to(self.device)
                )

            if i % 2 != 0:
                layers.append(nn.AvgPool2d(kernel_size=2))

            if i == 4:
                layers.append(
                    InceptionBlock(
                        in_channels=self.config[i]["in_channel"],
                        out_1x1=self.config[i]["out_11"],
                        red_3x3=self.config[i]["in_33"],
                        out_3x3=self.config[i]["out_33"],
                        red_5x5=self.config[i]["in_55"],
                        out_5x5=self.config[i]["out_55"],
                        out_pool=self.config[i]["out_mxpl"],
                        is_custom=True,
                    ).to(self.device)
                )

        layers.append(nn.Flatten().to(self.device))
        layers.append(nn.Linear(self.embed_dim, 1096).to(self.device))
        layers.append(nn.ReLU().to(self.device))
        layers.append(nn.Linear(1096, 1096).to(self.device))
        return layers

    def forward(self, x):
        if (not self.uk_paper) and (not self.magnitude):
            y = self.vis_inception(x)
        else:
            # y = self.vis_inception(x)
            y = self.vis_inception(x[0])

        if self.Inception_only:
            y = self.Inception_head_block(y)

        elif self.magnitude:
            x_mag = self.magnitude_block(x[1].float())
            concat_mag_vit = torch.cat((y, x_mag), axis=1)
            if self.uk_paper:
                y = self.head_incept_mag(concat_mag_vit)
            else:
                y = concat_mag_vit
        return y
