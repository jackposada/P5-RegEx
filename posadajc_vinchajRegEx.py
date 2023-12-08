import re
import networkx as nx
import matplotlib.pyplot as plt



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

        # print("Pattern is found: start = " + str(startIndex) + ", end = " + str(endIndex))
        str = match.group(0)
        str0 = str.lower()
        # print("Group 0 = " + str0)


        if isLengthValid(str0):
            totalCount += 1
            uniqueCount.add(str0)
            if emailCounts.get(str0) is None:
                emailCounts[str0] = 1 
            else:
                emailCounts[str0] += 1

    emailCountsSorted = [(email, count) for email, count in emailCounts.items()]
    emailCountsSorted.sort(key=lambda emailPair: emailPair[1], reverse=True)
    

    return totalCount, uniqueCount, emailCountsSorted


def loadFile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()
    
def main(args):
    try:        
        # extra credit regex for local
        # worked when tested on small files but runs for ever on the big files
        # pattern4_localuser_variant = r'(?:(?:\([^)]*\))?((?!\.)(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\w!#$%&\'*+/=?^_`{|}~. (),:;<>@[\]\\]+|\\[\\"])*")(?<!\.))(?:\([^)]*\))?)'
        pattern4_localuser_variant = r'(?:(?!\.)[a-z0-9!#$%&\*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*(?<!\.)|"[a-z0-9!#$%&\'*+/=?^_`{|}~.-]+")'

        pattern4_domain = "(?:(?:[a-z0-9]+(?:-[a-z0-9]+)*\\.)+[a-z0-9]+(?:-[a-z0-9]+)*|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:)\\])"

        pattern5 = pattern4_localuser_variant + "@" + pattern4_domain
   

        if not args:
            print("Use python script_name.py FILE")
            return

        text2 = loadFile(args[0])
        print("My regular expression is " + pattern5)
        print("My regular expression works as follows: the FIRST part, "
            "(?:(?!\.)[a-z0-9!#$%&\*+/=?^_{|}~-]+, specifies which characters the local "
            "part can start with and that it cannot start with a '.'; the SECOND part, "
            "(?:\.[a-z0-9!#$%&\'*+/=?^_{|}~-]+)*(?<!\.), allows the rest of the local "
            "part to contain a '.' along with the other characters and prevents the "
            "local part from ending with a dot, the THIRD part, "
            "\"[a-z0-9!#$%&\'*+/=?^_{|}~.-]+\"), allows for consecutive dots within "
            "double quotes, the FOURTH part, (?:(?:[a-z0-9]+(?:-[a-z0-9]+)*\\.)+[a-z0-9]+(?:-[a-z0-9]+)*), "
            "matches teh domain part of the email address and consists of letters and numbers "
            "that can be broken up by '.' or '-' where there can be zero or more hyphens and one or more "
            "dots but the hyphen cannot be the first nor last character in the domain part, the FIFTH part, "
            "|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|"
            "[a-z0-9-]*[a-z0-9]:)\\], is used when there is an IP address instead of a domain name, the IP "
            "address must be within brackets and the number ranges ensure an IP address is valid and the "
            "{3} means the pattern repeats 3 times")

        totalCount, uniqueCount, emailCounts = search(pattern5, text2)
        print("The total # is " + str(totalCount))
        print("The Unique total # is " + str(len(uniqueCount)))

        print()
        with open('posadajc_vinchaj_sorted_emailaddresses.txt', 'w') as file:
            for pair in emailCounts:
                file.write(pair[0] + ": " + str(pair[1]) + "\n")
        with open('posadajc_vinchaj_all_emailaddresses.txt', 'w') as file:
            for email in uniqueCount:
                file.write(email + "\n")
        
        graph_emails = {}
        G = nx.DiGraph()
        senders = []
        receivers = []
        # GRAPH BONUS QUESTION
        with open(args[0], 'r', encoding='utf-8') as file:
            print("PRINTING GRAPH NOW")
            
            sender = None
            receiver = None
            for line in file:
                line = line.strip()
                if line.startswith('From:'):
                    sender_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line, re.IGNORECASE)
                    if sender_match:
                        sender = sender_match.group()
                        senders.append(sender.lower())
                elif line.startswith('To:'):
                    receiver_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line, re.IGNORECASE)
                    if receiver_match:
                        receiver = receiver_match.group()
                        receivers.append(receiver.lower())

        for sender, receiver in zip(senders, receivers):
            if G.has_edge(sender, receiver):
                G[sender][receiver]['weight'] += 1
            else:
                G.add_edge(sender, receiver, weight=1)

        pos = nx.spring_layout(G, k=2.0)
        nx.draw_networkx_nodes(G, pos, node_size=50)
        edges = nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=5)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
        plt.show()  



    except Exception as ex:
        print(ex)

# If this script is run directly, call the main method with command line arguments
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
