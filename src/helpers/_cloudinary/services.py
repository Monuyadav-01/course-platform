def get_cloudinary_image_object(instance, field_name="image", as_html=False, width=200):
    if not hasattr(instance, field_name):
        return ""
    image_object = getattr(instance, field_name)
    if not image_object:
        return None
    image_options = {"width": width}
    if as_html:
        return image_object.image(**image_options)
    url = image_object.build_url(**image_options)
    return url



def get_cloudinary_video_object(
    instance, field_name="video", as_html=False, width=None, sign_url=False
):
    if not hasattr(instance, field_name):
        return ""
    video_object = getattr(instance, field_name)
    if not video_object:
        return None
    video_options = {"sign_url": sign_url, "width": width}
    if as_html:
        return video_object.video(**video_options)
    url = video_object.build_url(**video_options)
    return url
