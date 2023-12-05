import re


"""
 * Example Java code to use regular expression
 * @author Xunhua Wang (wangxx@jmu.edu). All rights reserved.
 * @date 11/24/2019; further revised on 12/01/2019, 12/04/2019, 12/06/2022
 """

#
# 1. The local-part of an email address must not exceed 64 characters
# 2. The domain part of an email address must not exceed 255 characters 
# 3. The total length of an email address must not exceed 254 characters
#
def isLengthValid(inEmailAddress):
    result = True

    pos = inEmailAddress.find('@')
    if pos < 0: 
        return False

    localuserName = inEmailAddress[:pos]
    domainPart = inEmailAddress[pos+1:]
    len1 = len(localuserName)
    len2 = len(domainPart)
    if len1 > 64: 
        return False
    if len2 > 255: 
        return False
    if len1 + len2 > 254: 
        return False
    return True

def testIsLengthValid():
    emailAddress1 = "wangxx@jmu.edu"
    result1 = isLengthValid(emailAddress1)

    emailAddress2 = "786762D781A7FF4FAC9060892B4044880360B6E00F@CLNTINET08"
    result2 = isLengthValid(emailAddress2)
    print("Is " + emailAddress1 + " valid? " + str(result1))
    print("Is " + emailAddress2 + " valid? " + str(result2))

def search(inPatternString, inText):
    r = re.compile(inPatternString, re.IGNORECASE)
    m = r.finditer(inText)
    totalCount = 0
    uniqueCount = set()
    emailCounts = {}
    # print("\n" + "PATTERN is " + inPatternString + "\tTEXT is " + inText)
    for match in m: # while
        startIndex = match.start()
        endIndex = match.end()

        print("Pattern is found: start = " + str(startIndex) + ", end = " + str(endIndex))
        str0 = match.group(0)
        print("Group 0 = " + str0)

        #
        # Check https://docs.oracle.com/javase/tutorial/essential/regex/groups.html
        # https://docs.oracle.com/javase/7/docs/api/java/util/regex/Matcher.html
        #
        # str1 = match.group(1)
        # print("Group 1 = " + str1)
        #

        if isLengthValid(str0):
            totalCount += 1
            uniqueCount.add(str0)
            if emailCounts.get(str0) is None:
                emailCounts[str0] = 1 
            else:
                emailCounts[str0] += 1

    emailCountsSorted = [(email, count) for email, count in emailCounts.items()]
    emailCountsSorted.sort(key=lambda emailPair: emailPair[1])
    
    # print("Total matched = " + str(totalCount))
    return totalCount, uniqueCount, emailCountsSorted

def loadFile(inFilename):
    sb = [] # StringBuffer

    with open(inFilename, 'r') as file:
        for st in file:
            # print(st)
            sb.append(st.strip().lower())
            sb.append("\n")

    return ''.join(sb)

#
# TODO: Refer to the project document for the exact printout requirements
#
def main(args):
    try:
        # TODO: put the regular expression for your local part here

        # pattern4_localuser_variant = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")"
        


        # all extra credit but johndoe@gmail.com are valid;
        # pattern4_localuser_variant = "(?:\\([^\\)]*\\))?(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.(?!\\.))[a-z0-9!#$%&'*+/=?^_`{|}~-]*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")(?:\\([^\\)]*\\))?"
        # pattern4_localuser_variant = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"

        # ^[a-z0-9!#$%&\'*+/=?^_`{|}~-] can start w any of these but cant start w '.'
        # [a-z0-9!#$%&\'*+/=?^_`{|}~.-] allows any of these characters
        # [a-z0-9!#$%&\'*+/=?^_`{|}~-]$ cannot end with a dot
        # should be working but is not
        pattern4_localuser_variant = "^[a-z0-9!#$%&'*+/=?^_`{|}~-][a-z0-9!#$%&'*+/=?^_`{|}~.-]*[a-z0-9!#$%&'*+/=?^_`{|}~-]$"

        pattern4_domain = "(?:(?:[a-z0-9]+(?:-[a-z0-9]+)*\\.)+[a-z0-9]+(?:-[a-z0-9]+)*|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        
        pattern5 = pattern4_localuser_variant + "@" + pattern4_domain
        # pattern5 = "((?!.*\.\.)[-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
        # Complete email pattern
        # pattern5 = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"


        if not args:
            print("Use python script_name.py FILE")
            return

        text2 = loadFile(args[0])
        print("My regular expression is " + pattern5)
        print("My regular expression works as follows: the FIRST part, ..., specifies ... ; the SECOND part, ..., specifies ... (TODO)")

        totalCount, uniqueCount, emailCounts = search(pattern5, text2) # pattern5
        print("The total # is " + str(totalCount))
        print("The Unique total # is " + str(len(uniqueCount)))
        for u in uniqueCount:
            print(u)

        print()
        for pair in emailCounts:
            print(pair[0] + ": " + str(pair[1]))


    except Exception as ex:
        print(ex)

# If this script is run directly, call the main method with command line arguments
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
