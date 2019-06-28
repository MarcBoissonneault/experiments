from __future__ import annotations


def _load_images(image_file_path: str, load_options: LoadImageOptions) -> Iterator[pil.Image]:
    frame_count = _get_number_of_frames(image_file_path)
    for frame_index in range(frame_count):
        name = f"{image_file_path}[{frame_index:d}]"
        try:
            wand_image = wand.Image(filename=name, resolution=load_options.dpi)
        except wand_exceptions.WandException as wand_exception:
            _logger.exception("Cannot open image as wand Image.")
            raise CannotOpenImageAsWandImage() from wand_exception
        with wand_image:
            wand_image.background_color = "white"
            wand_image.alpha_channel = "background"
            wand_image.merge_layers("flatten")
            wand_image.type = load_options.color_depth
            wand_image.colorspace = load_options.color_channels
            pil_image = _convert_to_pil_image(wand_image)
            yield pil_image


def _get_number_of_frames(path: str) -> int:
    cmd = ["identify", "-format", "%n\n", str(path)]
    pipe = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
    out, _ = pipe.communicate()
    frame_count = out.split(b"\n")[0]
    if frame_count == b"":
        raise InvalidImage("Cannot read source image.")
    return int(frame_count)


def _convert_to_pil_image(wand_image: wand.Image) -> pil.Image:
    with wand_image.convert("png") as converted_image:
        with io.BytesIO() as image_data:
            converted_image.save(file=image_data)
            image_data.seek(0)
            try:
                pil_image = pil.open(image_data)
            except IOError as pil_exception:
                _logger.exception("Cannot open image as PIL Image.")
                raise CannotOpenImageAsPILImage() from pil_exception

            with pil_image:
                return pil_image.convert("RGB")
