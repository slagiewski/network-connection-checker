LOCAL_HOST = "Local"
EXTERNAL_HOST = "External"

# Translation
ConnectionIssueWith = "Connection issue with"
LocalConnectionIsNotWorking = "Local connection is not working!"


def translate(text, lang="pl"):
    dictionary = {
        "pl":
            {
                "Connection issue with": "Problemy łączności z",
                "Local connection is not working!": "Brak łączności lokalnej!"
            }
    }
    return dictionary.get(
        lang,
        {text: text}
    ).get(
        text
    )
