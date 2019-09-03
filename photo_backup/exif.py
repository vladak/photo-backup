import json
import logging


def check_keywords(et, fullname, keywords):
    """
    Check if file has contains specified EXIF keywords.
    :param et: exiftool instance
    :param fullname: full path to the file
    :param keywords: list of keywords
    :return: true if the file contains a keyword from the list
    """

    logger = logging.getLogger(__name__)

    try:
        metadata = et.get_metadata(fullname)
        logger.debug("File {} metadata: {}".
                     format(fullname, metadata))
    except json.decoder.JSONDecodeError:
        logger.error("Cannot get metadata for {}".format(fullname))
        return

    try:
        file_keywords = metadata["IPTC:Keywords"]
        logger.debug("File {} has keywords: {}".
                     format(fullname, file_keywords))
    except KeyError:
        logger.debug("File {} does not contain keyword metadata".
                     format(fullname))
        return False

    for keyword in keywords:
        if keyword in file_keywords:
            logger.debug("File {} contains the '{}' keyword".
                         format(fullname, keyword))
            return True

    return False
