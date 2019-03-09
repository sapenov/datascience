import csv

FILE_PATH = "C:\\term_project\\"
DATA = FILE_PATH + "Projectdata.csv"
COURSES = {
"ARTS557":["19TH-CENTURY BRITISH LITERATURE", "19TH-CENT BRITISH LIT"],
"ARTS545":["20th Century Russian Literature: Fiction and Reality"],
"ARTS514":["A WORLD AT WAR"],
"ARTS551":["AESTHETICS"],
"ARTS492":["AFRICAN-AMERICAN LIT: AFRICAN-AMER LIT:CHANGE", "AFRICAN-AMERICAN LIT"],
"ARTS493":["AMERICAN HEALTH POLICY","AMERICAN HEALT POLICY"],
"ARTS541":["AMERICAN SOCIAL POLICY"],
"ARTS559":["AMERICAN SOUTH 1861-PRES"],
"ARTS512":["ANALYTICAL MECHANICS"],
"ARTS573":["ANALYZING THE POL WORLD"],
"ARTS543":["ART AND RELIGION", "ART & RELIGION"],
"ARTS401":["ART: ancient to 1945",
           "ART - from ancient to 1945",
           "ART ancient to 1945", "ART, from ancient to 1945",
           "ART: ancient to 1945"],
"ARTS561":["AUGUSTAN CULTRAL REVOLUTION", "AUGUSTAN CULTRL REVOL"],
"ARTS555":["BECOMING HUMAN"],
"ARTS516":["BEHAVIORAL PHARMACOLOGY"],
"ARTS583":["BRITISH POETRY 1660-1914"],
"ARTS494":["Business German: A Micro Perspective",
           "Business German - Micro Perspective",
           "Business German A Micro Perspective",
           "Business German, A Micro Perspective"],
"ARTS569":["CELL. BIOL. & BIOCHEM.",
            "CEL and BIO and BIOCHEMISTRY",
            "CEL BIO BIOCHEMISTRY",
            "CELL and BIO and BIOCHEMISTRY",
            "CELL BIOL & BIOCHEM",
            "CELL BIOLOGY & BIOCHEM",
            "CELL BIOLOGY and BIOCHEM",
            "CELL BIOLOGY and BIOCHEMISTRY",
            "CELL. BIOL. And BIOCHEM."
           ],
"ARTS495":["COMM and  THE PRESIDENCY", "COMM & THE PRESIDENCY"],
"ARTS547":["COMMUNICATIONS INTERNSHP", "COMMUNICATIONS INTERNSHiP"],
"ARTS581":["COMPARATIVE POLITICS"],
"ARTS486":["COMPUTER LINEAR ALGEBRA", "COMPUT LINEAR ALGEBRA"],
"ARTS497":["CONTEMP ART - 1945 to PRESENT",
           "CONTEMP ART - 1945 to today",
           "CONTEMP ART - since 1945",
           "CONTEMP ART:1945 to PRESENT"
           ],
"ARTS518":["CONTEMPORARY AFRICAN ART", "CONTEMPORARY AFRICAN-ART"],
"ARTS491":["CONTEMPORARY POL.THOUGHT"],
"ARTS585":["CONTEMPORARY SOCIO THEORY","CONTEMPORARY SOCIO THEOR"],
"ARTS488":["DEVIL'S PACT LIT/FILM"],
"ARTS579":["EARLY BALCAN HIST/SOC"],
"ARTS575":["EARLY MESOPOTAM HISTORY/SOCIETY",
           "EARLY MESOPOTAM HIST - SOC",
           "EARLY MESOPOTAM HIST/SOC",
           "EARLY MESOPOTAMIAN HIST - SOC"
           ],
"ARTS587":["ELEMENTARY ARABIC II"],
"ARTS567":["ELEMENTARY GERMAN 1","ELEMENTARY GERMAN I"],
"ARTS565":["Environmental Studies Research Seminar Junior Level",
           "Environmental Studies Research Seminar for Juniors"
           ],
"ARTS465":["ENVIRONMENTAL SYSTEMS II"],
"ARTS484":["EUROPE IN A WIDER WORLD"],
"ARTS485":["EVIDENCED BASED CRIME AND JUSTICE POLICY", "EVIDENCED BASED CRIME & JUSTICE POLICY"],
"ARTS400":["EXPERIMENTAL WRITING SEM: The Ecology of Poetry", "EXPERIMENTAL WRITING SEM"],
"ARTS520":["FOOD/FEAST ARCH OF TABLE"],
"ARTS577":["FRANCE & THE EUROP.UNION"],
"ARTS553":["French Thought Since 1945"],
"ARTS496":["French Thought Till 1945"],
"ARTS549":["FRESHWATER ECOLOGY"]
}

