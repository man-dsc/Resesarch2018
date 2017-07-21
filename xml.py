from lxml import etree
import csv

def get_tweet_list(app, category):
    tweet_list = []
    path = "C:/Users/Summer16/Documents/Summer '16 Henry/Twitter Data/Final_Compiled/Cleaned Text2/%s/%s.csv" % (category, app)
    source_file = open(path, 'rb')
    reader = csv.reader(source_file)
    data = list(reader)
    
    for i in range(len(data)):
        tweet_list.append(data[i][1])
    
    return tweet_list


def main(data_num, app, category):
    root = etree.Element('reviews_summary')
    reviews = etree.Element('reviews')
    root.append(reviews)
    
    tweet = get_tweet_list(app, category)
    err = 0
    
    for i in range(data_num):
        try:
            sub_review = etree.Element('review')
            reviews.append(sub_review)
            
            app_version = etree.Element('app_version')
            sub_review.append(app_version)
            
            user = etree.Element('user')
            sub_review.append(user)
            
            date = etree.Element('date')
            sub_review.append(date)
            
            star_rating = etree.Element('star_rating')
            sub_review.append(star_rating)
            
            review_title = etree.Element('review_title')
            sub_review.append(review_title)
            
            review_text = etree.Element('review_text')        
            review_text.text = tweet[i]
            sub_review.append(review_text)
        
        except:
            err += 1
            print(i)
            pass
    
    print(err)
    
    tree = etree.ElementTree(root)
    tree.write('C:/Users/Summer16/inputFile.xml', pretty_print = True, xml_declaration = None)
    
if __name__ == "__main__":
    main(555, 'facetune', 'TopFree')
    
    