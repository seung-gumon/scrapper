from scrapper.extractor import LinkExtractor

# 객체 생성 및 실행
extractor = LinkExtractor()
transformed_json = extractor.run()
print("Transformed JSON Data:",transformed_json)



