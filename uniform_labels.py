import files
from xml.etree import ElementTree
import os

PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019/annotated'
files = files.list_files(PATH)

def edit_xml_file(data):
    e = ElementTree.fromstring(data)

    for file_element in e.findall('file'):

        analyse_element = file_element.find('analyse')

        in_context_exact_element = analyse_element.find('inContextExact')
        in_context_exact_words = int(in_context_exact_element.get('words'))
        in_context_exact_element.set('words', '0')

        cross_file_repeated_element = analyse_element.find('crossFileRepeated')
        cross_file_repeated_words = int(cross_file_repeated_element.get('words'))
        cross_file_repeated_element.set('words', '0')

        total_element = analyse_element.find('total')
        total_element.set('words', str(in_context_exact_words + cross_file_repeated_words))

    xmlstr = ElementTree.tostring(e)
    return xmlstr

def main():

    source_directory = 'xmlfiles'

    for filename in os.listdir(source_directory):

        if not filename.endswith('.xml'):
            continue

        xml_file_path = os.path.join(source_directory, filename)
        with open(xml_file_path, 'r+b') as f:
            data = f.read()
            fixed_data = edit_xml_file(data)
            f.seek(0)
            f.write(fixed_data)
            f.truncate()


if __name__ == '__main__':
    main()





