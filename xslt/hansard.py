import lxml.etree

import stylesheet


def xslt_from_str(transform_str: str):
    return lxml.etree.XSLT(
        lxml.etree.fromstring(transform_str))


def process_hansard_xml(xml_file_name: str):
    xml_original = lxml.etree.parse(xml_file_name)

    xsl_add_speech_count = xslt_from_str(stylesheet.XSL_ADD_WORD_COUNT_BY_SPEECH)
    xml_add_speech_count = xsl_add_speech_count(xml_original)

    xsl_sum_word_count = xslt_from_str(stylesheet.XSL_SUM_WORD_COUNT_BY_NAME)
    xml_sum_word_count = xsl_sum_word_count(xml_add_speech_count)

    xsl_convert_to_html = xslt_from_str(stylesheet.XSL_ADD_TABLE_CONVERT_TO_HTML)
    html_final = xsl_convert_to_html(xml_sum_word_count)

    return html_final