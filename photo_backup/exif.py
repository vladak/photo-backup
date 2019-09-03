import json
import logging


def get_keywords(et, fullname):
    """
    Get EXIF keywords for a file.
    :param et: exiftool instance
    :param fullname: full path to the file
    :return: list of keywords
    """

    logger = logging.getLogger(__name__)

    try:
        metadata = et.get_metadata(fullname)
        logger.debug("File {} metadata: {}".
                     format(fullname, metadata))
    except json.decoder.JSONDecodeError:
        logger.error("Cannot get metadata for {}".format(fullname))
        raise

    try:
        file_keywords = metadata["IPTC:Keywords"]
        logger.debug("File {} has keywords: {}".
                     format(fullname, file_keywords))
    except KeyError:
        logger.debug("File {} does not contain keyword metadata".
                     format(fullname))
        return []

    return file_keywords


def check_keywords(et, fullname, keywords):
    """
    Check if file has contains specified EXIF keywords.
    :param et: exiftool instance
    :param fullname: full path to the file
    :param keywords: list of keywords
    :return: true if the file contains a keyword from the list
    """

    logger = logging.getLogger(__name__)

    for keyword in keywords:
        if keyword in get_keywords(et, fullname):
            logger.debug("File {} contains the '{}' keyword".
                         format(fullname, keyword))
            return True

    return False
