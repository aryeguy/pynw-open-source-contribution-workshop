import argparse
import requests
from bs4 import BeautifulSoup

COMMENTS_API_URL = 'https://plus.googleapis.com/u/0/_/widget/render/comments?first_party_property=YOUTUBE&href={video_url}'
HAPPY_WORDS = set(['love', 'loved', 'like', 'liked', 'awesome',
                   'amazing', 'good', 'great', 'excellent'])
SAD_WORDS = set(['hate', 'hated', 'dislike', 'disliked',
                 'awful', 'terrible', 'bad', 'painful', 'worst'])


def scrape_video_comments(video_url):
    """Scrape the comments from a Youtube video and return them as a list."""
    response = requests.get(COMMENTS_API_URL.format(video_url=video_url))
    soup = BeautifulSoup(response.content, "html.parser")
    comments = soup.findAll('div', {'class': 'Ct'})
    comments = [
        comment.text for comment in comments if comment not in [
            '', ' ']]
    return comments


def happy_or_sad_comment(comment):
    """Count the happy and sad words in a Youtube comment"""
    happy_count = sad_count = 0
    words = comment.split(' ')
    for word in words:
        if word in HAPPY_WORDS:
            happy_count += 1
        elif word in SAD_WORDS:
            sad_count += 1
    return (happy_count, sad_count)


def happy_or_sad(video_url):
    comments = scrape_video_comments(video_url)
    happy_count = sad_count = 0
    for comment in comments:
        happy_word_count, sad_word_count = happy_or_sad_comment(comment)
        happy_count += happy_word_count
        sad_count += sad_word_count

    verdict = 'Happy' if happy_count > sad_count else 'Sad'
    print(
        'From a sample size of {no_comments} comments, the responses to this video are mostly {verdict}. '
        'It contained {happy_count} happy keywords and {sad_count} sad keywords' .format(
            no_comments=len(comments),
            verdict=verdict,
            happy_count=happy_count,
            sad_count=sad_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Youtube video happy or sad')
    parser.add_argument('url', metavar='URL', help='URL of Youtube video')
    args = parser.parse_args()
    happy_or_sad(args.url)
