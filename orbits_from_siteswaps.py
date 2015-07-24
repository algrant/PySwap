import xml.etree.ElementTree

def get_patterns(filename):
    jml = xml.etree.ElementTree.parse(filename).getroot()[0]
    patterns = []
    for pattern in jml:
        patterns.append( pattern.text.strip() )
    return patterns[1:]

class Siteswap():
    def __init__(self,siteswap):
        self.siteswap = self.validate_siteswap(siteswap)
        self.orbits_by_index = []
        self.orbits_patterns = []
        self.unique_orbits = []
        self.unique_ball_colors = []
        self.repeated_ball_colors = []

        self.init_orbits()
        self.init_orbit_patterns()
        self.init_unique_orbits()

        self.orbits_category = [sum([int(c) for c in swap])/len(swap) for swap in self.orbits_patterns]
        self.orbits_category = [s for s in self.orbits_category if s != 0]
        self.orbits_category.sort()
        self.unique_orbits_category = [sum([sum([int(c) for c in swap])  for swap in swaps])/len(self.siteswap) for swaps in self.unique_orbits]
        self.unique_orbits_category = [s for s in self.unique_orbits_category if s != 0]
        self.unique_orbits_category.sort()
        self.unique_representation = self.orbits_category == self.unique_orbits_category

        self.init_colors_juggling_lab()

    def __repr__(self):
        return self.siteswap

    def validate_siteswap(self,siteswap):
        """ Should do some validation here """
        return siteswap

    def init_orbits(self):
        ss = self.siteswap
        orbits = []
        ss_indices = set(range(len(ss)))

        while ss_indices:
            orbit = [ss_indices.pop()]
            e = orbit[0]
            curPos = orbit[0]
            nextPos = (orbit[0] + int(ss[curPos]))%len(ss)
            for _ in range(len(ss)):
                if e == nextPos or nextPos not in ss_indices:
                    break
                else:
                    orbit.append(nextPos)
                    ss_indices.remove(nextPos)
                    curPos = nextPos
                    nextPos = (curPos + int(ss[curPos]))%len(ss)
            orbits.append(orbit)
        numObjects = sum([int(i) for i in ss])/len(ss)

        self.orbits_by_index = orbits

    def init_orbit_patterns(self):
        self.orbits_patterns = [''.join([self.siteswap[i] if i in orbit else '0' for i in range(len(self.siteswap))]) for orbit in self.orbits_by_index]

    def init_unique_orbits(self):
        oP = self.orbits_patterns
        uO = self.unique_orbits
        for orb in oP:
            inUO = False
            for unOrb in uO:
                if self.isCircularSiteSwap(unOrb[0],orb):
                    unOrb.append(orb)
                    inUO = True
                    break
            if not inUO:
                uO.append([orb])

    def isCircularSiteSwap(self,str1,str2):
        if len(str1) != len(str2):
            return False
        return str1 in str2+ str2

    def init_colors_juggling_lab(self):
        self.unique_ball_colors = []
        self.repeated_ball_colors = []

        colours = ["red", "blue", "yellow", "green"]

        total_objects = sum([int(i) for i in self.siteswap])/len(self.siteswap)
        object_indices = set(range(total_objects))


#siteswap_list = ["534","552","633","642","561","723","741","822","831","714","912"]
#siteswap_list = get_patterns("4balls_max9_async_period3.jml") + get_patterns("4balls_max9_async_period4.jml") + get_patterns("4balls_max9_async_period5.jml")
siteswap_list = get_patterns("5balls_max9_async_period3.jml") + \
                get_patterns("5balls_max9_async_period4.jml") + \
                get_patterns("5balls_max9_async_period5.jml") + \
                get_patterns("5balls_max9_async_period6.jml") + \
                get_patterns("5balls_max8_async_period7.jml") +\
                get_patterns("5balls_max9_async_period7_90.jml")  + \
                get_patterns("5balls_max9_async_period7_92.jml")  + \
                get_patterns("5balls_max9_async_period7_93.jml") + \
                get_patterns("5balls_max9_async_period7_94.jml") + \
                get_patterns("5balls_max9_async_period7_95.jml") +\
                get_patterns("5balls_max9_async_period7_96.jml") + \
                get_patterns("5balls_max9_async_period7_97.jml") + \
                get_patterns("5balls_max9_async_period7_99.jml")

siteswap_dict = {ss: Siteswap(ss) for ss in siteswap_list}
orbits_dict = {}

for ss in [Siteswap(ss) for ss in siteswap_list]:
    if "0" not in ss.siteswap and "2" not in ss.siteswap:
        u_o_c = tuple(ss.unique_orbits_category)
        if u_o_c not in orbits_dict:
            orbits_dict[u_o_c] = {"unique":[ss.siteswap], "repeated":[]}
        else:
            orbits_dict[u_o_c]["unique"].append(ss.siteswap)
        if not ss.unique_representation:
            r_o_c = tuple(ss.orbits_category)
            if r_o_c not in orbits_dict:
                orbits_dict[r_o_c] = {"unique":[], "repeated":[ss.siteswap]}
            else:
                orbits_dict[r_o_c]["repeated"].append(ss.siteswap)

orbit_list = [orbit for orbit in orbits_dict]
orbit_list.sort()

for orbit in orbit_list:
    siteswaps = orbits_dict[orbit]
    if siteswaps["unique"] or siteswaps["repeated"]:
        print "\n\n",orbit
    if (siteswaps["unique"]):
        print "Unique",
        siteswaps["unique"].sort(key=lambda ss: "abcdefghijklmnopqrstuvwxyz"[len(ss)]+ss)
        cur_len = 0 
        for ss_obj in siteswaps["unique"]:
            ss = ss_obj #.siteswap
            if len(ss) > cur_len:
                print "\n\t Period %i \n\t\t"%len(ss),
                cur_len = len(ss)
            print ss,
        print ""
             
    if (siteswaps["repeated"]):
        print "Repeated",
        siteswaps["repeated"].sort(key=lambda ss: "abcdefghijklmnopqrstuvwxyz"[len(ss)]+ss)
        cur_len = 0 
        for ss_obj in siteswaps["repeated"]:
            ss = ss_obj#.siteswap
            if len(ss) > cur_len:
                print "\n\t Period %i \n\t\t"%len(ss),
                cur_len = len(ss)
            print ss,

