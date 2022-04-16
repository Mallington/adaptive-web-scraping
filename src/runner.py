import os.path

import src.scraping.hyper_physics_urls
from src.scraping.archive_builder import ArchiveBuilder
from src.scraping.support.extractors.dom_selector_extractor import DomExtractorSelector
from src.scraping.yolo_config_generator import YoloConfigGenerator
import os
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
    archive_location = "/Users/mathew/github/adaptive-web-scraping/shopping-validation/"
    # product_extractor = DomExtractorSelector(["title", "summary", "figure", "formula", "table"])
    product_extractor = DomExtractorSelector(["interest_area", "not_interesting"])
    archive_builder = ArchiveBuilder(archive_location)

    myJSON = src.scraping.hyper_physics_urls.hyper_physics_urls

    myJSON=["https://www.amazon.co.uk/Echo-Dot-3rd-Gen-Charcoal/dp/B07PJV3JPR/",
            "https://uk.banggood.com/Vintage-Floral-Printed-O-neck-Long-Sleeve-Irregular-Hem-T-shirt-For-Women-p-1743627.html",
            "https://uk.banggood.com/Women-Vintage-Abstract-Figure-Printed-O-Neck-Irregular-Hem-Long-Sleeve-Blouse-p-1743629.html"]
    count =0

    try:
        for el in myJSON[1:]:
            if count % 2 ==0 and not confirm("Do you want to continue?"):
                print("Another 50 done")
            if count >500:
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