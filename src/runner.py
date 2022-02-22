
import tools.image_manipulation as im
from src.scraping.archive_builder import ArchiveBuilder
from src.scraping.support.etsy_extractor import EtsyExtractor

if __name__ == "__main__":
    print("Adaptive Web Scraping by Github.com/Mallington")

    product_extractor = EtsyExtractor()

    archive_builder = ArchiveBuilder("/home/mathew/temp/archive-test")

    myJSON = [
  "https://www.etsy.com/uk/listing/951735480/heart-necklace-set-made-with-authentic?click_key=60f72e166acc142086c9cebffd2393be31ec8c6f%3A951735480&click_sum=492c3c08&ref=hp_rv-1&sts=1",
  "https://www.etsy.com/uk/listing/1124510683/couple-magnetic-matching-necklace-couple?click_key=7cea71856761213174708088a5b70a8549903e64%3A1124510683&click_sum=3d819d5e&ref=hp_rv-2",
  "https://www.etsy.com/uk/listing/924627809/heart-necklace-made-with-lego-bricks-o?click_key=eafbf045b1c64195a29d089298254d9f7833ae3a%3A924627809&click_sum=cc3de6d0&ref=hp_rv-3&sts=1",
  "https://www.etsy.com/uk/listing/1098739525/romantic-couples-925-sterling-silver?click_key=96d60c492abc94058aac50893ec28db34de2dee0%3A1098739525&click_sum=99ff01d6&ref=hp_rv-4&frs=1",
  "https://www.etsy.com/uk/listing/95754955/heart-necklace-set-made-with-authentic?click_key=c789cffcebdc83d9e51c4b8b32b41e757c98b35f%3A95754955&click_sum=8532d336&ref=hp_rv-5&sts=1",
  "https://www.etsy.com/uk/listing/965144513/heart-necklace-set-made-with-authentic?click_key=ca6a951924efa3b550549f9431945a82650dd6cf%3A965144513&click_sum=e541f24e&ref=hp_more_from_this_shop-1&sts=1",
  "https://www.etsy.com/uk/listing/951172360/heart-keychain-set-made-with-authentic?click_key=91bb7d6cf38891bb6f4ab67cc22c50d7ac987205%3A951172360&click_sum=45beb719&ref=hp_more_from_this_shop-2&sts=1",
  "https://www.etsy.com/uk/listing/1105790223/heart-necklace-set-made-with-authentic?click_key=92889afbaba44612b5fd4485b68e09f95ff11a46%3A1105790223&click_sum=3e026673&ref=hp_more_from_this_shop-3&sts=1",
  "https://www.etsy.com/uk/listing/965143193/heart-keychain-set-made-with-authentic?click_key=267893f4adc5c7593e2d53f85545885785d78ded%3A965143193&click_sum=41add0cb&ref=hp_more_from_this_shop-4&sts=1",
  "https://www.etsy.com/uk/listing/1045541120/heart-necklace-set-made-with-authentic?click_key=e630987d318bee8ef8aa99bda9d391ef930841fb%3A1045541120&click_sum=0b4548a7&ref=hp_more_from_this_shop-5&sts=1",
  "https://www.etsy.com/uk/listing/1124510683/couple-magnetic-matching-necklace-couple?click_key=89ad030273810dd4a1a811da6502ac7fb7933b69%3A1124510683&click_sum=5da7bc14&ref=hp_signed_out_opfy-1",
  "https://www.etsy.com/uk/listing/924627809/heart-necklace-made-with-lego-bricks-o?click_key=cbe5dddc042e987601b04e26428fbcfb201140eb%3A924627809&click_sum=bbc0adde&ref=hp_signed_out_opfy-2&sts=1",
  "https://www.etsy.com/uk/listing/1098739525/romantic-couples-925-sterling-silver?click_key=443806a3d368427f35024097bea932607fe9bd6a%3A1098739525&click_sum=89676bd8&ref=hp_signed_out_opfy-3",
  "https://www.etsy.com/uk/listing/95754955/heart-necklace-set-made-with-authentic?click_key=d4165bae6f7a9a6f1c8419cfa5d18275bf4a33f4%3A95754955&click_sum=9f481cb6&ref=hp_signed_out_opfy-4&sts=1",
  "https://www.etsy.com/uk/listing/1076614855/2pcs-couple-anatomical-heart-puzzle?click_key=baf5b9fe4190bfa73c2bab63fddeecb72cf5abfb%3A1076614855&click_sum=f098a236&ref=hp_signed_out_opfy-5",
  "https://www.etsy.com/uk/listing/1080721210/couple-necklace-friendship-necklace?click_key=37a14c4285bde2aeda6dbd137777fe6d89c3e0b4%3A1080721210&click_sum=8a6d7ff5&ref=hp_signed_out_opfy-6",
  "https://www.etsy.com/uk/listing/1127647582/couple-necklace-cartoon-couple-necklace?click_key=c2d615e74c1b5244e35382c03ce01981b7bc3fad%3A1127647582&click_sum=3c85e114&ref=hp_signed_out_opfy-7",
  "https://www.etsy.com/uk/listing/940514132/two-personalized-necklaces-silver-rose?click_key=d64627d053e0ef10822cc5f84e7002b2804b27fa%3A940514132&click_sum=7f0ed3b0&ref=hp_signed_out_opfy-8",
  "https://www.etsy.com/uk/listing/1053289130/embroidery-kit-wildflower-meadow-golden?click_key=14ffbeadcb97eaf31b0135e3950b7132c537727d%3A1053289130&click_sum=78d1c142&ref=hp_editors_picks_primary-1&sts=1",
  "https://www.etsy.com/uk/listing/784790982/fun-new-parents-decision-flip-coin-37mm?click_key=c4bd735de9bce86796551ff5eeb804ce73424440%3A784790982&click_sum=f788eae0&ref=hp_editors_picks_primary-2",
  "https://www.etsy.com/uk/listing/253282161/pet-portrait-pillow-custom-designed?click_key=18c0766cbba1708dadc1a9c38b315bb9318b28c5%3A253282161&click_sum=3faf6c72&ref=hp_editors_picks_primary-3",
  "https://www.etsy.com/uk/listing/661620252/motherly-love-coupons-mothers-day-gift?click_key=0db5fbc64de2c24bf4c5b21142dc835323d4fc3e%3A661620252&click_sum=ee45eb36&ref=hp_editors_picks_primary-4",
  "https://www.etsy.com/uk/listing/783969419/personalised-story-book-for-grandma?click_key=675ad5c1e9595d57faf69ba3467d4e216b56b825%3A783969419&click_sum=8c134a34&ref=hp_editors_picks_primary-5",
  "https://www.etsy.com/uk/listing/990113530/scripted-personalised-painted-candles?click_key=4a1738cb12ab4a7c3b693f8330536a8cb876704a%3A990113530&click_sum=252888b9&ref=hp_editors_picks_primary-6",
  "https://www.etsy.com/uk/listing/667238651/scented-soy-candle-fig-forest-soy-wax?click_key=0f06cd46a51b73be47a97c447bc536ddb9fdbf33%3A667238651&click_sum=f369172f&ref=hp_merch_co-1&sts=1",
  "https://www.etsy.com/uk/listing/1056926605/tufted-rug-mirror-in-teal-yellow-and?click_key=ec32858a68f9893ab08a19f93af766efbbbf314f%3A1056926605&click_sum=61baf28d&ref=hp_merch_co-2",
  "https://www.etsy.com/uk/listing/804517234/aromatherapy-candles-focus-tranquility?click_key=ba6496f706128ca23a659d6f051e5a290c8a3fd3%3A804517234&click_sum=f4bc634a&ref=hp_merch_co-3",
  "https://www.etsy.com/uk/listing/1036815952/handmade-light-green-and-white-cow-print?click_key=c243413a153260d4e9ac99ec4dfb102752b83311%3A1036815952&click_sum=5e661691&ref=hp_merch_co-4",
  "https://www.etsy.com/uk/listing/834119654/macrame-tufted-cushion-cover-grey-stripe?click_key=f0069122fbc8e80962132899a1a86e18c26f2af7%3A834119654&click_sum=1c83e08a&ref=hp_merch_co-5",
  "https://www.etsy.com/uk/listing/929438789/pillow-cover-throw-pillow-tassel-pillow?click_key=bd629edb9ff9ddaf16b950231e7783255bd65e65%3A929438789&click_sum=1bd4f43e&ref=hp_merch_co-6",
  "https://www.etsy.com/uk/listing/281181782/aromatherapy-bergamot-soy-candle?ref=hp_merch_co-0"
]
    for el in myJSON:
        print(el)
        archive_builder.add_site(el, product_extractor)

    # archive_builder.add_site("https://www.etsy.com/uk/listing/951735480/heart-necklace-set-made-with-authentic", product_extractor)
    # archive_builder.add_site("https://www.etsy.com/uk/listing/1105790223/heart-necklace-set-made-with-authentic", product_extractor)
    # archive_builder.add_site("https://www.etsy.com/uk/listing/1045541120/heart-necklace-set-made-with-authentic", product_extractor)

    archive_builder.save()