from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# class Word(models.Model):
#     name = models.CharField(max_length=255)
#     correct_transcription = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'words'

#     def __str__(self):
#         return f'{self.id}: {self.name}'

# class Sentence(models.Model):
#     name = models.CharField(max_length=255)
#     correct_transcription = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'sentences'

#     def __str__(self):
#         return f'{self.id}: {self.name}'

class BaseItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        abstract = True

class CatLev0(BaseItem):
    class Meta:
        managed = False
        db_table = "cat_lev0"
    # def __str__(self):
    #     return f'{self.id}: {self.name}'
    
class CatLev1(BaseItem):
    cat_lev0 = models.ForeignKey(CatLev0, on_delete=models.CASCADE, db_column='cat_lev0')
    class Meta:
        managed = False
        db_table = "cat_lev1"
    # def __str__(self):
    #     return f'{self.id}: {self.name}'
    
class CatLev2(BaseItem):
    cat_lev1 = models.ForeignKey(CatLev1, on_delete=models.CASCADE, db_column='cat_lev1')
    class Meta:
        managed = False
        db_table = "cat_lev2"
    # def __str__(self):
    #     return f'{self.id}: {self.name}'

class CatLev3(BaseItem):
    cat_lev2 = models.ForeignKey(CatLev2, on_delete=models.CASCADE, db_column='cat_lev2')
    class Meta:
        managed = False
        db_table = "cat_lev3"
    # def __str__(self):
    #     return f'{self.id}: {self.name}'

class BaseTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    cat_lev0 = models.IntegerField(null=True, blank=True)
    cat_lev1 = models.IntegerField(null=True, blank=True)
    cat_lev2 = models.IntegerField(null=True, blank=True)
    cat_lev3 = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        abstract = True

class HumorEnGeluiden(BaseTable):
    class Meta:
        managed = False
        db_table = "Humor en geluiden"


class FysiekeGedrag(BaseTable):
    class Meta:
        managed = False
        db_table = "Fysiekegedrag"

class MuziekEnGeluid(BaseTable):
   class Meta:
        managed = False
        db_table = "Muziek en geluid"
        
class TafelDekken(BaseTable):
    class Meta:
        managed = False
        db_table = "Tafel dekken"

class PersoonlijkenBezittelijkVoornaamwoord(BaseTable):
    class Meta:
        managed = False
        db_table = "Persoonlijk en bezittelijk voornaamwoor"

class Gevaarlijk(BaseTable):
    class Meta:
        managed = False
        db_table = 'Gevaarlijk'

class OmgaanMetSpullen(BaseTable):
    class Meta:
        managed = False
        db_table = 'Omgaan met spullen'

class TandenVerzorgen(BaseTable):
    class Meta:
        managed = False
        db_table = 'Tanden verzorgen' 

class VerbondenheidEnGevoelens(BaseTable):
    class Meta:
        managed = False
        db_table = 'Verbondenheid en gevoelens'

class Gevoel(BaseTable):
    class Meta:
        managed = False
        db_table = 'Gevoel'

class Ontbijten(BaseTable):
    class Meta:
        managed = False
        db_table = 'Ontbijten'

class Tekenen(BaseTable):
    class Meta:
        managed = False
        db_table = "Tekenen"

class AanUitkleding(BaseTable):
    class Meta:
        managed = False
        db_table = 'Aan en uitkleding'

class Groente(BaseTable):
    class Meta:
        managed = False
        db_table = 'Groente'

class OpDeBeurt(BaseTable):
    class Meta:
        managed = False
        db_table = 'Op de beurt'

class Tellen(BaseTable):
    class Meta:
        managed = False
        db_table = 'Tellen'

class Afscheid(BaseTable):
    class Meta:
        managed = False
        db_table = 'Afscheid'

class Groeten(BaseTable):
    class Meta:
        managed = False
        db_table = 'Groeten'

class OpReis(BaseTable):
    class Meta:
        managed = False
        db_table = 'Op reis'

class Tijd(BaseTable):
    class Meta:
        managed = False
        db_table = 'Tijd'

class AlgemeenMensen(BaseTable):
    class Meta:
        managed = False
        db_table = 'Mensen algemeen'

class Gymnastiek(BaseTable):
    class Meta:
        managed = False
        db_table = 'Gymnastiek'

class OpenEnDichtDoen(BaseTable):
    class Meta:
        managed = False
        db_table = 'Open en dicht doen'

class Toeval(BaseTable):
    class Meta:
        managed = False
        db_table = "Toeval"

