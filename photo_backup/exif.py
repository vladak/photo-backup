import logging

import exifread


def get_metadata(file_path):
    """
    Get EXIF metadata for a file.
    :param file_path: full path to the file
    :return: metadata dictionary
    """

    logger = logging.getLogger(__name__)

    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

    logger.debug("File {} tags: {}".format(file_path, tags))

    return tags


def get_keywords(file_path):
    """
    Get EXIF keywords for a file.
    :param file_path: full path to the file
    :return: list of keywords
    """

    logger = logging.getLogger(__name__)

    metadata = get_metadata(file_path)

    try:
        file_keywords = metadata["IPTC:Keywords"]
        logger.debug("File {} has keywords: {}".
                     format(file_path, file_keywords))
    except KeyError:
        logger.debug("File {} does not contain keyword metadata".
                     format(file_path))
        return []

    if not isinstance(file_keywords, list):
        file_keywords = [file_keywords]

    return file_keywords


def check_keywords(file_path, keywords):
    """
    Check if file has contains specified EXIF keywords.
    :param file_path: full path to the file
    :param keywords: list of keywords
    :return: true if the file contains a keyword from the list
    """

    logger = logging.getLogger(__name__)

    for keyword in keywords:
        if keyword in get_keywords(file_path):
            logger.debug("File {} contains the '{}' keyword".
                         format(file_path, keyword))
            return True

    return False
