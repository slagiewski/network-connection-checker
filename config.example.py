import constants

hosts = [
    {
        "name":     "External host 1 name",
        "type":     constants.EXTERNAL_HOST,
        "address":  "192.168.2.1"
    },
    {
        "name":     "External host 2 name",
        "type":     constants.EXTERNAL_HOST,
        "address":  "192.168.3.1"
    },
    {
        "name":     "Getaway (Local host)",
        "type":     constants.LOCAL_HOST,
        "address":  "192.168.1.1"
    }
]

smtp = {
    "email":    "user@mail.com",
    "password": "pswd",
    "server":   "smtp.mail.com"
}

email_receiver = "user@mail.com"
email_subject = "Connection issues!"
