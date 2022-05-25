import glob
import io
import json
import os
import random

#
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageSequence

from .util.Util import *
from .config.Config import Config


class NFT(Config):

    """A class used to represent a Configuration object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG
    """

    """
    Methods
    -------
    """

    def __init__(
        self, encrypted_config=True, config_file_path="auth.json", key_file_path=None
    ):
        """Class init

        Parameters
        ----------
        encrypted_config : bool
            use an encrypted configuration file
        config_file_path : str
            path to the configuration file
        key_file_path : str
            path to encryption key file
        """
        super().__init__(encrypted_config, config_file_path, key_file_path)

    def create_nft_image(self, all_images, config):
        #
        new_image = {}
        for layer in config["layers"]:
            new_image[layer["name"]] = random.choices(
                layer["values"], layer["weights"]
            )[0]
        #
        for incomp in config["incompatibilities"]:
            for attr in new_image:
                if (
                    new_image[incomp["layer"]] == incomp["value"]
                    and new_image[attr] in incomp["incompatible_with"]
                ):
                    return self.create_new_image(all_images, config)
        #
        if new_image in all_images:
            return self.create_new_image(all_images, config)
        else:
            return new_image

    def generate_unique_images(self, amount, config, nft_art_output_directory_path):
        #
        print("Generating {} unique NFTs...".format(amount))
        pad_amount = len(str(amount))
        trait_files = {}
        #
        for trait in config["layers"]:
            trait_files[trait["name"]] = {}
            for x, key in enumerate(trait["values"]):
                trait_files[trait["name"]][key] = trait["filename"][x]
        #
        all_images = []
        for i in range(amount):
            new_trait_image = self.create_new_image(all_images, config)
            all_images.append(new_trait_image)
        #
        i = 1
        for item in all_images:
            item["tokenId"] = i
            i += 1
        #
        for i, token in enumerate(all_images):
            #
            attributes = []
            for key in token:
                if key != "tokenId":
                    attributes.append({"trait_type": key, "value": token[key]})
            #
            token_metadata = {
                "image": config["baseURI"]
                + "/images/"
                + str(token["tokenId"])
                + ".png",
                "tokenId": token["tokenId"],
                "name": config["name"] + str(token["tokenId"]).zfill(pad_amount),
                "description": config["description"],
                "attributes": attributes,
            }
            #
            with open("./metadata/" + str(token["tokenId"]) + ".json", "w") as outfile:
                json.dump(token_metadata, outfile, indent=4)
        #
        with open("./metadata/all-objects.json", "w") as outfile:
            json.dump(all_images, outfile, indent=4)
        #
        for item in all_images:
            #
            layers = []
            for index, attr in enumerate(item):
                #
                if attr != "tokenId":
                    layers.append([])
                    layers[index] = Image.open(
                        f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png'
                    ).convert("RGBA")
            #
            if len(layers) == 1:
                rgb_im = layers[0].convert("RGBA")
                file_name = str(item["tokenId"]) + ".png"
                rgb_im.save(nft_art_output_directory_path + file_name)
            elif len(layers) == 2:
                main_composite = Image.alpha_composite(layers[0], layers[1])
                rgb_im = main_composite.convert("RGBA")
                file_name = str(item["tokenId"]) + ".png"
                rgb_im.save(nft_art_output_directory_path + file_name)
            elif len(layers) >= 3:
                main_composite = Image.alpha_composite(layers[0], layers[1])
                layers.pop(0)
                layers.pop(0)
            #
            for index, remaining in enumerate(layers):
                main_composite = Image.alpha_composite(main_composite, remaining)
                rgb_im = main_composite.convert("RGBA")
                file_name = str(item["tokenId"]) + ".png"
                rgb_im.save(nft_art_output_directory_path + file_name)

        # v1.0.2 addition
        print(
            "\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit."
        )
        # cid = input("IPFS Image CID (): ")
        cid = self.upload_directory_to_ipfs(nft_art_output_directory_path)
        #
        if len(cid) > 0:
            #
            if not cid.startswith("ipfs://"):
                cid = "ipfs://{}".format(cid)
            if cid.endswith("/"):
                cid = cid[:-1]
            #
            for i, item in enumerate(all_images):
                #
                with open(
                    "./metadata/" + str(item["tokenId"]) + ".json", "r"
                ) as infile:
                    original_json = json.loads(infile.read())
                    original_json["image"] = original_json["image"].replace(
                        config["baseURI"] + "/", cid + "/"
                    )
                #
                with open(
                    "./metadata/" + str(item["tokenId"]) + ".json", "w"
                ) as outfile:
                    json.dump(original_json, outfile, indent=4)