class AvondEten(BaseTable):
    class Meta:
        managed = False
        db_table = "Avond eten"

class HaarVerzorgen(BaseTable):
    class Meta:
        managed = False
        db_table = "Haar verzorgen"

class Overig(BaseTable):
    class Meta:
        managed = False
        db_table = "Overig"

class TuinEnPark(BaseTable):
    class Meta:
        managed = False
        db_table = "Tuin en park"
        
class Badkamer(BaseTable):
    class Meta:
        managed = False
        db_table = "Badkamer"

class HebbenEnDelen(BaseTable):
    class Meta:
        managed = False
        db_table = "Hebben en delen"

class Personen(BaseTable):
    class Meta:
        managed = False
        db_table = "Personen"

class Uitjes(BaseTable):
    class Meta:
        managed = False
        db_table = "Uitjes"
        
class Bal(BaseTable):
    class Meta:
        managed = False
        db_table = "Bal"

class Herfst(BaseTable):
    class Meta:
        managed = False
        db_table = "Herfst"

class Planten(BaseTable):
    class Meta:
        managed = False
        db_table = "Planten"
        
class Vergelijken(BaseTable):
    class Meta:
        managed = False
        db_table = "Vergelijken"
        
class BelangrijkeWoordjes(BaseTable):
    class Meta:
        managed = False
        db_table = "Belangrijke woordjes"

class Huis(BaseTable):
    class Meta:
        managed = False
        db_table = "Huis"

class PoepenEnPlassen(BaseTable):
    class Meta:
        managed = False
        db_table = "Poepen en plassen"

class Verjaardag(BaseTable):
    class Meta:
        managed = False
        db_table = "Verjaardag"

class Boerderij(BaseTable):
    class Meta:
        managed = False
        db_table = "Boerderij"

class HuisWerken(BaseTable):
    class Meta:
        managed = False
        db_table = "Huis werken"

class Rekenen(BaseTable):
    class Meta:
        managed = False
        db_table = "Rekenen"

class Voortuigen(BaseTable):
    class Meta:
        managed = False
        db_table = "Voortuigen"

class BoodschappenDoen(BaseTable):
    class Meta:
        managed = False
        db_table = "Boodschappen doen"

class Huisdieren(BaseTable):
    class Meta:
        managed = False
        db_table = "Huisdieren"

class RichtingDeWeg(BaseTable):
    class Meta:
        managed = False
        db_table = "Richting de weg"

class Vormen(BaseTable):
    class Meta:
        managed = False
        db_table = "Vormen"

class Bos(BaseTable):
    class Meta:
        managed = False
        db_table = "Bos"

class Kerst(BaseTable):
    class Meta:
        managed = False
        db_table = "Kerst"

class RollenspelEnSprookjes(BaseTable):
    class Meta:
        managed = False
        db_table = "Rollenspel en sprookjes"
        
class Vraagwoorden(BaseTable):
    class Meta:
        managed = False
        db_table = "Vraagwoorden"

class Buiten(BaseTable):
    class Meta:
        managed = False
        db_table = "Buiten"

class Kleding(BaseTable):
    class Meta:
        managed = False
        db_table = "Kleding"

class Ruimte(BaseTable):
    class Meta:
        managed = False
        db_table = "Ruimte"

class Vuur(BaseTable):
    class Meta:
        managed = False
        db_table = "Vuur"

class Communiceren(BaseTable):
    class Meta:
        managed = False
        db_table = "Communiceren"

class KleineDiertjes(BaseTable):
    class Meta:
        managed = False
        db_table = "Kleine diertjes"

class SamenAktiviteiten(BaseTable):
    class Meta:
        managed = False
        db_table = "Samen aktiviteiten"

class Wassen(BaseTable):
    class Meta:
        managed = False
        db_table = "Wassen"

class Denken(BaseTable):
    class Meta:
        managed = False
        db_table = "Denken"

class Kleuren(BaseTable):
    class Meta:
        managed = False
        db_table = "Kleuren"

class Schoen(BaseTable):
    class Meta:
        managed = False
        db_table = "Schoen"

class Water(BaseTable):
    class Meta:
        managed = False
        db_table = "Water"

class Dieren(BaseTable):
    class Meta:
        managed = False
        db_table = "Dieren"

class Knutselen(BaseTable):
    class Meta:
        managed = False
        db_table = "Knutselen"

class Schrijven(BaseTable):
    class Meta:
        managed = False
        db_table = "Schrijven"

class Weer(BaseTable):
    class Meta:
        managed = False
        db_table = "Weer"

