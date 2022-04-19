from functions import get_urls
from functions import get_text_from_urls
from functions import analyze_texts_from_urls
from functions import create_dataframe

def main():
    PATH = "../urls/urls.txt"
    urls = get_urls(PATH)
    text = get_text_from_urls(urls)
    analysis = analyze_texts_from_urls(text)
    return analysis

if __name__ == "__main__":
    analysis = main()
    df = create_dataframe(analysis)
    df.to_csv("../results/results.csv", index=False)

    # print(df.sort_values(by=["Count"], ascending=False))
