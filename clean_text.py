# coding=utf-8
import re
import json


def clean(edited):

    edited = re.sub("^(RT|rt) .*", "", edited)
    edited = re.sub("^@.*", "", edited)
    edited = re.sub("@", "", edited)
    edited = re.sub("“", "\"", edited)
    edited = re.sub("”", "\"", edited)
    edited = re.sub(r"^(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub(r"^\"(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub("\n", " ", edited)
    # edited = re.sub("#([a-zA-Z0-9])+", "", edited)
    edited = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", edited)
    edited = re.sub("-", " ", edited)
    edited = re.sub("\\\\", " ", edited)
    edited = re.sub("/", " ", edited)
    edited = re.sub("^ ", "", edited)
    edited = re.sub(r"^ +", "", edited)
    edited = re.sub(r" $", "", edited)

    edited = re.sub("/", " ", edited)
    edited = re.sub(" {2}", " ", edited)
    edited = re.sub("^ ", "", edited)

    # with open('configs/replacements.json', 'r') as json_file:
    #     data = json.load(json_file)
    #     for replacement in data["replacements"]:
    #         edited = re.sub(replacement["old"], replacement["new"], edited)

    edited = re.sub(r"^ +", "", edited)
    edited = re.sub(r" $", "", edited)

    return edited
