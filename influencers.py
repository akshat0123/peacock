import random

class Influencers:
    """ Create class influencers
        Set baseline list of influencers
    """

    def __init__(self):
        # self.allInfluencers = ["katyperry", "justinbieber", "BarackObama", "taylorswift13", "ladygaga", "TheEllenShow", "jtimberlake", "KimKardashian", "britneyspears", "ArianaGrande", "ddlovato", "selenagomez", "jimmyfallon", "BillGates", "JLo", "BrunoMars", "Oprah", "nytimes", "KingJames", "MileyCyrus", "SportsCenter", "KevinHart4real", "LilTunechi", "wizkhalifa", "Pink", "aliciakeys", "NASA", "ConanOBrien", "chrisbrown", "ActuallyNPH", "NBA", "danieltosh", "pitbull", "KendallJenner", "khloekardashian", "KylieJenner", "NFL", "kourtneykardash", "Eminem", "HillaryClinton", "NICKIMINAJ", "MariahCarey", "blakeshelton", "LeoDiCaprio", "aplusk", "ShawnMendes", "StephenAtHome", "JimCarrey", "ParisHilton", "SnoopDogg", "FoxNews", "KDTrey5", "kanyewest", "xtina", "RyanSeacrest", "camerondallas", "ZacEfron", "WSJ", "PlayStation", "tomhanks", "Diddy", "tyrabanks", "Beyonce", "SHAQ", "maroon5", "POTUS44", "BigSean", "SethMacFarlane", "funnyordie", "ashleytisdale", "TreySongz", "ABC", "kobebryant", "nickjonas", "ObamaWhiteHouse", "voguemagazine", "Zendaya", "iamwill", "Usher", "TheRock", "SarahKSilverman", "AP", "neiltyson", "kelly_clarkson", "washingtonpost", "StephenCurry30", "charliesheen", "johnlegend", "Ludacris", "mindykaling", "enews", "Starbucks", "jimmykimmel", "MarcAnthony", "DisneyPixar", "TheOnion", "JohnCena", "billmaher", "azizansari", "TEDTalks"]
        self.allInfluencers = ["katyperry", "justinbieber", "BarackObama", "taylorswift13"]
        self.infGroup = random.sample(self.allInfluencers, 2)
        self.discard = self.infGroup
        self.infAvail = list(filter(lambda x: x not in self.infGroup, self.allInfluencers))
        self.infPerformance = {influencer: 0 for influencer in self.allInfluencers}
        

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
