import torch
import torch.nn as nn
import timm.models.vision_transformer
import torch.nn.functional as F
from functools import partial
from timm.models.vision_transformer import VisionTransformer
from blocks.photoz import InceptionBlock, Input_Mix_Model


class ViT_Astro(nn.Module):
    def __init__(self, embed_dim, vit_layers):
        super(ViT_Astro, self).__init__()
        self.embed_dim = embed_dim

        self.fc_norm = partial(nn.LayerNorm, eps=1e-6)(self.embed_dim)
        self.head = nn.Linear(self.embed_dim, self.embed_dim)

        self.inception_model = Input_Mix_Model(
            in_channel=5,
            out_channel=32,
            embed_dim=self.embed_dim,
            Inception_only=False,
            magnitude=True,
            uk_paper=False,
        )

        self.cls_token = self.freeze(vit_layers["cls_token"], "cls_token")
        self.pos_embed = self.freeze(vit_layers["pos_embed"], "pose_embed")
        self.blocks = self.freeze(vit_layers["blocks"], "block")
        self.patch_embed = self.freeze(vit_layers["patch_embed"], "patch_embed")

        self.vit_block = nn.Sequential(
            nn.Linear(self.embed_dim, 1096), nn.ReLU(), nn.Linear(1096, 1096)
        )

        self.concat_block = nn.Sequential(
            nn.Linear(3216, 1024), nn.ReLU(), nn.Linear(1024, 1)
        )

    def freeze(self, module, module_name):
        frozen_module = None
        if module_name == "block":
            for blk in module:
                for param in blk.parameters():
                    param.requires_grad = False
            frozen_module = module
        elif module_name == "patch_embed":
            for param in module.parameters():
                param.requres_grad = False

            module.proj.weight.requires_grad = False
            module.proj.bias.requires_grad = False

            frozen_module = module
        else:
            module.requires_grad = False
            frozen_module = module

        return frozen_module

    def forward(self, x):
        B = x[0].shape[0]
        vit_out = self.patch_embed(x[0])
        cls_tokens = self.cls_token.expand(
            B, -1, -1
        )  # stole cls_tokens impl from Phil Wang, thanks
        vit_out = torch.cat((cls_tokens, vit_out), dim=1)

        vit_out = vit_out + self.pos_embed

        for blk in self.blocks:
            vit_out = blk(vit_out)

        vit_out = vit_out[:, 1:, :].mean(dim=1)  # global pool without cls token
        vit_out = self.fc_norm(vit_out)

        vit_out = self.head(vit_out)
        vit_out = self.vit_block(vit_out)

        mag_incept = self.inception_model(x)

        concat_mag_vit = torch.cat((vit_out, mag_incept), axis=1)
        outpt = self.concat_block(concat_mag_vit)
        return outpt
