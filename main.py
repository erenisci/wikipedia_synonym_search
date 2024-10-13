import glob

from src.parser import parse_xml_and_store_in_mongo


def main():
    xml_files = glob.glob(
        "resources/*.xml"
    )  # resources klasöründeki tüm XML dosyalarını al

    for xml_file in xml_files:
        try:
            parse_xml_and_store_in_mongo(xml_file)
            print(f"Successfully processed: '{xml_file}'")  # Başarı mesajı
        except Exception as e:
            print(f"Error processing file '{xml_file}': {e}")


if __name__ == "__main__":
    main()
