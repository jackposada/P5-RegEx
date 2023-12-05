import java.util.regex.*;
import java.io.*;

import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

/**
 * Example Java code to use regular expression
 * @author Xunhua Wang (wangxx@jmu.edu). All rights reserved.
 * @date 11/24/2019; further revised on 12/01/2019, 12/04/2019, 12/06/2022
 */
public class DoeJohnRegEx {

        //
        // 1. The local-part of an email address must not exceed 64 characters
        // 2. The domain part of an email address must not exceed 255 characters 
        // 3. The total length of an email address must not exceed 254 characters
        //
        public boolean isLengthValid (String inEmailAddress) {
                boolean result = true;

                int pos = inEmailAddress.indexOf('@');
                if (pos < 0) return false;

                String localuserName = inEmailAddress.substring (0, pos);
                String domainPart = inEmailAddress.substring (pos+1);
                int len1 = localuserName.length();
                int len2 = domainPart.length();
                if (len1 > 64) return false;
                if (len2 > 255) return false;
                if (len1 + len2 > 254) return false;
                return true;
        }

        public void testIsLengthValid () {
                String emailAddress1 = "wangxx@jmu.edu";
                boolean result1 = isLengthValid (emailAddress1);

                String emailAddress2 = "786762D781A7FF4FAC9060892B4044880360B6E00F@CLNTINET08";
                boolean result2 = isLengthValid (emailAddress2);
                System.out.println ("Is " + emailAddress1 + " valid? " + result1);
                System.out.println ("Is " + emailAddress2 + " valid? " + result2);
        }

	public int search (String inPatternString, String inText) {
		Pattern r = Pattern.compile (inPatternString, Pattern.CASE_INSENSITIVE);
		Matcher m = r.matcher (inText);
		int totalCount = 0;

		// System.out.println (System.getProperty("line.separator") + "PATTERN is " + inPatternString + "\tTEXT is " + inText);
		while (m.find()) { // while
			int startIndex = m.start();
			int endIndex = m.end();

			System.out.println ("Pattern is found: start = " + startIndex + ", end = " + endIndex);
			String str0 = m.group (0);
			System.out.println ("Group 0 = " + str0);

			//
			// Check https://docs.oracle.com/javase/tutorial/essential/regex/groups.html
			// https://docs.oracle.com/javase/7/docs/api/java/util/regex/Matcher.html
			//
			// String str1 = m.group (1);
			// System.out.println ("Group 1 = " + str1);
			//

                        if (isLengthValid (str0)) {
			    totalCount++;

                            //
                            // TODO: other meaningful operations
                            //
                        }
		}

		// System.out.println ("Total matched = " + totalCount);
		return totalCount;
	}

	public String loadFile (String inFilename) throws Exception {
		StringBuffer sb = new StringBuffer (); // hillary-clinton-emails-august-31-release_djvu_copy.txt

		File file = new File(inFilename);
		BufferedReader br = new BufferedReader(new FileReader(file)); 
  
		String st; 
		while ((st = br.readLine()) != null) {
			// System.out.println(st); 
			sb.append (st.toLowerCase());
			sb.append (System.getProperty("line.separator"));
		} 

		return sb.toString();
	}


	//
	// TODO: Refer to the project document for the exact printout requirements
	//
	public static void main (String args[]) {
		try {
			DoeJohnRegEx djre = new DoeJohnRegEx ();

			// TODO: put the regular expression for your local part here
			String pattern4_localuser_variant = "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+";
            String pattern4_domain = "[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*";
            String pattern5 = pattern4_localuser_variant + "@" + pattern4_domain;
            
			if (args.length == 0) {
				System.out.println ("Use java DoeJohnRegEx FILE");
				return;
			}

			String text2 = djre.loadFile(args[0]);
			System.out.println ("My regular expression is " + pattern5);
			System.out.println ("My regular expression works as follows: the FIRST part, ..., specifies ... ; the SECOND part, ..., specifies ... (TODO)");

			int totalCount = djre.search (pattern5, text2); // pattern5
			System.out.println ("The total # is " + totalCount);
		} catch (Exception ex) {
			ex.printStackTrace ();
		}
	}
}