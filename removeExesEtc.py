import re

def clean_text(edited):

    edited = re.sub("rt ","",edited)
    edited = re.sub(r"^(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub(r"^\"(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub("@","",edited)
    edited = re.sub("\"","",edited)
    edited = re.sub("\n"," ",edited)
    edited = re.sub("#([a-zA-Z0-9])+","",edited)
    edited = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+","",edited)
    edited = re.sub("-"," ",edited)
    edited = re.sub("\\\\"," ",edited)
    edited = re.sub("/"," ",edited)
    edited = re.sub("[^a-zA-Z\d\s]","",edited)
    edited = re.sub("  "," ",edited)
    edited = re.sub("^ ","",edited)


    edited = re.sub("blueskypizza ","Dawood ",edited)
    edited = re.sub("enigmaticshrub ","Dawood ",edited)
    edited = re.sub("lesgressins ","Dawood ",edited)
    edited = re.sub("lesgressins ","Dawood ",edited)
    edited = re.sub("dadurath ","Dawood ",edited)
    edited = re.sub("bloodorphan ","Dawood ",edited)
    edited = re.sub("necrodentist ","Dawood ",edited)
    edited = re.sub("mohlhean ","Dawood ",edited)
    edited = re.sub("monotonino ","Dawood ",edited)
    edited = re.sub("mehanadurath ","Dawood ",edited)
    edited = re.sub("FeelMyNaduwrath ","Dawood ",edited)

    edited = re.sub("7e5h|7E5H","Sam",edited)

    edited = re.sub("TrippyTrevMC ","Trevor ",edited)

    edited = re.sub("imnotnorman ","Emily ",edited)

    edited = re.sub("stinfriggins ","Austin ",edited)

    edited = re.sub("briannahicks11 ","Bri ",edited)

    edited = re.sub("(b|B)eallnet ","Sarah ",edited)

    edited = re.sub("bijanmustard ","Bijan ",edited)

    edited = re.sub("GarrettOdom45 ","Garrett ",edited)

    edited = re.sub("ohhohowoah ","Elizabeth ",edited)
    edited = re.sub("spookyghastwoah ","Elizabeth ",edited)
    edited = re.sub("hohosantawoah ","Elizabeth ",edited)
    edited = re.sub("hohosannawoah ","Elizabeth ",edited)

    edited = re.sub("(a|A)rmaan(z|Z)irakchi ","Armaan ",edited)

    edited = re.sub("annannunciates ","Anna ",edited)
    edited = re.sub("(B|b)anananana(A|a)nna ","Anna ",edited)

    edited = re.sub("brandonrivera ","Brandon ",edited)

    edited = re.sub("andrewiswhite ","Andrew ",edited)

    edited = re.sub(r"^ +", "", edited)
    return edited



def clean_csv():
    path = "tweets.csv"
    with open(path, 'r') as file:
        text = file.read()
    tweets = []

    banned_words = ["julie","everyword","dubstep","doctor who","minecraft"]

    text = re.sub(r"\n\"\d{9,}\"", "?????????please", text)

    # print(text)
    for line in text.split("?????????please"):
        split = line.split("\",\"")
        lower = split[4].lower()
        # if lower == '' or re.match(lower,r"[0-9]+"):
        #     lower = split[4]
        good = True
        for word in banned_words:
            if word.lower() in lower:
                good = False
        if good:
            tweets.append(lower)

    with open('cleaned_tweets.txt', 'w') as f:
        for tweet in tweets:
            clean = clean_text(tweet)
            if len(clean) != 0 and len(clean.split(" 3")) >= 1:
                f.write("~~~~~~~~~~" + clean + "\n")