class Dierentuin(BaseTable):
    class Meta:
        managed = False
        db_table = "Dierentuin"

class Koken(BaseTable):
    class Meta:
        managed = False
        db_table = "Koken"

class Sinterklaas(BaseTable):
    class Meta:
        managed = False
        db_table = "Sinterklaas"

class WegwijsInDeGroep(BaseTable):
    class Meta:
        managed = False
        db_table = "Wegwijs in de groep"

class Doen(BaseTable):
    class Meta:
        managed = False
        db_table = "Doen"

class KopjesEnBakers(BaseTable):
    class Meta:
        managed = False
        db_table = "Kopjes en bakers"

class Smaken(BaseTable):
    class Meta:
        managed = False
        db_table = "Smaken"

class Welkom(BaseTable):
    class Meta:
        managed = False
        db_table = "Welkom"

class Drankjes(BaseTable):
    class Meta:
        managed = False
        db_table = "Drankjes"

class Kringroutines(BaseTable):
    class Meta:
        managed = False
        db_table = "Kringroutines"

class Snoep(BaseTable):
    class Meta:
        managed = False
        db_table = "Snoep"

class Winter(BaseTable):
    class Meta:
        managed = False
        db_table = "Winter"

class Drinken(BaseTable):
    class Meta:
        managed = False
        db_table = "Drinken"

class Kruipen(BaseTable):
    class Meta:
        managed = False
        db_table = "Kruipen"

class Speelgoed(BaseTable):
    class Meta:
        managed = False
        db_table = "Speelgoed"

class WinterKleding(BaseTable):
    class Meta:
        managed = False
        db_table = "Winterkleding"

class Emotie(BaseTable):
    class Meta:
        managed = False
        db_table = "Emotie"

class Lente(BaseTable):
    class Meta:
        managed = False
        db_table = "Lente"

class Speeltuin(BaseTable):
    class Meta:
        managed = False
        db_table = "Speeltuin"

class ZeeSwembad(BaseTable):
    class Meta:
        managed = False
        db_table = "Zee en zwemen"

class Eruitzien(BaseTable):
    class Meta:
        managed = False
        db_table = "Eruitzien"

class Lichaamsdelen(BaseTable):
    class Meta:
        managed = False
        db_table = "Lichaamsdelen"

class Spelen(BaseTable):
    class Meta:
        managed = False
        db_table = "Spelen"
        
class Ziek(BaseTable):
    class Meta:
        managed = False
        db_table = "Ziek"
        
class Eten(BaseTable):
    class Meta:
        managed = False
        db_table = "Eten"

class Lunch(BaseTable):
    class Meta:
        managed = False
        db_table = "Lunch"
        
class SpelenEnWerken(BaseTable):
    class Meta:
        managed = False
        db_table = "Spelen en werken"

class Zintuigen(BaseTable):
    class Meta:
        managed = False
        db_table = "Zintuigen"

class Familie(BaseTable):
    class Meta:
        managed = False
        db_table = "Familie"

class MensenEnRelaties(BaseTable):
    class Meta:
        managed = False
        db_table = "Mensen en relaties"
        
class Spelletje(BaseTable):
    class Meta:
        managed = False
        db_table = "Spelletje"

class Zomer(BaseTable):
    class Meta:
        managed = False
        db_table = "Zomer"
        
class Fruit(BaseTable):
    class Meta:
        managed = False
        db_table = "Fruit"

class Meten(BaseTable):
    class Meta:
        managed = False
        db_table = "Meten"

class StraatEnVerkeer(BaseTable):
    class Meta:
        managed = False
        db_table = "Straat en verkeer"

# standard setup of public templates database 
class ThemeName(models.Model):
    theme_name = models.CharField(max_length=255)
    def __str__(self):
        return self.theme_name
    class Meta:
        db_table = "themenames"
        
class PageName(models.Model):
    page_name = models.CharField(max_length=255)
    block_row = models.IntegerField()
    block_column = models.IntegerField()
    theme_name = models.ForeignKey(ThemeName, on_delete=models.CASCADE, related_name='pages')
    def __str__(self):
        return self.page_name
    class Meta:
        #managed = False
        # Use the exact page_name as the table name
        db_table = 'pagenames'

class PageBlock(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    option = models.IntegerField()
    page_name = models.ForeignKey(PageName, on_delete=models.CASCADE, related_name='blocks')

    def __str__(self):
        return f"{self.name} - {self.page_name.page_name}"
    class Meta:
        #managed = False
        # Use the exact page_name as the table name
        db_table = 'pageblocks'