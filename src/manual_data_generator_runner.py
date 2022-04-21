import os.path

from src.scraping.url_lists import master_link_list, raw_links
from src.scraping.archive_builder import ArchiveBuilder
from src.scraping.support.extractors.dom_selector_extractor import DomExtractorSelector
from src.scraping.yolo_config_generator import YoloConfigGenerator
import os

import pickle as pk
# click event handler

def confirm(question, default_no=True):
    os.system(f"say {question} answer in console &")
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True



    return False


if __name__ == "__main__":
    print("Adaptive Web Scraping by Github.com/Mallington")
    archive_location = "/Users/mathew/github/adaptive-web-scraping/data/retail-individual-fields-dataset"
    cookie_save_location = '/Users/mathew/github/adaptive-web-scraping/cookies/user-cookies.pkl'

    # product_extractor = DomExtractorSelector(["title", "summary", "figure", "formula", "table"])
    product_extractor = DomExtractorSelector(["title", "price", "description", "image"], other_elements="other_elements")
    archive_builder = ArchiveBuilder(archive_location)

    if os.path.exists(cookie_save_location):
        cookies_dict = pk.load(open(cookie_save_location, "rb"))
        product_extractor.accept_cookies_auto(archive_builder.driver, cookies_dict)

    else:
        cookies_dict = product_extractor.accept_cookies(archive_builder.driver, raw_links)
        pk.dump(cookies_dict, open(cookie_save_location, "wb"))



    urls_to_train = master_link_list
    count =0

    try:
        for el in urls_to_train[1:]:
            if count %50 ==0 and count>0:
                if not confirm("Do you want to continue?"):
                    break
            print(el)
            print(count, "done")
            archive_builder.add_site(el, product_extractor)
            count += 1
    except Exception as e:

        archive_builder.close()
        print(e)
        pass
    # archive_builder.add_site("https://www.etsy.com/uk/listing/951735480/heart-necklace-set-made-with-authentic", product_extractor)
    # # archive_builder.add_site("https://www.etsy.com/uk/listing/1105790223/heart-necklace-set-made-with-authentic", product_extractor)
    # # archive_builder.add_site("https://www.etsy.com/uk/listing/1045541120/heart-necklace-set-made-with-authentic", product_extractor)

    archive_builder.save()

    archive_builder.close()

    generator = YoloConfigGenerator(archive_location)
    generator.generate_configuration()

    id = archive_builder.element_archiver.index_dictionary["master_snapshots"][0]["id"]
    label = os.path.join(archive_location, "labels/", f"{id}.txt")
    image = os.path.join(archive_location, "master-screenshots/", f"{id}.png")

    # viewer = YoloBoxVisualiser(image, label)
    #
    # viewer.show_image()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()