NONELECTIVES = ["ARTS400","ARTS401","ARTS465","ARTS486","ARTS512","ARTS514","ARTS516","ARTS518","ARTS520"]

ELECTIVES_KEYS = set(COURSES.keys()) - set(NONELECTIVES)

def compress_items(d):
    ret = dict()
    for k, v in d.items():
        ret[k] = ["".join(i.split()).lower() for i in v]

    return ret

def clean_courses(fname):
    csv.field_size_limit(500 * 1024 * 1024)
    csvfile = open(fname, newline='')
    reader = csv.reader(csvfile, delimiter=',',
                        quotechar='"',
                        quoting=csv.QUOTE_ALL,
                        skipinitialspace=True)
    i = 0
    compressed_courses = compress_items(COURSES)
    cleaned = []
    for row in reader:
        if len(row) == 0:
            continue
        else:
            for code, course_aliases in compressed_courses.items():
                # get rid of all spaces
                line = "".join(row[2].split()).lower()

                # build
                if line in course_aliases:
                    # print(f"{i}: {code} - {row[2]}")
                    r = row
                    r.append(code)
                    cleaned.append(r)

        i +=1

    return cleaned

def remove_duplicates(d):
    clean = {}
    for row in d:
        elem1 = "".join(row[0].split()).lower()
        elem2 = "".join(row[1].split()).lower()
        elem3 = "".join(row[3].split()).lower()
        k = elem1 + "_" + elem2 + "_" + elem3
        clean[k] = row

    return clean

def remove_duplicates2(d):
    clean = {}
    for row in d:
        elem1 = "".join(row[0].split()).lower()
        elem2 = "".join(row[3].split()).lower()
        k = elem1 + "_" + elem2
        clean[k] = row

    return clean

def flatten(d):
    clean = {}
    for k, v in d.items():
        k = "".join(v[0].split()).lower()
        clean[k] = []

    for k, v in d.items():
        k = "".join(v[0].split()).lower()
        clean[k].append(v[3])
    return clean

def get_electives(d):
    clean = {}
    for k, v in d.items():
        res = set(v) - set(NONELECTIVES)
        if len(res) > 0:
            clean[k]  = res
    return clean

def frequency_counts(d):
    ret = {}

    for k, v in d.items():
        for el in v:
            if el in ret.keys():
                ret[el] += 1
            else:
                ret[el] = 0
    return ret



#print(compress_items(COURSES))
phase1 = clean_courses(DATA)
print("Total number of records:",len(phase1), phase1)

#phase2 = remove_duplicates(phase1)
#print(len(phase2), phase2)

phase22 = remove_duplicates2(phase1)
print("Deduped records:",len(phase22), phase22)

# create lists of courses
#phase3 = flatten(phase2)
#print(len(phase3), phase3)

phase33 = flatten(phase22)
print("List of all courses per user:",len(phase33), phase33)

# get electives only
phase4 = get_electives(phase33)
print("List of electives per user:", len(phase4), phase4)
# 296 records
# {
# 'billmumy': {'ARTS497', 'ARTS569'},
# 'ruthbaderginsburg': {'ARTS559'},
# 'geraldineferraro': {'ARTS587'}, ...

# Use apriori algorithm to find
# step 1. get frequency counts
phase5 = frequency_counts(phase4)
print("Frequency counts aka L1:",len(phase5), phase5)
# 29 records
# {'ARTS569': 75, 'ARTS497': 15, 'ARTS559': 23, 'ARTS587': 63 ...

# see most popular items
#phase6 = {k:v for k,v in phase5.items() if v > 50}
#print(len(phase6), phase6)

"""
Algorithm:  Apriori [Agrawal1994]
Input:
     I - items
     D - tranaction database
     S - threshold on support
Output:
     Association rules
Algorithm:
     L = {∅}
     Generate L1 by traversing database and counting the occurence of each item;
     Prune all items I1 of L1 for which support s(I1) < S
     for (k=2;Lk−1≠ϕ;k++) do
          // generate k-itemset
          Lk = apriori-gen(Lk-1);
          Prune all items Ik of Lk for which support s(Ik) < S
          L=L∪Lk
     end
     Generate the desired rules from L
end
"""
D = phase4
# 1. Determine all the items in the database.
I = ELECTIVES_KEYS

S = 0.1
L1 = phase5
Total = len(phase4)
L2 = {}
# 2. Compute the support of all 1-itemsets and remove
# those itemsets with support below the threshold level
for course_code, counts in L1.items():
    support = counts/Total
    #print(f"support for {course_code} is {support}")
    if support > S:
        L2[course_code] = counts

print("Apriori - L2 with 10% support:", L2)



