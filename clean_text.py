import re


def clean_text(edited):
    edited = re.sub("^(RT|rt) .*", "", edited)
    edited = re.sub("^@.*", "", edited)
    edited = re.sub(r"^(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub(r"^\"(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub("@", "", edited)
    edited = re.sub("\"", "", edited)
    edited = re.sub("\n", " ", edited)
    edited = re.sub("#([a-zA-Z0-9])+", "", edited)
    edited = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", edited)
    edited = re.sub("-", " ", edited)
    edited = re.sub("\\\\", " ", edited)
    edited = re.sub("/", " ", edited)
    edited = re.sub("[^a-zA-Z\d\s]", "", edited)
    edited = re.sub("  ", " ", edited)
    edited = re.sub("^ ", "", edited)
    edited = re.sub(r"^ +", "", edited)
    edited = re.sub(r" $", "", edited)
    edited = " ".join(edited.split())

    return edited
