def dateCorrect(date):
    arr = date.split("-")
    nDate = arr[1]+"/"+arr[2]+"/"+arr[0][2:4]
    return nDate