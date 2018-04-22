import random

class Influencers:
    """ Create class influencers
        Set baseline list of influencers
    """

    def __init__(self):
        self.allInfluencers = ["katyperry","justinbieber","BarackObama","rihanna","taylorswift13","ladygaga","TheEllenShow","Cristiano","YouTube","jtimberlake","Twitter","KimKardashian","britneyspears","ArianaGrande","selenagomez","ddlovato","cnnbrk","shakira","jimmyfallon","realDonaldTrump","BillGates","JLo","Oprah","BrunoMars","narendramodi","nytimes","KingJames","MileyCyrus","CNN","NiallOfficial","instagram","neymarjr","BBCBreaking","Drake","SportsCenter","KevinHart4real","iamsrk","espn","LilTunechi","SrBachchan","wizkhalifa","Louis_Tomlinson","Pink","LiamPayne","BeingSalmanKhan","Harry_Styles","onedirection","aliciakeys","KAKA","realmadrid","NASA","Adele","EmmaWatson","ConanOBrien","FCBarcelona","chrisbrown","ActuallyNPH","NBA","danieltosh","pitbull","zaynmalik","KendallJenner","khloekardashian","akshaykumar","PMOIndia","sachin_rt","KylieJenner","coldplay","NFL","imVkohli","kourtneykardash","deepikapadukone","TheEconomist","aamir_khan","iHrithik","BBCWorld","POTUS","Eminem","andresiniesta8","NatGeo","MesutOzil1088","HillaryClinton","priyankachopra","AvrilLavigne","davidguetta","MohamadAlarefe","NICKIMINAJ","blakeshelton","MariahCarey","elonmusk","ChampionsLeague","ricky_martin","Google","edsheeran","arrahman","Reuters","AlejandroSanz","LeoDiCaprio","aplusk","Dr_alqarn"]
        self.infGroup = random.sample(self.allInfluencers, 1)
        self.discard = self.infGroup
        self.infAvail = list(filter(lambda x: x not in self.infGroup, self.allInfluencers))
        

    def replaceOne(self, discardItem):
        """
        Replace one item in infGroup, append to discard
        Select a new item, append to infGroup and remove from infAvail
        """
        self.infGroup.remove(discardItem)
        self.discard.append(discardItem)
        newItem = random.sample(self.infAvail, 1)[0]
        self.infGroup.append(newItem)
        self.infAvail.remove(newItem)
