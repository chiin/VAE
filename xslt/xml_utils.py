import lxml


def reformat_xml(xml_file_name: str) -> bool:
    xml_original = lxml.etree.parse(xml_file_name)

    xml_object = lxml.etree.tostring(xml_original,
                                     pretty_print=True,
                                     xml_declaration=True,
                                     encoding='UTF-8')

    with open(xml_file_name, "wb") as writter:
        writter.write(xml_object)
    return True
